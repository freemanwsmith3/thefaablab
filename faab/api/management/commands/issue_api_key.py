"""Issue a public API key. The key is printed once and never recoverable."""
from django.core.management.base import BaseCommand

from api.models import ApiTier
from api.services import apikeys


class Command(BaseCommand):
    help = 'Issue an API key for the public data API.'

    def add_arguments(self, parser):
        parser.add_argument('name', help='What this key is for.')
        parser.add_argument('--email', default='')
        parser.add_argument(
            '--tier', default=ApiTier.FREE,
            choices=[t.value for t in ApiTier if t != ApiTier.ANON],
        )

    def handle(self, *args, **opts):
        key, full = apikeys.issue(opts['name'], opts['email'], opts['tier'])
        self.stdout.write(self.style.SUCCESS(f'\n  {full}\n'))
        self.stdout.write(
            f'  tier {key.tier} · {key.monthly_quota:,} calls/month · prefix {key.prefix}'
        )
        self.stdout.write(self.style.WARNING(
            '  Only the hash is stored. Copy it now -- it cannot be shown again.'
        ))
