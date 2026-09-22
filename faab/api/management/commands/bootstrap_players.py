"""
Create Player/Team/Position rows from Sleeper's player dump.

For a fresh database. An existing install already has players and should use
sync_sleeper_players instead, which only attaches sleeper_id to what is there.
By default this creates only players that ingested market bids actually
reference, so the table stays proportional to the data rather than importing
Sleeper's entire roster.
"""
from django.core.management.base import BaseCommand
from django.db import transaction

from api.models import MarketBid, Player, Position, Team
from api.services.sleeper import SleeperClient

FANTASY_POSITIONS = {'QB', 'RB', 'WR', 'TE', 'K', 'DEF'}
# Sleeper serves headshots from a stable public CDN path.
HEADSHOT = 'https://sleepercdn.com/content/nfl/players/{}.jpg'
TEAM_LOGO = 'https://sleepercdn.com/images/team_logos/nfl/{}.png'


class Command(BaseCommand):
    help = 'Create Player rows from the Sleeper player dump.'

    def add_arguments(self, parser):
        parser.add_argument('--refresh', action='store_true', help='Bypass the disk cache.')
        parser.add_argument(
            '--all', action='store_true',
            help='Import every fantasy-relevant player, not just referenced ones.',
        )

    def handle(self, *args, **opts):
        from api.management.commands.sync_sleeper_players import load_players

        blob = load_players(SleeperClient(), refresh=opts['refresh'])
        if not blob:
            self.stderr.write('could not load Sleeper player dump')
            return

        if opts['all']:
            wanted = None
        else:
            wanted = set(
                MarketBid.objects.values_list('sleeper_player_id', flat=True).distinct()
            )
            if not wanted:
                self.stderr.write('no market bids yet; pass --all or ingest first')
                return

        existing = set(Player.objects.exclude(sleeper_id=None).values_list('sleeper_id', flat=True))
        teams, positions = {}, {}
        created = skipped = 0

        with transaction.atomic():
            for sleeper_id, p in blob.items():
                sleeper_id = str(sleeper_id)
                if not isinstance(p, dict) or sleeper_id in existing:
                    continue
                if wanted is not None and sleeper_id not in wanted:
                    continue
                pos = p.get('position')
                if pos not in FANTASY_POSITIONS:
                    continue

                name = (p.get('full_name')
                        or f"{p.get('first_name', '')} {p.get('last_name', '')}").strip()
                if not name:
                    continue
                # Player.name is unique; a collision means we already have them
                # under a different (or missing) sleeper id.
                if Player.objects.filter(name=name).exists():
                    skipped += 1
                    continue

                abbr = (p.get('team') or 'FA')[:4]
                if abbr not in teams:
                    teams[abbr], _ = Team.objects.get_or_create(
                        abbreviation=abbr, defaults={'team_name': abbr}
                    )
                if pos not in positions:
                    positions[pos], _ = Position.objects.get_or_create(position_type=pos)

                Player.objects.create(
                    name=name,
                    sleeper_id=sleeper_id,
                    team=teams[abbr],
                    position=positions[pos],
                    image=(TEAM_LOGO.format(sleeper_id.lower()) if pos == 'DEF'
                           else HEADSHOT.format(sleeper_id)),
                )
                created += 1

        self.stdout.write(f'  created: {created}  name-collisions skipped: {skipped}')
        self.stdout.write(self.style.SUCCESS(
            f'player table now holds {Player.objects.count()} rows'
        ))
