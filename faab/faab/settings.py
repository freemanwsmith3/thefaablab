"""
Django settings for faab.

All secrets and environment-specific values come from the environment.
Nothing in this file may contain a credential. See .env.example.
"""
import os
from pathlib import Path

import dj_database_url
from decouple import Config, Csv, RepositoryEmpty, RepositoryEnv

BASE_DIR = Path(__file__).resolve().parent.parent

# Resolve .env explicitly rather than relying on an implicit upward search,
# which resolves differently depending on the working directory a command is
# run from. On Heroku there is no file and real environment variables are used,
# which RepositoryEmpty falls through to.
ENV_FILE = next(
    (
        candidate
        for candidate in (
            Path(os.environ.get('DJANGO_ENV_FILE', '')) if os.environ.get('DJANGO_ENV_FILE') else None,
            BASE_DIR / '.env',
            BASE_DIR.parent / '.env',
        )
        if candidate and candidate.is_file()
    ),
    None,
)
config = Config(RepositoryEnv(str(ENV_FILE)) if ENV_FILE else RepositoryEmpty())

# --------------------------------------------------------------------------
# Core / secrets
# --------------------------------------------------------------------------
DEBUG = config('DEBUG', default=False, cast=bool)

# In production the process refuses to boot without a real key rather than
# silently falling back to a shared default.
SECRET_KEY = config('SECRET_KEY', default='' if not DEBUG else 'dev-only-insecure-key')
if not SECRET_KEY:
    raise RuntimeError('SECRET_KEY must be set when DEBUG is off')

ALLOWED_HOSTS = config(
    'ALLOWED_HOSTS',
    default='.faablab.app,.herokuapp.com,127.0.0.1,localhost',
    cast=Csv(),
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'drf_spectacular',
    'api.apps.ApiConfig',
]

# Order matters: security first, then whitenoise, then gzip, then cors.
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
]

ROOT_URLCONF = 'faab.urls'
WSGI_APPLICATION = 'faab.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --------------------------------------------------------------------------
# Database
# --------------------------------------------------------------------------
# CONN_MAX_AGE keeps connections alive between requests. Postgres connection
# setup is expensive and Heroku plans cap connection count, so reusing them
# cuts both latency and the plan size you need.
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL', default=f'sqlite:///{BASE_DIR / "db.sqlite3"}'),
        conn_max_age=config('DB_CONN_MAX_AGE', default=600, cast=int),
        conn_health_checks=True,
        ssl_require=config('DB_SSL_REQUIRE', default=not DEBUG, cast=bool),
    )
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --------------------------------------------------------------------------
# Cache
# --------------------------------------------------------------------------
# Falls back to in-process memory so there is no Redis bill until traffic
# actually justifies one. Set REDIS_URL to switch without a code change.
_redis_url = config('REDIS_URL', default='')
if _redis_url:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': _redis_url,
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'faab-locmem',
            'OPTIONS': {'MAX_ENTRIES': 2000},
        }
    }

# How long a computed week payload stays fresh, in seconds. Aggregates only
# change when a bid lands, and the endpoint is public and identical for every
# visitor, so this absorbs essentially all read traffic.
WEEK_CACHE_SECONDS = config('WEEK_CACHE_SECONDS', default=60, cast=int)

# --------------------------------------------------------------------------
# I18N / static
# --------------------------------------------------------------------------
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'
STORAGES = {
    'default': {'BACKEND': 'django.core.files.storage.FileSystemStorage'},
    'staticfiles': {'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage'},
}

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# --------------------------------------------------------------------------
# CORS
# --------------------------------------------------------------------------
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='https://www.faablab.app,https://faablab.app,http://localhost:3000',
    cast=Csv(),
)
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='https://www.faablab.app,https://faablab.app',
    cast=Csv(),
)

# --------------------------------------------------------------------------
# Security headers (all no-ops under DEBUG so local dev over http still works)
# --------------------------------------------------------------------------
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_REFERRER_POLICY = 'same-origin'
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
if not DEBUG:
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Signing key for the anonymous submitter cookie. Defaults to SECRET_KEY so
# there is one less required variable, but can be rotated independently.
SUBMITTER_SIGNING_SALT = config('SUBMITTER_SIGNING_SALT', default='faab.submitter')

