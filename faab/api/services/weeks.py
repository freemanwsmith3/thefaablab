"""
Translating the legacy running week counter into (season, nfl_week).

The old schema stored an opaque incrementing week (27, 29, 53...) and the
frontend subtracted a constant to display it. That coupling is the reason the
app breaks every September, so everything new is keyed on an explicit
(season, week) pair and the legacy value is translated at the edge.
"""
from django.conf import settings

NFL_WEEKS = range(1, 19)


def offsets() -> dict:
    return getattr(settings, 'LEGACY_WEEK_OFFSETS', {}) or {}


def to_season_week(legacy_week: int):
    """
    Resolve a legacy week to (season, nfl_week), or (None, None) if no
    configured offset produces a sane NFL week.
    """
    legacy_week = int(legacy_week)
    best = None
    for season, offset in sorted(offsets().items()):
        candidate = legacy_week - int(offset)
        if candidate in NFL_WEEKS:
            # Later seasons win ties: offsets are ascending, so the last match
            # is the most recent season that can explain this value.
            best = (season, candidate)
    return best if best else (None, None)


def to_legacy_week(season: int, week: int):
    """Inverse of to_season_week, or None if the season has no offset."""
    offset = offsets().get(int(season))
    return int(week) + int(offset) if offset is not None else None
