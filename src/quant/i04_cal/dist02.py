"""DIST-02: cost-aware deterministic batch queue for the remaining I04-CAL cells.

Operational infrastructure only. This module schedules cells that already
exist; it never changes cell content, seeds, expected results or I04-CAL rules.

Design: DIST-02 batches are persisted as DIST-01 shard manifests (schema
I04-CAL-DIST-v1, ``shard-NNNNN.json`` layout) extended with DIST-02 fields, so
the qualified DIST-01 primitives ``load_shard``, ``run_shard`` and ``merge``
are reused verbatim. Execution order inside a batch stays canonical
(``run_shard`` iterates ``expected_cells``); only batch composition is
cost-balanced.
"""

from __future__ import annotations

import argparse
import json
import math
import os
import statistics
import tarfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from quant.i04_cal.distributed import (
    canonical_config,
    digest,
    load_shard,
    merge,
    run_shard,
    scientific_identity,
)
from quant.i04_cal.params import CalConfig
from quant.i04_cal.pipeline import (
    _atomic_json,
    _checkpoint_path,
    _git_head,
    _load_completed,
    expected_cell_ids,
)

# Control numerical library threading (same contract as pipeline.py)
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")

DIST02_VERSION = "I04-CAL-DIST02-v1"
PLAN_SCHEMA = "I04-CAL-DIST02-PLAN-v1"
BATCH_SCHEMA = "I04-CAL-DIST02-BATCH-v1"
KAGGLE_WORKERS = 2  # frozen: 4 workers give no throughput gain and slow each cell
BLAS_VARS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS")

# Qualified scientific code head (same value DIST-01 records as source_code_head)
QUALIFIED_SOURCE_HEAD = "a268029440d757a3e283f80e1e33f09db5ab86a8"

# ---------------------------------------------------------------------------
# Cost model (operational scheduling estimate only -- no scientific meaning)
# ---------------------------------------------------------------------------
# Anchors: qualified measurements only.
#   G0   ~ 9.0 s  : mandate benchmark, Kaggle, S0a/b0/W20 ~8-9 s
#   G3   ~14.0 s  : qualified Windows refs, M=2/W20, 13.5-14.3 s
#   GORD ~14.6 s  : qualified Windows refs, D=3,tau=1/W60, 14.2-15.0 s
#   G1   ~104.0 s : Kaggle benchmark, gamma=0.1, ~103.7 s/cell at 2 workers
# Unmeasured families (G2, G4, G5, G7): conservative flat fallback of 60 s,
# between G0-class and G1-class per PERF-02 expectations.
# Window scaling: flat for all families (measured anchors W20 vs W60 are
# within noise: pair counts are ~constant in W) EXCEPT G1 whose soft-DTW
# distance is O(W^2) per pair -> documented quadratic W exponent.
COST_MODEL = {
    "version": "I04-CAL-COST-v1",
    "unit": "estimated_seconds",
    "family_anchor_s": {"G0": 9.0, "G3": 14.0, "GORD": 14.6, "G1": 104.0},
    "fallback_family_s": 60.0,
    "w2_exponent_families": ["G1"],
    "w_reference": 20,
}
COST_MODEL_VERSION = COST_MODEL["version"]


def parse_cell_id(cell_id: str) -> tuple[str, int, int, str, str]:
    """'S0a|b=0|W=20|G3:M=2' -> ('S0a', 0, 20, 'G3', 'M=2')."""
    world, b_part, w_part, variant = cell_id.split("|", 3)
    return world, int(b_part[2:]), int(w_part[2:]), variant.split(":", 1)[0], variant.split(":", 1)[1]


def estimate_cell_cost(cell_id: str, model: dict[str, Any] | None = None) -> float:
    model = model or COST_MODEL
    _, _, W, gid, _ = parse_cell_id(cell_id)
    base = model["family_anchor_s"].get(gid, model["fallback_family_s"])
    if gid in model["w2_exponent_families"]:
        base *= (W / model["w_reference"]) ** 2
    return float(base)


DEFAULT_PLANNER_CONFIG = {
    "planner_version": "I04-CAL-PLANNER-v1",
    "strategy": "lpt_desc_cost",
    "batch_target_cost_s": 1800.0,
    # optional explicit override: "batch_count": N
}

_SNAPSHOT_IDENTITY_FIELDS = (
    "run_id", "completed_local", "remaining_count", "remaining_ids_hash",
    "universe_count", "universe_hash", "config_hash", "seed_contract",
    "generator_oracle_version", "geometry_specs_hash",
)


