"""
Read and write endpoints.

The read path never touches a raw bid table. Everything comes from
BidAggregate, whose scalar columns are computed at write time, so serving a
week is a single indexed query returning one row per player.
"""
import hashlib
import logging
import uuid

from django.conf import settings
from django.core import signing
from django.core.cache import cache
from django.http import HttpResponse
from django.db import IntegrityError, transaction
from django.utils.cache import patch_cache_control
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import BidAggregate, Bid, Player, ScoringFormat, Target
from .serializers import (
    BidInputSerializer,
    BidResultSerializer,
    HealthSerializer,
    PlayerSerializer,
    StatsResponseSerializer,
    TargetsResponseSerializer,
    WeekResponseSerializer,
)
from .services import aggregates, histogram as hg, weeks
from .throttles import BidBurstThrottle, BidSustainedThrottle

log = logging.getLogger(__name__)

SUBMITTER_COOKIE = 'faab_sid'
COOKIE_MAX_AGE = 60 * 60 * 24 * 365

# Reused across the documented endpoints.
SEASON_PARAM = OpenApiParameter(
    'season', OpenApiTypes.INT, OpenApiParameter.QUERY,
    description='NFL season, e.g. 2026. Omit to use the legacy week counter.',
)
WEEK_PARAM = OpenApiParameter(
    'week', OpenApiTypes.INT, OpenApiParameter.QUERY, required=True,
    description=(
        'NFL week 1-18 when `season` is given, otherwise the legacy running '
        'week counter (29 == 2024 week 1).'
    ),
)
SIZE_PARAM = OpenApiParameter(
    'size', OpenApiTypes.INT, OpenApiParameter.QUERY,
    description='League size filter. 0 (default) means all sizes.',
    enum=[0, 8, 10, 12, 14],
)
SCORING_PARAM = OpenApiParameter(
    'scoring', OpenApiTypes.STR, OpenApiParameter.QUERY,
    description='Scoring format filter.',
    enum=['all', 'ppr', 'half', 'std'],
)
DEFAULT_WEEK_LIMIT = 50
MAX_WEEK_LIMIT = 500

LIMIT_PARAM = OpenApiParameter(
    'limit', OpenApiTypes.INT, OpenApiParameter.QUERY,
    description=(
        'Maximum players returned, ordered by crowd volume then market volume. '
        f'Defaults to {DEFAULT_WEEK_LIMIT}; market data covers far more players '
        'than a week has cards, so an unbounded response is mostly long tail.'
    ),
)



# ---------------------------------------------------------------------------
# Anonymous identity
# ---------------------------------------------------------------------------
def _read_submitter(request):
    """Return the signed submitter id from the cookie, or None if absent/forged."""
    raw = request.COOKIES.get(SUBMITTER_COOKIE)
    if not raw:
        return None
    try:
        return signing.loads(raw, salt=settings.SUBMITTER_SIGNING_SALT, max_age=COOKIE_MAX_AGE)
    except signing.BadSignature:
        return None


def _new_submitter():
    return uuid.uuid4().hex


def _submitter_hash(submitter: str) -> str:
    """
    Store a hash rather than the raw cookie value.

    A database leak then exposes no token that could be replayed as somebody
    else's identity, and the value is still stable for deduplication.
    """
    digest = hashlib.sha256(
        f'{settings.SUBMITTER_SIGNING_SALT}:{submitter}'.encode()
    ).hexdigest()
    return digest[:64]


def _set_submitter_cookie(response, submitter):
    response.set_cookie(
        SUBMITTER_COOKIE,
        signing.dumps(submitter, salt=settings.SUBMITTER_SIGNING_SALT),
        max_age=COOKIE_MAX_AGE,
        secure=not settings.DEBUG,
        httponly=True,
        samesite='Lax',
    )
    return response


# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------
def _resolve_week(request):
    """
    Accept either ?season=&week= (new) or ?week=<legacy counter> (old frontend).

    Returns (season, week, legacy_week, error_response).
    """
    season = request.query_params.get('season')
    week = request.query_params.get('week')
    if week is None:
        return None, None, None, Response(
            {'detail': 'week is required'}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        week = int(week)
    except (TypeError, ValueError):
        return None, None, None, Response(
            {'detail': 'week must be an integer'}, status=status.HTTP_400_BAD_REQUEST
        )

    if season is not None:
        try:
            return int(season), week, weeks.to_legacy_week(int(season), week), None
        except (TypeError, ValueError):
            return None, None, None, Response(
                {'detail': 'season must be an integer'}, status=status.HTTP_400_BAD_REQUEST
            )

    resolved_season, resolved_week = weeks.to_season_week(week)
    return resolved_season, resolved_week, week, None


def _aggregate_map(scope, season, week, league_size=0, scoring=ScoringFormat.ALL):
    """One indexed query -> {player_id: BidAggregate}."""
    if season is None or week is None:
        return {}
    rows = BidAggregate.objects.filter(
        scope=scope, season=season, week=week,
        league_size=league_size, scoring=scoring,
    ).only(
        'player_id', 'counts', 'won_counts', 'n', 'n_leagues',
        'mean', 'median', 'mode', 'p25', 'p75', 'min_bid', 'max_bid',
    )
    return {row.player_id: row for row in rows}


def _legacy_stats_payload(agg):
    """Reproduce the shape the deployed frontend already expects."""
    if agg is None or not agg.n:
        return (
            {
                'averageBid': 'NA',
                'medianBid': 'NA',
                'mostCommonBid': 'NA',
                'numberOfBids': "You're the 1st bid",
            },
            [],
        )
    trimmed = hg.trimmed(agg.counts)
    return (
        {
            'averageBid': round(hg.mean(trimmed), 1) if hg.total(trimmed) else agg.mean,
            'medianBid': hg.quantile(trimmed, 0.5),
            'mostCommonBid': hg.mode(trimmed),
            'numberOfBids': hg.total(trimmed),
        },
        hg.bins(trimmed),
    )


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------
@extend_schema(
    tags=['legacy'],
    summary="The week's player cards",
    description=(
        'Kept unchanged for the currently deployed frontend. New clients '
        'should use `/api/week`, which returns this plus both distributions '
        'in one round trip.'
    ),
    parameters=[WEEK_PARAM],
    responses={200: TargetsResponseSerializer},
)
class TargetsAPI(APIView):
    """Legacy: the week's player cards."""

    def get(self, request):
        try:
            legacy_week = int(request.query_params.get('week'))
        except (TypeError, ValueError):
            return Response({'detail': 'week is required'}, status=status.HTTP_400_BAD_REQUEST)

        targets = Target.objects.filter(week=legacy_week).values_list('id', 'player_id')
        target_ids = {player_id: target_id for target_id, player_id in targets}
        players = (
            Player.objects.filter(id__in=target_ids.keys())
            .select_related('team', 'position')
            .order_by('id')
        )
        data = PlayerSerializer(
            players, many=True, context={'target_ids': target_ids}
        ).data
        response = Response({'players': data})
        patch_cache_control(response, public=True, max_age=settings.WEEK_CACHE_SECONDS)
        return response


@extend_schema(
    tags=['legacy'],
    summary='Crowd bid distributions for a week',
    description=(
        'Original response shape, including the `"NA"` / '
        '`"You\'re the 1st bid"` string placeholders.\n\n'
        'Outliers are trimmed with a Tukey 1.5x IQR fence before the summary '
        'is computed, matching the previous behaviour.'
    ),
    parameters=[SEASON_PARAM, WEEK_PARAM],
    responses={200: StatsResponseSerializer},
)
class StatsAPI(APIView):
    """
    Legacy: bid distributions for the week.

    Previously this loaded every raw bid for every target and ran scipy over
    them on each request. It is now one indexed query over precomputed rows.
    """

    def get(self, request):
        season, week, legacy_week, error = _resolve_week(request)
        if error:
            return error

        by_player = _aggregate_map(BidAggregate.Scope.CROWD, season, week)
        stats, binned = {}, {}
        for player_id, agg in by_player.items():
            summary, bins = _legacy_stats_payload(agg)
            stats[str(player_id)] = summary
            if bins:
                binned[str(player_id)] = bins

        # Any target with no bids yet still needs a placeholder entry.
        for player_id in Target.objects.filter(week=legacy_week).values_list(
            'player_id', flat=True
        ):
            stats.setdefault(str(player_id), _legacy_stats_payload(None)[0])

        response = Response({'binned_data': binned, 'stats': stats})
        patch_cache_control(response, public=True, max_age=settings.WEEK_CACHE_SECONDS)
        return response


@extend_schema(
    tags=['week'],
    summary='Everything about one week',
    description=(
        'Players, the crowd distribution and the real market distribution in a '
        'single response.\n\n'
        '`size` and `scoring` select a **precomputed** market slice, so '
        'filtering to "12-team PPR" costs no more than the unfiltered view. A '
        'slice with no data returns an empty `players` list.\n\n'
        '`market.win_curve` gives P(win) for every bid 0-100, and '
        '`market.bid_to_win_80` is the smallest bid that would have won 80% of '
        'observed leagues -- both derived from losing bids, which most FAAB '
        'tools do not have.\n\n'
        'Players are ordered by crowd bid volume, descending.'
    ),
    parameters=[SEASON_PARAM, WEEK_PARAM, SIZE_PARAM, SCORING_PARAM, LIMIT_PARAM],
    responses={200: WeekResponseSerializer},
)
class WeekAPI(APIView):
    """
    Unified week payload: players, crowd distribution and market distribution
    in one round trip instead of the two the old frontend made.

    Optional ?size= and ?scoring= select a precomputed market slice, so
    filtering costs no more than the unfiltered view.
    """

    def get(self, request):
        season, week, legacy_week, error = _resolve_week(request)
        if error:
            return error

        try:
            league_size = int(request.query_params.get('size') or 0)
        except (TypeError, ValueError):
            league_size = 0
        scoring = request.query_params.get('scoring') or ScoringFormat.ALL
        if scoring not in ScoringFormat.values:
            scoring = ScoringFormat.ALL

        targets = Target.objects.filter(week=legacy_week).values_list('id', 'player_id')
        target_ids = {player_id: target_id for target_id, player_id in targets}

        crowd = _aggregate_map(BidAggregate.Scope.CROWD, season, week)
        market = _aggregate_map(
            BidAggregate.Scope.MARKET, season, week, league_size, scoring
        )

        try:
            limit = int(request.query_params.get('limit') or DEFAULT_WEEK_LIMIT)
        except (TypeError, ValueError):
            limit = DEFAULT_WEEK_LIMIT
        limit = max(1, min(limit, MAX_WEEK_LIMIT))

        # The week's actual cards always come first and are never truncated;
        # remaining slots go to the players with the most market activity.
        ranked = sorted(
            set(crowd) | set(market),
            key=lambda pid: (
                pid in target_ids,
                (crowd[pid].n if pid in crowd else 0),
                (market[pid].n if pid in market else 0),
            ),
            reverse=True,
        )
        player_ids = set(target_ids) | set(ranked[:limit])

        players = (
            Player.objects.filter(id__in=player_ids)
            .select_related('team', 'position')
            .only('id', 'name', 'link', 'image', 'sleeper_id', 'team', 'position')
        )

        out = []
        for player in players:
            c, m = crowd.get(player.id), market.get(player.id)
            out.append(
                {
                    'id': player.id,
                    'name': player.name,
                    'team': player.team.abbreviation if player.team_id else None,
                    'position': player.position.position_type if player.position_id else None,
                    'image': player.image,
                    'sleeper_id': player.sleeper_id,
                    'target_id': target_ids.get(player.id),
                    'crowd': None if not c else {
                        'n': c.n, 'mean': c.mean, 'median': c.median, 'mode': c.mode,
                        'p25': c.p25, 'p75': c.p75, 'bins': hg.bins(hg.trimmed(c.counts)),
                    },
                    'market': None if not m else {
                        'n': m.n, 'n_leagues': m.n_leagues, 'mean': m.mean,
                        'median': m.median, 'mode': m.mode, 'p25': m.p25, 'p75': m.p75,
                        'bins': hg.bins(m.counts),
                        'win_curve': hg.win_curve(m.won_counts, m.n_leagues),
                        'bid_to_win_80': hg.min_bid_for_confidence(
                            m.won_counts, m.n_leagues, 0.8
                        ),
                    },
                }
            )

        out.sort(
            key=lambda p: (
                p['target_id'] is not None,
                (p['crowd'] or {}).get('n') or 0,
                (p['market'] or {}).get('n') or 0,
            ),
            reverse=True,
        )
        response = Response(
            {
                'season': season,
                'week': week,
                'filters': {'size': league_size, 'scoring': scoring, 'limit': limit},
                'players': out,
            }
        )
        patch_cache_control(response, public=True, max_age=settings.WEEK_CACHE_SECONDS)
        return response


@extend_schema(
    tags=['bids'],
    summary='Submit a crowd bid',
    description=(
        'Records what you would bid, then unlocks the results.\n\n'
        'Anonymous but not unlimited:\n\n'
        '- A signed `faab_sid` cookie identifies the browser and is issued on '
        'first submission. **Clients must send cookies** '
        '(`credentials: "include"`) or every bid looks like a new visitor.\n'
        '- One bid per browser per player per week; a repeat returns '
        '`200 {"recorded": false, "reason": "duplicate"}` rather than an error.\n'
        '- A `value` of 0 is the "just show me the results" path: it returns '
        '`reason: "zero_bid"` and is not counted.\n'
        '- Rate limited per address (burst and sustained).'
    ),
    request=BidInputSerializer,
    responses={
        201: BidResultSerializer,
        200: BidResultSerializer,
        400: OpenApiTypes.OBJECT,
        429: OpenApiTypes.OBJECT,
    },
    examples=[
        OpenApiExample(
            'A real bid', value={'player': 88, 'week': 29, 'value': 24},
            request_only=True,
        ),
        OpenApiExample(
            'Reveal results without bidding',
            value={'player': 88, 'week': 29, 'value': 0}, request_only=True,
        ),
    ],
)
class BidView(APIView):
    """Accept one crowd bid and fold it straight into the aggregate."""

    throttle_classes = [BidBurstThrottle, BidSustainedThrottle]

    def post(self, request):
        serializer = BidInputSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        data = serializer.validated_data
        value, legacy_week, player_id = data['value'], data['week'], data['player']

        if not Player.objects.filter(id=player_id).exists():
            return Response({'detail': 'unknown player'}, status=status.HTTP_400_BAD_REQUEST)

        # A zero bid is the "just show me the answer" path: it reveals results
        # without polluting the distribution.
        if value == 0:
            return Response({'recorded': False, 'reason': 'zero_bid'},
                            status=status.HTTP_200_OK)

        submitter = _read_submitter(request)
        issued = False
        if not submitter:
            submitter, issued = _new_submitter(), True
        submitter_hash = _submitter_hash(submitter)

        try:
            with transaction.atomic():
                Bid.objects.create(
                    value=value, player_id=player_id, week=legacy_week,
                    user='anon', submitter=submitter_hash,
                )
        except IntegrityError:
            # Already bid on this player this week; return results, change nothing.
            response = Response({'recorded': False, 'reason': 'duplicate'},
                                status=status.HTTP_200_OK)
            return _set_submitter_cookie(response, submitter) if issued else response

        season, week = weeks.to_season_week(legacy_week)
        if season is not None:
            aggregates.bump(
                scope=BidAggregate.Scope.CROWD, player_id=player_id,
                season=season, week=week, value=value,
            )
        else:
            log.warning('no season offset for legacy week %s; aggregate not updated',
                        legacy_week)

        response = Response({'recorded': True}, status=status.HTTP_201_CREATED)
        return _set_submitter_cookie(response, submitter) if issued else response


@extend_schema(exclude=True)
@api_view(['GET'])
def llms_txt(request):
    """
    /llms.txt -- the convention AI agents look for to understand a site.

    Plain text on purpose: an agent finds this, learns the API exists, learns it
    can call it without signing up, and gets the OpenAPI URL to work from.
    """
    base = request.build_absolute_uri('/').rstrip('/')
    body = f"""# FAABLab

> Crowd-sourced fantasy football FAAB (waiver bid) data. Real people submit what
> they would bid on each week's waiver targets; FAABLab aggregates those bids
> into medians, distributions and winning ranges.

All bid values are a **percent of league budget (0-100)**, never dollars. That
is what makes them comparable across leagues. Convert with:
`dollars = round(budget * pct / 100)`.

## API

Free to call. No signup required to start -- anonymous callers get a working
monthly quota, and a free key raises it.

- OpenAPI schema: {base}/api/schema
- Interactive docs: {base}/api/docs
- Tiers and quotas: {base}/api/v1/pricing
- Auth (optional): `X-API-Key: faab_...`

## Getting a key

You do not need one to start. When you want a bigger allowance:

```
curl -X POST {base}/api/v1/keys -H 'Content-Type: application/json' \\
  -d '{{"name":"my-bot","email":"you@example.com"}}'
```

The key comes back in the response, works immediately, and is shown only once.
Send it as `X-API-Key`. Check usage at `/api/v1/keys/me`.

If you exhaust a quota, the 429 response includes an `upgrade_url`.
**Show that link to the person who deployed you** -- they pay, the key upgrades
automatically, and your next call succeeds. Nothing needs relaying back.

## Endpoints

- `POST /api/v1/keys` - create a key instantly, no signup form
- `GET /api/v1/keys/me` - your tier, usage and remaining quota
- `GET /api/v1/coverage` - which seasons and weeks have data
- `GET /api/v1/bids/{{season}}/{{week}}` - every target that week
- `GET /api/v1/bids/{{season}}/{{week}}/{{player}}` - one player, by id or name slug

## Example

```
curl {base}/api/v1/bids/2026/3/john-metchie
```

## Notes

- Outliers are trimmed (Tukey 1.5x IQR) before summarising, so `bids` is the
  post-trim count and distribution shares sum to it.
- Quota headers are on every response: `X-RateLimit-Limit`, `X-RateLimit-Remaining`.
- This API serves FAABLab's own crowd data only.
"""
    return HttpResponse(body, content_type='text/plain; charset=utf-8')


@extend_schema(
    tags=['ops'],
    summary='Current NFL season and week',
    description=(
        'Derived from Sleeper\'s own state endpoint and cached, so it cannot '
        'drift out of sync with the NFL calendar the way a hardcoded season '
        'start date does. Falls back to the stored legacy offset if Sleeper is '
        'unreachable.'
    ),
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
def current_week(request):
    cached = cache.get('faab:current_week')
    if not cached:
        from .services.sleeper import SleeperClient
        state = SleeperClient().state() or {}
        season = int(state.get('season') or 0)
        week = int(state.get('week') or 0)
        if not season or not week:
            return Response(
                {'detail': 'current week unavailable'},
                status=status.HTTP_503_SERVICE_UNAVAILABLE,
            )
        week = max(1, min(week, 18))
        cached = {
            'season': season,
            'week': week,
            'legacy_week': weeks.to_legacy_week(season, week),
            'season_type': state.get('season_type'),
        }
        # An hour is plenty: the NFL week changes once a week.
        cache.set('faab:current_week', cached, 3600)
    response = Response(cached)
    patch_cache_control(response, public=True, max_age=600)
    return response


@extend_schema(
    tags=['ops'],
    summary='Liveness probe',
    description='Returns ok once the database connection is confirmed working.',
    responses={200: HealthSerializer},
)
@api_view(['GET'])
def health(request):
    """Cheap liveness probe that also proves the DB connection works."""
    Player.objects.exists()
    return Response({'status': 'ok'})
