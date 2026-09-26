"""Benchmark I04-CAL runtime per geometry family under restored contract.

GOV-01: Core strides restored to 8/4 (higher runtime than 16/16 drift).
This script measures per-family performance to identify bottlenecks.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.pipeline import run_calibration
from quant.i04_cal.params import CalConfig, WINDOWS


def benchmark_geometry(geometry_id: str, max_cells: int = 10) -> dict:
    """Benchmark a single geometry family."""
    print(f"Benchmarking {geometry_id}...")
    cfg = CalConfig(
        B=1,
        worlds=("S0a", "S1"),  # Minimal world set for benchmarking
        geometries=(geometry_id,),
        windows=(20,),  # Single window for benchmarking
    )

    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        out_dir = Path(tmpdir) / "bench"
        t0 = time.perf_counter()
        man = run_calibration(out_dir, cfg, max_cells=max_cells)
        elapsed = time.perf_counter() - t0

        return {
            "geometry_id": geometry_id,
            "n_cells": man.get("n_rows", 0),
            "elapsed_seconds": elapsed,
            "sec_per_cell": elapsed / max_cells if max_cells else None,
        }


def main():
    """Benchmark all geometry families."""
    # Tier A geometries
    tier_a = ["G0", "G3", "G4", "G7", "GORD"]
    # Tier B geometries
    tier_b = ["G1", "G2", "G5"]

    print("=" * 60)
    print("I04-CAL Runtime Benchmark (GOV-01 restored contract)")
    print("=" * 60)
    print()

    print("Tier A (Core geometries):")
    tier_a_results = []
    for geo in tier_a:
        result = benchmark_geometry(geo, max_cells=5)
        tier_a_results.append(result)
        print(f"  {geo}: {result['sec_per_cell']:.3f}s/cell ({result['elapsed_seconds']:.2f}s total)")

    print()
    print("Tier B (Extended families):")
    tier_b_results = []
    for geo in tier_b:
        result = benchmark_geometry(geo, max_cells=5)
        tier_b_results.append(result)
        print(f"  {geo}: {result['sec_per_cell']:.3f}s/cell ({result['elapsed_seconds']:.2f}s total)")

    print()
    print("=" * 60)
    print("Summary")
    print("=" * 60)

    # Calculate estimated full runtime
    # Full workload: 9 worlds * 32 B * 3 windows * N_geometries
    # Tier A: 5 geometries
    # Tier B: 3 geometries
    full_cells_per_geo = 9 * 32 * 3  # 864 cells per geometry

    tier_a_avg = sum(r["sec_per_cell"] for r in tier_a_results if r["sec_per_cell"]) / len(tier_a_results)
    tier_b_avg = sum(r["sec_per_cell"] for r in tier_b_results if r["sec_per_cell"]) / len(tier_b_results)

    tier_a_estimated = tier_a_avg * full_cells_per_geo * len(tier_a)
    tier_b_estimated = tier_b_avg * full_cells_per_geo * len(tier_b)
    total_estimated = tier_a_estimated + tier_b_estimated

    print(f"Tier A estimated runtime: {tier_a_estimated / 3600:.2f} hours")
    print(f"Tier B estimated runtime: {tier_b_estimated / 3600:.2f} hours")
    print(f"Total estimated runtime: {total_estimated / 3600:.2f} hours")

    print()
    print("Note: These are estimates based on minimal benchmark configuration.")
    print("Actual runtime may vary with full world set and all windows.")


if __name__ == "__main__":
    main()
