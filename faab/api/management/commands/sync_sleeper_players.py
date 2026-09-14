"""
Attach Sleeper player ids to local Player rows.

Promotes the mapping out of the side-car JSON file and into an indexed column
so market ingest can join in SQL. The ~5MB player dump is cached to disk and
refreshed at most daily, per Sleeper's guidance.
"""
import json
import re
import time
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import Player
from api.services.sleeper import SleeperClient

CACHE_PATH = Path(settings.BASE_DIR) / '.cache' / 'sleeper_players.json'
CACHE_TTL = 60 * 60 * 24  # Sleeper asks for at most one call per day.

SUFFIXES = {'jr', 'sr', 'ii', 'iii', 'iv', 'v'}


def normalise(name: str) -> str:
    """Lowercase, strip punctuation and generational suffixes, collapse spaces."""
    cleaned = re.sub(r"[^a-z\s]", '', (name or '').lower())
    parts = [p for p in cleaned.split() if p and p not in SUFFIXES]
    return ' '.join(parts)


def load_players(client: SleeperClient, refresh: bool = False) -> dict:
    if not refresh and CACHE_PATH.exists():
        if time.time() - CACHE_PATH.stat().st_mtime < CACHE_TTL:
            return json.loads(CACHE_PATH.read_text())
    data = client.all_players() or {}
    if data:
        CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        CACHE_PATH.write_text(json.dumps(data))
    return data


class Command(BaseCommand):
    help = 'Match local players to Sleeper player ids by normalised name.'

    def add_arguments(self, parser):
        parser.add_argument('--refresh', action='store_true', help='Bypass the disk cache.')
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **opts):
        client = SleeperClient()
        blob = load_players(client, refresh=opts['refresh'])
        if not blob:
            self.stderr.write('could not load Sleeper player dump')
            return

        # Only fantasy-relevant positions; ambiguity across the full dump is
        # much higher and produces bad matches.
        by_name = {}
        for sleeper_id, p in blob.items():
            if not isinstance(p, dict):
                continue
            pos = p.get('position')
            if pos not in {'QB', 'RB', 'WR', 'TE', 'K', 'DEF'}:
                continue
            full = p.get('full_name') or f"{p.get('first_name','')} {p.get('last_name','')}"
            key = normalise(full)
            if key:
                # A name colliding across players is not safely resolvable here.
                by_name.setdefault(key, set()).add(str(sleeper_id))

        matched = ambiguous = missed = 0
        updates = []
        for player in Player.objects.filter(sleeper_id__isnull=True).only('id', 'name'):
            candidates = by_name.get(normalise(player.name))
            if not candidates:
                missed += 1
            elif len(candidates) > 1:
                ambiguous += 1
            else:
                player.sleeper_id = next(iter(candidates))
                updates.append(player)
                matched += 1

        if updates and not opts['dry_run']:
            # Unique constraint means a duplicate would abort the batch, so
            # drop ids already claimed by another row first.
            taken = set(
                Player.objects.filter(
                    sleeper_id__in=[p.sleeper_id for p in updates]
                ).values_list('sleeper_id', flat=True)
            )
            updates = [p for p in updates if p.sleeper_id not in taken]
            Player.objects.bulk_update(updates, ['sleeper_id'], batch_size=500)

        self.stdout.write(
            f'  matched: {matched}  ambiguous: {ambiguous}  unmatched: {missed}'
            f'{"  (dry run)" if opts["dry_run"] else ""}'
        )
        self.stdout.write(self.style.SUCCESS('player sync complete'))
