"""
API key issuance, authentication and monthly metering.

Keys are shown once at issue time and stored only as a SHA-256 hash, so a
database leak yields nothing replayable.
"""
import hashlib
import secrets
from datetime import date

from django.db.models import F
from django.utils import timezone

from ..models import ApiKey, ApiTier, ApiUsage, TIER_QUOTAS

PREFIX = 'faab'


def generate_key() -> tuple:
    """Return (full_key, prefix, hash). The full key is never stored."""
    body = secrets.token_urlsafe(32)
    full = f'{PREFIX}_{body}'
    return full, full[:12], hash_key(full)


def hash_key(full_key: str) -> str:
    return hashlib.sha256(full_key.encode()).hexdigest()


def issue(name: str, email: str = '', tier: str = ApiTier.FREE) -> tuple:
    """Create a key. Returns (ApiKey, full_key) -- show the full key once."""
    full, prefix, digest = generate_key()
    obj = ApiKey.objects.create(
        name=name, email=email, tier=tier, prefix=prefix, key_hash=digest
    )
    return obj, full


def resolve(full_key: str):
    """Look up an active key by its plaintext value, or None."""
    if not full_key:
        return None
    return ApiKey.objects.filter(key_hash=hash_key(full_key), is_active=True).first()


def current_period() -> str:
    today = date.today()
    return f'{today.year:04d}-{today.month:02d}'


def consume(key=None, client_ip: str = '') -> dict:
    """
    Record one call and report the caller's standing.

    Returns {allowed, used, quota, tier}. The counter is incremented with an
    F() expression so concurrent requests cannot lose updates.
    """
    period = current_period()
    if key:
        usage, _ = ApiUsage.objects.get_or_create(key=key, period=period)
        quota, tier = key.monthly_quota, key.tier
    else:
        usage, _ = ApiUsage.objects.get_or_create(
            key=None, client_ip=client_ip or 'unknown', period=period
        )
        quota, tier = TIER_QUOTAS[ApiTier.ANON], ApiTier.ANON

    if usage.calls >= quota:
        return {'allowed': False, 'used': usage.calls, 'quota': quota, 'tier': tier}

    ApiUsage.objects.filter(pk=usage.pk).update(calls=F('calls') + 1)
    if key:
        ApiKey.objects.filter(pk=key.pk).update(last_used_at=timezone.now())

    return {'allowed': True, 'used': usage.calls + 1, 'quota': quota, 'tier': tier}


def extract(request) -> str:
    """
    Pull a key from wherever the caller put it.

    Three forms are accepted because agents guess differently, and a caller who
    supplied a key in a form we ignore looks identical to one who supplied none.
    """
    body = ''
    if getattr(request, 'data', None) and isinstance(request.data, dict):
        body = request.data.get('api_key') or ''
    return str(
        request.headers.get('X-API-Key')
        or request.headers.get('Authorization', '').removeprefix('Bearer ').strip()
        or body
        or request.query_params.get('api_key', '')
    ).strip()


def client_ip_of(request) -> str:
    """Caller address, honouring the proxy header the platform sets."""
    forwarded = request.META.get('HTTP_X_FORWARDED_FOR', '')
    if forwarded:
        return forwarded.split(',')[0].strip()
    return request.META.get('REMOTE_ADDR', '')
