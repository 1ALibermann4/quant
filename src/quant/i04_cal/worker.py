"""CAL worker module for multiprocessing.

This module contains module-level functions that can be imported
by spawned processes on Windows. All functions must be picklable
and importable in spawned context.
"""

import os
import sys
import traceback
from pathlib import Path
from typing import Any, Dict, Tuple

# Ensure src is in path for spawned processes
_src_path = str(Path(__file__).parent.parent.parent)
if _src_path not in sys.path:
    sys.path.insert(0, _src_path)

# Process-local cache (initialized in each spawned process)
_process_world_cache: Dict[Tuple[str, int], Any] = {}


def initialize_worker() -> None:
    """Initialize worker process.

    Called once per worker process after spawn to set up
    process-local state.
    """
    # Ensure src is in path
    if _src_path not in sys.path:
        sys.path.insert(0, _src_path)

    # Re-import required modules in worker context
    global _process_world_cache
    _process_world_cache = {}

    # Import here to avoid circular imports in main process
    from quant.i04_cal.worlds import generate_world
    globals()['generate_world'] = generate_world


def execute_cal_cell(
    world: str,
    b: int,
    W: int,
    spec_dict: Dict[str, Any],
) -> Dict[str, Any]:
    """Execute a single CAL cell.

    Args:
        world: World identifier (e.g., "S0a")
        b: Realization index
        W: Window size
        spec_dict: Serialized geometry spec dict

    Returns:
        Result dict with cell_key, status, gates, etc.
    """
    from quant.i04_cal.gates import compute_gates_for_spec
    from quant.i04_cal.geometries import GeometrySpec
    from quant.i04_cal.params import gate_seed
    from quant.i04_cal.worlds import generate_world

    # Reconstruct spec from dict
    spec = GeometrySpec(
        geometry_id=spec_dict["geometry_id"],
        variant_id=spec_dict["variant_id"],
        params=spec_dict["params"],
        status=spec_dict["status"],
    )

    # Get or create world (process-local cache)
    wb = _process_world_cache.get((world, b))
    if wb is None:
        wb = generate_world(world, b)
        _process_world_cache[(world, b)] = wb

    # Compute seed
    seed = gate_seed(world, b, W, spec.geometry_id, spec.variant_id)

    # Compute gates
    try:
        gates = compute_gates_for_spec(wb, spec, W, seed=int(seed) & 0x7FFFFFFF)
        return {
            "cell_key": f"{world}|b={b}|W={W}|{spec.geometry_id}:{spec.variant_id}",
            "world_id": world,
            "b": b,
            "seed": wb.seed,
            "gate_seed": seed,
            "W": W,
            "world_status": wb.world_status.value,
            "oracle_status": wb.oracle_status.value,
            "oracle_meta": wb.oracle_meta,
            "latent_notes": wb.notes,
            "gates": gates,
            "status": "OK",
        }
    except Exception as e:
        return {
            "cell_key": f"{world}|b={b}|W={W}|{spec.geometry_id}:{spec.variant_id}",
            "world_id": world,
            "b": b,
            "W": W,
            "status": "FAILED_TECHNICAL",
            "error": repr(e),
            "traceback": traceback.format_exc(),
        }