# --------------------------------------------------------------------------
# DRF
# --------------------------------------------------------------------------
REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        ['rest_framework.renderers.JSONRenderer']
        if not DEBUG
        else [
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
        ]
    ),
    # No DEFAULT_THROTTLE_CLASSES: throttling is opt-in per view. Applying the
    # bid limits globally would rate-limit the public read endpoints and the
    # schema, which are cacheable and meant to be hit freely.
    'DEFAULT_THROTTLE_RATES': {
        'bid_burst': config('THROTTLE_BID_BURST', default='10/min'),
        'bid_sustained': config('THROTTLE_BID_SUSTAINED', default='120/day'),
        # Key creation is deliberately self-serve; this only stops one address
        # minting thousands.
        'api_signup': config('THROTTLE_API_SIGNUP', default='20/day'),
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'UNAUTHENTICATED_USER': None,
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    # Keeps numbers numeric in structured error bodies; agents parse these.
    'EXCEPTION_HANDLER': 'api.exception_handlers.handler',
}

# --------------------------------------------------------------------------
# API documentation (OpenAPI 3 / Swagger)
# --------------------------------------------------------------------------
# The API is public and read-mostly, so the docs are on by default. Set
# ENABLE_API_DOCS=False to unmount the schema and both UIs.
ENABLE_API_DOCS = config('ENABLE_API_DOCS', default=True, cast=bool)

SPECTACULAR_SETTINGS = {
    'TITLE': 'FAAB Lab API',
    'DESCRIPTION': (
        'Crowd-sourced and real-market FAAB waiver bid data.\n\n'
        '**Two independent sources feed every endpoint:**\n\n'
        '- `crowd` -- what visitors say they would bid.\n'
        '- `market` -- what real Sleeper leagues actually paid, normalised to '
        'percent of each league budget. Includes losing bids, which is what '
        'makes the win-probability curve possible.\n\n'
        'All bid values are integers 0-100. Market bids are a percentage of the '
        "league's waiver budget, so a 60 in a 250-budget league means a raw bid "
        'of 149.\n\n'
        'Read endpoints are public, cacheable and require no authentication. '
        'The single write endpoint (`POST /api/bid`) is anonymous but rate '
        'limited and deduplicated per browser.'
    ),
    'VERSION': '2.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SORT_OPERATIONS': False,
    'TAGS': [
        {'name': 'week', 'description': 'Unified per-week payload. Prefer this.'},
        {'name': 'bids', 'description': 'Submitting a crowd bid.'},
        {'name': 'legacy', 'description': 'Original endpoints kept for the deployed frontend.'},
        {'name': 'ops', 'description': 'Health and diagnostics.'},
    ],
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': False,
        'displayOperationId': False,
    },
}

# --------------------------------------------------------------------------
# Sleeper ingest
# --------------------------------------------------------------------------
SLEEPER_BASE_URL = config('SLEEPER_BASE_URL', default='https://api.sleeper.app/v1')
# Sleeper documents a 1000 req/min ceiling. Default well under it.
SLEEPER_RATE_LIMIT_PER_MIN = config('SLEEPER_RATE_LIMIT_PER_MIN', default=300, cast=int)
SLEEPER_MAX_WORKERS = config('SLEEPER_MAX_WORKERS', default=8, cast=int)
SLEEPER_TIMEOUT = config('SLEEPER_TIMEOUT', default=15, cast=int)
SLEEPER_USER_AGENT = config('SLEEPER_USER_AGENT', default='faablab/2.0 (+https://faablab.app)')

# Legacy Bid.week used an opaque running counter. Map season -> offset so that
# nfl_week = legacy_week - offset. VERIFY THESE before running the backfill:
# 2024 is derived from faab_value_metrics_2024.json (legacy 29 == NFL week 1).
LEGACY_WEEK_OFFSETS = {
    int(k): int(v)
    for k, v in (
        pair.split(':')
        for pair in config('LEGACY_WEEK_OFFSETS', default='2024:28', cast=Csv())
    )
}

# --------------------------------------------------------------------------
# Billing (optional -- the API works without it; upgrades just fall back to a
# static payment link or the pricing page)
# --------------------------------------------------------------------------
SITE_URL = config('SITE_URL', default='https://www.faablab.app')
STRIPE_SECRET_KEY = config('STRIPE_SECRET_KEY', default='')
STRIPE_WEBHOOK_SECRET = config('STRIPE_WEBHOOK_SECRET', default='')
STRIPE_PRICE_HOBBY = config('STRIPE_PRICE_HOBBY', default='')
STRIPE_PRICE_PRO = config('STRIPE_PRICE_PRO', default='')
# Used when Stripe is not wired yet: any hosted payment link will do.
STRIPE_PAYMENT_LINK = config('STRIPE_PAYMENT_LINK', default='')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {'simple': {'format': '%(levelname)s %(name)s %(message)s'}},
    'handlers': {'console': {'class': 'logging.StreamHandler', 'formatter': 'simple'}},
    'root': {'handlers': ['console'], 'level': config('LOG_LEVEL', default='INFO')},
}
