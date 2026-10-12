"""Deterministic bi-machine cell attribution for I04-CAL (engineering only).

Splits the canonical universe into disjoint allowlists without changing
scientific cell identities. Cost weights are operational heuristics from
measured family runtimes — not hyperparameters of the experiment.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Iterable

from quant.i04_cal.params import (
    B_WORLD,
    CANDIDATE_STRIDE,
    K_NEIGHBORS,
    QUERY_STRIDE,
    WINDOWS,
    WORLD_INDEX,
    CalConfig,
)
from quant.i04_cal.pipeline import config_hash, expected_cell_ids, geometry_specs

# Relative cost weights (seconds scale arbitrary; ratios matter).
# Seeded from HP microbench + Soft-DTW scaling; refined by runner microbench.
# Post Numba Soft-DTW: G1 (expensive strides 32/32) is cheap vs G2/G5 (core 8/4).
DEFAULT_FAMILY_WEIGHTS: dict[str, float] = {
    "G0": 3.0,
    "G1": 1.5,
    "G2": 40.0,
    "G3": 3.5,
    "G4": 12.0,
    "G5": 25.0,
    "G7": 5.0,
    "GORD": 4.0,
}

CANONICAL_GEOMETRIES = ("G0", "G1", "G2", "G3", "G4", "G5", "G7", "GORD")


def canonical_config() -> CalConfig:
    return CalConfig(
        B=B_WORLD,
        windows=WINDOWS,
        query_stride=QUERY_STRIDE,
        candidate_stride=CANDIDATE_STRIDE,
        k_neighbors=K_NEIGHBORS,
        worlds=tuple(WORLD_INDEX.keys()),
        geometries=CANONICAL_GEOMETRIES,
    )


def _family_of(cell_key: str) -> str:
    # cell_key: world|b=n|W=n|GID:variant
    geo = cell_key.rsplit("|", 1)[-1]
    return geo.split(":", 1)[0]


def cell_weight(cell_key: str, weights: dict[str, float] | None = None) -> float:
    w = weights or DEFAULT_FAMILY_WEIGHTS
    return float(w.get(_family_of(cell_key), 1.0))


def load_completed_keys(ckpt_or_results: Path) -> set[str]:
    """Load completed cell keys from a prior run directory or results.jsonl."""
    p = Path(ckpt_or_results)
    keys: set[str] = set()
    if p.is_dir():
        results = p / "results.jsonl"
        ckpt = p / "ckpt"
        if results.is_file():
            for line in results.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("status") == "OK" and row.get("cell_key"):
                    keys.add(row["cell_key"])
        elif ckpt.is_dir():
            for f in ckpt.glob("*.json"):
                row = json.loads(f.read_text(encoding="utf-8"))
                if row.get("status") == "OK" and row.get("cell_key"):
                    keys.add(row["cell_key"])
        return keys
    if p.is_file():
        for line in p.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("status") == "OK" and row.get("cell_key"):
                keys.add(row["cell_key"])
    return keys


def split_remaining(
    *,
    completed: Iterable[str] = (),
    machine_a: str = "ASUS",
    machine_b: str = "OPTIPLEX",
    capacity_a: float = 1.0,
    capacity_b: float = 1.0,
    weights: dict[str, float] | None = None,
) -> dict[str, object]:
    """Greedy cost-aware disjoint split of remaining canonical cells.

    capacity_* scales relative throughput (e.g. OptiPlex unknown → start 1.0,
    refine after microbench). Assignment is deterministic given identical inputs.
    """
    cfg = canonical_config()
    universe = expected_cell_ids(cfg)
    ch = config_hash(cfg)
    done = set(completed)
    remaining = [k for k in universe if k not in done]
    # Stable sort by weight desc then key for determinism
    remaining.sort(key=lambda k: (-cell_weight(k, weights), k))
    load_a = 0.0
    load_b = 0.0
    assign_a: list[str] = []
    assign_b: list[str] = []
    ca = max(float(capacity_a), 1e-9)
    cb = max(float(capacity_b), 1e-9)
    for key in remaining:
        w = cell_weight(key, weights)
        # Compare normalized load
        if (load_a / ca) <= (load_b / cb):
            assign_a.append(key)
            load_a += w
        else:
            assign_b.append(key)
            load_b += w
    assign_a.sort()
    assign_b.sort()
    overlap = set(assign_a) & set(assign_b)
    if overlap:
        raise RuntimeError("STOP: bi-machine overlap")
    if set(assign_a) | set(assign_b) != set(remaining):
        raise RuntimeError("STOP: bi-machine coverage incomplete")
    payload = {
        "schema": "I04-CAL-BIMACHINE-SPLIT-v1",
        "config_hash": ch,
        "universe_size": len(universe),
        "completed_excluded": len(done),
        "remaining": len(remaining),
        "machine_a": machine_a,
        "machine_b": machine_b,
        "capacity_a": ca,
        "capacity_b": cb,
        "weight_load_a": load_a,
        "weight_load_b": load_b,
        "n_a": len(assign_a),
        "n_b": len(assign_b),
        "weights": weights or DEFAULT_FAMILY_WEIGHTS,
        "allowlist_a_sha256": hashlib.sha256("\n".join(assign_a).encode()).hexdigest(),
        "allowlist_b_sha256": hashlib.sha256("\n".join(assign_b).encode()).hexdigest(),
        "note": "Operational split only — NO scientific retune — NO Kaggle",
    }
    return {
        "manifest": payload,
        "allowlist_a": assign_a,
        "allowlist_b": assign_b,
    }


def write_split(
    out_dir: Path,
    *,
    completed_run: Path | None = None,
    capacity_a: float = 1.0,
    capacity_b: float = 1.0,
) -> dict[str, object]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    done: set[str] = set()
    if completed_run is not None:
        done = load_completed_keys(completed_run)
    split = split_remaining(
        completed=done, capacity_a=capacity_a, capacity_b=capacity_b
    )
    (out_dir / "split_manifest.json").write_text(
        json.dumps(split["manifest"], indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / "allowlist_ASUS.txt").write_text(
        "\n".join(split["allowlist_a"]) + "\n", encoding="utf-8"
    )
    (out_dir / "allowlist_OPTIPLEX.txt").write_text(
        "\n".join(split["allowlist_b"]) + "\n", encoding="utf-8"
    )
    return split["manifest"]  # type: ignore[return-value]


def main(argv: list[str] | None = None) -> int:
    import argparse

    p = argparse.ArgumentParser(prog="python -m quant.i04_cal.bimachine")
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--exclude-completed", type=Path, default=None)
    p.add_argument("--capacity-asus", type=float, default=1.0)
    p.add_argument("--capacity-optiplex", type=float, default=1.0)
    args = p.parse_args(argv)
    man = write_split(
        args.out_dir,
        completed_run=args.exclude_completed,
        capacity_a=args.capacity_asus,
        capacity_b=args.capacity_optiplex,
    )
    print(json.dumps(man, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
