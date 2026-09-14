"""
Rebuild aggregates from raw rows.

Safe to re-run: aggregates are derived data, so this is the recovery path if a
write is ever missed or the summary logic changes.
"""
from django.core.management.base import BaseCommand

from api.services.aggregates import rebuild_crowd_week, rebuild_market_week
from api.services.weeks import NFL_WEEKS, to_legacy_week


class Command(BaseCommand):
    help = 'Rebuild crowd and/or market aggregates for a season.'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, required=True)
        parser.add_argument('--week', type=int, help='Single NFL week; default all.')
        parser.add_argument('--scope', choices=['crowd', 'market', 'both'], default='both')
        parser.add_argument('--no-slices', action='store_true')

    def handle(self, *args, **opts):
        season = opts['season']
        weeks = [opts['week']] if opts['week'] else list(NFL_WEEKS)

        for week in weeks:
            if opts['scope'] in ('crowd', 'both'):
                legacy = to_legacy_week(season, week)
                if legacy is None:
                    self.stderr.write(
                        f'  season {season} has no LEGACY_WEEK_OFFSETS entry; '
                        f'skipping crowd rebuild'
                    )
                else:
                    n = rebuild_crowd_week(season=season, week=week, legacy_week=legacy)
                    if n:
                        self.stdout.write(f'  crowd {season}w{week} (legacy {legacy}): {n}')

            if opts['scope'] in ('market', 'both'):
                n = rebuild_market_week(
                    season=season, week=week, slices=not opts['no_slices']
                )
                if n:
                    self.stdout.write(f'  market {season}w{week}: {n}')

        self.stdout.write(self.style.SUCCESS('rebuild complete'))
