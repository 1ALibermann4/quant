"""I04-CAL calibration runner with fail-closed checkpointing and deterministic parallelism."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
import traceback
import uuid
from datetime import datetime, timezone
from concurrent.futures import FIRST_COMPLETED, ProcessPoolExecutor, wait
from multiprocessing import get_context
from pathlib import Path
from typing import Any

import numpy as np

from quant.i04_cal.gates import compute_gates_for_spec
from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.params import DEFAULT_CAL_CONFIG, CalConfig, SEED_CONTRACT_VERSION, SPEC_ID
from quant.i04_cal.types import ExecStatus, GeometryStatus
from quant.i04_cal.worlds import generate_world
from quant.i04_cal.worker import execute_cal_cell


# Control numerical library threading to prevent oversubscription
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")


def _serialize_spec(spec: Any) -> dict[str, Any]:
    """Serialize GeometrySpec to dict for multiprocessing."""
    return {
        "geometry_id": spec.geometry_id,
        "variant_id": spec.variant_id,
        "params": spec.params,
        "status": spec.status.value if hasattr(spec.status, "value") else spec.status,
    }


def _git_head() -> str | None:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"], stderr=subprocess.DEVNULL, text=True
        ).strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def _git_dirty() -> bool:
    try:
        out = subprocess.check_output(
            ["git", "status", "--porcelain"], stderr=subprocess.DEVNULL, text=True
        )
        return bool(out.strip())
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return True


# Module-level world cache for multiprocessing
# Each process maintains its own cache since processes are isolated
_process_world_cache: dict[tuple[str, int], Any] = {}


def geometry_specs(cfg: CalConfig) -> list[Any]:
    return [
        spec for spec in iter_geometry_specs(include_hold=cfg.include_hold_geometries)
        if spec.geometry_id in cfg.geometries and spec.status != GeometryStatus.HOLD
    ]


def expected_cells(cfg: CalConfig) -> list[tuple[str, int, int, Any]]:
    specs = geometry_specs(cfg)
    return [
        (world, b, W, spec)
        for world in cfg.worlds for b in range(cfg.B)
        for W in cfg.windows for spec in specs
    ]


def expected_cell_ids(cfg: CalConfig) -> list[str]:
    return [cell_key(world, b, W, f"{spec.geometry_id}:{spec.variant_id}")
            for world, b, W, spec in expected_cells(cfg)]


def config_hash(cfg: CalConfig) -> str:
    identity = {
        "config": cfg.to_dict(),
        "geometry_specs": [_serialize_spec(spec) for spec in geometry_specs(cfg)],
        "seed_contract": SEED_CONTRACT_VERSION,
        "generator_oracle_version": SPEC_ID,
    }
    blob = json.dumps(identity, sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def cell_key(world: str, b: int, W: int, geo_variant: str) -> str:
    return f"{world}|b={b}|W={W}|{geo_variant}"


def _fsync_dir(path: Path) -> None:
    if os.name != "nt":
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def _atomic_json(path: Path, data: dict[str, Any]) -> None:
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("w", encoding="utf-8") as f:
        json.dump(data, f, sort_keys=True, default=str)
        f.write("\n")
        f.flush()
        os.fsync(f.fileno())
    os.replace(temp, path)
    _fsync_dir(path.parent)


def _checkpoint_path(ckpt: Path, key: str) -> Path:
    return ckpt / (hashlib.sha256(key.encode("utf-8")).hexdigest() + ".json")


def _record_hash(row: dict[str, Any]) -> str:
    payload = {k: v for k, v in row.items() if k != "record_hash"}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, default=str).encode()).hexdigest()


def _load_completed(ckpt: Path, expected: set[str], ch: str) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for path in ckpt.glob("*.json"):
        row = json.loads(path.read_text(encoding="utf-8"))
        key = row.get("cell_key")
        if key not in expected or path != _checkpoint_path(ckpt, key):
            raise RuntimeError(f"STOP: unexpected checkpoint {path}")
        if (row.get("config_hash") != ch or row.get("status") != "OK" or key in rows
                or row.get("record_hash") != _record_hash(row)):
            raise RuntimeError(f"STOP: invalid/duplicate checkpoint {path}")
        rows[key] = row
    return rows


def _rebuild_results(path: Path, keys: list[str], rows: dict[str, dict[str, Any]]) -> None:
    temp = path.with_suffix(".jsonl.tmp")
    with temp.open("w", encoding="utf-8") as fout:
        for key in keys:
            if key in rows:
                fout.write(json.dumps(rows[key], default=str) + "\n")
        fout.flush()
        os.fsync(fout.fileno())
    os.replace(temp, path)
    _fsync_dir(path.parent)


def run_calibration(
    out_dir: Path,
    cfg: CalConfig | None = None,
    *,
    resume: bool = False,
    max_cells: int | None = None,
    use_cache: bool = True,
) -> dict[str, Any]:
    """Execute I04-CAL. max_cells is TEST-ONLY (requires I04_CAL_ALLOW_TEST_OVERRIDES=1).

    use_cache: Enable deterministic caching of embeddings and distances
    across cells sharing (world, b, W, geometry) configuration.
    """

    cfg = cfg or DEFAULT_CAL_CONFIG
    if max_cells is not None and os.environ.get("I04_CAL_ALLOW_TEST_OVERRIDES") != "1":
        raise RuntimeError("max_cells requires I04_CAL_ALLOW_TEST_OVERRIDES=1")
    if cfg.workers < 1:
        raise ValueError("workers must be positive")

    # Clear caches if caching is disabled
    if not use_cache:
        from quant.i04_cal.cache import clear_caches
        clear_caches()

    all_cells = expected_cells(cfg)
    keys = expected_cell_ids(cfg)
    if len(keys) != len(set(keys)):
        raise RuntimeError("STOP: duplicate expected cell IDs")
    expected = set(keys)
    ch = config_hash(cfg)
    head = _git_head() or "unknown"
    out_dir = Path(out_dir)
    if (out_dir / "ABORTED_NONCANONICAL.txt").exists():
        raise RuntimeError("STOP: aborted noncanonical run cannot be resumed")
    manifest_path = out_dir / "manifest.json"
    results_path = out_dir / "results.jsonl"
    ckpt = out_dir / "ckpt"
    if resume:
        if not manifest_path.is_file() or not ckpt.is_dir():
            raise RuntimeError("STOP: missing checkpoint manifest")
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        if (manifest.get("config_hash") != ch or manifest.get("git_commit") != head
                or manifest.get("seed_contract") != SEED_CONTRACT_VERSION
                or manifest.get("generator_oracle_version") != SPEC_ID
                or manifest.get("geometry_specs") != [_serialize_spec(s) for s in geometry_specs(cfg)]
                or manifest.get("expected_cells") != len(keys)):
            raise RuntimeError("STOP: checkpoint scientific identity mismatch")
        rows = _load_completed(ckpt, expected, ch)
        _rebuild_results(results_path, keys, rows)
    else:
        if manifest_path.exists() or results_path.exists() or ckpt.exists():
            raise RuntimeError("STOP: run exists; pass resume=True or use fresh out_dir")
        out_dir.mkdir(parents=True, exist_ok=True)
        ckpt.mkdir()
        rows = {}
        manifest = {
            "schema": "I04-CAL-MANIFEST-v1",
            "run_id": str(uuid.uuid4()),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "spec_id": SPEC_ID,
            "git_commit": head,
            "git_dirty": _git_dirty(),
            "config": cfg.to_dict(),
            "config_hash": ch,
            "seed_contract": SEED_CONTRACT_VERSION,
            "generator_oracle_version": SPEC_ID,
            "geometry_specs": [_serialize_spec(s) for s in geometry_specs(cfg)],
            "environment": {
                "python": sys.version.replace("\n", " "),
                "platform": platform.platform(),
                "executable": sys.executable,
                "numpy": np.__version__,
            },
            "use_cache": use_cache,
            "workers": cfg.workers,
            "status": ExecStatus.INCOMPLETE.value,
            "note": "SYNTHETIC ONLY — NO MARKET DATA — NO GEOMETRY WINNER",
            "expected_cells": len(keys),
            "n_rows": 0,
        }
        _atomic_json(manifest_path, manifest)
        _rebuild_results(results_path, keys, rows)

    _atomic_json(out_dir / "progress.json", {
        "completed_cells": len(rows), "expected_cells": len(keys), "failed_cells": 0,
        "elapsed_seconds": 0,
    })
    cells = [c for c, key in zip(all_cells, keys) if key not in rows]
    if max_cells is not None:
        cells = cells[:int(max_cells)]
    t0 = time.perf_counter()
    failures: list[dict[str, Any]] = []

    def receive(key: str, row: dict[str, Any]) -> None:
        if row.get("cell_key") != key or key not in expected or key in rows:
            raise RuntimeError(f"STOP: worker returned invalid/duplicate cell {key}")
        row["config_hash"] = ch
        if row.get("status") != "OK":
            failures.append({"cell_key": key, "error": row.get("error"),
                             "traceback": row.get("traceback"), "status": row.get("status")})
            return
        row["record_hash"] = _record_hash(row)
        _atomic_json(_checkpoint_path(ckpt, key), row)
        with results_path.open("a", encoding="utf-8") as fout:
            fout.write(json.dumps(row, default=str) + "\n")
            fout.flush()
            os.fsync(fout.fileno())
        rows[key] = row
        manifest["n_rows"] = len(rows)
        _atomic_json(out_dir / "progress.json", {
            "completed_cells": len(rows), "expected_cells": len(keys),
            "failed_cells": len(failures), "elapsed_seconds": round(time.perf_counter() - t0, 3),
        })
        print(f"I04-CAL cells {len(rows)}/{len(keys)} last={key} status=OK", flush=True)

    # Phase 5: Deterministic multiprocessing
    if cfg.workers > 1 and cells:
        # Parallel execution with deterministic ordering
        # Each worker has its own process-local cache
        # Use ProcessPoolExecutor with spawn context for Windows compatibility
        ctx = get_context("spawn")
        with ProcessPoolExecutor(max_workers=cfg.workers, mp_context=ctx) as executor:
            pending: dict[Any, str] = {}
            iterator = iter(cells)

            def submit() -> bool:
                try:
                    world, b, W, spec = next(iterator)
                except StopIteration:
                    return False
                key = cell_key(world, b, W, f"{spec.geometry_id}:{spec.variant_id}")
                # Serialize spec to dict for multiprocessing
                pending[executor.submit(execute_cal_cell, world, b, W, _serialize_spec(spec))] = key
                return True

            for _ in range(min(len(cells), cfg.workers * 2)):
                submit()
            # Collect results as they complete
            while pending:
                done, _ = wait(pending, return_when=FIRST_COMPLETED)
                for future in done:
                    key = pending.pop(future)
                    try:
                        receive(key, future.result())
                    except Exception as e:
                        # Worker failure - fail closed
                        failures.append({"cell_key": key, "error": repr(e),
                                         "traceback": traceback.format_exc(), "status": "FAILED_TECHNICAL"})
                if not failures:
                    while len(pending) < cfg.workers * 2 and submit():
                        pass
    else:
        # Serial execution (original path)
        for world, b, W, spec in cells:
            # Use worker function for consistency
            key = cell_key(world, b, W, f"{spec.geometry_id}:{spec.variant_id}")
            try:
                receive(key, execute_cal_cell(world, b, W, _serialize_spec(spec)))
            except Exception as e:
                failures.append({"cell_key": key, "error": repr(e),
                                 "traceback": traceback.format_exc(), "status": "FAILED_TECHNICAL"})
            if failures:
                break

    if failures:
        _atomic_json(out_dir / "technical_failures.json", {"failures": failures})
        _atomic_json(out_dir / "progress.json", {
            "completed_cells": len(rows), "expected_cells": len(keys),
            "failed_cells": len(failures), "elapsed_seconds": round(time.perf_counter() - t0, 3),
        })
    durable = _load_completed(ckpt, expected, ch)
    if set(durable) != set(rows):
        raise RuntimeError("STOP: checkpoint/result disagreement")
    _rebuild_results(results_path, keys, durable)
    elapsed = time.perf_counter() - t0
    # Determine completeness: count expected without max_cells
    complete = max_cells is None and set(durable) == expected and not failures
    manifest["status"] = (ExecStatus.FAILED_TECHNICAL.value if failures else
                          ExecStatus.COMPLETE.value if complete else ExecStatus.INCOMPLETE.value)
    manifest["n_rows"] = len(durable)
    manifest["expected_cells"] = len(keys)
    manifest["elapsed_seconds"] = round(elapsed, 3)
    manifest["workers"] = cfg.workers
    manifest["technical_failures"] = len(failures)

    # Add cache statistics if caching was used
    if use_cache:
        from quant.i04_cal.cache import get_cache_stats
        manifest["cache_stats"] = get_cache_stats()

    _atomic_json(manifest_path, manifest)
    return manifest
