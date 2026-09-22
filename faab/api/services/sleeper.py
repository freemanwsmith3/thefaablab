"""
Sleeper API client.

Read-only and unauthenticated, so there is no credential to manage here. What
does need managing is politeness: Sleeper documents a 1000 req/min ceiling and
blocks IPs that exceed it, so every call goes through a shared rate limiter and
the default budget is well under the published limit.
"""
import logging
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Dict, Iterable, List, Optional

import requests
from django.conf import settings

log = logging.getLogger(__name__)

# Sleeper's numeric waiver_type for FAAB budgets.
WAIVER_TYPE_FAAB = 2


class RateLimiter:
    """Thread-safe minimum-interval pacer shared across worker threads."""

    def __init__(self, per_minute: int):
        self._interval = 60.0 / max(per_minute, 1)
        self._lock = threading.Lock()
        self._next_at = 0.0

    def acquire(self) -> None:
        with self._lock:
            now = time.monotonic()
            wait = self._next_at - now
            if wait > 0:
                time.sleep(wait)
                now = time.monotonic()
            self._next_at = now + self._interval


class SleeperClient:
    def __init__(
        self,
        base_url: Optional[str] = None,
        per_minute: Optional[int] = None,
        timeout: Optional[int] = None,
        max_retries: int = 3,
    ):
        self.base_url = (base_url or settings.SLEEPER_BASE_URL).rstrip('/')
        self.timeout = timeout or settings.SLEEPER_TIMEOUT
        self.max_retries = max_retries
        self.limiter = RateLimiter(per_minute or settings.SLEEPER_RATE_LIMIT_PER_MIN)
        self._local = threading.local()
        self.calls = 0
        self._calls_lock = threading.Lock()

    @property
    def session(self) -> requests.Session:
        # One session per thread: connection pooling without cross-thread state.
        s = getattr(self._local, 'session', None)
        if s is None:
            s = requests.Session()
            s.headers.update(
                {'User-Agent': settings.SLEEPER_USER_AGENT, 'Accept': 'application/json'}
            )
            self._local.session = s
        return s

    def get(self, path: str):
        """GET a path, returning parsed JSON or None. Never raises for 404."""
        url = f'{self.base_url}/{path.lstrip("/")}'
        backoff = 1.0
        for attempt in range(self.max_retries):
            self.limiter.acquire()
            try:
                resp = self.session.get(url, timeout=self.timeout)
                with self._calls_lock:
                    self.calls += 1
                if resp.status_code == 404:
                    return None
                if resp.status_code == 429:
                    # Backed off hard: we are over budget, not merely unlucky.
                    log.warning('sleeper 429 on %s, backing off %.1fs', path, backoff * 5)
                    time.sleep(backoff * 5)
                    backoff *= 2
                    continue
                resp.raise_for_status()
                return resp.json()
            except (requests.RequestException, ValueError) as exc:
                if attempt == self.max_retries - 1:
                    log.warning('sleeper GET %s failed: %s', path, exc)
                    return None
                time.sleep(backoff)
                backoff *= 2
        return None

    # -- endpoints ---------------------------------------------------------
    def state(self) -> Optional[dict]:
        return self.get('state/nfl')

    def user(self, username_or_id: str) -> Optional[dict]:
        return self.get(f'user/{username_or_id}')

    def user_leagues(self, user_id: str, season: int) -> List[dict]:
        return self.get(f'user/{user_id}/leagues/nfl/{season}') or []

    def league(self, league_id: str) -> Optional[dict]:
        return self.get(f'league/{league_id}')

    def league_users(self, league_id: str) -> List[dict]:
        return self.get(f'league/{league_id}/users') or []

    def transactions(self, league_id: str, week: int) -> List[dict]:
        return self.get(f'league/{league_id}/transactions/{week}') or []

    def trending(self, kind: str = 'add', lookback_hours: int = 24, limit: int = 25):
        return (
            self.get(
                f'players/nfl/trending/{kind}'
                f'?lookback_hours={lookback_hours}&limit={limit}'
            )
            or []
        )

    def all_players(self) -> Optional[dict]:
        """
        The ~5MB player dump. Sleeper asks that this be called at most once a
        day, so callers must cache it -- never touch this on a request path.
        """
        return self.get('players/nfl')

    # -- fan-out -----------------------------------------------------------
    def map(self, fn: Callable, items: Iterable, workers: Optional[int] = None) -> List:
        """Run fn over items in a thread pool; the rate limiter still applies."""
        items = list(items)
        if not items:
            return []
        workers = workers or settings.SLEEPER_MAX_WORKERS
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return list(pool.map(fn, items))


def classify_scoring(scoring_settings: Optional[dict]) -> tuple:
    """
    Map a league's reception value to a coarse format bucket.

    Real leagues use 0, 0.25, 0.3, 0.5, 0.75 and 1, so anything that is not
    clearly standard or half gets bucketed by nearest sensible neighbour.
    """
    rec = float((scoring_settings or {}).get('rec', 0) or 0)
    if rec >= 0.75:
        return 'ppr', rec
    if rec >= 0.25:
        return 'half', rec
    return 'std', rec


def is_faab(league: dict) -> bool:
    s = league.get('settings') or {}
    return s.get('waiver_type') == WAIVER_TYPE_FAAB and bool(s.get('waiver_budget'))


def normalise_bid(bid_raw: int, budget: int) -> int:
    """
    Convert a raw bid to percent of budget, clamped to 0..100.

    This is the single most important transform in the ingest. Budgets range
    from 100 to 1000 in the wild, so averaging raw values across leagues
    produces a meaningless number.
    """
    if not budget or budget <= 0:
        budget = 100
    pct = round(100.0 * bid_raw / budget)
    return max(0, min(100, int(pct)))