def snapshot_identity_hash(snapshot: dict[str, Any]) -> str:
    return digest({k: snapshot.get(k) for k in _SNAPSHOT_IDENTITY_FIELDS})


def validate_snapshot(snapshot: dict[str, Any], cfg: CalConfig) -> tuple[list[str], dict[str, Any]]:
    """Fail-closed snapshot validation (D02-I1). Returns (canonical_remaining, identity)."""
    identity = scientific_identity(cfg)
    universe = expected_cell_ids(cfg)
    for field in ("config_hash", "universe_hash", "universe_count",
                  "geometry_specs_hash", "seed_contract", "generator_oracle_version"):
        if snapshot.get(field) != identity[field]:
            raise RuntimeError(f"STOP: snapshot {field} mismatch")
    remaining = snapshot.get("remaining_ids")
    if not isinstance(remaining, list) or not remaining:
        raise RuntimeError("STOP: snapshot has no remaining_ids")
    if len(remaining) != snapshot.get("remaining_count"):
        raise RuntimeError("STOP: snapshot remaining_count mismatch")
    canonical = [key for key in universe if key in set(remaining)]
    if canonical != remaining or len(canonical) != len(set(remaining)):
        raise RuntimeError("STOP: remaining_ids not canonical or duplicated/unknown")
    if digest(remaining) != snapshot.get("remaining_ids_hash"):
        raise RuntimeError("STOP: snapshot remaining_ids_hash mismatch")
    if snapshot.get("completed_local", -1) + len(remaining) != len(universe):
        raise RuntimeError("STOP: snapshot completed_local + remaining != universe")
    return canonical, identity


def plan_batches(snapshot: dict[str, Any], *, cfg: CalConfig | None = None,
                 planner_config: dict[str, Any] | None = None,
                 distribution_code_head: str | None = None,
                 created_at: str | None = None) -> dict[str, Any]:
    """Deterministic cost-aware batch plan over snapshot.remaining_ids (D02-I2/I4)."""
    cfg = cfg or canonical_config()
    pcfg = {**DEFAULT_PLANNER_CONFIG, **(planner_config or {})}
    remaining, identity = validate_snapshot(snapshot, cfg)
    universe = expected_cell_ids(cfg)
    canonical_index = {key: i for i, key in enumerate(universe)}

    costs = {key: estimate_cell_cost(key) for key in remaining}
    total_cost = sum(costs.values())
    if "batch_count" in pcfg:
        batch_count = int(pcfg["batch_count"])
        if batch_count < 1 or batch_count > len(remaining):
            raise ValueError("invalid batch_count")
    else:
        target = float(pcfg["batch_target_cost_s"])
        if target <= 0:
            raise ValueError("invalid batch_target_cost_s")
        batch_count = max(1, min(len(remaining), math.ceil(total_cost / target)))

    # LPT: descending estimated cost, canonical index tiebreak; assign to the
    # least-loaded batch (lowest index on ties). Fully deterministic.
    loads = [0.0] * batch_count
    assigned: list[list[str]] = [[] for _ in range(batch_count)]
    for key in sorted(remaining, key=lambda k: (-costs[k], canonical_index[k])):
        index = min(range(batch_count), key=lambda i: (loads[i], i))
        assigned[index].append(key)
        loads[index] += costs[key]

    planner_identity = {**pcfg, "cost_model": COST_MODEL}
    planner_hash = digest(planner_identity)
    snap_hash = snapshot_identity_hash(snapshot)
    requested_hash = digest(remaining)
    if requested_hash != snapshot["remaining_ids_hash"]:
        raise RuntimeError("STOP: canonical requested hash mismatch")
    code_head = distribution_code_head if distribution_code_head is not None else _git_head()

    common = {
        "schema": "I04-CAL-DIST-v1",            # DIST-01 shard compatibility
        "batch_schema": BATCH_SCHEMA,
        "dist_version": DIST02_VERSION,
        "run_id": f"{snapshot['run_id']}-DIST02",
        "created_at": created_at,
        "source_code_head": QUALIFIED_SOURCE_HEAD,
        "distribution_code_head": code_head,
        "snapshot_hash": snap_hash,
        "requested_ids_hash": requested_hash,
        "requested_count": len(remaining),
        "shard_count": batch_count,
        "workers_per_notebook": KAGGLE_WORKERS,
        "planner_hash": planner_hash,
        "planner": planner_identity,
        "cost_model_version": COST_MODEL_VERSION,
        **identity,
    }
    batches = []
    for index, ids in enumerate(assigned):
        ordered = [key for key in universe if key in set(ids)]  # canonical order
        batches.append({
            **common,
            "shard_id": f"batch-{index:05d}",
            "batch_id": f"BATCH-{index:04d}",
            "shard_index": index,
            "batch_index": index,
            "cell_ids": ordered,
            "cell_count": len(ordered),
            "cell_ids_hash": digest(ordered),
            "estimated_cost_s": round(loads[index], 3),
        })
    # plan.json content (batches live in shard-NNNNN.json files); plan_hash pins
    # every batch manifest byte-for-byte via batch_manifest_hashes.
    plan_doc = {
        **{k: v for k, v in common.items() if k != "schema"},
        "schema": PLAN_SCHEMA,
        "batch_count": batch_count,
        "ordered_batch_ids": [b["batch_id"] for b in batches],
        "batch_manifest_hashes": [digest(b) for b in batches],
        "total_estimated_cost_s": round(total_cost, 3),
    }
    plan_doc["plan_hash"] = digest({k: v for k, v in plan_doc.items()
                                    if k not in ("plan_hash", "created_at")})
    return {**plan_doc, "batches": batches}


