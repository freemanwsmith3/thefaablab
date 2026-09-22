"""Weekly sweep: pull real FAAB bids for every registered league."""
from django.core.management.base import BaseCommand

from api.models import SleeperLeague
from api.services.aggregates import rebuild_market_week
from api.services.ingest import ingest_week, link_orphan_market_bids
from api.services.sleeper import SleeperClient


class Command(BaseCommand):
    help = 'Ingest Sleeper waiver bids for a week and rebuild market aggregates.'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int)
        parser.add_argument('--week', type=int)
        parser.add_argument(
            '--limit', type=int, default=0, help='Cap leagues swept (for testing).'
        )
        parser.add_argument(
            '--waiver-day', type=int, nargs='+',
            help='Only sweep leagues that process on these days (0=Sunday .. '
                 '6=Saturday, matching Sleeper). Useful mid-week: leagues that '
                 'have not run yet cost a call and return nothing.',
        )
        parser.add_argument(
            '--no-slices', action='store_true',
            help='Rebuild only the unfiltered aggregate, skipping filter slices.',
        )
        parser.add_argument('--skip-aggregates', action='store_true')

    def handle(self, *args, **opts):
        client = SleeperClient()

        season, week = opts.get('season'), opts.get('week')
        if season is None or week is None:
            # Derive from Sleeper itself so a scheduled run needs no arguments
            # and cannot drift out of sync with the real NFL calendar.
            state = client.state() or {}
            season = season or int(state.get('season') or 0)
            week = week or int(state.get('week') or 0)
            self.stdout.write(f'resolved from Sleeper state: season={season} week={week}')
        if not season or not week:
            self.stderr.write('could not resolve season/week')
            return

        leagues = SleeperLeague.objects.filter(season=season, is_active=True)
        if opts.get('waiver_day'):
            leagues = leagues.filter(waiver_day__in=opts['waiver_day'])
            self.stdout.write(
                f'  limited to waiver day(s) {opts["waiver_day"]}: {leagues.count()} leagues'
            )
        if opts['limit']:
            leagues = leagues[: opts['limit']]

        result = ingest_week(client, season, week, leagues=leagues)
        for key, value in result.items():
            self.stdout.write(f'  {key}: {value}')

        # Bids for players that were not mapped at ingest time would otherwise
        # never reach an aggregate.
        linked = link_orphan_market_bids(season=season)
        if linked:
            self.stdout.write(f'  orphan bids linked: {linked}')
        if result.get('unmatched_players'):
            self.stdout.write(self.style.WARNING(
                f'  {result["unmatched_players"]} bid(s) have no local player; '
                f'run sync_sleeper_players to map them'
            ))

        if result.get('leagues') and not result.get('bids'):
            self.stdout.write(self.style.WARNING(
                '  every league came back empty -- waivers have probably not '
                'processed for this week yet. No league was marked inactive.'
            ))

        if not opts['skip_aggregates']:
            written = rebuild_market_week(
                season=season, week=week, slices=not opts['no_slices']
            )
            self.stdout.write(f'  aggregates written: {written}')
        self.stdout.write(self.style.SUCCESS('ingest complete'))
