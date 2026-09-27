"""Independent deterministic CPU shards for the frozen I04-CAL cell universe."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import socket
import sys
import time
import traceback
from collections import defaultdict
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from datetime import datetime, timezone
from multiprocessing import get_context
from pathlib import Path
from typing import Any

from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.params import CalConfig, SEED_CONTRACT_VERSION, SPEC_ID
from quant.i04_cal.pipeline import (
    _atomic_json,
    _checkpoint_path,
    _git_head,
    _load_completed,
    _rebuild_results,
    _record_hash,
    _serialize_spec,
    cell_key,
    config_hash,
    expected_cell_ids,
    expected_cells,
    geometry_specs,
)
from quant.i04_cal.worker import execute_cal_cell


def canonical_config(workers: int = 1) -> CalConfig:
    return CalConfig(geometries=tuple(dict.fromkeys(s.geometry_id for s in iter_geometry_specs())), workers=workers)


def digest(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")).hexdigest()


def scientific_identity(cfg: CalConfig) -> dict[str, Any]:
    ids = expected_cell_ids(cfg)
    return {
        "config_hash": config_hash(cfg),
        "universe_hash": digest(ids),
        "universe_count": len(ids),
        "geometry_specs_hash": digest([_serialize_spec(spec) for spec in geometry_specs(cfg)]),
        "seed_contract": SEED_CONTRACT_VERSION,
        "generator_oracle_version": SPEC_ID,
    }


def snapshot_local_remaining(local_dir: Path, cfg: CalConfig) -> dict[str, Any]:
    identity = scientific_identity(cfg)
    universe = expected_cell_ids(cfg)
    manifest = json.loads((local_dir / "manifest.json").read_text(encoding="utf-8"))
    preflight = json.loads((local_dir / "preflight.json").read_text(encoding="utf-8"))
    if (manifest.get("git_commit") != preflight.get("qualified_code_head")
            or manifest.get("config_hash") != identity["config_hash"]
            or manifest.get("seed_contract") != identity["seed_contract"]
            or manifest.get("generator_oracle_version") != identity["generator_oracle_version"]
            or manifest.get("expected_cells") != len(universe)
            or preflight.get("expected_cell_ids_sha256") != identity["universe_hash"]
            or preflight.get("geometry_specs_sha256") != identity["geometry_specs_hash"]):
        raise RuntimeError("STOP: incompatible local canonical snapshot")
    completed = _load_completed(local_dir / "ckpt", set(universe), identity["config_hash"])
    remaining = [key for key in universe if key not in completed]
    return {
        "run_id": preflight["canonical_run_id"], "snapshot_at": datetime.now(timezone.utc).isoformat(),
        "completed_local": len(completed), "remaining_count": len(remaining),
        "remaining_ids_hash": digest(remaining), "remaining_ids": remaining, **identity,
    }


def _check_identity(record: dict[str, Any], identity: dict[str, Any]) -> None:
    if any(record.get(name) != value for name, value in identity.items()):
        raise RuntimeError("STOP: distributed scientific identity mismatch")


def _cell_group(cell_id: str) -> tuple[str, str, str]:
    world, realization, window, variant = cell_id.split("|", 3)
    return (variant, window, world)


def plan_shards(cfg: CalConfig, run_id: str, shard_count: int, requested_ids: list[str]) -> dict[str, Any]:
    universe = expected_cell_ids(cfg)
    valid = set(universe)
    selected = set(requested_ids)
    if (shard_count < 1 or shard_count > len(selected) or not run_id
            or len(selected) != len(requested_ids) or not selected.issubset(valid)):
        raise ValueError("invalid shard count, run ID, duplicate or unexpected requested cell")
    groups: dict[tuple[str, str, str], list[str]] = defaultdict(list)
    for key in universe:
        if key in selected:
            groups[_cell_group(key)].append(key)
    assignments: dict[str, int] = {}
    loads = [0] * shard_count
    for group in sorted(groups):
        start = int(digest(group)[:8], 16) % shard_count
        for key in groups[group]:
            index = min(range(shard_count), key=lambda i: (loads[i], (i - start) % shard_count))
            assignments[key] = index
            loads[index] += 1
    shards = [[key for key in universe if assignments.get(key) == index] for index in range(shard_count)]
    identity = scientific_identity(cfg)
    created_at = datetime.now(timezone.utc).isoformat()
    common = {
        "schema": "I04-CAL-DIST-v1", "run_id": run_id, "created_at": created_at,
        "source_code_head": "a268029440d757a3e283f80e1e33f09db5ab86a8",
        "requested_ids_hash": digest([key for key in universe if key in selected]),
        "requested_count": len(selected), "shard_count": shard_count,
        **identity,
    }
    return {
        **common,
        "shards": [
            {**common, "shard_id": f"shard-{i:05d}", "shard_index": i,
             "cell_ids": ids, "cell_count": len(ids)}
            for i, ids in enumerate(shards)
        ],
    }


def save_plan(path: Path, plan: dict[str, Any]) -> None:
    if path.exists():
        raise RuntimeError("STOP: plan directory already exists")
    path.mkdir(parents=True)
    _atomic_json(path / "plan.json", {key: value for key, value in plan.items() if key != "shards"})
    for shard in plan["shards"]:
        _atomic_json(path / f"{shard['shard_id']}.json", shard)


def load_shard(path: Path, cfg: CalConfig) -> dict[str, Any]:
    shard = json.loads(path.read_text(encoding="utf-8"))
    _check_identity(shard, scientific_identity(cfg))
    universe = expected_cell_ids(cfg)
    allowed = set(universe)
    ids = shard.get("cell_ids")
    if (not isinstance(ids, list) or not ids or len(ids) != len(set(ids))
            or not set(ids).issubset(allowed) or shard.get("cell_count") != len(ids)
            or shard.get("shard_index", -1) not in range(shard.get("shard_count", 0))):
        raise RuntimeError("STOP: invalid shard IDs")
    if [key for key in universe if key in set(ids)] != ids:
        raise RuntimeError("STOP: shard IDs are not in canonical order")
    return shard


def execute_timed_cell(world: str, b: int, W: int, spec: dict[str, Any], shard_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = datetime.now(timezone.utc).isoformat()
    clock = time.perf_counter()
    row = execute_cal_cell(world, b, W, spec)
    timing = {
        "cell_id": row["cell_key"], "shard_id": shard_id, "host_id": socket.gethostname(),
        "worker_pid": os.getpid(), "started_at": start,
        "finished_at": datetime.now(timezone.utc).isoformat(),
        "wall_duration_s": time.perf_counter() - clock,
        "execution_status": row["status"],
    }
    return row, timing


def run_shard(shard_path: Path, out_dir: Path, workers: int, *, resume: bool = False, cfg: CalConfig | None = None) -> dict[str, Any]:
    cfg = cfg or canonical_config(workers)
    if workers < 1 or cfg.workers != workers:
        raise ValueError("worker count mismatch")
    shard = load_shard(shard_path, cfg)
    keys = shard["cell_ids"]
    expected = set(keys)
    ch = config_hash(cfg)
    out_dir = Path(out_dir)
    ckpt = out_dir / "ckpt"
    timing_dir = out_dir / "timings"
    manifest_path = out_dir / "manifest.json"
    results_path = out_dir / "results.jsonl"
    code_head = _git_head()
    if resume:
        if not manifest_path.is_file() or not ckpt.is_dir() or not timing_dir.is_dir():
            raise RuntimeError("STOP: missing shard checkpoint")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        for field in ("run_id", "shard_id", "universe_hash", "requested_ids_hash", "config_hash", "seed_contract", "generator_oracle_version"):
            if manifest.get(field) != shard.get(field):
                raise RuntimeError(f"STOP: shard resume {field} mismatch")
        if manifest.get("code_head") != code_head or manifest.get("cell_ids") != keys:
            raise RuntimeError("STOP: shard resume code/cells mismatch")
        rows = _load_completed(ckpt, expected, ch)
        for key in rows:
            if not _checkpoint_path(timing_dir, key).is_file():
                raise RuntimeError("STOP: missing completed-cell telemetry")
        _rebuild_results(results_path, keys, rows)
    else:
        if out_dir.exists():
            raise RuntimeError("STOP: shard output already exists")
        out_dir.mkdir(parents=True)
        ckpt.mkdir()
        timing_dir.mkdir()
        rows = {}
        manifest = {**{field: shard[field] for field in (
            "run_id", "shard_id", "universe_hash", "requested_ids_hash", "config_hash", "seed_contract", "generator_oracle_version"
        )}, "schema": "I04-CAL-SHARD-RUN-v1", "code_head": code_head,
            "cell_ids": keys, "expected_cells": len(keys), "workers": workers,
            "status": "INCOMPLETE", "completed_cells": 0,
            "environment": {"python": sys.version.split()[0], "numpy": __import__("numpy").__version__,
                            "platform": platform.platform()},
        }
        _atomic_json(manifest_path, manifest)
        _rebuild_results(results_path, keys, rows)
    _atomic_json(out_dir / "progress.json", {"durable_completed": len(rows), "expected": len(keys), "failures": 0})
    cells = [cell for cell in expected_cells(cfg) if cell_key(cell[0], cell[1], cell[2], f"{cell[3].geometry_id}:{cell[3].variant_id}") in expected - rows.keys()]
    failures: list[dict[str, Any]] = []

    def persist(key: str, result: tuple[dict[str, Any], dict[str, Any]]) -> None:
        row, timing = result
        if key not in expected or key in rows or row.get("cell_key") != key or timing.get("cell_id") != key or timing.get("shard_id") != shard["shard_id"]:
            raise RuntimeError("STOP: invalid returned shard cell")
        if row.get("status") != "OK":
            failures.append({"cell_id": key, "error": row.get("error"), "traceback": row.get("traceback")})
            return
        row["config_hash"] = ch
        row["record_hash"] = _record_hash(row)
        _atomic_json(_checkpoint_path(timing_dir, key), timing)
        _atomic_json(_checkpoint_path(ckpt, key), row)
        with results_path.open("a", encoding="utf-8") as fout:
            fout.write(json.dumps(row, default=str) + "\n")
            fout.flush()
            os.fsync(fout.fileno())
        rows[key] = row
        _atomic_json(out_dir / "progress.json", {"durable_completed": len(rows), "expected": len(keys), "failures": len(failures)})
        print(f"DIST-01 {shard['shard_id']} {len(rows)}/{len(keys)}", flush=True)

    if workers > 1 and cells:
        with ProcessPoolExecutor(max_workers=workers, mp_context=get_context("spawn")) as pool:
            iterator = iter(cells)
            pending: dict[Any, str] = {}

            def submit() -> bool:
                try:
                    world, b, W, spec = next(iterator)
                except StopIteration:
                    return False
                key = cell_key(world, b, W, f"{spec.geometry_id}:{spec.variant_id}")
                pending[pool.submit(execute_timed_cell, world, b, W, _serialize_spec(spec), shard["shard_id"])] = key
                return True

            for _ in range(min(len(cells), workers * 2)):
                submit()
            while pending:
                done, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in done:
                    key = pending.pop(future)
                    try:
                        persist(key, future.result())
                    except Exception as exc:
                        failures.append({"cell_id": key, "error": repr(exc), "traceback": traceback.format_exc()})
                if not failures:
                    while len(pending) < workers * 2 and submit():
                        pass
    else:
        for world, b, W, spec in cells:
            key = cell_key(world, b, W, f"{spec.geometry_id}:{spec.variant_id}")
            try:
                persist(key, execute_timed_cell(world, b, W, _serialize_spec(spec), shard["shard_id"]))
            except Exception as exc:
                failures.append({"cell_id": key, "error": repr(exc), "traceback": traceback.format_exc()})
            if failures:
                break
    if failures:
        _atomic_json(out_dir / "technical_failures.json", {"failures": failures})
    durable = _load_completed(ckpt, expected, ch)
    if set(durable) != set(rows):
        raise RuntimeError("STOP: inconsistent shard checkpoints")
    _rebuild_results(results_path, keys, durable)
    manifest["completed_cells"] = len(durable)
    manifest["status"] = "FAILED_TECHNICAL" if failures else "COMPLETE" if set(durable) == expected else "INCOMPLETE"
    _atomic_json(manifest_path, manifest)
    return manifest


def merge(plan_dir: Path, shard_dirs: list[Path], output: Path, *, cfg: CalConfig | None = None,
          local_dir: Path | None = None, repro_dirs: list[Path] | None = None,
          allow_identical_duplicates: bool = False) -> dict[str, Any]:
    cfg = cfg or canonical_config()
    plan = json.loads((plan_dir / "plan.json").read_text(encoding="utf-8"))
    identity = scientific_identity(cfg)
    _check_identity(plan, identity)
    requested: list[str] = []
    planned: dict[str, dict[str, Any]] = {}
    for index in range(plan["shard_count"]):
        shard = load_shard(plan_dir / f"shard-{index:05d}.json", cfg)
        if shard["run_id"] != plan["run_id"] or shard["requested_ids_hash"] != plan["requested_ids_hash"]:
            raise RuntimeError("STOP: wrong shard plan")
        if shard["shard_id"] in planned:
            raise RuntimeError("STOP: duplicate shard identity")
        planned[shard["shard_id"]] = shard
        requested.extend(shard["cell_ids"])
    universe = expected_cell_ids(cfg)
    selected = set(requested)
    if len(selected) != len(requested) or len(selected) != plan["requested_count"] or digest([key for key in universe if key in selected]) != plan["requested_ids_hash"]:
        raise RuntimeError("STOP: missing/overlapping plan cells")
    seen: dict[str, dict[str, Any]] = {}
    duplicates = 0

    def add(rows: dict[str, dict[str, Any]]) -> None:
        nonlocal duplicates
        for key, row in rows.items():
            if key in seen:
                if not allow_identical_duplicates or row != seen[key]:
                    raise RuntimeError(f"STOP: duplicate/conflicting cell {key}")
                duplicates += 1
            else:
                seen[key] = row

    if local_dir is not None:
        local_manifest = json.loads((local_dir / "manifest.json").read_text(encoding="utf-8"))
        if (local_manifest.get("git_commit") != plan["source_code_head"]
                or local_manifest.get("config_hash") != identity["config_hash"]
                or local_manifest.get("seed_contract") != identity["seed_contract"]
                or local_manifest.get("generator_oracle_version") != identity["generator_oracle_version"]
                or local_manifest.get("expected_cells") != len(universe)):
            raise RuntimeError("STOP: local scientific identity mismatch")
        add(_load_completed(local_dir / "ckpt", set(universe), identity["config_hash"]))
    if len(set(str(path.resolve()) for path in shard_dirs)) != len(shard_dirs):
        raise RuntimeError("STOP: duplicate shard output directory")
    received: set[str] = set()
    for path in shard_dirs:
        manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        shard_id = manifest.get("shard_id")
        if shard_id not in planned or shard_id in received:
            raise RuntimeError("STOP: missing/unexpected shard")
        shard = planned[shard_id]
        if (manifest.get("run_id") != plan["run_id"] or manifest.get("status") != "COMPLETE"
                or manifest.get("cell_ids") != shard["cell_ids"]):
            raise RuntimeError("STOP: incomplete/wrong shard run")
        _check_identity(manifest, {k: identity[k] for k in ("config_hash", "universe_hash", "seed_contract", "generator_oracle_version")})
        add(_load_completed(path / "ckpt", set(shard["cell_ids"]), identity["config_hash"]))
        received.add(shard_id)
    if received != set(planned) or set(seen) != (set(universe) if local_dir is not None else selected):
        raise RuntimeError("STOP: missing/unexpected merged cells")
    for path in repro_dirs or []:
        manifest = json.loads((path / "manifest.json").read_text(encoding="utf-8"))
        shard_id = manifest.get("shard_id")
        if shard_id not in planned or manifest.get("cell_ids") != planned[shard_id]["cell_ids"]:
            raise RuntimeError("STOP: wrong reproducibility shard")
        _check_identity(manifest, {k: identity[k] for k in ("config_hash", "universe_hash", "seed_contract", "generator_oracle_version")})
        add(_load_completed(path / "ckpt", set(manifest["cell_ids"]), identity["config_hash"]))
    if set(seen) != (set(universe) if local_dir is not None else selected):
        raise RuntimeError("STOP: missing/unexpected merged cells")
    if output.exists():
        raise RuntimeError("STOP: merged output already exists")
    output.mkdir(parents=True)
    order = universe if local_dir is not None else [key for key in universe if key in selected]
    _rebuild_results(output / "results.jsonl", order, seen)
    result = {**identity, "schema": "I04-CAL-DIST-MERGE-v1", "run_id": plan["run_id"],
              "status": "COMPLETE", "requested_cells": len(selected), "completed_cells": len(seen),
              "identical_duplicates": duplicates, "source_shards": sorted(received),
              "local_source": str(local_dir) if local_dir is not None else None}
    _atomic_json(output / "manifest.json", result)
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="python -m quant.i04_cal.distributed")
    commands = parser.add_subparsers(dest="command", required=True)
    snapshot = commands.add_parser("snapshot")
    snapshot.add_argument("--local-dir", type=Path, required=True)
    snapshot.add_argument("--out-file", type=Path, required=True)
    plan = commands.add_parser("plan")
    plan.add_argument("--out-dir", type=Path, required=True)
    plan.add_argument("--run-id", required=True)
    plan.add_argument("--shard-count", type=int, required=True)
    plan.add_argument("--cell-manifest", type=Path, required=True)
    plan.add_argument("--handoff", type=Path)
    plan.add_argument("--qualification", action="store_true")
    execute = commands.add_parser("execute")
    execute.add_argument("--cell-manifest", type=Path, required=True)
    execute.add_argument("--out-dir", type=Path, required=True)
    execute.add_argument("--shard-index", type=int)
    execute.add_argument("--workers", type=int, default=1)
    execute.add_argument("--resume", action="store_true")
    merging = commands.add_parser("merge")
    merging.add_argument("--plan-dir", type=Path, required=True)
    merging.add_argument("--shard-results", action="append", type=Path, required=True)
    merging.add_argument("--local-dir", type=Path)
    merging.add_argument("--out-dir", type=Path, required=True)
    args = parser.parse_args(argv)
    if args.command == "snapshot":
        if args.out_file.exists():
            raise RuntimeError("STOP: snapshot already exists")
        _atomic_json(args.out_file, snapshot_local_remaining(args.local_dir, canonical_config()))
    elif args.command == "plan":
        source = json.loads(args.cell_manifest.read_text(encoding="utf-8"))
        if isinstance(source, dict):
            _check_identity(source, scientific_identity(canonical_config()))
            if args.handoff is None:
                raise RuntimeError("STOP: local scheduler handoff required before distributed dispatch")
            handoff = json.loads(args.handoff.read_text(encoding="utf-8"))
            if (handoff.get("run_id") != source.get("run_id")
                    or handoff.get("local_scheduler_quiesced") is not True
                    or handoff.get("snapshot_hash") != source.get("remaining_ids_hash")):
                raise RuntimeError("STOP: unverified local scheduler handoff")
            selected = source["remaining_ids"]
            if len(selected) != source["remaining_count"] or digest(selected) != source["remaining_ids_hash"]:
                raise RuntimeError("STOP: corrupted completion snapshot")
        elif args.qualification and isinstance(source, list) and len(source) <= 64:
            selected = source
        else:
            raise RuntimeError("STOP: production plan requires validated local snapshot and handoff")
        save_plan(args.out_dir, plan_shards(canonical_config(), args.run_id, args.shard_count, selected))
    elif args.command == "execute":
        if args.shard_index is not None and load_shard(args.cell_manifest, canonical_config(args.workers))["shard_index"] != args.shard_index:
            raise RuntimeError("STOP: shard index mismatch")
        run_shard(args.cell_manifest, args.out_dir, args.workers, resume=args.resume)
    else:
        merge(args.plan_dir, args.shard_results, args.out_dir, local_dir=args.local_dir)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
