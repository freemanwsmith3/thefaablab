"""
Set the week's waiver targets.

Replaces faab/faab/weekly_waivers_csv.py, which hardcoded the week at the top
of the file, carried production credentials in source, hand-mapped team names to
integer ids, and inserted duplicate rows on a re-run.

Two sources:
  --from-trending   the players Sleeper users are actually adding (default)
  --csv <path>      a FantasyPros-style export, for a hand-picked list

Safe to re-run: targets are keyed on (player, season, nfl_week), so a second run
updates rather than duplicating.
"""
import csv
import re
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import Player, Target
from api.services.sleeper import SleeperClient
from api.services.weeks import to_legacy_week

SKIP_POSITIONS = {'K', 'DEF', 'DST'}

# Where the weekly exports live, named <season>_week_<week>.csv
CSV_DIR = Path(__file__).resolve().parents[3] / 'faab' / 'stats'


def bare_position(value: str) -> str:
    """'RB1' -> 'RB', 'DST2' -> 'DST', 'K3' -> 'K'. The export ranks within
    position, so the trailing digits have to come off before comparing."""
    return re.sub(r'\d+$', '', (value or '').strip().upper())


def default_csv_for(season: int, week: int) -> Path:
    return CSV_DIR / f'{season}_week_{week}.csv'


def legacy_week_for(season: int, week: int) -> int:
    """
    A value for the old `week` column that cannot collide with real history.

    That column has a unique constraint with player_id and still holds genuine
    targets from past seasons at low numbers (0-53). Writing an NFL week
    straight into it would overwrite them. When a season has a configured
    offset we honour it; otherwise we allocate from a block that predates
    nothing: 1500 + (season - 2000) * 20 + week, which stays inside the
    column's 0-2000 validator and is unique per season and week.
    """
    mapped = to_legacy_week(season, week)
    if mapped is not None:
        return mapped
    return 1500 + (int(season) - 2000) % 25 * 20 + int(week)


