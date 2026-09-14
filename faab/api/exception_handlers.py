"""
Custom DRF exception handling for the public API.

DRF coerces every value in an exception's detail to a string, so a structured
error like {"calls_per_month": 5000} reaches the caller as {"calls_per_month":
"5000"}. That is fine for a human reading a message and wrong for an agent
parsing a number, which is most of this API's audience.
"""
from rest_framework.views import exception_handler as drf_handler

from .permissions import QuotaExhausted


def handler(exc, context):
    response = drf_handler(exc, context)
    if response is not None and isinstance(exc, QuotaExhausted):
        # Replace the stringified copy with the dict as it was built.
        detail = exc.args[0] if exc.args else None
        if isinstance(detail, dict):
            response.data = detail
    return response
