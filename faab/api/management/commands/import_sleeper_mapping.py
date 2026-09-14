"""
Load an existing faab_id -> sleeper_id mapping CSV onto Player.sleeper_id.

Player.sleeper_id is unique, so any Sleeper id claimed by two FAAB rows would
abort the whole write. Rather than failing halfway, this validates first,
reports every conflict, and skips them -- a duplicate almost always means two
Player rows for the same person (one with a generational suffix, one without),
which is a data-quality problem to fix rather than something to paper over.

Dry run by default. Pass --write to commit.
"""
import csv
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api.models import Player

# Below this, a fuzzy name match is more likely wrong than right.
SIMILARITY_FLOOR = 0.85


class Command(BaseCommand):
    help = 'Import a faab_id -> sleeper_id CSV onto Player.sleeper_id.'

    def add_arguments(self, parser):
        parser.add_argument('csv_path')
        parser.add_argument('--write', action='store_true', help='Commit (default is a dry run).')
        parser.add_argument(
            '--min-similarity', type=float, default=SIMILARITY_FLOOR,
            help=f'Skip fuzzy matches below this score (default {SIMILARITY_FLOOR}).',
        )
        parser.add_argument(
            '--overwrite', action='store_true',
            help='Replace a sleeper_id already set on a player.',
        )

    def handle(self, *args, **opts):
        path = Path(opts['csv_path'])
        if not path.exists():
            raise CommandError(f'no such file: {path}')

        rows = [r for r in csv.DictReader(path.open()) if (r.get('sleeper_id') or '').strip()]
        self.stdout.write(f'{len(rows)} rows with a sleeper_id')

        # 1) Reject anything the unique constraint would reject.
        by_sleeper = {}
        for r in rows:
            by_sleeper.setdefault(r['sleeper_id'], []).append(r)
        conflicts = {k: v for k, v in by_sleeper.items() if len(v) > 1}

        # 2) Reject weak fuzzy matches.
        weak = []
        for r in rows:
            try:
                score = float(r.get('similarity_score') or 1)
            except ValueError:
                score = 1
            if score < opts['min_similarity']:
                weak.append((r, score))

        skip_ids = {r['faab_id'] for group in conflicts.values() for r in group}
        skip_ids |= {r['faab_id'] for r, _ in weak}

        if conflicts:
            self.stdout.write(self.style.WARNING(
                f'\n{len(conflicts)} sleeper_id(s) claimed by more than one player -- skipped:'
            ))
            for sid, group in conflicts.items():
                names = ' | '.join(f"#{r['faab_id']} {r['faab_name']}" for r in group)
                self.stdout.write(f'  {sid}: {names}')
        if weak:
            self.stdout.write(self.style.WARNING(
                f'\n{len(weak)} match(es) below {opts["min_similarity"]} similarity -- skipped:'
            ))
            for r, score in weak:
                self.stdout.write(
                    f"  #{r['faab_id']} '{r['faab_name']}' -> '{r['sleeper_name']}' ({score:.2f})"
                )

        # 3) Apply what is left.
        usable = [r for r in rows if r['faab_id'] not in skip_ids]
        existing = {
            str(p.id): p
            for p in Player.objects.filter(id__in=[int(r['faab_id']) for r in usable])
        }
        taken = set(
            Player.objects.exclude(sleeper_id=None)
            .values_list('sleeper_id', flat=True)
        )

        updates, missing, already, clash = [], [], [], []
        for r in usable:
            p = existing.get(r['faab_id'])
            if not p:
                missing.append(r)
                continue
            if p.sleeper_id and not opts['overwrite']:
                already.append(r)
                continue
            if r['sleeper_id'] in taken and p.sleeper_id != r['sleeper_id']:
                clash.append(r)
                continue
            p.sleeper_id = r['sleeper_id']
            updates.append(p)

        self.stdout.write('')
        self.stdout.write(f'  would set     : {len(updates)}')
        self.stdout.write(f'  already set   : {len(already)}')
        self.stdout.write(f'  no such player: {len(missing)}')
        self.stdout.write(f'  id taken      : {len(clash)}')
        self.stdout.write(f'  skipped above : {len(skip_ids)}')

        if not opts['write']:
            self.stdout.write(self.style.SUCCESS('\ndry run -- nothing written. Re-run with --write.'))
            return

        with transaction.atomic():
            Player.objects.bulk_update(updates, ['sleeper_id'], batch_size=500)
        self.stdout.write(self.style.SUCCESS(
            f'\nwrote {len(updates)} sleeper_ids. '
            f'{Player.objects.exclude(sleeper_id=None).count()} players now mapped.'
        ))
