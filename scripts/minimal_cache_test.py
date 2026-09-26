"""Minimal cache effectiveness test."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
from quant.i04_cal.cache import (
    clear_caches,
    get_cache_stats,
    set_cached_distance_symmetric,
    get_cached_distance_symmetric,
)


def test_cache_mechanics():
    """Test basic cache mechanics."""
    print("Cache Mechanics Test")
    print("=" * 60)

    clear_caches()

    # Set some distances
    n = 1000
    for i in range(n):
        set_cached_distance_symmetric("w", 0, 20, "G0", "default", i, i + 1, float(i))

    # Retrieve them
    hits = 0
    misses = 0
    for i in range(n):
        d = get_cached_distance_symmetric("w", 0, 20, "G0", "default", i, i + 1)
        if d is not None:
            hits += 1
        else:
            misses += 1

    print(f"Set {n} distances")
    print(f"Retrieved: {hits} hits, {misses} misses")
    print(f"Hit rate: {hits / n * 100:.1f}%")

    # Check cache size
    from quant.i04_cal.cache import _distance_cache
    print(f"Cache size: {len(_distance_cache)}")

    # Test eviction
    print("\nTesting cache limit...")
    for i in range(2000000):  # Exceed limit
        set_cached_distance_symmetric("w", 0, 20, "G0", "default", i, i + 1, float(i))

    print(f"After adding 2M distances:")
    print(f"Cache size: {len(_distance_cache)}")
    print(f"Stats: {get_cache_stats()}")


if __name__ == "__main__":
    test_cache_mechanics()
