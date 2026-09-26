"""Test caching layer for I04-CAL representations and distances."""

import os
import sys
from pathlib import Path

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

import numpy as np
from quant.i04_cal.cache import (
    clear_caches,
    get_cached_distance_symmetric,
    get_cached_embeddings,
    get_cache_stats,
    set_cached_distance_symmetric,
    set_cached_embeddings,
)
from quant.i04_cal.gates import build_embeddings
from quant.i04_cal.geometries import g0_embed, g0_distance


def test_embedding_cache():
    """Test that embeddings are cached correctly."""
    clear_caches()
    r = np.random.default_rng(0).normal(size=1000)
    W = 20
    indices = np.arange(W - 1, 100)
    cache_key = ("test_world", 0, W, "G0", "default")

    # First call: miss
    emb1 = build_embeddings(r, indices, W, g0_embed, cache_key=cache_key)
    stats = get_cache_stats()
    assert stats["embedding_misses"] == 1
    assert stats["embedding_hits"] == 0

    # Second call: hit
    emb2 = build_embeddings(r, indices, W, g0_embed, cache_key=cache_key)
    stats = get_cache_stats()
    assert stats["embedding_hits"] == 1
    assert stats["embedding_misses"] == 1

    # Should be identical
    assert emb1 == emb2


def test_distance_cache_symmetric():
    """Test that distances are cached symmetrically."""
    clear_caches()

    # Set symmetric distance
    set_cached_distance_symmetric("w", 0, 20, "G0", "default", 100, 200, 5.5)

    # Should retrieve same value for both orders
    d1 = get_cached_distance_symmetric("w", 0, 20, "G0", "default", 100, 200)
    d2 = get_cached_distance_symmetric("w", 0, 20, "G0", "default", 200, 100)

    assert d1 == 5.5
    assert d2 == 5.5


def test_cache_isolation():
    """Test that cache keys properly isolate different contexts."""
    clear_caches()

    # Different world_id
    set_cached_distance_symmetric("w1", 0, 20, "G0", "default", 100, 200, 5.5)
    set_cached_distance_symmetric("w2", 0, 20, "G0", "default", 100, 200, 6.5)

    d1 = get_cached_distance_symmetric("w1", 0, 20, "G0", "default", 100, 200)
    d2 = get_cached_distance_symmetric("w2", 0, 20, "G0", "default", 100, 200)

    assert d1 == 5.5
    assert d2 == 6.5


def test_cache_statistics():
    """Test that cache statistics are tracked correctly."""
    clear_caches()

    r = np.random.default_rng(0).normal(size=1000)
    W = 20
    indices = np.arange(W - 1, 100)
    cache_key = ("test_world_stats", 0, W, "G0", "default")

    # Miss then hit
    _ = build_embeddings(r, indices, W, g0_embed, cache_key=cache_key)
    _ = build_embeddings(r, indices, W, g0_embed, cache_key=cache_key)

    stats = get_cache_stats()
    # Check that second call was a hit (not a new miss)
    assert stats["embedding_hits"] >= 1
    assert stats["embedding_misses"] >= 1
