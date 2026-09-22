"""
Access control for the public data API.

Deliberately permissive by default: a caller with no key still gets a real,
working quota. An AI agent that discovers this API cannot sign up for anything,
so the first call has to succeed or the agent moves on and we never hear about
it again.

Failures raise explicit, self-describing errors rather than DRF's generic
"credentials were not provided" -- an agent has to be able to tell a bad key
from an exhausted quota and act differently on each.
"""
from rest_framework import status
from rest_framework.exceptions import APIException, AuthenticationFailed
from rest_framework.permissions import BasePermission

from .services import apikeys


class QuotaExhausted(APIException):
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    default_code = 'quota_exhausted'


class QuotaExceeded(BasePermission):
    """Meters the caller and attaches their standing to the request."""

    def has_permission(self, request, view):
        raw = apikeys.extract(request)
        key = apikeys.resolve(raw) if raw else None

        # A supplied-but-wrong key must say so rather than silently falling
        # back to the anonymous tier, which would look like a quota bug.
        if raw and not key:
            raise AuthenticationFailed(
                'Unknown or inactive API key. Omit the header entirely to use '
                'the free anonymous tier. See /api/v1/pricing.'
            )

        state = apikeys.consume(key=key, client_ip=apikeys.client_ip_of(request))
        request.api_state = state
        request.api_key = key

        if not state['allowed']:
            raise QuotaExhausted(self._quota_detail(request, key, state))
        return True

    @staticmethod
    def _quota_detail(request, key, state):
        """
        A structured error an agent can act on without guessing.

        The whole point of the paid tier is that the agent hits this, shows
        `upgrade_url` to the human who deployed it, and that human pays. So the
        link has to be in the error itself, not somewhere the agent must go
        hunting for.
        """
        from .services import billing

        site = request.build_absolute_uri('/').rstrip('/')
        detail = {
            'error': 'quota_exhausted',
            'tier': str(state['tier']),
            'calls_per_month': state['quota'],
            'resets': 'the 1st of each month',
            'pricing_url': f'{site}/api/v1/pricing',
        }
        if key:
            detail['message'] = (
                f"This key's monthly quota is used up. Show the checkout link to "
                f"the developer who set this up -- the key upgrades automatically "
                f"once they pay, and the next call will work."
            )
            detail['upgrade_url'] = billing.checkout_url(key)
        else:
            detail['message'] = (
                'Anonymous quota used up. Create a free key for a larger '
                'allowance -- one POST, no signup form.'
            )
            detail['get_a_free_key'] = f'POST {site}/api/v1/keys'
        return detail
