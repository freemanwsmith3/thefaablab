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


def surname_key(name: str) -> str:
    """
    'Kenneth Gainwell' and 'Kenny Gainwell' both -> 'k gainwell'.

    A fallback for when exact names differ by a nickname. Deliberately coarse,
    so callers must check it resolves to exactly one candidate before trusting
    it -- two players sharing a surname and initial would collide.
    """
    parts = normalise(name).split()
    if len(parts) < 2:
        return ''
    return f'{parts[0][0]} {parts[-1]}'


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
        candidates_for = {}
        for player in Player.objects.filter(sleeper_id__isnull=True).only('id', 'name'):
            found = by_name.get(normalise(player.name))
            if not found:
                missed += 1
            elif len(found) > 1:
                ambiguous += 1
            else:
                candidates_for.setdefault(next(iter(found)), []).append(player)

        # Two local rows can normalise to the same name -- "D.J. Chark Jr." and
        # "DJ Chark Jr." both reduce to "dj chark" -- and would then be assigned
        # the same Sleeper id. sleeper_id is unique, so that aborts the whole
        # batch. These are duplicate player records rather than a matching
        # failure, so report them and leave both unmapped.
        collisions = {sid: ps for sid, ps in candidates_for.items() if len(ps) > 1}

        # Ids already claimed in the database cannot be assigned again either.
        taken = set(
            Player.objects.exclude(sleeper_id=None)
            .filter(sleeper_id__in=list(candidates_for))
            .values_list('sleeper_id', flat=True)
        )

        updates = []
        for sleeper_id, players in candidates_for.items():
            if len(players) > 1 or sleeper_id in taken:
                continue
            players[0].sleeper_id = sleeper_id
            updates.append(players[0])
        matched = len(updates)

        if collisions:
            self.stdout.write(self.style.WARNING(
                f'\n  {len(collisions)} Sleeper id(s) matched by more than one player '
                f'-- skipped, these look like duplicate records:'
            ))
            for sid, players in collisions.items():
                names = ' | '.join(f'#{p.id} {p.name}' for p in players)
                self.stdout.write(f'    {sid}: {names}')
        if taken:
            self.stdout.write(self.style.WARNING(
                f'  {len(taken)} id(s) already assigned to another player -- skipped'
            ))

        if updates and not opts['dry_run']:
            Player.objects.bulk_update(updates, ['sleeper_id'], batch_size=500)

        self.stdout.write(
            f'\n  matched: {matched}  ambiguous: {ambiguous}  unmatched: {missed}'
            f'{"  (dry run)" if opts["dry_run"] else ""}'
        )
        self.stdout.write(self.style.SUCCESS('player sync complete'))
