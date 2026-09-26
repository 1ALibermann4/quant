"""Quick focused profiling of I04-CAL hotspots."""

import os
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

from quant.i04_cal.gates import compute_gates_for_spec
from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.worlds import generate_world

def quick_profile():
    """Profile key geometries with minimal configuration."""
    geometries = ["G0", "G1", "G3"]
    results = {}

    for geo in geometries:
        print(f"Profiling {geo}...")
        specs = iter_geometry_specs()
        spec = next(s for s in specs if s.geometry_id == geo)

        # World generation
        t0 = time.perf_counter()
        world = generate_world("S0a", 0)
        t1 = time.perf_counter()
        world_time = t1 - t0

        # Full gate computation (W=20)
        t0 = time.perf_counter()
        gates = compute_gates_for_spec(world, spec, W=20, seed=123)
        t1 = time.perf_counter()
        gate_time = t1 - t0

        results[geo] = {
            "world_generation": world_time,
            "gate_computation": gate_time,
            "total": world_time + gate_time,
        }

        print(f"  World gen: {world_time:.3f}s")
        print(f"  Gate comp: {gate_time:.3f}s")
        print(f"  Total: {world_time + gate_time:.3f}s")
        print()

    print("Summary:")
    for geo, times in results.items():
        print(f"  {geo}: {times['total']:.3f}s (world={times['world_generation']:.3f}s, gates={times['gate_computation']:.3f}s)")

if __name__ == "__main__":
    quick_profile()
