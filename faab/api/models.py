"""
Data model for FAAB Lab.

Two independent sources of truth feed one shared aggregate table:

  crowd  -- what visitors say they would bid (the original product)
  market -- what Sleeper leagues actually paid (ingested weekly)

Raw rows are append-only and are never read to serve a page. Every read-path
statistic comes from BidAggregate, which stores a 101-slot count array. Because
a normalised bid is an integer 0..100, that array is a complete sufficient
statistic: mean, median, mode, any percentile and the win-probability curve are
all exactly derivable from it without touching a raw row.
"""
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

BID_MIN = 0
BID_MAX = 100
NUM_BUCKETS = BID_MAX + 1


def zero_counts():
    """Default factory for a 101-slot histogram."""
    return [0] * NUM_BUCKETS


# ---------------------------------------------------------------------------
# Reference data
# ---------------------------------------------------------------------------
class Team(models.Model):
    team_name = models.CharField(max_length=50, unique=True)
    abbreviation = models.CharField(max_length=4, unique=True)

    def __str__(self):
        return self.abbreviation


class Position(models.Model):
    position_type = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.position_type


class Player(models.Model):
    name = models.CharField(max_length=50, unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='teams', null=True)
    position = models.ForeignKey(
        Position, on_delete=models.CASCADE, related_name='positions', null=True
    )
    link = models.CharField(max_length=256, unique=True, null=True)
    image = models.CharField(max_length=256, null=True)

    # Sleeper's player id, promoted from the side-car mapping JSON to a real
    # indexed column so market ingest can join without loading a dict.
    sleeper_id = models.CharField(
        max_length=16, null=True, blank=True, unique=True, db_index=True
    )

    class Meta:
        indexes = [models.Index(fields=['name'], name='player_name_idx')]

    def __str__(self):
        return self.name


# ---------------------------------------------------------------------------
# Crowd side (existing product)
# ---------------------------------------------------------------------------
class Target(models.Model):
    """A player surfaced for bidding in a given legacy week."""

    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='targets')
    week = models.IntegerField(
        null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )

    class Meta:
        indexes = [models.Index(fields=['week', 'player'], name='target_week_player_idx')]


class BidOriginal(models.Model):
    value = models.IntegerField(
        null=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    target = models.ForeignKey(Target, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(
        null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )
    user = models.CharField(max_length=50)


class Bid(models.Model):
    """Append-only crowd bid. Never scanned on the read path."""

    value = models.IntegerField(
        null=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='bids')
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(
        null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )
    user = models.CharField(max_length=50)

    # Stable per-browser identity derived from a signed cookie. Null for the
    # historical rows written before this existed.
    submitter = models.CharField(max_length=64, null=True, blank=True, db_index=True)

    class Meta:
        indexes = [
            # Serves the backfill and any ad-hoc analysis. The read path does
            # not use this table at all.
            models.Index(fields=['week', 'player'], name='bid_week_player_idx'),
        ]
        constraints = [
            # One bid per browser per player per week. Historical rows have a
            # null submitter and are exempt, so this applies going forward only.
            models.UniqueConstraint(
                fields=['player', 'week', 'submitter'],
                condition=models.Q(submitter__isnull=False),
                name='uniq_bid_per_submitter_player_week',
            )
        ]


class Ranking(models.Model):
    rank = models.IntegerField(
        null=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    Player = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='rankings')
    created_at = models.DateTimeField(auto_now_add=True)
    week = models.IntegerField(
        null=False, validators=[MinValueValidator(0), MaxValueValidator(2000)]
    )
    user = models.CharField(max_length=50)
    opponent = models.ForeignKey(
        Team, on_delete=models.CASCADE, related_name='opponents', null=True
    )

    class Meta:
        indexes = [
            models.Index(fields=['week', 'Player'], name='ranking_week_player_idx'),
            models.Index(fields=['week', 'user'], name='ranking_week_user_idx'),
        ]


class Auction(models.Model):
    rank = models.IntegerField(
        null=False, default=0, validators=[MinValueValidator(0), MaxValueValidator(200)]
    )
    Player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='auction_rankings'
    )


# ---------------------------------------------------------------------------
# Market side (Sleeper)
# ---------------------------------------------------------------------------
class ScoringFormat(models.TextChoices):
    ALL = 'all', 'All formats'
    PPR = 'ppr', 'PPR'
    HALF = 'half', 'Half PPR'
    STANDARD = 'std', 'Standard'


class SleeperLeague(models.Model):
    """
    A discovered FAAB league. This registry is the corpus: the weekly ingest
    walks it, so discovery cost is paid once and amortised over the season.
    """

    league_id = models.CharField(max_length=32, unique=True)
    season = models.IntegerField(db_index=True)
    total_rosters = models.IntegerField(default=0)
    waiver_budget = models.IntegerField(default=100)
    waiver_type = models.IntegerField(default=2)
    waiver_day = models.IntegerField(null=True, blank=True)
    scoring = models.CharField(
        max_length=8, choices=ScoringFormat.choices, default=ScoringFormat.STANDARD
    )
    ppr_value = models.FloatField(default=0.0)
    previous_league_id = models.CharField(max_length=32, null=True, blank=True)

    # Set false once a league proves inactive so it stops costing API calls.
    is_active = models.BooleanField(default=True, db_index=True)
    last_ingested_week = models.IntegerField(default=0)
    empty_week_streak = models.IntegerField(default=0)
    discovered_at = models.DateTimeField(auto_now_add=True)
    last_seen_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=['season', 'is_active'], name='league_season_active_idx'),
        ]

    def __str__(self):
        return f'{self.league_id} ({self.season}, {self.total_rosters}-team)'


