"""
Statistics over a 101-slot count array.

Bids are integers 0..100 after normalisation, so `counts[v] = number of bids
worth exactly v` is a complete sufficient statistic for the distribution. Every
function here is O(101) and uses no numpy or scipy, which keeps the web process
free of the scientific stack entirely.
"""
from typing import Dict, List, Optional, Sequence

NUM_BUCKETS = 101


def empty() -> List[int]:
    return [0] * NUM_BUCKETS


def add(counts: List[int], value: int, weight: int = 1) -> List[int]:
    """Fold one observation into a count array, in place."""
    if not 0 <= value < NUM_BUCKETS:
        raise ValueError(f'bid {value} outside 0..{NUM_BUCKETS - 1}')
    counts[value] += weight
    return counts


def total(counts: Sequence[int]) -> int:
    return sum(counts)


def quantile(counts: Sequence[int], q: float) -> Optional[float]:
    """
    Value at quantile q (0..1) using the nearest-rank method.

    Nearest-rank always returns a value that someone actually bid, which reads
    more honestly than an interpolated 17.4 that no one ever entered.
    """
    n = total(counts)
    if n == 0:
        return None
    target = q * n
    seen = 0
    for value, c in enumerate(counts):
        if c == 0:
            continue
        seen += c
        if seen >= target:
            return float(value)
    return float(NUM_BUCKETS - 1)


def mean(counts: Sequence[int]) -> Optional[float]:
    n = total(counts)
    if n == 0:
        return None
    return sum(value * c for value, c in enumerate(counts)) / n


def mode(counts: Sequence[int]) -> Optional[int]:
    """
    Most common bid. Ties resolve to the lowest tied value, which keeps the
    result stable across rebuilds -- statistics.mode would return whichever
    tied value it happened to see first.
    """
    n = total(counts)
    if n == 0:
        return None
    best_value, best_count = 0, -1
    for value, c in enumerate(counts):
        if c > best_count:
            best_value, best_count = value, c
    return best_value


def bounds(counts: Sequence[int]):
    """(min, max) of observed values, or (None, None)."""
    lo = hi = None
    for value, c in enumerate(counts):
        if c:
            if lo is None:
                lo = value
            hi = value
    return lo, hi


def trimmed(counts: Sequence[int], k: float = 1.5) -> List[int]:
    """
    Drop Tukey outliers -- values outside [q1 - k*iqr, q3 + k*iqr].

    Replaces the old scipy.stats.iqr call. Returns a new array so the raw
    counts stay intact as the source of truth.
    """
    q1, q3 = quantile(counts, 0.25), quantile(counts, 0.75)
    if q1 is None or q3 is None:
        return list(counts)
    iqr = q3 - q1
    lo, hi = q1 - k * iqr, q3 + k * iqr
    return [c if lo <= value <= hi else 0 for value, c in enumerate(counts)]


def summarize(counts: Sequence[int]) -> Dict[str, Optional[float]]:
    """Scalar summary denormalised onto BidAggregate at write time."""
    n = total(counts)
    lo, hi = bounds(counts)
    return {
        'n': n,
        'mean': round(mean(counts), 1) if n else None,
        'median': quantile(counts, 0.5),
        'mode': mode(counts) if n else None,
        'p25': quantile(counts, 0.25),
        'p75': quantile(counts, 0.75),
        'min_bid': lo,
        'max_bid': hi,
    }


def bins(counts: Sequence[int], num_bins: int = 4) -> List[Dict[str, object]]:
    """
    Collapse to display bins of equal width spanning the observed range.

    Four bins by default, matching the original np.linspace(min, max, 5)
    contract the card design is built against, without importing numpy per
    request. Each value lands in exactly one bin; the last bin is inclusive on
    the right so the maximum observed bid is never dropped.
    """
    n = total(counts)
    lo, hi = bounds(counts)
    if not n or lo is None:
        return []
    if lo == hi:
        return [{'label': str(lo), 'lo': lo, 'hi': lo, 'bids': n}]

    width = (hi - lo) / num_bins
    buckets = [0] * num_bins
    for value, c in enumerate(counts):
        if not c:
            continue
        idx = int((value - lo) / width)
        if idx >= num_bins:  # value == hi
            idx = num_bins - 1
        buckets[idx] += c

    out = []
    for i, bucket in enumerate(buckets):
        b_lo = lo + i * width
        b_hi = hi if i == num_bins - 1 else lo + (i + 1) * width
        out.append(
            {
                'label': f'{round(b_lo)} - {round(b_hi)}',
                'lo': round(b_lo),
                'hi': round(b_hi),
                'bids': bucket,
            }
        )
    return out


def win_curve(won_counts: Sequence[int], n_leagues: int) -> List[Dict[str, float]]:
    """
    P(win | bid = v), as the CDF of winning bids -- a bid of v wins wherever
    the actual winning bid was <= v.

    Emitted sparsely: only the breakpoints where the probability actually
    changes, plus the endpoints. The curve is a step function with typically a
    handful of distinct winning bids, so sending all 101 points wastes roughly
    an order of magnitude of payload for no extra information. Clients should
    render it as a step function (hold each value until the next breakpoint).

    This only exists because Sleeper exposes failed claims alongside successful
    ones.
    """
    if not n_leagues:
        return []
    out, cumulative, last = [], 0, None
    for value, c in enumerate(won_counts):
        cumulative += c
        pct = round(100.0 * cumulative / n_leagues, 1)
        if pct != last:
            out.append({'bid': value, 'win_pct': pct})
            last = pct
    # Anchor the end so a client never has to guess where the curve stops.
    if out and out[-1]['bid'] != len(won_counts) - 1:
        out.append({'bid': len(won_counts) - 1, 'win_pct': last})
    return out


def min_bid_for_confidence(won_counts: Sequence[int], n_leagues: int, target: float = 0.8):
    """Smallest bid that would have won at least `target` of observed leagues."""
    if not n_leagues:
        return None
    need = target * n_leagues
    cumulative = 0
    for value, c in enumerate(won_counts):
        cumulative += c
        if cumulative >= need:
            return value
    return None
