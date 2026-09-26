"""Quick Soft-DTW self-term reuse benchmark."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
from quant.i04_cal.geometries import soft_dtw, soft_dtw_divergence, _SDTW_SELF_CACHE


def quick_benchmark():
    """Quick benchmark showing self-term reuse benefit."""
    print("Soft-DTW Self-Term Reuse Benchmark")
    print("=" * 60)

    W = 20
    x = np.linspace(0, 1, W)
    y = x + 0.1
    gamma = 1.0
    n = 50

    # Without caching
    _SDTW_SELF_CACHE.clear()
    t0 = time.perf_counter()
    for _ in range(n):
        d = (
            soft_dtw(x, y, gamma)
            - 0.5 * soft_dtw(x, x, gamma)
            - 0.5 * soft_dtw(y, y, gamma)
        )
    t1 = time.perf_counter()
    no_cache = (t1 - t0) / n

    # With caching
    _SDTW_SELF_CACHE.clear()
    t0 = time.perf_counter()
    for _ in range(n):
        d = soft_dtw_divergence(x, y, gamma)
    t1 = time.perf_counter()
    with_cache = (t1 - t0) / n

    print(f"Without self-term cache: {no_cache:.6f}s")
    print(f"With self-term cache:    {with_cache:.6f}s")
    print(f"Speedup:                 {no_cache / with_cache:.2f}x")
    print(f"Time saved per call:     {(no_cache - with_cache):.6f}s")
    print(f"Cache size:              {len(_SDTW_SELF_CACHE)} entries")


if __name__ == "__main__":
    quick_benchmark()
