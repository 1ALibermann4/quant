"""Deterministic caching for I04-CAL representations and distances.

Caching is keyed by (world_id, b, W, geometry_id, variant_id) for embeddings
and (world_id, b, W, geometry_id, variant_id, t, s) for distances.

Caches are only valid within a single process/session and are cleared
between runs.
"""

from __future__ import annotations

from typing import Any

import numpy as np


# In-memory caches (bounded by usage patterns)
_embedding_cache: dict[tuple[Any, ...], dict[int, Any]] = {}
_distance_cache: dict[tuple[Any, ...], float] = {}

# Cache size limits (memory management)
MAX_EMBEDDING_CACHE_SIZE = 10  # Keep last 10 (world, W, geometry) configs
MAX_DISTANCE_CACHE_SIZE = 1000000  # Keep up to 1M distances


def clear_caches() -> None:
    """Clear all caches."""
    _embedding_cache.clear()
    _distance_cache.clear()


def _make_embedding_key(
    world_id: str,
    b: int,
    W: int,
    geometry_id: str,
    variant_id: str,
) -> tuple[Any, ...]:
    """Create cache key for embeddings."""
    return (world_id, int(b), int(W), geometry_id, variant_id)


def _make_distance_key(
    world_id: str,
    b: int,
    W: int,
    geometry_id: str,
    variant_id: str,
    t: int,
    s: int,
) -> tuple[Any, ...]:
    """Create cache key for distance between indices t and s."""
    return (world_id, int(b), int(W), geometry_id, variant_id, int(t), int(s))


def get_cached_embeddings(key: tuple[Any, ...]) -> dict[int, Any] | None:
    """Retrieve cached embeddings."""
    return _embedding_cache.get(key)


def set_cached_embeddings(key: tuple[Any, ...], embeddings: dict[int, Any]) -> None:
    """Cache embeddings with size limit."""
    if len(_embedding_cache) >= MAX_EMBEDDING_CACHE_SIZE:
        # Remove oldest entry (simple FIFO)
        _embedding_cache.pop(next(iter(_embedding_cache)))
    _embedding_cache[key] = embeddings


def get_cached_distance(key: tuple[Any, ...]) -> float | None:
    """Retrieve cached distance."""
    return _distance_cache.get(key)


def set_cached_distance(key: tuple[Any, ...], distance: float) -> None:
    """Cache distance with size limit."""
    if len(_distance_cache) >= MAX_DISTANCE_CACHE_SIZE:
        # Remove oldest entries (simple FIFO)
        # Remove half the cache when limit reached
        items = list(_distance_cache.items())
        for k, _ in items[:MAX_DISTANCE_CACHE_SIZE // 2]:
            _distance_cache.pop(k)
    _distance_cache[key] = distance


def get_cached_distance_symmetric(
    world_id: str,
    b: int,
    W: int,
    geometry_id: str,
    variant_id: str,
    t: int,
    s: int,
) -> float | None:
    """Retrieve cached distance, checking both (t,s) and (s,t) for symmetric distances."""
    key1 = _make_distance_key(world_id, b, W, geometry_id, variant_id, t, s)
    if key1 in _distance_cache:
        return _distance_cache[key1]

    key2 = _make_distance_key(world_id, b, W, geometry_id, variant_id, s, t)
    if key2 in _distance_cache:
        return _distance_cache[key2]

    return None


def set_cached_distance_symmetric(
    world_id: str,
    b: int,
    W: int,
    geometry_id: str,
    variant_id: str,
    t: int,
    s: int,
    distance: float,
) -> None:
    """Cache distance symmetrically (both directions)."""
    key1 = _make_distance_key(world_id, b, W, geometry_id, variant_id, t, s)
    key2 = _make_distance_key(world_id, b, W, geometry_id, variant_id, s, t)

    _distance_cache[key1] = distance
    _distance_cache[key2] = distance  # Symmetric


# Statistics tracking
_stats = {
    "embedding_hits": 0,
    "embedding_misses": 0,
    "distance_hits": 0,
    "distance_misses": 0,
}


def get_cache_stats() -> dict[str, int]:
    """Get cache statistics."""
    return _stats.copy()


def record_embedding_hit() -> None:
    """Record cache hit."""
    _stats["embedding_hits"] += 1


def record_embedding_miss() -> None:
    """Record cache miss."""
    _stats["embedding_misses"] += 1


def record_distance_hit() -> None:
    """Record cache hit."""
    _stats["distance_hits"] += 1


def record_distance_miss() -> None:
    """Record cache miss."""
    _stats["distance_misses"] += 1
