"""Build the league corpus by crawling the public Sleeper graph."""
from django.core.management.base import BaseCommand, CommandError

from api.models import SleeperLeague
from api.services.ingest import discover
from api.services.sleeper import SleeperClient


class Command(BaseCommand):
    help = 'Discover FAAB leagues by crawling the Sleeper social graph from seeds.'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, required=True)
        parser.add_argument(
            '--seed-league', action='append', default=[],
            help='Seed league id. Repeatable.',
        )
        parser.add_argument(
            '--seed-user', action='append', default=[],
            help='Seed Sleeper username; all of their leagues become seeds. Repeatable.',
        )
        parser.add_argument('--max-leagues', type=int, default=2000)
        parser.add_argument('--max-depth', type=int, default=3)
        parser.add_argument(
            '--revisit-known', action='store_true',
            help='Re-fetch leagues already in the registry. Off by default so '
                 'scheduled incremental runs only spend calls on new leagues.',
        )
        parser.add_argument(
            '--reseed-from-registry', action='store_true',
            help='Also seed from leagues already stored for this season.',
        )

    def handle(self, *args, **opts):
        client = SleeperClient()
        seeds = list(opts['seed_league'])

        for username in opts['seed_user']:
            user = client.user(username)
            if not user or not user.get('user_id'):
                self.stderr.write(f'  unknown user: {username}')
                continue
            seeds += [
                str(lg['league_id'])
                for lg in client.user_leagues(user['user_id'], opts['season'])
                if lg.get('league_id')
            ]

        if opts['reseed_from_registry']:
            seeds += list(
                SleeperLeague.objects.filter(season=opts['season'])
                .values_list('league_id', flat=True)[:200]
            )

        seeds = list(dict.fromkeys(seeds))
        if not seeds:
            raise CommandError('no seeds; pass --seed-league or --seed-user')

        self.stdout.write(f'crawling from {len(seeds)} seed(s)...')
        result = discover(
            client, seeds, opts['season'],
            max_leagues=opts['max_leagues'], max_depth=opts['max_depth'],
            skip_known=not opts['revisit_known'],
        )
        for key, value in result.items():
            self.stdout.write(f'  {key}: {value}')
        self.stdout.write(self.style.SUCCESS(
            f'registry now holds '
            f'{SleeperLeague.objects.filter(season=opts["season"]).count()} '
            f'FAAB leagues for {opts["season"]}'
        ))