class Command(BaseCommand):
    help = "Set a week's waiver targets from Sleeper trending or a CSV."

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, help='Defaults to the live NFL season.')
        parser.add_argument('--week', type=int, help='Defaults to the live NFL week.')
        parser.add_argument(
            '--csv',
            help='Path to a weekly export. Defaults to '
                 'faab/faab/stats/<season>_week_<week>.csv when that file exists.',
        )
        parser.add_argument(
            '--from-trending', action='store_true',
            help='Use Sleeper trending adds (the default when no --csv is given).',
        )
        parser.add_argument('--limit', type=int, default=25, help='How many targets.')
        parser.add_argument(
            '--lookback-hours', type=int, default=48,
            help='Trending window. 48h spans the days after most waivers run.',
        )
        parser.add_argument(
            '--replace', action='store_true',
            help='Remove targets for the week that are not in this run.',
        )
        parser.add_argument(
            '--create-missing', action='store_true',
            help="Create Player rows for names not in the table, matched against "
                 "Sleeper's player dump. Without this they are simply skipped, "
                 "which is usually why a week loads far fewer targets than the "
                 "export lists.",
        )
        parser.add_argument('--dry-run', action='store_true')

    # -- sources ---------------------------------------------------------
    def _from_trending(self, client, limit, lookback):
        rows = client.trending('add', lookback_hours=lookback, limit=limit * 3)
        if not rows:
            raise CommandError('Sleeper returned no trending players')
        ids = [str(r['player_id']) for r in rows]
        counts = {str(r['player_id']): r['count'] for r in rows}
        # One query, then filter in Python -- the dump has no position filter.
        found = Player.objects.filter(sleeper_id__in=ids).select_related('position')
        by_sleeper = {p.sleeper_id: p for p in found}

        picked = []
        for sid in ids:                       # preserve Sleeper's ordering
            p = by_sleeper.get(sid)
            if not p:
                continue
            pos = p.position.position_type if p.position_id else ''
            if pos in SKIP_POSITIONS:
                continue
            picked.append((p, counts.get(sid)))
            if len(picked) >= limit:
                break
        unmatched = len(ids) - len(by_sleeper)
        return picked, unmatched

    def _from_csv(self, path, limit):
        p = Path(path)
        if not p.exists():
            raise CommandError(f'no such file: {p}')
        names, skipped = [], 0
        for row in csv.DictReader(p.open()):
            name = (row.get('PLAYER NAME') or row.get('player_name') or '').strip()
            pos = bare_position(row.get('POS') or row.get('pos') or '')
            if not name:
                continue
            if pos in SKIP_POSITIONS:
                skipped += 1
                continue
            names.append(name)
        if skipped:
            self.stdout.write(f'  skipped {skipped} kicker/defense row(s)')
        return names[:limit]

    def _resolve_names(self, names, create_missing, client):
        """Names -> Player rows, optionally creating any the table lacks."""
        by_name = {p.name: p for p in Player.objects.filter(name__in=names)}
        missing = [n for n in names if n not in by_name]

        if missing and create_missing:
            created = self._create_from_sleeper(missing, client)
            by_name.update(created)
            missing = [n for n in missing if n not in by_name]

        picked = [(by_name[n], None) for n in names if n in by_name]
        return picked, missing

    def _create_from_sleeper(self, names, client):
        """
        Look the missing names up in Sleeper's dump and create them.

        Matched on a normalised name so generational suffixes do not block it --
        the export writes "Harold Fannin Jr." where Sleeper has "Harold Fannin".
        """
        from api.management.commands.sync_sleeper_players import (
            load_players, normalise, surname_key,
        )
        from api.models import Position, Team

        blob = load_players(client)
        if not blob:
            self.stdout.write(self.style.WARNING('  could not load the Sleeper dump'))
            return {}

        wanted = {normalise(n): n for n in names}
        # Second pass for nickname mismatches ("Kenneth" in the export,
        # "Kenny" on Sleeper). Only used when it resolves unambiguously.
        by_surname = {}
        for n in names:
            k = surname_key(n)
            if k:
                by_surname.setdefault(k, []).append(n)
        fallback = {k: v[0] for k, v in by_surname.items() if len(v) == 1}
        surname_hits = {}
        taken = set(
            Player.objects.exclude(sleeper_id=None).values_list('sleeper_id', flat=True)
        )
        teams, positions, created = {}, {}, {}

        for sleeper_id, sp in blob.items():
            if not isinstance(sp, dict):
                continue
            pos = sp.get('position')
            if pos in SKIP_POSITIONS or pos not in {'QB', 'RB', 'WR', 'TE'}:
                continue
            full = sp.get('full_name') or f"{sp.get('first_name','')} {sp.get('last_name','')}"
            key = normalise(full)
            if str(sleeper_id) in taken:
                continue
            if key in wanted:
                original = wanted.pop(key)
            else:
                # Nickname fallback: collect candidates, resolve after the loop
                # so an ambiguous surname is never guessed at.
                sk = surname_key(full)
                if sk in fallback:
                    surname_hits.setdefault(sk, []).append((sleeper_id, sp, full))
                continue
            abbr = (sp.get('team') or 'FA')[:4]
            if abbr not in teams:
                teams[abbr], _ = Team.objects.get_or_create(
                    abbreviation=abbr, defaults={'team_name': abbr}
                )
            if pos not in positions:
                positions[pos], _ = Position.objects.get_or_create(position_type=pos)

            player, _ = Player.objects.get_or_create(
                name=original,
                defaults={
                    'sleeper_id': str(sleeper_id),
                    'team': teams[abbr],
                    'position': positions[pos],
                    'image': f'https://sleepercdn.com/content/nfl/players/{sleeper_id}.jpg',
                },
            )
            created[original] = player

        # Resolve the nickname fallbacks that matched exactly one Sleeper player.
        for sk, hits in surname_hits.items():
            original = fallback.get(sk)
            if not original or original in created or len(hits) != 1:
                if len(hits) > 1:
                    self.stdout.write(self.style.WARNING(
                        f'  {fallback.get(sk)}: ambiguous, {len(hits)} Sleeper '
                        f'players share that surname and initial -- skipped'
                    ))
                continue
            sleeper_id, sp, full = hits[0]
            abbr = (sp.get('team') or 'FA')[:4]
            pos = sp.get('position')
            if abbr not in teams:
                teams[abbr], _ = Team.objects.get_or_create(
                    abbreviation=abbr, defaults={'team_name': abbr}
                )
            if pos not in positions:
                positions[pos], _ = Position.objects.get_or_create(position_type=pos)
            player, _ = Player.objects.get_or_create(
                name=original,
                defaults={
                    'sleeper_id': str(sleeper_id),
                    'team': teams[abbr],
                    'position': positions[pos],
                    'image': f'https://sleepercdn.com/content/nfl/players/{sleeper_id}.jpg',
                },
            )
            created[original] = player
            self.stdout.write(f"  matched '{original}' to Sleeper's '{full}'")

        if created:
            self.stdout.write(self.style.SUCCESS(
                f'  created {len(created)} player(s): ' + ', '.join(list(created)[:6])
            ))
        return created

    # -- main ------------------------------------------------------------
    def handle(self, *args, **opts):
        client = SleeperClient()
        season, week = opts.get('season'), opts.get('week')
        if not season or not week:
            state = client.state() or {}
            season = season or int(state.get('season') or 0)
            week = week or int(state.get('week') or 0)
            self.stdout.write(f'resolved from Sleeper: season={season} week={week}')
        if not season or not week:
            raise CommandError('could not resolve season/week; pass --season and --week')

        # Prefer the weekly export when one exists for this season/week; fall
        # back to Sleeper trending so the command still works with no file.
        csv_path = Path(opts['csv']) if opts.get('csv') else default_csv_for(season, week)
        use_csv = bool(opts.get('csv')) or (csv_path.exists() and not opts['from_trending'])

        if use_csv:
            self.stdout.write(f'reading {csv_path}')
            names = self._from_csv(csv_path, opts['limit'])
            picked, problems = self._resolve_names(
                names, opts['create_missing'], client
            )
            if problems:
                self.stdout.write(self.style.WARNING(
                    f'  {len(problems)} name(s) still unmatched: '
                    + ', '.join(problems[:8])
                    + ('' if opts['create_missing'] else '  (try --create-missing)')
                ))
        else:
            if not opts['from_trending']:
                self.stdout.write(
                    f'no {csv_path.name} found -- using Sleeper trending instead'
                )
            picked, unmatched = self._from_trending(
                client, opts['limit'], opts['lookback_hours']
            )
            if unmatched:
                self.stdout.write(self.style.WARNING(
                    f'  {unmatched} trending player(s) have no local record -- '
                    f'run sync_sleeper_players to map them'
                ))

        if not picked:
            raise CommandError('no targets resolved; nothing written')

        self.stdout.write(f'\n{len(picked)} target(s) for {season} week {week}:')
        for p, count in picked:
            pos = p.position.position_type if p.position_id else '?'
            extra = f'  {count:,} adds' if count else ''
            self.stdout.write(f'  {p.name} ({pos}){extra}')

        if opts['dry_run']:
            self.stdout.write(self.style.SUCCESS('\ndry run -- nothing written.'))
            return

        # Written for both keying schemes so the original frontend, which asks
        # by the legacy counter, still sees them.
        legacy = legacy_week_for(season, week)
        kept = []
        with transaction.atomic():
            for p, count in picked:
                obj, _ = Target.objects.update_or_create(
                    player=p, week=legacy,
                    defaults={
                        'season': season, 'nfl_week': week, 'trending_adds': count,
                    },
                )
                kept.append(obj.pk)
            removed = 0
            if opts['replace']:
                removed, _ = (
                    Target.objects.filter(season=season, nfl_week=week)
                    .exclude(pk__in=kept).delete()
                )

        self.stdout.write(self.style.SUCCESS(
            f'\nwrote {len(kept)} target(s)'
            + (f', removed {removed} no longer trending' if opts['replace'] else '')
            + f'. Legacy week column set to {legacy}.'
        ))
