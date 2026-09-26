"""I04-CAL calibration runner with fail-closed checkpointing."""

from __future__ import annotations

import hashlib
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from quant.i04_cal.gates import compute_gates_for_spec
from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.params import DEFAULT_CAL_CONFIG, CalConfig, SPEC_ID, world_seed
from quant.i04_cal.types import ExecStatus, GeometryStatus
from quant.i04_cal.worlds import generate_world


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


def config_hash(cfg: CalConfig) -> str:
    blob = json.dumps(cfg.to_dict(), sort_keys=True).encode()
    return hashlib.sha256(blob).hexdigest()


def cell_key(world: str, b: int, W: int, geo_variant: str) -> str:
    return f"{world}|b={b}|W={W}|{geo_variant}"


def run_calibration(
    out_dir: Path,
    cfg: CalConfig | None = None,
    *,
    resume: bool = False,
    max_cells: int | None = None,
) -> dict[str, Any]:
    """Execute I04-CAL. max_cells is TEST-ONLY (requires I04_CAL_ALLOW_TEST_OVERRIDES=1)."""

    cfg = cfg or DEFAULT_CAL_CONFIG
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt = out_dir / "ckpt"
    ckpt.mkdir(exist_ok=True)
    results_path = out_dir / "results.jsonl"
    manifest_path = out_dir / "manifest.json"

    if max_cells is not None and os.environ.get("I04_CAL_ALLOW_TEST_OVERRIDES") != "1":
        raise RuntimeError("max_cells requires I04_CAL_ALLOW_TEST_OVERRIDES=1")

    ch = config_hash(cfg)
    head = _git_head() or "unknown"
    manifest = {
        "schema": "I04-CAL-MANIFEST-v1",
        "spec_id": SPEC_ID,
        "git_commit": head,
        "git_dirty": _git_dirty(),
        "config": cfg.to_dict(),
        "config_hash": ch,
        "environment": {
            "python": sys.version.replace("\n", " "),
            "platform": platform.platform(),
            "executable": sys.executable,
            "numpy": np.__version__,
        },
        "status": ExecStatus.INCOMPLETE.value,
        "note": "SYNTHETIC ONLY — NO MARKET DATA — NO GEOMETRY WINNER",
    }

    existing: set[str] = set()
    if resume and results_path.is_file():
        with results_path.open(encoding="utf-8") as f:
            for line in f:
                if not line.strip():
                    continue
                row = json.loads(line)
                if row.get("config_hash") != ch:
                    raise RuntimeError("STOP: checkpoint config_hash mismatch")
                existing.add(row["cell_key"])
    elif results_path.is_file() and not resume:
        raise RuntimeError("STOP: results exist; pass resume=True or use fresh out_dir")

    if not resume:
        manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
        results_path.write_text("", encoding="utf-8")

    specs = [
        s
        for s in iter_geometry_specs(include_hold=cfg.include_hold_geometries)
        if s.geometry_id in cfg.geometries and s.status != GeometryStatus.HOLD
    ]

    cells: list[tuple[str, int, int, Any]] = []
    for world in cfg.worlds:
        for b in range(cfg.B):
            for W in cfg.windows:
                for spec in specs:
                    key = cell_key(world, b, W, f"{spec.geometry_id}:{spec.variant_id}")
                    if key in existing:
                        continue
                    cells.append((world, b, W, spec))

    if max_cells is not None:
        cells = cells[: int(max_cells)]

    t0 = time.perf_counter()
    n_done = 0
    with results_path.open("a", encoding="utf-8") as fout:
        # Cache worlds per (world,b)
        world_cache: dict[tuple[str, int], Any] = {}
        for world, b, W, spec in cells:
            wb = world_cache.get((world, b))
            if wb is None:
                wb = generate_world(world, b)
                world_cache[(world, b)] = wb
            seed = world_seed(world, b) + 17 * W + hash(spec.variant_id) % 997
            try:
                gates = compute_gates_for_spec(wb, spec, W, seed=int(seed) & 0x7FFFFFFF)
                row = {
                    "cell_key": cell_key(
                        world, b, W, f"{spec.geometry_id}:{spec.variant_id}"
                    ),
                    "config_hash": ch,
                    "world_id": world,
                    "b": b,
                    "seed": wb.seed,
                    "W": W,
                    "world_status": wb.world_status.value,
                    "oracle_status": wb.oracle_status.value,
                    "oracle_meta": wb.oracle_meta,
                    "latent_notes": wb.notes,
                    "gates": gates,
                    "status": "OK",
                }
            except Exception as e:  # noqa: BLE001 — capture technical failure per cell
                row = {
                    "cell_key": cell_key(
                        world, b, W, f"{spec.geometry_id}:{spec.variant_id}"
                    ),
                    "config_hash": ch,
                    "world_id": world,
                    "b": b,
                    "W": W,
                    "status": "FAILED_TECHNICAL",
                    "error": repr(e),
                }
            fout.write(json.dumps(row, default=str) + "\n")
            fout.flush()
            n_done += 1
            if n_done % 1 == 0:
                print(
                    f"I04-CAL cells {n_done}/{len(cells)} last={row['cell_key']} "
                    f"status={row.get('status')}",
                    flush=True,
                )

    elapsed = time.perf_counter() - t0
    # Determine completeness: count expected without max_cells
    expected = (
        len(cfg.worlds) * cfg.B * len(cfg.windows) * len(specs)
        if max_cells is None
        else n_done
    )
    # recount file
    n_rows = sum(1 for _ in results_path.open(encoding="utf-8") if _.strip())
    complete = max_cells is None and n_rows >= expected
    manifest["status"] = (
        ExecStatus.COMPLETE.value if complete else ExecStatus.INCOMPLETE.value
    )
    manifest["n_rows"] = n_rows
    manifest["expected_cells"] = expected
    manifest["elapsed_seconds"] = round(elapsed, 3)
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    return manifest
