"""Benchmark Soft-DTW self-term reuse optimization."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
from quant.i04_cal.geometries import soft_dtw, soft_dtw_divergence, _SDTW_SELF_CACHE


def benchmark_divergence(n_pairs=100):
    """Benchmark divergence with and without self-term caching."""
    print(f"Soft-DTW Divergence Benchmark ({n_pairs} pairs)")
    print("=" * 60)

    # Create test data
    W = 20
    rng = np.random.default_rng(42)
    xs = [rng.normal(size=W) for _ in range(10)]
    ys = [rng.normal(size=W) for _ in range(10)]

    # Without caching (recompute everything)
    _SDTW_SELF_CACHE.clear()

    t0 = time.perf_counter()
    for i in range(n_pairs):
        x = xs[i % len(xs)]
        y = ys[i % len(ys)]
        # Manual divergence without caching
        d = (
            soft_dtw(x, y, 1.0)
            - 0.5 * soft_dtw(x, x, 1.0)
            - 0.5 * soft_dtw(y, y, 1.0)
        )
    t1 = time.perf_counter()
    no_cache_time = (t1 - t0) / n_pairs

    # With caching
    _SDTW_SELF_CACHE.clear()

    t0 = time.perf_counter()
    for i in range(n_pairs):
        x = xs[i % len(xs)]
        y = ys[i % len(ys)]
        d = soft_dtw_divergence(x, y, 1.0)
    t1 = time.perf_counter()
    with_cache_time = (t1 - t0) / n_pairs

    print(f"Without self-term cache: {no_cache_time:.6f}s per divergence")
    print(f"With self-term cache:    {with_cache_time:.6f}s per divergence")
    print(f"Speedup:                 {no_cache_time / with_cache_time:.2f}x")
    print(f"Cache size:              {len(_SDTW_SELF_CACHE)} entries")
    print(f"Cache entries:           {len(xs)} x-self + {len(ys)} y-self")

    return no_cache_time, with_cache_time


def estimate_g1_improvement():
    """Estimate improvement for G1 full CAL."""
    print("\n" + "=" * 60)
    print("G1 Full CAL Impact Estimate")
    print("=" * 60)

    # G1 parameters
    n_queries = 255
    n_candidates = 255
    n_pairs_per_cell = n_queries * n_candidates
    n_cells = 32 * 3 * 3 * 10  # worlds * W * k * gamma

    print(f"Pairs per cell: {n_pairs_per_cell:,}")
    print(f"Total cells: {n_cells:,}")
    print(f"Total pairs: {n_pairs_per_cell * n_cells:,}")

    # Assume each unique index appears in ~n_queries pairs
    # Self-terms are shared across all pairs involving that index
    n_unique_indices = n_queries + n_candidates
    print(f"Unique indices: {n_unique_indices}")
    print(f"Self-terms needed: {n_unique_indices}")
    print(f"Self-terms computed: {n_unique_indices} (vs {n_pairs_per_cell * 2} without caching)")

    # Estimate time
    no_cache_time, with_cache_time = benchmark_divergence(1000)

    old_time_per_cell = no_cache_time * n_pairs_per_cell
    new_time_per_cell = with_cache_time * n_pairs_per_cell

    print(f"\nTime per cell:")
    print(f"  Without caching: {old_time_per_cell:.1f}s")
    print(f"  With caching:    {new_time_per_cell:.1f}s")
    print(f"  Speedup:         {old_time_per_cell / new_time_per_cell:.2f}x")

    total_old = old_time_per_cell * n_cells / 3600
    total_new = new_time_per_cell * n_cells / 3600

    print(f"\nTotal G1 runtime:")
    print(f"  Without caching: {total_old:.1f} hours")
    print(f"  With caching:    {total_new:.1f} hours")
    print(f"  Speedup:         {total_old / total_new:.2f}x")


if __name__ == "__main__":
    estimate_g1_improvement()
