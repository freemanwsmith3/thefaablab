"""
The public, metered data API.

Serves FAABLab's own crowd data only -- what real people said they would bid.
The Sleeper-derived market figures are deliberately absent: that data comes from
an API whose terms describe it as non-commercial, so it stays on the site rather
than being resold here.

Every response carries quota headers so a caller (human or agent) can see where
it stands without a separate call.
"""
from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.response import Response

from .models import ApiTier, BidAggregate, Player, TIER_PRICES_USD, TIER_QUOTAS
from .permissions import QuotaExceeded
from .services import histogram as hg
from .services import weeks

V1_TAG = 'public data api'


def _with_quota(response, request):
    """Expose the caller's standing on every response."""
    state = getattr(request, 'api_state', None)
    if state:
        response['X-RateLimit-Tier'] = str(state.get('tier', ''))
        response['X-RateLimit-Limit'] = str(state.get('quota', ''))
        response['X-RateLimit-Remaining'] = str(
            max(0, (state.get('quota') or 0) - (state.get('used') or 0))
        )
    return response


def _slug(name):
    import re
    return re.sub(r'[^a-z0-9]+', '-', (name or '').lower()).strip('-')


def _crowd_payload(agg):
    counts = agg.counts or []
    trimmed = hg.trimmed(counts)
    return {
        'median_pct': agg.median,
        'mean_pct': agg.mean,
        'mode_pct': agg.mode,
        'p25_pct': agg.p25,
        'p75_pct': agg.p75,
        'min_pct': agg.min_bid,
        'max_pct': agg.max_bid,
        'bids': hg.total(trimmed),
        'distribution': [
            {'lo_pct': b['lo'], 'hi_pct': b['hi'], 'bids': b['bids']}
            for b in hg.bins(trimmed)
        ],
    }


SEASON = OpenApiParameter('season', OpenApiTypes.INT, OpenApiParameter.PATH)
WEEK = OpenApiParameter('week', OpenApiTypes.INT, OpenApiParameter.PATH)


