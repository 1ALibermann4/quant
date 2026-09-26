"""Quick runtime estimate based on single cell measurement."""

import time
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

import os
os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.pipeline import run_calibration
from quant.i04_cal.params import CalConfig
import tempfile

# Benchmark G0 with minimal configuration
cfg = CalConfig(
    B=1,
    worlds=("S0a",),
    geometries=("G0",),
    windows=(20,),
)

with tempfile.TemporaryDirectory() as tmpdir:
    out_dir = Path(tmpdir) / "bench"
    t0 = time.perf_counter()
    man = run_calibration(out_dir, cfg, max_cells=1)
    elapsed = time.perf_counter() - t0

    print(f"G0 single cell: {elapsed:.3f}s")

    # Estimate full workload
    # Full: 9 worlds * 32 B * 3 windows * 5 Tier-A geometries = 4320 cells
    # Plus Tier-B: 9 * 32 * 3 * 3 = 2592 cells
    # Total: 6912 cells

    tier_a_cells = 9 * 32 * 3 * 5  # 4320
    tier_b_cells = 9 * 32 * 3 * 3  # 2592
    total_cells = tier_a_cells + tier_b_cells

    # G0 is likely the fastest; G1 (Soft-DTW) will be much slower
    # Conservative estimate: G0 = 1x, G3/G4/G7/GORD = 2-5x, G1/G2/G5 = 10-50x

    tier_a_estimated = elapsed * tier_a_cells * 2  # Conservative 2x for other Tier-A
    tier_b_estimated = elapsed * tier_b_cells * 20  # Conservative 20x for expensive Tier-B
    total_estimated = tier_a_estimated + tier_b_estimated

    print(f"\nEstimated full runtime (conservative):")
    print(f"  Tier A: {tier_a_estimated / 3600:.2f} hours")
    print(f"  Tier B: {tier_b_estimated / 3600:.2f} hours")
    print(f"  Total: {total_estimated / 3600:.2f} hours")