def save_batch_plan(plan_dir: Path, plan: dict[str, Any]) -> None:
    """Persist plan as plan.json + shard-NNNNN.json (DIST-01 layout; merge-compatible)."""
    plan_dir = Path(plan_dir)
    if plan_dir.exists():
        raise RuntimeError("STOP: batch plan directory already exists")
    plan_dir.mkdir(parents=True)
    _atomic_json(plan_dir / "plan.json",
                 {k: v for k, v in plan.items() if k != "batches"})
    for batch in plan["batches"]:
        _atomic_json(plan_dir / f"shard-{batch['shard_index']:05d}.json", batch)


def _load_plan(plan_dir: Path, cfg: CalConfig) -> dict[str, Any]:
    """Load plan.json + shard-NNNNN.json, verify identity, plan hash and batch pins."""
    plan_dir = Path(plan_dir)
    plan = json.loads((plan_dir / "plan.json").read_text(encoding="utf-8"))
    identity = scientific_identity(cfg)
    for field, value in identity.items():
        if plan.get(field) != value:
            raise RuntimeError(f"STOP: plan {field} identity mismatch")
    if plan.get("plan_hash") != digest({k: v for k, v in plan.items()
                                        if k not in ("plan_hash", "created_at")}):
        raise RuntimeError("STOP: plan hash mismatch")
    pins = plan.get("batch_manifest_hashes")
    batches = []
    for index in range(plan["batch_count"]):
        batch = json.loads((plan_dir / f"shard-{index:05d}.json").read_text(encoding="utf-8"))
        if not isinstance(pins, list) or len(pins) != plan["batch_count"] or digest(batch) != pins[index]:
            raise RuntimeError(f"STOP: batch manifest pin mismatch shard-{index:05d}")
        if batch.get("batch_id") != plan["ordered_batch_ids"][index]:
            raise RuntimeError(f"STOP: batch order mismatch shard-{index:05d}")
        batches.append(batch)
    return {**plan, "batches": batches}


def load_batch(plan_dir: Path, batch_ref: str | int, cfg: CalConfig) -> tuple[dict[str, Any], Path]:
    """Resolve 'BATCH-0037'/index -> (validated batch manifest, shard file path)."""
    plan_dir = Path(plan_dir)
    plan = _load_plan(plan_dir, cfg)
    if isinstance(batch_ref, str):
        ref = batch_ref.strip().upper()
        try:
            index = int(ref.split("-", 1)[1]) if ref.startswith("BATCH-") else -1
        except ValueError:
            index = -1
    else:
        index = int(batch_ref)
    if index < 0 or index >= plan["batch_count"]:
        raise RuntimeError(f"STOP: unknown batch {batch_ref}")
    path = plan_dir / f"shard-{index:05d}.json"
    shard = load_shard(path, cfg)  # DIST-01 identity + canonical order checks
    if (shard.get("batch_id") != f"BATCH-{index:04d}" or shard.get("shard_index") != index
            or shard.get("shard_count") != plan["batch_count"]):
        raise RuntimeError("STOP: batch identity mismatch")
    if (digest(shard["cell_ids"]) != shard.get("cell_ids_hash")
            or shard.get("planner_hash") != plan.get("planner_hash")
            or shard.get("requested_ids_hash") != plan.get("requested_ids_hash")
            or shard.get("run_id") != plan.get("run_id")
            or shard.get("snapshot_hash") != plan.get("snapshot_hash")):
        raise RuntimeError("STOP: batch hash mismatch")
    return shard, path


