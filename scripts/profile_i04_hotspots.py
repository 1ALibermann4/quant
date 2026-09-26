"""Phase 0: Profile I04-CAL computational hotspots per geometry.

Measures independent timing for:
A. world generation
B. representation construction
C. candidate construction
D. distance computation
E. nearest-neighbor extraction
F. CAL-G1
G. CAL-G2
H. CAL-G3
I. CAL-G4
J. CAL-G5
K. CAL-6
L. serialization

Profiles per geometry and per W where relevant.
"""

from __future__ import annotations

import os
import sys
import time
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

os.environ["I04_CAL_ALLOW_TEST_OVERRIDES"] = "1"

import numpy as np
from quant.i04_cal.gates import (
    admissible_indices,
    build_embeddings,
    candidate_indices,
    compute_gates_for_spec,
    embargo_ok,
    query_indices,
)
from quant.i04_cal.geometries import embed_and_distance_fns, iter_geometry_specs
from quant.i04_cal.params import (
    CANDIDATE_STRIDE,
    EXPENSIVE_CANDIDATE_STRIDE,
    EXPENSIVE_GEOMETRIES,
    EXPENSIVE_QUERY_STRIDE,
    K_NEIGHBORS,
    QUERY_STRIDE,
)
from quant.i04_cal.types import GeometrySpec
from quant.i04_cal.worlds import generate_world


def profile_geometry_cell(
    geometry_id: str,
    world_id: str = "S0a",
    b: int = 0,
    W: int = 20,
) -> dict[str, Any]:
    """Profile a single cell for a geometry."""
    results = {
        "geometry_id": geometry_id,
        "world_id": world_id,
        "b": b,
        "W": W,
        "timings": {},
    }

    # A. World generation
    t0 = time.perf_counter()
    world = generate_world(world_id, b)
    t1 = time.perf_counter()
    results["timings"]["A_world_generation"] = t1 - t0

    r = world.returns
    T = int(r.shape[0])

    # Get geometry spec
    specs = iter_geometry_specs()
    spec = next(s for s in specs if s.geometry_id == geometry_id)

    # Determine strides
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

    # B. Query/candidate index construction
    t0 = time.perf_counter()
    q_idx = query_indices(T, W, stride=q_stride)
    c_idx = candidate_indices(T, W, stride=c_stride)
    union_idx = np.unique(np.concatenate([q_idx, c_idx]))
    t1 = time.perf_counter()
    results["timings"]["B_index_construction"] = t1 - t0

    # C. Representation construction
    embed_fn, dist_fn = embed_and_distance_fns(spec)
    t0 = time.perf_counter()
    emb = build_embeddings(r, union_idx, W, embed_fn)
    t1 = time.perf_counter()
    results["timings"]["C_representation_construction"] = t1 - t0
    results["n_embeddings"] = len(emb)

    # D. Distance computation (sample 100 pairs)
    t0 = time.perf_counter()
    n_sample = min(100, len(q_idx) * len(c_idx))
    distances = []
    for i in range(n_sample):
        qi = q_idx[i % len(q_idx)]
        ci = c_idx[i % len(c_idx)]
        if qi in emb and ci in emb and embargo_ok(qi, ci, W):
            d = dist_fn(emb[qi], emb[ci])
            if np.isfinite(d):
                distances.append(d)
    t1 = time.perf_counter()
    results["timings"]["D_distance_computation"] = t1 - t0
    results["n_distances_sampled"] = len(distances)

    # E. Full gate computation (includes kNN, all gates)
    t0 = time.perf_counter()
    gates = compute_gates_for_spec(world, spec, W, seed=123)
    t1 = time.perf_counter()
    results["timings"]["E_full_gate_computation"] = t1 - t0

    # F. CAL-G1 contrast (from gates)
    t0 = time.perf_counter()
    contrast = gates["k"]["5"]["CAL_G1_contrast_median"]
    t1 = time.perf_counter()
    results["timings"]["F_CAL_G1_extract"] = t1 - t0

    # G. CAL-G2 persistence (from gates)
    t0 = time.perf_counter()
    persistence = gates["k"]["5"]["CAL_G2_EP"]
    t1 = time.perf_counter()
    results["timings"]["G_CAL_G2_extract"] = t1 - t0

    # H. CAL-G3 recurrence (from gates)
    t0 = time.perf_counter()
    recurrence = gates["CAL_G3"][f"H={2*W}"]["R_mean"]
    t1 = time.perf_counter()
    results["timings"]["H_CAL_G3_extract"] = t1 - t0

    # I. CAL-G4 perturbation (from gates)
    t0 = time.perf_counter()
    perturbation = gates["CAL_G4"]["c=0.05"]["spearman_rank"]
    t1 = time.perf_counter()
    results["timings"]["I_CAL_G4_extract"] = t1 - t0

    # J. CAL-G5 nuisance (from gates)
    t0 = time.perf_counter()
    nuisance = gates["CAL_G5"]["dGVOL"]
    t1 = time.perf_counter()
    results["timings"]["J_CAL_G5_extract"] = t1 - t0

    # K. CAL-6 oracle (from gates)
    t0 = time.perf_counter()
    cal6 = gates["CAL_6"]
    t1 = time.perf_counter()
    results["timings"]["K_CAL_6_extract"] = t1 - t0

    # L. Serialization (json dump)
    t0 = time.perf_counter()
    import json
    _ = json.dumps(gates, default=str)
    t1 = time.perf_counter()
    results["timings"]["L_serialization"] = t1 - t0

    # Total
    total = sum(results["timings"].values())
    results["timings"]["TOTAL"] = total

    # Percentages
    for key, val in results["timings"].items():
        if key != "TOTAL":
            results["timings"][f"{key}_pct"] = (val / total) * 100 if total > 0 else 0

    return results


