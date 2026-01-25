"""Simple caching utilities.

This module defines basic decorators or helpers for caching expensive
function calls.  For v0.1 we rely on Python’s built‑in ``functools.lru_cache``.
Future versions might implement file‑based caching or time‑based invalidation.
"""

from functools import lru_cache
from typing import Callable, TypeVar


F = TypeVar("F", bound=Callable)


def cached(func: F) -> F:
    """Decorator that wraps a function with an unbounded LRU cache.

    Use this decorator on data provider functions to avoid repeated API
    calls within a single session.  Note that for functions without
    arguments, the cache effectively stores a single result.  In a
    production system you might want to implement time‑based expiration
    instead.

    Args:
        func: The function to cache.

    Returns:
        The cached function.
    """
    return lru_cache(maxsize=None)(func)  # type: ignore[return-value]