@extend_schema(
    tags=[V1_TAG],
    # Explicit ids: generated clients turn these into method names, and the
    # auto-derived ones collide between the week and player routes.
    operation_id='getWeekBids',
    summary='Crowd bids for every target in a week',
    description=(
        'All FAABLab bidders\' data for one NFL week.\n\n'
        '**Every value is a percent of league budget (0-100), not dollars.** '
        'That is what makes bids comparable across leagues with different '
        'budgets. Multiply by the budget to show currency: '
        '`dollars = round(budget * pct / 100)`.\n\n'
        'Outliers are removed with a Tukey 1.5x IQR fence before the summary is '
        'computed, so `bids` is the post-trim count and distribution shares sum '
        'to it exactly.\n\n'
        'No key is required. Anonymous callers get a working monthly quota; a '
        'free key raises it. See `/api/v1/pricing`.'
    ),
    parameters=[SEASON, WEEK],
    responses={200: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
@permission_classes([QuotaExceeded])
def week_bids(request, season, week):
    rows = (
        BidAggregate.objects.filter(
            scope=BidAggregate.Scope.CROWD, season=season, week=week
        )
        .select_related('player', 'player__team', 'player__position')
        .order_by('-n')
    )
    players = [
        {
            'player_id': a.player_id,
            'name': a.player.name,
            'slug': _slug(a.player.name),
            'team': a.player.team.abbreviation if a.player.team_id else None,
            'position': a.player.position.position_type if a.player.position_id else None,
            'sleeper_id': a.player.sleeper_id,
            'crowd': _crowd_payload(a),
        }
        for a in rows
    ]
    return _with_quota(
        Response({
            'season': int(season), 'week': int(week),
            'unit': 'percent_of_budget',
            'source': 'faablab_crowd',
            'players': players,
        }),
        request,
    )


@extend_schema(
    tags=[V1_TAG],
    operation_id='getPlayerBids',
    summary='Crowd bids for one player in a week',
    description=(
        'Accepts either a numeric FAABLab player id or a name slug '
        '(`john-metchie`). All values are percent of budget.'
    ),
    parameters=[SEASON, WEEK,
                OpenApiParameter('player', OpenApiTypes.STR, OpenApiParameter.PATH)],
    responses={200: OpenApiTypes.OBJECT, 404: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
@permission_classes([QuotaExceeded])
def player_bids(request, season, week, player):
    qs = BidAggregate.objects.filter(
        scope=BidAggregate.Scope.CROWD, season=season, week=week
    ).select_related('player', 'player__team', 'player__position')

    agg = None
    if str(player).isdigit():
        agg = qs.filter(player_id=int(player)).first()
    if agg is None:
        agg = next((a for a in qs if _slug(a.player.name) == str(player).lower()), None)
    if agg is None:
        return _with_quota(
            Response({'detail': 'No crowd data for that player and week.'},
                     status=status.HTTP_404_NOT_FOUND),
            request,
        )

    return _with_quota(
        Response({
            'season': int(season), 'week': int(week),
            'unit': 'percent_of_budget',
            'source': 'faablab_crowd',
            'player_id': agg.player_id,
            'name': agg.player.name,
            'slug': _slug(agg.player.name),
            'team': agg.player.team.abbreviation if agg.player.team_id else None,
            'position': agg.player.position.position_type if agg.player.position_id else None,
            'sleeper_id': agg.player.sleeper_id,
            'crowd': _crowd_payload(agg),
        }),
        request,
    )


@extend_schema(
    tags=[V1_TAG],
    operation_id='getCoverage',
    summary='Which seasons and weeks have data',
    description='Use this to discover what is available before requesting a week.',
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
@permission_classes([QuotaExceeded])
def coverage(request):
    rows = (
        BidAggregate.objects.filter(scope=BidAggregate.Scope.CROWD)
        .values_list('season', 'week')
        .distinct()
        .order_by('-season', '-week')
    )
    by_season = {}
    for season, week in rows:
        by_season.setdefault(season, []).append(week)
    return _with_quota(
        Response({
            'unit': 'percent_of_budget',
            'source': 'faablab_crowd',
            'seasons': [
                {'season': s, 'weeks': sorted(w)} for s, w in sorted(by_season.items(), reverse=True)
            ],
        }),
        request,
    )


@extend_schema(
    tags=[V1_TAG],
    operation_id='getPricing',
    summary='Tiers and quotas',
    description='No authentication required. Lists what each tier allows.',
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
def pricing(request):
    return Response({
        'currency': 'USD',
        'billing': 'monthly',
        'note': (
            'No key is needed to start -- anonymous callers get a working quota. '
            'A free key raises it. Quotas reset on the first of each month.'
        ),
        'tiers': [
            {
                'tier': tier.value,
                'label': tier.label,
                'calls_per_month': TIER_QUOTAS[tier],
                'price_usd': TIER_PRICES_USD[tier],
                'requires_key': tier != ApiTier.ANON,
            }
            for tier in ApiTier
        ],
        'auth': {
            'header': 'X-API-Key: faab_...',
            'alternatives': ['Authorization: Bearer faab_...', '?api_key=faab_...'],
        },
    })


# ---------------------------------------------------------------------------
# Self-serve signup and upgrade
#
# An agent can do two of the three things needed to become a customer: it can
# create a key, and it can read a quota error. It cannot pay. So creating a key
# is instant and unauthenticated, and the upgrade path produces a URL the agent
# hands to the human who deployed it.
# ---------------------------------------------------------------------------
from django.utils import timezone
from rest_framework.throttling import AnonRateThrottle

from .models import ApiKey
from .services import apikeys, billing


class SignupThrottle(AnonRateThrottle):
    """Keeps key creation self-serve without letting one address mint thousands."""

    scope = 'api_signup'


@extend_schema(
    tags=[V1_TAG],
    operation_id='createApiKey',
    summary='Create an API key instantly',
    description=(
        '**No signup flow, no email confirmation, no captcha.** POST here and a '
        'free key comes back in the response, usable immediately.\n\n'
        'This exists because an AI agent cannot complete a signup form. It can '
        'make this call.\n\n'
        'The key is shown **once** and stored only as a hash -- it cannot be '
        'recovered, only replaced. `email` is optional but is the only way to '
        'reach you about the key later.'
    ),
    request=OpenApiTypes.OBJECT,
    responses={201: OpenApiTypes.OBJECT},
    examples=[
        OpenApiExample(
            'Minimal', value={'name': 'my-waiver-bot'}, request_only=True
        ),
        OpenApiExample(
            'With contact',
            value={'name': 'my-waiver-bot', 'email': 'dev@example.com'},
            request_only=True,
        ),
    ],
)
@api_view(['POST'])
@permission_classes([])
@throttle_classes([SignupThrottle])
def create_key(request):
    name = (request.data.get('name') or 'unnamed').strip()[:120]
    email = (request.data.get('email') or '').strip()[:254]
    key, full = apikeys.issue(name=name, email=email, tier=ApiTier.FREE)
    site = request.build_absolute_uri('/').rstrip('/')
    return Response(
        {
            'api_key': full,
            'prefix': key.prefix,
            'tier': key.tier,
            'calls_per_month': key.monthly_quota,
            'usage_url': f'{site}/api/v1/keys/me',
            'upgrade_url': f'{site}/api/v1/keys/upgrade',
            'how_to_use': 'Send it as the header  X-API-Key: <api_key>',
            'warning': 'Store this now. It is hashed on our side and cannot be shown again.',
        },
        status=status.HTTP_201_CREATED,
    )


@extend_schema(
    tags=[V1_TAG],
    operation_id='getKeyStatus',
    summary='Check your key, usage and remaining quota',
    description='Send the key you want to inspect. Does not count against quota.',
    responses={200: OpenApiTypes.OBJECT, 403: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
@permission_classes([])
def key_status(request):
    raw = apikeys.extract(request)
    key = apikeys.resolve(raw) if raw else None
    if not key:
        return Response(
            {'detail': 'Send a valid key as X-API-Key to see its status.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    period = apikeys.current_period()
    used = next(
        (u.calls for u in key.usage.all() if u.period == period), 0
    )
    site = request.build_absolute_uri('/').rstrip('/')
    return Response({
        'prefix': key.prefix,
        'name': key.name,
        'tier': key.tier,
        'period': period,
        'calls_used': used,
        'calls_per_month': key.monthly_quota,
        'calls_remaining': max(0, key.monthly_quota - used),
        'last_used_at': key.last_used_at,
        'upgrade_url': f'{site}/api/v1/keys/upgrade',
    })


@extend_schema(
    tags=[V1_TAG],
    operation_id='getUpgradeLink',
    summary='Get a payment link for a key',
    description=(
        'Returns a checkout URL for the supplied key.\n\n'
        'An agent should **surface this URL to the person who deployed it** '
        'rather than trying to follow it. Once that person pays, the key is '
        'upgraded automatically and the agent\'s next call succeeds -- nothing '
        'needs to be relayed back.'
    ),
    parameters=[
        OpenApiParameter('tier', OpenApiTypes.STR, OpenApiParameter.QUERY,
                         enum=['hobby', 'pro'], description='Defaults to hobby.'),
    ],
    responses={200: OpenApiTypes.OBJECT},
)
@api_view(['GET'])
@permission_classes([])
def upgrade_link(request):
    raw = apikeys.extract(request)
    key = apikeys.resolve(raw) if raw else None
    if not key:
        return Response(
            {'detail': 'Send the key to upgrade as X-API-Key.'},
            status=status.HTTP_403_FORBIDDEN,
        )
    tier = request.query_params.get('tier') or ApiTier.HOBBY
    if tier not in (ApiTier.HOBBY, ApiTier.PRO):
        tier = ApiTier.HOBBY
    return Response({
        'prefix': key.prefix,
        'current_tier': key.tier,
        'upgrade_to': tier,
        'price_usd_per_month': TIER_PRICES_USD.get(tier),
        'calls_per_month': TIER_QUOTAS.get(tier),
        'checkout_url': billing.checkout_url(key, tier),
        'instructions': (
            'Open this link to pay. The key upgrades automatically once payment '
            'completes -- no need to send us anything.'
        ),
    })


@extend_schema(exclude=True)
@api_view(['POST'])
@permission_classes([])
def stripe_webhook(request):
    """
    Stripe calls this when a payment completes or a subscription lapses.

    The signature is verified when a signing secret is configured; without one
    the endpoint refuses to act, because an unverified webhook is an open door
    to free upgrades.
    """
    from django.conf import settings

    secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
    if not secret:
        return Response(
            {'detail': 'Webhook not configured.'},
            status=status.HTTP_503_SERVICE_UNAVAILABLE,
        )
    try:
        import stripe
        event = stripe.Webhook.construct_event(
            payload=request.body,
            sig_header=request.headers.get('Stripe-Signature', ''),
            secret=secret,
        )
    except Exception:
        return Response({'detail': 'Invalid signature.'},
                        status=status.HTTP_400_BAD_REQUEST)

    result = billing.apply_webhook(event)
    return Response({'result': result})
