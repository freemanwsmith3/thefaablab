"""
Sleeper ingest: discovery and the weekly transaction sweep.

Discovery walks the public social graph -- league -> its members -> those
members' other leagues -- which lets the corpus be built without ever asking a
visitor for anything. It is deliberately a separate, occasional job: the weekly
sweep then costs exactly one API call per registered league.
"""
import logging
from collections import deque
from typing import Iterable, List, Optional, Set

from datetime import datetime, timezone as dt_timezone

from django.db import transaction

from ..models import MarketBid, Player, SleeperLeague
from .sleeper import SleeperClient, classify_scoring, is_faab, normalise_bid

log = logging.getLogger(__name__)

# A league that yields no transactions for this many consecutive ingests is
# treated as abandoned and stops costing API calls.
EMPTY_WEEK_LIMIT = 4


def _league_defaults(league: dict) -> dict:
    settings_blob = league.get('settings') or {}
    scoring, ppr = classify_scoring(league.get('scoring_settings'))
    return {
        'season': int(league.get('season') or 0),
        'total_rosters': league.get('total_rosters') or 0,
        'waiver_budget': settings_blob.get('waiver_budget') or 100,
        'waiver_type': settings_blob.get('waiver_type') or 0,
        'waiver_day': settings_blob.get('waiver_day_of_week'),
        'scoring': scoring,
        'ppr_value': ppr,
        'previous_league_id': league.get('previous_league_id'),
    }


def save_league(league: dict) -> Optional[SleeperLeague]:
    """Upsert one league into the registry if it runs FAAB waivers."""
    if not league or not league.get('league_id') or not is_faab(league):
        return None
    obj, _ = SleeperLeague.objects.update_or_create(
        league_id=str(league['league_id']), defaults=_league_defaults(league)
    )
    return obj


def discover(
    client: SleeperClient,
    seed_league_ids: Iterable[str],
    season: int,
    max_leagues: int = 2000,
    max_depth: int = 3,
    skip_known: bool = True,
) -> dict:
    """
    Breadth-first crawl of the Sleeper league graph from a set of seeds.

    Expansion is geometric: each league exposes ~10-14 members and each member
    typically belongs to several leagues, so a handful of seeds reaches the
    low thousands within a few hops.

    With skip_known (the default), leagues already in the registry are treated
    as visited. That makes the crawl resumable: a run scheduled to fire
    repeatedly through the day spends its whole budget on leagues it has never
    seen instead of re-fetching the corpus it already has.
    """
    seen_leagues: Set[str] = set()
    if skip_known:
        seen_leagues.update(
            SleeperLeague.objects.filter(season=season)
            .values_list('league_id', flat=True)
        )
    seen_users: Set[str] = set()
    saved = faab_count = 0
    seeds = [str(lid) for lid in seed_league_ids]
    queue = deque((lid, 0) for lid in seeds)
    seed_set = set(seeds)

    while queue and saved < max_leagues:
        league_id, depth = queue.popleft()
        # A known league is still worth expanding through if it was handed in
        # as a seed -- that is how a resumed crawl reaches new territory.
        already = league_id in seen_leagues and league_id not in seed_set
        if already:
            continue
        seen_leagues.add(league_id)

        if league_id not in seed_set or not SleeperLeague.objects.filter(
            league_id=league_id
        ).exists():
            league = client.league(league_id)
            if not league:
                continue
            if save_league(league):
                faab_count += 1
            saved += 1

        if depth >= max_depth:
            continue

        # Expand: every member of this league, and every league they are in.
        members = client.league_users(league_id)
        new_users = [
            u['user_id'] for u in members
            if u.get('user_id') and u['user_id'] not in seen_users
        ]
        seen_users.update(new_users)

        for leagues in client.map(lambda uid: client.user_leagues(uid, season), new_users):
            for lg in leagues:
                lid = str(lg.get('league_id') or '')
                if lid and lid not in seen_leagues:
                    queue.append((lid, depth + 1))

    return {
        'visited': len(seen_leagues),
        'saved': saved,
        'faab': faab_count,
        'users_seen': len(seen_users),
        'api_calls': client.calls,
    }


def _player_lookup(sleeper_ids: Iterable[str]) -> dict:
    """Map Sleeper player ids to local Player ids in one query."""
    return dict(
        Player.objects.filter(sleeper_id__in=list(sleeper_ids))
        .values_list('sleeper_id', 'id')
    )


