"""
Maintaining BidAggregate rows.

Two write paths:

  bump()    -- incremental, one bid at a time, used when a visitor submits.
  rebuild() -- batch, recomputes a whole slice from raw rows.

Both keep `counts` (the source of truth) and the denormalised scalars in sync,
so a read never has to touch a raw bid table or recompute a percentile.
"""
import logging
from typing import Iterable, Optional

from django.db import transaction
from django.db.models import Count

from ..models import BidAggregate, MarketBid, ScoringFormat
from . import histogram as hg

log = logging.getLogger(__name__)

# Slice dimensions materialised for the market scope. 0 / 'all' is the
# unfiltered row every unfiltered page read hits.
LEAGUE_SIZE_SLICES = (0, 8, 10, 12, 14)
SCORING_SLICES = (ScoringFormat.ALL, ScoringFormat.PPR, ScoringFormat.HALF, ScoringFormat.STANDARD)


def _apply_summary(agg: BidAggregate) -> None:
    """Recompute denormalised scalars from the count array."""
    for field, value in hg.summarize(agg.counts).items():
        setattr(agg, field, value)
    agg.n_leagues = hg.total(agg.won_counts)


@transaction.atomic
def bump(*, scope: str, player_id: int, season: int, week: int, value: int,
         won: Optional[bool] = None, league_size: int = 0,
         scoring: str = ScoringFormat.ALL) -> BidAggregate:
    """
    Fold a single bid into its aggregate row, creating it if needed.

    select_for_update serialises concurrent writers on this one row. Bids
    trickle in over days rather than arriving in a thundering herd, so the lock
    is uncontended in practice; if that ever changes, split `counts` into a
    (value -> count) row per bucket to spread the contention across 101 rows.
    """
    agg, _ = BidAggregate.objects.select_for_update().get_or_create(
        scope=scope, player_id=player_id, season=season, week=week,
        league_size=league_size, scoring=scoring,
    )
    counts = list(agg.counts or hg.empty())
    hg.add(counts, value)
    agg.counts = counts

    if won:
        won_counts = list(agg.won_counts or hg.empty())
        hg.add(won_counts, value)
        agg.won_counts = won_counts

    _apply_summary(agg)
    agg.save()
    return agg


def rebuild_market_slice(*, season: int, week: int, league_size: int = 0,
                         scoring: str = ScoringFormat.ALL) -> int:
    """
    Recompute every market aggregate for one (season, week, slice).

    Aggregation happens in the database -- one grouped query per slice rather
    than per player -- and only the resulting counts cross the wire.
    """
    qs = MarketBid.objects.filter(season=season, week=week, player__isnull=False)
    if league_size:
        qs = qs.filter(league__total_rosters=league_size)
    if scoring != ScoringFormat.ALL:
        qs = qs.filter(league__scoring=scoring)

    all_rows = qs.values('player_id', 'bid_pct').annotate(c=Count('id'))
    won_rows = qs.filter(won=True).values('player_id', 'bid_pct').annotate(c=Count('id'))

    counts_by_player, won_by_player = {}, {}
    for row in all_rows:
        counts_by_player.setdefault(row['player_id'], hg.empty())[row['bid_pct']] += row['c']
    for row in won_rows:
        won_by_player.setdefault(row['player_id'], hg.empty())[row['bid_pct']] += row['c']

    written = 0
    for player_id, counts in counts_by_player.items():
        agg, _ = BidAggregate.objects.get_or_create(
            scope=BidAggregate.Scope.MARKET, player_id=player_id, season=season,
            week=week, league_size=league_size, scoring=scoring,
        )
        agg.counts = counts
        agg.won_counts = won_by_player.get(player_id, hg.empty())
        _apply_summary(agg)
        agg.save()
        written += 1
    return written


def rebuild_market_week(*, season: int, week: int, slices: bool = True) -> int:
    """Rebuild the unfiltered row plus, optionally, every filter slice."""
    written = rebuild_market_slice(season=season, week=week)
    if not slices:
        return written
    for size in LEAGUE_SIZE_SLICES:
        for scoring in SCORING_SLICES:
            if size == 0 and scoring == ScoringFormat.ALL:
                continue  # already done above
            written += rebuild_market_slice(
                season=season, week=week, league_size=size, scoring=scoring
            )
    return written


def rebuild_crowd_week(*, season: int, week: int, legacy_week: int) -> int:
    """
    Rebuild crowd aggregates for one week from the legacy Bid table.

    Zero-value rows are excluded: roughly half of all historical rows are 0 and
    they represent "show me the answer" clicks rather than real valuations.
    """
    from ..models import Bid  # local import keeps module import cheap

    rows = (
        Bid.objects.filter(week=legacy_week, value__gte=1, value__lte=100)
        .values('player_id', 'value')
        .annotate(c=Count('id'))
    )
    counts_by_player = {}
    for row in rows:
        counts_by_player.setdefault(row['player_id'], hg.empty())[row['value']] += row['c']

    written = 0
    for player_id, counts in counts_by_player.items():
        agg, _ = BidAggregate.objects.get_or_create(
            scope=BidAggregate.Scope.CROWD, player_id=player_id, season=season,
            week=week, league_size=0, scoring=ScoringFormat.ALL,
        )
        agg.counts = counts
        _apply_summary(agg)
        agg.save()
        written += 1
    return written