def _check_blas_env() -> None:
    bad = {v: os.environ.get(v) for v in BLAS_VARS if os.environ.get(v) != "1"}
    if bad:
        raise RuntimeError(f"STOP: BLAS thread env must be 1: {bad}")


def run_batch(plan_dir: Path, batch_ref: str | int, out_dir: Path, *,
              workers: int = KAGGLE_WORKERS, cfg: CalConfig | None = None) -> dict[str, Any]:
    """Run one batch on this notebook via the qualified DIST-01 engine."""
    cfg = cfg or canonical_config(workers)
    if workers != KAGGLE_WORKERS or cfg.workers != KAGGLE_WORKERS:
        raise RuntimeError("STOP: Kaggle production requires exactly 2 workers")
    _check_blas_env()
    shard, shard_path = load_batch(plan_dir, batch_ref, cfg)
    head = _git_head()
    expected_head = shard.get("distribution_code_head")
    if head is not None and expected_head is not None and head != expected_head:
        raise RuntimeError(f"STOP: code identity mismatch HEAD={head} expected={expected_head}")
    out_dir = Path(out_dir)
    manifest = run_shard(shard_path, out_dir, workers, resume=out_dir.exists(), cfg=cfg)
    manifest = {**manifest, "batch_id": shard["batch_id"]}
    _atomic_json(out_dir / "batch_manifest.json", manifest)
    return manifest


def classify_batch_output(plan_dir: Path, batch: dict[str, Any], out_dir: Path,
                          cfg: CalConfig) -> tuple[str, str | None]:
    """Read-only classification: COMPLETE / INCOMPLETE / INVALID."""
    try:
        manifest = json.loads((Path(out_dir) / "manifest.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return "INVALID", f"manifest unreadable: {exc}"
    try:
        identity = scientific_identity(cfg)
        for field in ("run_id", "requested_ids_hash"):
            if manifest.get(field) != batch[field]:
                raise RuntimeError(f"identity {field} mismatch")
        for field in ("universe_hash", "config_hash", "seed_contract", "generator_oracle_version"):
            if manifest.get(field) != identity[field]:
                raise RuntimeError(f"identity {field} mismatch")
        if manifest.get("shard_id") != batch["shard_id"] or manifest.get("cell_ids") != batch["cell_ids"]:
            raise RuntimeError("batch binding mismatch")
        rows = _load_completed(Path(out_dir) / "ckpt", set(batch["cell_ids"]), identity["config_hash"])
        if manifest.get("status") == "COMPLETE" and len(rows) == batch["cell_count"]:
            return "COMPLETE", None
        if manifest.get("status") in ("INCOMPLETE", "FAILED_TECHNICAL"):
            return "INCOMPLETE", f"{len(rows)}/{batch['cell_count']} durable"
        return "INVALID", f"status {manifest.get('status')} vs {len(rows)}/{batch['cell_count']} durable"
    except Exception as exc:
        return "INVALID", str(exc)


def queue_status(plan_dir: Path, outputs_root: Path, *, cfg: CalConfig | None = None) -> dict[str, Any]:
    """Read-only queue status from repatriated batch outputs (no shared FS assumed).

    ``outputs_root`` contains one directory per executed batch (any name); each
    is bound to its batch via the embedded manifest shard_id.
    """
    cfg = cfg or canonical_config()
    plan = _load_plan(plan_dir, cfg)
    batches = {b["shard_id"]: b for b in plan["batches"]}
    found: dict[str, Path] = {}
    outputs_root = Path(outputs_root)
    if outputs_root.is_dir():
        for child in sorted(outputs_root.iterdir()):
            manifest = child / "manifest.json"
            if not manifest.is_file():
                continue
            try:
                sid = json.loads(manifest.read_text(encoding="utf-8")).get("shard_id")
            except json.JSONDecodeError:
                sid = None
            if sid in batches:
                if sid in found:
                    raise RuntimeError(f"STOP: duplicate output for {sid}")
                found[sid] = child
    status: dict[str, dict[str, Any]] = {}
    for batch in plan["batches"]:
        out = found.get(batch["shard_id"])
        if out is None:
            status[batch["batch_id"]] = {"status": "NOT_STARTED", "detail": None}
        else:
            cls, detail = classify_batch_output(plan_dir, batch, out, cfg)
            status[batch["batch_id"]] = {"status": cls, "detail": detail, "output_dir": str(out)}
    counts = {s: sum(1 for v in status.values() if v["status"] == s)
              for s in ("COMPLETE", "INCOMPLETE", "NOT_STARTED", "INVALID")}
    return {
        "schema": "I04-CAL-DIST02-STATUS-v1", "run_id": plan["run_id"],
        "batch_count": plan["batch_count"], "counts": counts,
        "next_available": [b["batch_id"] for b in plan["batches"]
                           if status[b["batch_id"]]["status"] == "NOT_STARTED"],
        "invalid": [b for b, v in status.items() if v["status"] == "INVALID"],
        "batches": status,
    }


def export_batch(out_dir: Path, dest_file: Path) -> Path:
    """Package a batch output directory as a self-contained tar.gz artifact."""
    out_dir, dest_file = Path(out_dir), Path(dest_file)
    manifest = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))
    if dest_file.exists():
        raise RuntimeError("STOP: export destination already exists")
    dest_file.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(dest_file, "w:gz") as tar:
        tar.add(out_dir, arcname=manifest.get("shard_id", out_dir.name))
    return dest_file