def parse_transactions(league: SleeperLeague, week: int, transactions: List[dict]) -> List[dict]:
    """
    Turn raw Sleeper transactions into normalised MarketBid dicts.

    Keeps failed claims as well as successful ones: the losing bids are what
    make a win-probability curve possible, and they are roughly half the data.
    """
    out = []
    for txn in transactions or []:
        if txn.get('type') != 'waiver':
            continue
        bid_raw = (txn.get('settings') or {}).get('waiver_bid')
        if bid_raw is None:
            continue
        adds = txn.get('adds') or {}
        if not adds:
            continue
        status = txn.get('status')
        created = txn.get('created')
        for sleeper_player_id in adds:
            out.append(
                {
                    # One transaction can add multiple players; keep the ids
                    # unique so the idempotency constraint still holds.
                    'transaction_id': f'{txn.get("transaction_id")}:{sleeper_player_id}',
                    'league': league,
                    'sleeper_player_id': str(sleeper_player_id),
                    'season': league.season,
                    'week': week,
                    'bid_raw': int(bid_raw),
                    'budget': league.waiver_budget,
                    'bid_pct': normalise_bid(int(bid_raw), league.waiver_budget),
                    'won': status == 'complete',
                    'processed_at': (
                        datetime.fromtimestamp(created / 1000, tz=dt_timezone.utc)
                        if created else None
                    ),
                }
            )
    return out


def ingest_week(
    client: SleeperClient,
    season: int,
    week: int,
    leagues: Optional[Iterable[SleeperLeague]] = None,
    include_zero_bids: bool = True,
) -> dict:
    """
    Sweep every active league for one week and persist normalised bids.

    One API call per league. At the default rate limit a corpus of a few
    thousand leagues finishes in minutes, well inside the window between when
    early leagues process waivers and when later ones do.
    """
    if leagues is None:
        leagues = SleeperLeague.objects.filter(season=season, is_active=True)
    leagues = list(leagues)
    if not leagues:
        return {'leagues': 0, 'bids': 0, 'created': 0, 'api_calls': client.calls}

    def fetch(league):
        return league, client.transactions(league.league_id, week)

    rows, empty_leagues = [], []
    for league, transactions in client.map(fetch, leagues):
        parsed = parse_transactions(league, week, transactions)
        if not parsed:
            empty_leagues.append(league)
        rows.extend(parsed)

    if not include_zero_bids:
        rows = [r for r in rows if r['bid_pct'] > 0]

    lookup = _player_lookup({r['sleeper_player_id'] for r in rows})
    created = 0
    with transaction.atomic():
        objects = [
            MarketBid(
                transaction_id=r['transaction_id'],
                league=r['league'],
                player_id=lookup.get(r['sleeper_player_id']),
                sleeper_player_id=r['sleeper_player_id'],
                season=r['season'],
                week=r['week'],
                bid_raw=r['bid_raw'],
                budget=r['budget'],
                bid_pct=r['bid_pct'],
                won=r['won'],
                processed_at=r['processed_at'],
            )
            for r in rows
        ]
        # ignore_conflicts makes a re-run of the same week a no-op, so a
        # partially failed ingest can simply be retried.
        MarketBid.objects.bulk_create(objects, batch_size=1000, ignore_conflicts=True)
        created = len(objects)

        touched = [lg.pk for lg in leagues if lg not in empty_leagues]
        SleeperLeague.objects.filter(pk__in=touched).update(
            last_ingested_week=week, empty_week_streak=0
        )
        for league in empty_leagues:
            league.empty_week_streak += 1
            league.is_active = league.empty_week_streak < EMPTY_WEEK_LIMIT
            league.save(update_fields=['empty_week_streak', 'is_active'])

    return {
        'leagues': len(leagues),
        'bids': created,
        'unmatched_players': sum(1 for r in rows if r['sleeper_player_id'] not in lookup),
        'empty_leagues': len(empty_leagues),
        'api_calls': client.calls,
    }


def link_orphan_market_bids(season: Optional[int] = None) -> int:
    """
    Attach a Player to MarketBids ingested before that player was mapped.

    Ingest stores every bid whether or not the player is known locally, but
    aggregation only counts rows with a player, so without this pass any bid
    that arrived ahead of the Sleeper player sync would be silently dropped.
    Run after sync_sleeper_players.
    """
    qs = MarketBid.objects.filter(player__isnull=True)
    if season:
        qs = qs.filter(season=season)

    orphan_ids = set(qs.values_list('sleeper_player_id', flat=True).distinct())
    if not orphan_ids:
        return 0

    lookup = _player_lookup(orphan_ids)
    linked = 0
    for sleeper_id, player_id in lookup.items():
        linked += qs.filter(sleeper_player_id=sleeper_id).update(player_id=player_id)
    return linked
