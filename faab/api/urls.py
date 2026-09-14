from django.conf import settings
from django.urls import path

from . import views, views_public

urlpatterns = [
    # New unified read path.
    path('week', views.WeekAPI.as_view(), name='week'),
    path('health', views.health, name='health'),
    path('current-week', views.current_week, name='current-week'),
    path('llms.txt', views.llms_txt, name='llms-txt'),
    # Retained so the currently deployed frontend keeps working unchanged.
    path('targets', views.TargetsAPI.as_view(), name='targets'),
    path('stats', views.StatsAPI.as_view(), name='stats'),
    path('bid', views.BidView.as_view(), name='bid'),

    # Public, metered data API. Versioned separately from the site's own
    # endpoints so the site can change without breaking external callers.
    path('v1/pricing', views_public.pricing, name='v1-pricing'),
    path('v1/coverage', views_public.coverage, name='v1-coverage'),
    path('v1/bids/<int:season>/<int:week>', views_public.week_bids, name='v1-week'),
    path('v1/bids/<int:season>/<int:week>/<str:player>',
         views_public.player_bids, name='v1-player'),

    # Self-serve signup: an agent can create its own key and fetch a payment
    # link to hand to the developer who deployed it.
    path('v1/keys', views_public.create_key, name='v1-create-key'),
    path('v1/keys/me', views_public.key_status, name='v1-key-status'),
    path('v1/keys/upgrade', views_public.upgrade_link, name='v1-upgrade'),
    path('v1/stripe/webhook', views_public.stripe_webhook, name='v1-stripe-webhook'),
]

# Interactive docs. Unmounted entirely when ENABLE_API_DOCS is off, so turning
# them off removes the routes rather than just hiding the links.
if getattr(settings, 'ENABLE_API_DOCS', False):
    from drf_spectacular.views import (
        SpectacularAPIView,
        SpectacularRedocView,
        SpectacularSwaggerView,
    )

    urlpatterns += [
        path('schema', SpectacularAPIView.as_view(), name='schema'),
        path(
            'docs',
            SpectacularSwaggerView.as_view(url_name='schema'),
            name='swagger-ui',
        ),
        path('redoc', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    ]
