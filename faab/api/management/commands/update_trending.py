"""
Refresh Sleeper add counts for the week's existing targets.

Separate from load_targets on purpose. Loading decides *which* players are on
the board and should happen once, after waivers; this only updates *how many*
Sleeper users are adding each one, which moves all week. Running it never adds
or removes a target, so it is safe on a short schedule -- every few hours is
reasonable, and it costs one API call per run regardless of target count.
"""
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from api.models import Target
from api.services.sleeper import SleeperClient


class Command(BaseCommand):
    help = "Refresh Sleeper trending add counts for a week's targets."

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, help='Defaults to the live NFL season.')
        parser.add_argument('--week', type=int, help='Defaults to the live NFL week.')
        parser.add_argument(
            '--lookback-hours', type=int, default=24,
            help='Trending window. Shorter reacts faster to news; 24h is a good default.',
        )
        parser.add_argument(
            '--depth', type=int, default=200,
            help='How far down the trending list to look for your targets.',
        )
        parser.add_argument('--dry-run', action='store_true')

    def handle(self, *args, **opts):
        client = SleeperClient()
        season, week = opts.get('season'), opts.get('week')
        if not season or not week:
            state = client.state() or {}
            season = season or int(state.get('season') or 0)
            week = week or int(state.get('week') or 0)
        if not season or not week:
            raise CommandError('could not resolve season/week; pass --season and --week')

        targets = list(
            Target.objects.filter(season=season, nfl_week=week)
            .select_related('player')
        )
        if not targets:
            self.stdout.write(self.style.WARNING(
                f'no targets for {season} week {week} -- run load_targets first'
            ))
            return

        rows = client.trending('add', lookback_hours=opts['lookback_hours'],
                               limit=opts['depth'])
        counts = {str(r['player_id']): r['count'] for r in (rows or [])}
        if not counts:
            raise CommandError('Sleeper returned no trending data')

        now = timezone.now()
        changed, unranked, unmapped = [], [], 0
        for t in targets:
            sid = t.player.sleeper_id
            if not sid:
                unmapped += 1
                continue
            count = counts.get(sid)
            if count is None:
                # Outside the top `depth`: genuinely low demand right now, so
                # record zero rather than leaving a stale number in place.
                count = 0
                unranked.append(t.player.name)
            was = t.trending_adds
            t.trending_adds = count
            t.trending_updated_at = now
            if was != count:
                changed.append((t.player.name, was, count))

        self.stdout.write(f'{season} week {week} -- {len(targets)} target(s)')
        for name, was, now_count in sorted(changed, key=lambda x: -x[2])[:15]:
            arrow = '' if was is None else f'  (was {was:,})'
            self.stdout.write(f'  {name:24} {now_count:>9,}{arrow}')
        if unranked:
            self.stdout.write(self.style.WARNING(
                f'  {len(unranked)} outside the top {opts["depth"]}, set to 0: '
                + ', '.join(unranked[:6])
            ))
        if unmapped:
            self.stdout.write(self.style.WARNING(
                f'  {unmapped} target(s) have no sleeper_id -- run sync_sleeper_players'
            ))

        if opts['dry_run']:
            self.stdout.write(self.style.SUCCESS('\ndry run -- nothing written.'))
            return

        Target.objects.bulk_update(
            targets, ['trending_adds', 'trending_updated_at'], batch_size=200
        )
        self.stdout.write(self.style.SUCCESS(
            f'\nupdated {len(targets)} target(s), {len(changed)} changed. '
            f'1 API call used.'
        ))
