"""
Database connection for the standalone ETL scripts.

These scripts previously each carried a full set of production Postgres
credentials in plaintext. They now read DATABASE_URL from the environment, so
there is exactly one place a credential lives and it is never in the repo.

Usage:
    from db import connect
    with connect() as conn:
        ...
"""
import os
import sys

import psycopg2


def database_url() -> str:
    url = os.environ.get('DATABASE_URL', '').strip()
    if not url:
        sys.exit(
            'DATABASE_URL is not set.\n'
            'Load it from your .env (see .env.example) or export it:\n'
            '  export DATABASE_URL="postgres://user:pass@host:5432/dbname"'
        )
    return url


def connect(**overrides):
    """Open a connection using DATABASE_URL. Caller owns closing it."""
    return psycopg2.connect(database_url(), **overrides)
