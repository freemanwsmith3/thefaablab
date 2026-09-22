"""
Write-path throttling.

Bids are anonymous, so the only thing standing between the aggregates and a
scripted loop is rate limiting plus the per-submitter unique constraint. Both
are needed: the constraint stops one browser voting twice on a player, the
throttle stops someone cycling identities.
"""
from rest_framework.throttling import AnonRateThrottle


class BidBurstThrottle(AnonRateThrottle):
    """Short window: blocks a tight submission loop."""

    scope = 'bid_burst'


class BidSustainedThrottle(AnonRateThrottle):
    """Long window: caps how much one address can shift a week's totals."""

    scope = 'bid_sustained'
