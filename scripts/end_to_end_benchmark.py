"""End-to-end benchmark of PERF-02 optimizations."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
import tempfile
import shutil
from quant.i04_cal.params import CalConfig
from quant.i04_cal.pipeline import run_calibration


def benchmark_config(workers, max_cells, geometry="G0"):
    """Benchmark a configuration."""
    test_base = Path("bench_results")
    test_base.mkdir(exist_ok=True)

    try:
        out = test_base / f"w{workers}_g{geometry}"
        if out.exists():
            shutil.rmtree(out)

        cfg = CalConfig(
            B=1,
            windows=(20,),
            workers=workers,
            worlds=("S0a",),
            geometries=(geometry,),
        )

        t0 = time.perf_counter()
        man = run_calibration(out, cfg, max_cells=max_cells, use_cache=True)
        t1 = time.perf_counter()

        elapsed = t1 - t0
        rows = man["n_rows"]
        time_per_cell = elapsed / rows if rows > 0 else 0

        return {
            "workers": workers,
            "geometry": geometry,
            "cells": rows,
            "elapsed": elapsed,
            "time_per_cell": time_per_cell,
            "status": man["status"],
        }
    finally:
        if test_base.exists():
            shutil.rmtree(test_base)


def run_benchmarks():
    """Run comprehensive benchmarks."""
    print("PERF-02 End-to-End Benchmark")
    print("=" * 60)

    results = []

    # Test G0 (fast geometry) with different worker counts
    print("\nG0 (L2) Geometry:")
    for workers in [1, 2, 4]:
        r = benchmark_config(workers, 3, "G0")
        results.append(r)
        print(f"  workers={workers}: {r['elapsed']:.2f}s for {r['cells']} cells ({r['time_per_cell']:.3f}s/cell)")

    # Test G1 (expensive geometry) - smaller test
    print("\nG1 (Soft-DTW) Geometry:")
    for workers in [1, 2]:
        r = benchmark_config(workers, 1, "G1")  # Only 1 cell for G1
        results.append(r)
        print(f"  workers={workers}: {r['elapsed']:.2f}s for {r['cells']} cells ({r['time_per_cell']:.3f}s/cell)")

    # Summary
    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    # Calculate speedup for G0
    g0_w1 = next(r for r in results if r["workers"] == 1 and r["geometry"] == "G0")
    g0_w4 = next(r for r in results if r["workers"] == 4 and r["geometry"] == "G0")

    if g0_w1["time_per_cell"] > 0:
        speedup = g0_w1["time_per_cell"] / g0_w4["time_per_cell"]
        print(f"G0 multiprocessing speedup (4 vs 1 workers): {speedup:.2f}x")

    print("\nAll benchmarks complete!")


if __name__ == "__main__":
    run_benchmarks()