def validate_global(plan_dir: Path, outputs_root: Path, *, local_dir: Path | None = None,
                    merge_out: Path | None = None, cfg: CalConfig | None = None) -> dict[str, Any]:
    """Fail-closed global validation; calls DIST-01 merge only at exact completion."""
    cfg = cfg or canonical_config()
    plan = _load_plan(plan_dir, cfg)
    universe = set(expected_cell_ids(cfg))
    status = queue_status(plan_dir, outputs_root, cfg=cfg)
    if status["counts"]["INVALID"]:
        raise RuntimeError(f"STOP: invalid batch outputs {status['invalid']}")
    complete_dirs: list[Path] = []
    seen: dict[str, dict[str, Any]] = {}
    conflicts: list[str] = []
    local_cells = 0
    if local_dir is not None:
        local_dir = Path(local_dir)
        identity = scientific_identity(cfg)
        local_manifest = json.loads((local_dir / "manifest.json").read_text(encoding="utf-8"))
        if (local_manifest.get("git_commit") != plan["source_code_head"]
                or local_manifest.get("config_hash") != identity["config_hash"]
                or local_manifest.get("seed_contract") != identity["seed_contract"]
                or local_manifest.get("generator_oracle_version") != identity["generator_oracle_version"]
                or local_manifest.get("expected_cells") != len(universe)):
            raise RuntimeError("STOP: local scientific identity mismatch")
        local_rows = _load_completed(local_dir / "ckpt", universe, identity["config_hash"])
        local_cells = len(local_rows)
        seen.update(local_rows)
    for batch in plan["batches"]:
        entry = status["batches"][batch["batch_id"]]
        if entry["status"] != "COMPLETE":
            continue
        out = Path(entry["output_dir"])
        complete_dirs.append(out)
        rows = _load_completed(out / "ckpt", set(batch["cell_ids"]), plan["config_hash"])
        for key, row in rows.items():
            if key not in universe:
                raise RuntimeError(f"STOP: unexpected cell {key}")
            if key in seen:
                if seen[key] != row:
                    conflicts.append(key)
                else:
                    raise RuntimeError(f"STOP: duplicate cell {key}")
            else:
                seen[key] = row
    if conflicts:
        raise RuntimeError(f"STOP: conflicting duplicate cells {conflicts[:5]}")
    distributed_done = len(seen) - local_cells
    missing = [b["batch_id"] for b in plan["batches"]
               if status["batches"][b["batch_id"]]["status"] != "COMPLETE"]
    report = {
        "schema": "I04-CAL-DIST02-VALIDATION-v1", "run_id": plan["run_id"],
        "batch_count": plan["batch_count"],
        "batches_complete": plan["batch_count"] - len(missing),
        "batches_missing": missing,
        "distributed_cells": distributed_done,
        "expected_distributed": plan["requested_count"],
        "conflicts": 0,
        "complete": not missing and distributed_done == plan["requested_count"],
    }
    if merge_out is not None:
        if not report["complete"]:
            raise RuntimeError(f"STOP: merge refused, {len(missing)} batches not COMPLETE")
        merged = merge(Path(plan_dir), complete_dirs, Path(merge_out), cfg=cfg, local_dir=local_dir)
        report["merge"] = merged
    return report


