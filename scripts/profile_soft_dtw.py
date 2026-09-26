"""Phase 3: Profile G1 Soft-DTW internals."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
from quant.i04_cal.geometries import soft_dtw, soft_dtw_divergence


def profile_soft_dtw_internal():
    """Profile Soft-DTW internal operations."""
    print("Soft-DTW Internal Profile")
    print("=" * 60)

    # Test data
    W = 20
    x = np.linspace(0, 1, W)
    y = x + 0.1

    # Time soft_dtw call
    n_iter = 100
    t0 = time.perf_counter()
    for _ in range(n_iter):
        d = soft_dtw(x, y, gamma=1.0, band=max(2, W // 4))
    t1 = time.perf_counter()
    sdtw_time = (t1 - t0) / n_iter

    print(f"Soft-DTW (single call): {sdtw_time:.6f}s")

    # Time soft_dtw_divergence call
    t0 = time.perf_counter()
    for _ in range(n_iter):
        d = soft_dtw_divergence(x, y, gamma=1.0)
    t1 = time.perf_counter()
    div_time = (t1 - t0) / n_iter

    print(f"Soft-DTW divergence (single call): {div_time:.6f}s")
    print(f"  Self-term calls per divergence: 2 (x,x) + (y,y)")

    # Decompose divergence
    t0 = time.perf_counter()
    sdtw_xy = soft_dtw(x, y, gamma=1.0, band=max(2, W // 4))
    t1 = time.perf_counter()
    sdtw_xy_time = t1 - t0

    t0 = time.perf_counter()
    sdtw_xx = soft_dtw(x, x, gamma=1.0, band=max(2, W // 4))
    t1 = time.perf_counter()
    sdtw_xx_time = t1 - t0

    t0 = time.perf_counter()
    sdtw_yy = soft_dtw(y, y, gamma=1.0, band=max(2, W // 4))
    t1 = time.perf_counter()
    sdtw_yy_time = t1 - t0

    total_div = sdtw_xy - 0.5 * sdtw_xx - 0.5 * sdtw_yy

    print(f"\nDecomposition:")
    print(f"  SDTW(x,y): {sdtw_xy_time:.6f}s")
    print(f"  SDTW(x,x): {sdtw_xx_time:.6f}s")
    print(f"  SDTW(y,y): {sdtw_yy_time:.6f}s")
    print(f"  Total (3 calls): {sdtw_xy_time + sdtw_xx_time + sdtw_yy_time:.6f}s")
    print(f"  Divergence result: {total_div:.6f}")

    # Check if self-terms are needed
    print(f"\nSelf-term reuse opportunity:")
    print(f"  If we cache SDTW(x,x) and SDTW(y,y), we could save:")
    print(f"    {sdtw_xx_time + sdtw_yy_time:.6f}s per divergence")
    print(f"    = {(sdtw_xx_time + sdtw_yy_time) / div_time * 100:.1f}% of divergence time")

    # Check Soft-DTW internals
    print(f"\nSoft-DTW internals:")
    print(f"  Band width: {max(2, W // 4)}")
    print(f"  Band cells: {W * (W // 4)} vs full {W * W}")
    print(f"  Band reduction: {(1 - (W // 4) / W) * 100:.1f}% fewer cells")


if __name__ == "__main__":
    profile_soft_dtw_internal()
