"""Phase 2B: Audit cache effectiveness for I04-CAL.

Measures:
- requested distance pairs
- unique distance pairs
- cache hits/misses
- hit rate
- evictions
- peak cache size
- peak memory

For representative workloads per geometry.
"""

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
    get_cached_distance_symmetric,
)
from quant.i04_cal.gates import compute_gates_for_spec
from quant.i04_cal.geometries import embed_and_distance_fns, iter_geometry_specs
from quant.i04_cal.params import (
    CANDIDATE_STRIDE,
    EXPENSIVE_CANDIDATE_STRIDE,
    EXPENSIVE_GEOMETRIES,
    EXPENSIVE_QUERY_STRIDE,
    QUERY_STRIDE,
)
from quant.i04_cal.worlds import generate_world


def audit_geometry(geometry_id: str, world_id: str = "S0a", b: int = 0, W: int = 20):
    """Audit cache effectiveness for a single geometry."""
    world = generate_world(world_id, b)
    r = world.returns
    T = int(r.shape[0])

    specs = iter_geometry_specs()
    spec = next(s for s in specs if s.geometry_id == geometry_id)
    embed_fn, dist_fn = embed_and_distance_fns(spec)

    q_stride = (
        EXPENSIVE_QUERY_STRIDE
        if geometry_id in EXPENSIVE_GEOMETRIES
        else QUERY_STRIDE
    )
    c_stride = (
        EXPENSIVE_CANDIDATE_STRIDE
        if geometry_id in EXPENSIVE_GEOMETRIES
        else CANDIDATE_STRIDE
    )

    from quant.i04_cal.gates import admissible_indices, candidate_indices, query_indices
    q_idx = query_indices(T, W, stride=q_stride)
    c_idx = candidate_indices(T, W, stride=c_stride)
    union_idx = np.unique(np.concatenate([q_idx, c_idx]))

    print(f"\n{geometry_id} (W={W}):")
    print(f"  Query indices: {len(q_idx)}")
    print(f"  Candidate indices: {len(c_idx)}")
    print(f"  Union indices: {len(union_idx)}")

    # Count requested pairs
    n_requested = 0
    for t in q_idx:
        for s in c_idx:
            t_i = int(t)
            s_i = int(s)
            if t_i != s_i and abs(t_i - s_i) >= W:
                n_requested += 1

    print(f"  Requested pairs: {n_requested}")

    # Unique pairs (symmetric)
    n_unique = 0
    seen = set()
    for t in q_idx:
        for s in c_idx:
            t_i = int(t)
            s_i = int(s)
            if t_i != s_i and abs(t_i - s_i) >= W:
                key = (min(t_i, s_i), max(t_i, s_i))
                if key not in seen:
                    seen.add(key)
                    n_unique += 1

    print(f"  Unique pairs (symmetric): {n_unique}")

    # Clear cache and run
    clear_caches()
    t0 = time.perf_counter()
    gates = compute_gates_for_spec(world, spec, W, seed=123)
    t1 = time.perf_counter()

    stats = get_cache_stats()
    print(f"  Execution time: {t1 - t0:.3f}s")
    print(f"  Cache stats:")
    print(f"    Embedding hits: {stats['embedding_hits']}")
    print(f"    Embedding misses: {stats['embedding_misses']}")
    print(f"    Distance hits: {stats['distance_hits']}")
    print(f"    Distance misses: {stats['distance_misses']}")

    # Calculate hit rate
    total = stats["distance_hits"] + stats["distance_misses"]
    if total > 0:
        hit_rate = stats["distance_hits"] / total * 100
        print(f"    Hit rate: {hit_rate:.1f}%")

    # Check cache size
    from quant.i04_cal.cache import _distance_cache, _embedding_cache
    print(f"    Cache size: {len(_distance_cache)} distances, {len(_embedding_cache)} embeddings")

    return {
        "geometry_id": geometry_id,
        "W": W,
        "n_requested": n_requested,
        "n_unique": n_unique,
        "stats": stats,
        "cache_size": len(_distance_cache),
        "hit_rate": hit_rate if total > 0 else 0,
    }


def main():
    """Audit cache effectiveness across geometries."""
    print("=" * 80)
    print("I04-CAL PERF-02 Phase 2B: Cache Effectiveness Audit")
    print("=" * 80)

    geometries = ["G0", "G1", "G3", "G4", "G7", "GORD"]
    results = []

    for geo in geometries:
        try:
            result = audit_geometry(geo)
            results.append(result)
        except Exception as e:
            print(f"  Error auditing {geo}: {e}")
            continue

    print("\n" + "=" * 80)
    print("Summary")
    print("=" * 80)

    for r in results:
        print(f"\n{r['geometry_id']}:")
        print(f"  Requested pairs: {r['n_requested']}")
        print(f"  Unique pairs: {r['n_unique']}")
        print(f"  Unique reduction: {(1 - r['n_unique'] / r['n_requested']) * 100:.1f}%")
        print(f"  Hit rate: {r['hit_rate']:.1f}%")
        print(f"  Cache size: {r['cache_size']} distances")


if __name__ == "__main__":
    main()