def plan_diagnostics(plan: dict[str, Any]) -> dict[str, Any]:
    """Operational plan diagnostics (counts/costs only -- no scientific content)."""
    batches = plan["batches"]
    cells = [b["cell_count"] for b in batches]
    costs = [b["estimated_cost_s"] for b in batches]
    by_geo: dict[str, int] = {}
    by_world: dict[str, int] = {}
    by_w: dict[str, int] = {}
    for b in batches:
        for key in b["cell_ids"]:
            world, _, W, gid, _ = parse_cell_id(key)
            by_geo[gid] = by_geo.get(gid, 0) + 1
            by_world[world] = by_world.get(world, 0) + 1
            by_w[str(W)] = by_w.get(str(W), 0) + 1
    return {
        "batch_count": len(batches),
        "cells_per_batch": {"min": min(cells), "median": statistics.median(cells), "max": max(cells)},
        "estimated_cost_per_batch_s": {"min": round(min(costs), 1),
                                       "median": round(statistics.median(costs), 1),
                                       "max": round(max(costs), 1)},
        "cost_max_median_ratio": round(max(costs) / statistics.median(costs), 3),
        "total_estimated_cost_s": plan["total_estimated_cost_s"],
        "cells_by_geometry": dict(sorted(by_geo.items())),
        "cells_by_world": dict(sorted(by_world.items())),
        "cells_by_W": dict(sorted(by_w.items())),
        "plan_hash": plan["plan_hash"],
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m quant.i04_cal.dist02")
    commands = parser.add_subparsers(dest="command", required=True)

    plan = commands.add_parser("plan")
    plan.add_argument("--snapshot", type=Path, required=True)
    plan.add_argument("--out-dir", type=Path, required=True)
    plan.add_argument("--batch-target-cost-s", type=float)
    plan.add_argument("--batch-count", type=int)
    plan.add_argument("--code-head", type=str, default=None)
    plan.add_argument("--created-at", type=str, default=None)

    run = commands.add_parser("run-batch")
    run.add_argument("--plan-dir", type=Path, required=True)
    run.add_argument("--batch", required=True)
    run.add_argument("--out-dir", type=Path, required=True)
    run.add_argument("--workers", type=int, default=KAGGLE_WORKERS)

    status = commands.add_parser("status")
    status.add_argument("--plan-dir", type=Path, required=True)
    status.add_argument("--outputs-root", type=Path, required=True)

    export = commands.add_parser("export")
    export.add_argument("--out-dir", type=Path, required=True)
    export.add_argument("--dest", type=Path, required=True)

    validate = commands.add_parser("validate")
    validate.add_argument("--plan-dir", type=Path, required=True)
    validate.add_argument("--outputs-root", type=Path, required=True)
    validate.add_argument("--local-dir", type=Path)
    validate.add_argument("--merge-out", type=Path)

    diag = commands.add_parser("diagnostics")
    diag.add_argument("--plan-dir", type=Path, required=True)

    args = parser.parse_args(argv)
    if args.command == "plan":
        snapshot = json.loads(args.snapshot.read_text(encoding="utf-8"))
        pcfg = {}
        if args.batch_target_cost_s is not None:
            pcfg["batch_target_cost_s"] = args.batch_target_cost_s
        if args.batch_count is not None:
            pcfg["batch_count"] = args.batch_count
        result = plan_batches(snapshot, planner_config=pcfg or None,
                              distribution_code_head=args.code_head,
                              created_at=args.created_at)
        save_batch_plan(args.out_dir, result)
        print(json.dumps(plan_diagnostics(result), indent=2, sort_keys=True))
    elif args.command == "run-batch":
        manifest = run_batch(args.plan_dir, args.batch, args.out_dir, workers=args.workers)
        print(json.dumps({k: manifest[k] for k in
                          ("batch_id", "shard_id", "status", "completed_cells", "expected_cells")},
                         indent=2, sort_keys=True))
    elif args.command == "status":
        print(json.dumps(queue_status(args.plan_dir, args.outputs_root), indent=2, sort_keys=True))
    elif args.command == "export":
        print(export_batch(args.out_dir, args.dest))
    elif args.command == "validate":
        print(json.dumps(validate_global(args.plan_dir, args.outputs_root,
                                         local_dir=args.local_dir, merge_out=args.merge_out),
                         indent=2, sort_keys=True))
    else:
        print(json.dumps(plan_diagnostics(_load_plan(args.plan_dir, canonical_config())),
                         indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
