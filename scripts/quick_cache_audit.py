"""Quick cache effectiveness audit for I04-CAL."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
from quant.i04_cal.cache import clear_caches, get_cache_stats
from quant.i04_cal.gates import compute_gates_for_spec
from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.worlds import generate_world


def quick_audit():
    """Quick audit of cache effectiveness."""
    print("Cache Effectiveness Audit (Small Workload)")
    print("=" * 60)

    # Test with G0 (fast geometry)
    geometries = ["G0", "G1"]

    for geo in geometries:
        print(f"\n{geo}:")
        world = generate_world("S0a", 0)
        specs = iter_geometry_specs()
        spec = next(s for s in specs if s.geometry_id == geo)

        # Clear cache
        clear_caches()

        # Run gates
        t0 = time.perf_counter()
        gates = compute_gates_for_spec(world, spec, W=20, seed=123)
        t1 = time.perf_counter()

        stats = get_cache_stats()
        print(f"  Time: {t1 - t0:.3f}s")
        print(f"  Embedding hits: {stats['embedding_hits']}")
        print(f"  Embedding misses: {stats['embedding_misses']}")
        print(f"  Distance hits: {stats['distance_hits']}")
        print(f"  Distance misses: {stats['distance_misses']}")

        total = stats["distance_hits"] + stats["distance_misses"]
        if total > 0:
            hit_rate = stats["distance_hits"] / total * 100
            print(f"  Hit rate: {hit_rate:.1f}%")

        # Check cache size
        from quant.i04_cal.cache import _distance_cache, _embedding_cache
        print(f"  Cache size: {len(_distance_cache)} distances, {len(_embedding_cache)} embeddings")


if __name__ == "__main__":
    quick_audit()