def main():
    """Profile all geometries."""
    geometries = ["G0", "G1", "G2", "G3", "G4", "G5", "G7", "GORD"]
    windows = [20, 40, 60]

    print("=" * 80)
    print("I04-CAL PERF-02 Phase 0: Computational Hotspot Profiling")
    print("=" * 80)
    print()

    all_results = []

    for geo in geometries:
        print(f"Profiling {geo}...")
        geo_results = []

        for W in windows:
            try:
                result = profile_geometry_cell(geo, world_id="S0a", b=0, W=W)
                geo_results.append(result)
            except Exception as e:
                print(f"  Error profiling {geo} W={W}: {e}")
                continue

        all_results.extend(geo_results)

    # Aggregate by geometry
    print()
    print("=" * 80)
    print("Summary by Geometry (averaged across W)")
    print("=" * 80)
    print()

    for geo in geometries:
        geo_data = [r for r in all_results if r["geometry_id"] == geo]
        if not geo_data:
            continue

        print(f"\n{geo}:")
        print(f"  Cells profiled: {len(geo_data)}")

        # Average timings
        for key in ["A_world_generation", "C_representation_construction", "D_distance_computation", "E_full_gate_computation"]:
            if key in geo_data[0]["timings"]:
                avg_time = np.mean([r["timings"][key] for r in geo_data])
                avg_pct = np.mean([r["timings"][f"{key}_pct"] for r in geo_data])
                print(f"  {key}: {avg_time:.3f}s ({avg_pct:.1f}%)")

        total_avg = np.mean([r["timings"]["TOTAL"] for r in geo_data])
        print(f"  TOTAL: {total_avg:.3f}s")

    # Identify dominant hotspots
    print()
    print("=" * 80)
    print("Dominant Hotspots (across all geometries)")
    print("=" * 80)
    print()

    hotspot_keys = [
        "A_world_generation",
        "C_representation_construction",
        "D_distance_computation",
        "E_full_gate_computation",
    ]

    for key in hotspot_keys:
        all_times = [r["timings"][key] for r in all_results if key in r["timings"]]
        if all_times:
            avg_time = np.mean(all_times)
            max_time = np.max(all_times)
            print(f"{key}: avg={avg_time:.3f}s, max={max_time:.3f}s")

    # Save detailed results
    import json
    from pathlib import Path

    output_dir = Path("research/I04/perf")
    output_dir.mkdir(parents=True, exist_ok=True)

    output_file = output_dir / "PERF-02-PROFILE-raw.json"
    with output_file.open("w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, default=str)

    print()
    print(f"Detailed results saved to: {output_file}")


if __name__ == "__main__":
    main()
