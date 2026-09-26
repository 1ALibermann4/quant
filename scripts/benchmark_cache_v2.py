"""Benchmark caching improvement with multiple geometries/windows."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.pipeline import run_calibration
from quant.i04_cal.params import CalConfig
import tempfile


def benchmark_realistic():
    """Benchmark with multiple geometries and windows (more realistic)."""
    cfg = CalConfig(
        B=1,
        worlds=("S0a",),  # Single world
        geometries=("G0", "G3", "G4", "G7", "GORD"),  # All Tier-A
        windows=(20,),  # Single window
    )

    # With cache
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir) / "with_cache"
        t0 = time.perf_counter()
        man = run_calibration(out_dir, cfg, max_cells=5, use_cache=True)
        elapsed_cached = time.perf_counter() - t0

    # Without cache
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir) / "without_cache"
        t0 = time.perf_counter()
        man = run_calibration(out_dir, cfg, max_cells=5, use_cache=False)
        elapsed_uncached = time.perf_counter() - t0

    print(f"With cache: {elapsed_cached:.3f}s")
    print(f"Without cache: {elapsed_uncached:.3f}s")
    print(f"Speedup: {elapsed_uncached / elapsed_cached:.2f}x")
    print(f"Speedup %: {(elapsed_uncached - elapsed_cached) / elapsed_uncached * 100:.1f}%")


if __name__ == "__main__":
    benchmark_realistic()
