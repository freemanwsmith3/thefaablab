"""
A terminal read on the week: the top targets at each position, side by side.

Puts the two independent signals next to each other -- what FAABLab bidders say
a player is worth, and what Sleeper leagues actually paid -- so a gap between
them is obvious at a glance. That comparison is the thing no other source can
produce, and it is easy to miss when the numbers live on separate cards.
"""
from django.core.management.base import BaseCommand

from api.models import BidAggregate, ScoringFormat, Target
from api.services.sleeper import SleeperClient

POSITIONS = ['QB', 'RB', 'WR', 'TE']


def dollars(pct, budget):
    return f'${round(budget * pct / 100)}' if pct is not None else '-'


class Command(BaseCommand):
    help = 'Print the top waiver targets per position with crowd and market data.'

    def add_arguments(self, parser):
        parser.add_argument('--season', type=int)
        parser.add_argument('--week', type=int)
        parser.add_argument('--top', type=int, default=5, help='Rows per position.')
        parser.add_argument(
            '--budget', type=int, default=200,
            help='Convert percentages to dollars against this budget.',
        )
        parser.add_argument(
            '--sort', choices=['crowd', 'adds', 'market'], default='crowd',
            help='Rank by crowd median, Sleeper adds, or market average.',
        )

    def handle(self, *args, **opts):
        season, week = opts.get('season'), opts.get('week')
        if not season or not week:
            state = SleeperClient().state() or {}
            season = season or int(state.get('season') or 0)
            week = week or int(state.get('week') or 0)
        if not season or not week:
            self.stderr.write('could not resolve season/week')
            return

        budget = opts['budget']
        targets = (
            Target.objects.filter(season=season, nfl_week=week)
            .select_related('player', 'player__team', 'player__position')
        )
        if not targets:
            self.stdout.write(f'no targets for {season} week {week}')
            return

        crowd = {
            a.player_id: a for a in BidAggregate.objects.filter(
                scope=BidAggregate.Scope.CROWD, season=season, week=week,
                league_size=0, scoring=ScoringFormat.ALL,
            )
        }
        market = {
            a.player_id: a for a in BidAggregate.objects.filter(
                scope=BidAggregate.Scope.MARKET, season=season, week=week,
                league_size=0, scoring=ScoringFormat.ALL,
            )
        }

        self.stdout.write(
            f'\n  {season} Week {week}  ·  {len(targets)} targets  ·  '
            f'figures in dollars of a ${budget} budget\n'
        )

        for pos in POSITIONS:
            rows = [t for t in targets
                    if t.player.position_id and t.player.position.position_type == pos]
            if not rows:
                continue

            def rank(t):
                c, m = crowd.get(t.player_id), market.get(t.player_id)
                if opts['sort'] == 'adds':
                    return t.trending_adds or 0
                if opts['sort'] == 'market':
                    return (m.mean or 0) if m else 0
                return (c.median or 0) if c else 0

            rows.sort(key=rank, reverse=True)

            self.stdout.write(self.style.MIGRATE_HEADING(f'  {pos}'))
            self.stdout.write(
                f'    {"PLAYER":<22}{"TM":<5}{"CROWD":>8}{"BIDS":>7}'
                f'{"SLEEPER":>9}{"LGS":>6}{"ADDS":>10}   GAP'
            )
            for t in rows[: opts['top']]:
                c, m = crowd.get(t.player_id), market.get(t.player_id)
                team = t.player.team.abbreviation if t.player.team_id else '-'
                cm = c.median if c else None
                mm = m.mean if m and m.n_leagues else None

                # The headline comparison: where the market paid more than the
                # crowd expects, the crowd is probably underbidding.
                gap = ''
                if cm is not None and mm is not None:
                    d = round(budget * (mm - cm) / 100)
                    gap = f'{"+" if d > 0 else ""}{d}' if d else 'even'

                self.stdout.write(
                    f'    {t.player.name[:21]:<22}{team:<5}'
                    f'{dollars(cm, budget):>8}{(c.n if c else 0):>7}'
                    f'{dollars(mm, budget):>9}{(m.n_leagues if m else 0):>6}'
                    f'{(f"{t.trending_adds:,}" if t.trending_adds else "-"):>10}'
                    f'   {gap}'
                )
            self.stdout.write('')

        with_market = sum(1 for t in targets if market.get(t.player_id))
        with_crowd = sum(1 for t in targets if crowd.get(t.player_id))
        self.stdout.write(
            f'  {with_crowd}/{len(targets)} have crowd bids · '
            f'{with_market}/{len(targets)} have Sleeper market data\n'
        )
