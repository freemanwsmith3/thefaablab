"""
Long-running league-ID crawler.

Walks the public Sleeper graph (league -> its members -> those members' other
leagues) as fast as the rate budget allows, persisting everything it finds.

Two things make this different from `sleeper_discover`, which is a one-shot:

  * The frontier survives restarts. Queued league ids and already-queried user
    ids are checkpointed to disk, so stopping and resuming does not re-walk
    ground already covered -- which matters when the crawl runs for hours.
  * It reports throughput live, so you can see whether the rate limit or the
    network is the binding constraint.

Rate limiting: Sleeper documents a 1000 req/min ceiling and says exceeding it
risks an IP block. The default here is 900/min. Raising it past 1000 is asking
to be blocked, and the block applies to your whole address, not just this
script. Note also that Sleeper's terms describe the API as free for
non-commercial use.
"""
import json
import signal
import time
from collections import deque
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from api.models import SleeperLeague
from api.services.ingest import save_league
from api.services.sleeper import SleeperClient


class Command(BaseCommand):
    help = 'Crawl Sleeper for league ids at a sustained rate, resumable.'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int, required=True)
        parser.add_argument(
            '--rate', type=int, default=900,
            help='Requests per minute. Sleeper blocks above 1000; default 900.',
        )
        parser.add_argument('--workers', type=int, default=16)
        parser.add_argument(
            '--target', type=int, default=0,
            help='Stop after this many FAAB leagues are stored. 0 = run until stopped.',
        )
        parser.add_argument(
            '--minutes', type=float, default=0,
            help='Stop after this many minutes. 0 = run until stopped.',
        )
        parser.add_argument(
            '--seed-league', action='append', default=[],
            help='Seed league id. Only needed for a cold start.',
        )
        parser.add_argument(
            '--state', default='',
            help='Frontier checkpoint path (default: <BASE_DIR>/.cache/crawl_<season>.json).',
        )
        parser.add_argument('--reset', action='store_true', help='Discard the saved frontier.')

    # -- checkpoint ------------------------------------------------------
    def _load(self, path, reset):
        if reset or not path.exists():
            return deque(), set(), set()
        try:
            blob = json.loads(path.read_text())
            return (
                deque(blob.get('queue', [])),
                set(blob.get('users', [])),
                set(blob.get('expanded', [])),
            )
        except Exception:
            return deque(), set(), set()

    def _save(self, path, queue, users, expanded):
        path.parent.mkdir(parents=True, exist_ok=True)
        # Cap what we persist: the queue can grow faster than it drains, and a
        # checkpoint is a resume hint, not an archive.
        path.write_text(json.dumps({
            'queue': list(queue)[:200000],
            'users': list(users)[:400000],
            'expanded': list(expanded)[:400000],
        }))

    def handle(self, *args, **opts):
        season = opts['season']
        state_path = Path(opts['state']) if opts['state'] else (
            Path(settings.BASE_DIR) / '.cache' / f'crawl_{season}.json'
        )
        queue, seen_users, expanded = self._load(state_path, opts['reset'])

        client = SleeperClient(per_minute=opts['rate'])

        known = set(
            SleeperLeague.objects.filter(season=season).values_list('league_id', flat=True)
        )
        for lid in opts['seed_league']:
            if str(lid) not in known:
                queue.append(str(lid))
        if not queue:
            # Cold start with no seeds: walk out from the corpus we already
            # have. These are known, so they are expanded rather than re-fetched.
            queue.extend(lid for lid in known if lid not in expanded)
        if not queue:
            self.stderr.write('nothing to crawl: pass --seed-league for a cold start')
            return

        stop = {'now': False}
        signal.signal(signal.SIGINT, lambda *_: stop.__setitem__('now', True))
        signal.signal(signal.SIGTERM, lambda *_: stop.__setitem__('now', True))

        started = time.monotonic()
        deadline = started + opts['minutes'] * 60 if opts['minutes'] else None
        found = 0
        checked = 0
        last_report = started

        self.stdout.write(
            f'crawling season {season} at {opts["rate"]}/min, '
            f'{len(known)} leagues known, queue {len(queue)}. Ctrl-C to checkpoint and stop.'
        )
        self.stdout.flush()

        try:
            while queue and not stop['now']:
                if deadline and time.monotonic() > deadline:
                    break
                if opts['target'] and found >= opts['target']:
                    break

                # Take a batch of leagues; each contributes its members.
                batch = [queue.popleft() for _ in range(min(opts['workers'], len(queue)))]
                # Already-expanded leagues have nothing left to give.
                batch = [b for b in batch if b not in expanded]
                if not batch:
                    continue

                # 1) Fetch only the leagues we do not already have. A league we
                #    know is still worth expanding, which is what makes a
                #    resumed crawl reach new territory instead of stalling.
                to_fetch = [b for b in batch if b not in known]
                for league in client.map(client.league, to_fetch):
                    checked += 1
                    if not league:
                        continue
                    lid = str(league.get('league_id') or '')
                    known.add(lid)
                    if save_league(league):
                        found += 1

                # 2) Expand: members of those leagues we have not queried yet.
                new_users = []
                for members in client.map(client.league_users, batch):
                    for u in members or []:
                        uid = u.get('user_id')
                        if uid and uid not in seen_users:
                            seen_users.add(uid)
                            new_users.append(uid)

                # 3) Every league those users belong to becomes frontier.
                for leagues in client.map(
                    lambda uid: client.user_leagues(uid, season), new_users
                ):
                    for lg in leagues or []:
                        lid = str(lg.get('league_id') or '')
                        if lid and lid not in expanded:
                            queue.append(lid)

                expanded.update(batch)

                now = time.monotonic()
                if now - last_report >= 15:
                    mins = (now - started) / 60
                    self.stdout.write(
                        f'  +{found} FAAB leagues | {checked} checked | '
                        f'queue {len(queue)} | users {len(seen_users)} | '
                        f'{client.calls} calls | {client.calls / max(mins, .01):.0f} calls/min | '
                        f'{found / max(mins, .01):.0f} leagues/min'
                    )
                    # Flush explicitly: this command is meant to run for hours
                    # with its output redirected to a log, and buffered progress
                    # lines are useless for monitoring.
                    self.stdout.flush()
                    last_report = now
                    self._save(state_path, queue, seen_users, expanded)
        finally:
            self._save(state_path, queue, seen_users, expanded)
            mins = (time.monotonic() - started) / 60
            total = SleeperLeague.objects.filter(season=season).count()
            self.stdout.write(self.style.SUCCESS(
                f'stopped after {mins:.1f} min: +{found} new FAAB leagues '
                f'({total} total for {season}), {client.calls} API calls, '
                f'queue {len(queue)} saved to {state_path}'
            ))