class MarketBid(models.Model):
    """
    One real waiver bid from one league, normalised to percent of budget.

    transaction_id is Sleeper's own id and is unique, which makes re-ingesting
    a week idempotent -- backfills can be re-run freely.
    """

    transaction_id = models.CharField(max_length=32, unique=True)
    league = models.ForeignKey(
        SleeperLeague, on_delete=models.CASCADE, related_name='market_bids'
    )
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='market_bids', null=True
    )
    sleeper_player_id = models.CharField(max_length=16, db_index=True)

    season = models.IntegerField()
    week = models.IntegerField()

    bid_raw = models.IntegerField()
    budget = models.IntegerField()
    # bid_raw / budget * 100, clamped to 0..100. Aggregate on this only --
    # league budgets in the wild range from 100 to 1000.
    bid_pct = models.IntegerField(
        validators=[MinValueValidator(BID_MIN), MaxValueValidator(BID_MAX)]
    )
    won = models.BooleanField()
    processed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(
                fields=['season', 'week', 'sleeper_player_id'], name='market_swp_idx'
            ),
            models.Index(fields=['season', 'week', 'player'], name='market_swplayer_idx'),
        ]


# ---------------------------------------------------------------------------
# The read path
# ---------------------------------------------------------------------------
class BidAggregate(models.Model):
    """
    Precomputed distribution for one (scope, player, season, week, slice).

    `counts` holds every bid; `won_counts` holds only winning bids, which is
    what makes the win-probability curve possible. Scalar columns are
    denormalised at write time so a page render selects numbers, not arrays.
    """

    class Scope(models.TextChoices):
        CROWD = 'crowd', 'Crowd'
        MARKET = 'market', 'Market'

    scope = models.CharField(max_length=8, choices=Scope.choices)
    player = models.ForeignKey(
        Player, on_delete=models.CASCADE, related_name='aggregates'
    )
    season = models.IntegerField()
    week = models.IntegerField()

    # Slice dimensions. 0 / 'all' means "every league", which is the row the
    # unfiltered page reads.
    league_size = models.IntegerField(default=0)
    scoring = models.CharField(
        max_length=8, choices=ScoringFormat.choices, default=ScoringFormat.ALL
    )

    counts = models.JSONField(default=zero_counts)
    won_counts = models.JSONField(default=zero_counts)

    n = models.IntegerField(default=0)
    n_leagues = models.IntegerField(default=0)
    mean = models.FloatField(null=True, blank=True)
    median = models.FloatField(null=True, blank=True)
    mode = models.IntegerField(null=True, blank=True)
    p25 = models.FloatField(null=True, blank=True)
    p75 = models.FloatField(null=True, blank=True)
    min_bid = models.IntegerField(null=True, blank=True)
    max_bid = models.IntegerField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['scope', 'player', 'season', 'week', 'league_size', 'scoring'],
                name='uniq_aggregate_slice',
            )
        ]
        indexes = [
            # The single index the week endpoint rides on.
            models.Index(
                fields=['scope', 'season', 'week', 'league_size', 'scoring'],
                name='agg_lookup_idx',
            ),
        ]

    def __str__(self):
        return f'{self.scope} p{self.player_id} {self.season}w{self.week} n={self.n}'


