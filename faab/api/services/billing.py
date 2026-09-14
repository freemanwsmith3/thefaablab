"""
Turning a quota wall into a payment, without the agent needing a card.

An AI agent can sign itself up and can read a 429, but it cannot complete a
checkout. So the flow splits: the agent gets a key instantly and, when it runs
out, receives a URL to hand to the human who deployed it. The human pays, a
webhook upgrades that exact key, and the agent's next call just works.

Stripe is optional. With no key configured this falls back to a static payment
link, so the upgrade path exists before any Stripe integration does.
"""
import logging

from django.conf import settings

from ..models import ApiTier

log = logging.getLogger(__name__)

# Price ids come from the environment so the same code runs in test and live.
TIER_PRICE_IDS = {
    ApiTier.HOBBY: getattr(settings, 'STRIPE_PRICE_HOBBY', ''),
    ApiTier.PRO: getattr(settings, 'STRIPE_PRICE_PRO', ''),
}


def _stripe():
    secret = getattr(settings, 'STRIPE_SECRET_KEY', '')
    if not secret:
        return None
    import stripe
    stripe.api_key = secret
    return stripe


def checkout_url(api_key, tier: str = ApiTier.HOBBY) -> str:
    """
    A URL the developer can open to upgrade this specific key.

    The key's prefix rides along in metadata so the webhook knows what to
    upgrade -- the agent never has to relay anything back to us.
    """
    site = getattr(settings, 'SITE_URL', '').rstrip('/')
    stripe = _stripe()
    price_id = TIER_PRICE_IDS.get(tier)

    if not stripe or not price_id:
        # Not configured yet: a static link still lets someone pay.
        fallback = getattr(settings, 'STRIPE_PAYMENT_LINK', '')
        if fallback:
            return f'{fallback}?client_reference_id={api_key.prefix}'
        return f'{site}/api/v1/pricing'

    try:
        session = stripe.checkout.Session.create(
            mode='subscription',
            line_items=[{'price': price_id, 'quantity': 1}],
            client_reference_id=api_key.prefix,
            metadata={'api_key_prefix': api_key.prefix, 'tier': str(tier)},
            success_url=f'{site}/api/v1/upgraded?key={api_key.prefix}',
            cancel_url=f'{site}/api/v1/pricing',
        )
        return session.url
    except Exception as exc:  # a billing outage must not break the data API
        log.warning('stripe checkout failed for %s: %s', api_key.prefix, exc)
        return f'{site}/api/v1/pricing'


def apply_webhook(event: dict) -> str:
    """
    Upgrade or downgrade the key a Stripe event refers to.

    Returns a short description of what happened, for the endpoint to log.
    """
    from ..models import ApiKey

    kind = event.get('type', '')
    obj = (event.get('data') or {}).get('object') or {}
    prefix = (
        obj.get('client_reference_id')
        or (obj.get('metadata') or {}).get('api_key_prefix')
        or ''
    )
    if not prefix:
        return 'ignored: no key reference'

    key = ApiKey.objects.filter(prefix=prefix).first()
    if not key:
        return f'ignored: unknown key {prefix}'

    if kind in ('checkout.session.completed', 'customer.subscription.updated'):
        tier = (obj.get('metadata') or {}).get('tier') or ApiTier.HOBBY
        key.tier = tier
        key.is_active = True
        if obj.get('customer'):
            key.stripe_customer_id = obj['customer']
        key.save(update_fields=['tier', 'is_active', 'stripe_customer_id'])
        return f'{prefix} upgraded to {tier}'

    if kind in ('customer.subscription.deleted', 'invoice.payment_failed'):
        # Drop to free rather than deactivating: a lapsed subscription should
        # degrade the agent's access, not break its integration outright.
        key.tier = ApiTier.FREE
        key.save(update_fields=['tier'])
        return f'{prefix} downgraded to free'

    return f'ignored: {kind}'