# ---------------------------------------------------------------------------
# Public API access
# ---------------------------------------------------------------------------
class ApiTier(models.TextChoices):
    """
    Tiers are deliberately generous at the bottom.

    An AI agent that discovers this API cannot sign up -- it has no email and no
    card. If its first call fails it moves on and we never hear about it. So
    anonymous callers get a real, working quota, a free key raises it, and the
    paid tiers exist for volume. The free tier is the marketing.
    """

    ANON = 'anon', 'Anonymous (no key)'
    FREE = 'free', 'Free'
    HOBBY = 'hobby', 'Hobby'
    PRO = 'pro', 'Pro'


# Monthly call allowance per tier. ANON is also capped per-IP per day.
TIER_QUOTAS = {
    ApiTier.ANON: 300,
    ApiTier.FREE: 5_000,
    ApiTier.HOBBY: 100_000,
    ApiTier.PRO: 1_000_000,
}

TIER_PRICES_USD = {
    ApiTier.ANON: 0,
    ApiTier.FREE: 0,
    ApiTier.HOBBY: 5,
    ApiTier.PRO: 25,
}


class ApiKey(models.Model):
    """
    A public API credential.

    Only a hash of the key is stored, so a database leak exposes nothing that
    can be replayed. The prefix is kept in clear to let a holder identify which
    key is which without revealing it.
    """

    name = models.CharField(max_length=120, help_text='What this key is for.')
    email = models.EmailField(blank=True, help_text='Where to reach the owner.')
    prefix = models.CharField(max_length=12, unique=True, db_index=True)
    key_hash = models.CharField(max_length=64, unique=True, db_index=True)
    tier = models.CharField(max_length=8, choices=ApiTier.choices, default=ApiTier.FREE)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)

    # Set by the billing webhook; nothing here talks to a payment provider.
    stripe_customer_id = models.CharField(max_length=64, blank=True)

    class Meta:
        indexes = [models.Index(fields=['key_hash', 'is_active'], name='apikey_lookup_idx')]

    def __str__(self):
        return f'{self.prefix}… ({self.tier})'

    @property
    def monthly_quota(self) -> int:
        return TIER_QUOTAS.get(self.tier, TIER_QUOTAS[ApiTier.FREE])


class ApiUsage(models.Model):
    """
    One row per key per month. Counting monthly rather than per call keeps the
    write path to a single UPDATE and makes the quota trivial to reason about.
    """

    key = models.ForeignKey(
        ApiKey, on_delete=models.CASCADE, related_name='usage', null=True, blank=True
    )
    # For anonymous callers, who have no key.
    client_ip = models.CharField(max_length=45, blank=True, db_index=True)
    period = models.CharField(max_length=7, help_text='YYYY-MM')
    calls = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['key', 'period'],
                condition=models.Q(key__isnull=False),
                name='uniq_usage_key_period',
            ),
            models.UniqueConstraint(
                fields=['client_ip', 'period'],
                condition=models.Q(key__isnull=True),
                name='uniq_usage_ip_period',
            ),
        ]
        indexes = [models.Index(fields=['period'], name='usage_period_idx')]
