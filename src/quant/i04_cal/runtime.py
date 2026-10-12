"""CLI entry for I04-CAL."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from quant.i04_cal.params import (
    DEFAULT_CAL_CONFIG,
    CalConfig,
    CANDIDATE_STRIDE,
    K_NEIGHBORS,
    QUERY_STRIDE,
    WINDOWS,
)
from quant.i04_cal.geometries import iter_geometry_specs
from quant.i04_cal.pipeline import run_calibration


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m quant.i04_cal")
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--resume", action="store_true")
    p.add_argument("--canonical", action="store_true")
    p.add_argument(
        "--max-cells",
        type=int,
        default=None,
        help="TEST ONLY; requires I04_CAL_ALLOW_TEST_OVERRIDES=1",
    )
    p.add_argument("--worlds", type=str, default=None)
    p.add_argument("--geometries", type=str, default=None)
    p.add_argument("--B", type=int, default=None, help="Override B (TEST ONLY)")
    p.add_argument(
        "--max-runtime-hours",
        type=float,
        default=None,
        help="Operational wall-clock limit (hours). Stops assigning new cells before limit.",
    )
    p.add_argument(
        "--shutdown-margin-minutes",
        type=float,
        default=20.0,
        help="Minutes reserved before max-runtime for clean drain (default 20).",
    )
    p.add_argument(
        "--cell-list",
        type=Path,
        default=None,
        help="Path to newline-separated cell_key allowlist (bi-machine disjoint split).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.canonical and (args.worlds or args.geometries or args.B is not None or args.max_cells is not None):
        raise SystemExit("--canonical forbids test/subset overrides")
    if (args.worlds or args.geometries or args.max_cells is not None) and os.environ.get("I04_CAL_ALLOW_TEST_OVERRIDES") != "1" and not args.canonical:
        raise SystemExit("subset overrides require I04_CAL_ALLOW_TEST_OVERRIDES=1")
    if args.canonical and os.environ.get("I04_CAL_ALLOW_TEST_OVERRIDES") == "1":
        raise SystemExit("--canonical forbids test-only overrides")
    worlds = DEFAULT_CAL_CONFIG.worlds
    geos = tuple(dict.fromkeys(spec.geometry_id for spec in iter_geometry_specs())) if args.canonical else DEFAULT_CAL_CONFIG.geometries
    B = DEFAULT_CAL_CONFIG.B
    if args.worlds:
        worlds = tuple(x.strip() for x in args.worlds.split(",") if x.strip())
    if args.geometries:
        geos = tuple(x.strip() for x in args.geometries.split(",") if x.strip())
    if args.B is not None:
        if os.environ.get("I04_CAL_ALLOW_TEST_OVERRIDES") != "1":
            raise SystemExit("--B override requires I04_CAL_ALLOW_TEST_OVERRIDES=1")
        B = int(args.B)
    cfg = CalConfig(
        B=B,
        windows=WINDOWS,
        query_stride=QUERY_STRIDE,
        candidate_stride=CANDIDATE_STRIDE,
        k_neighbors=K_NEIGHBORS,
        workers=int(args.workers),
        worlds=worlds,
        geometries=geos,
    )
    allowlist = None
    if args.cell_list is not None:
        raw = Path(args.cell_list).read_bytes()
        if raw.startswith(b"\xef\xbb\xbf"):
            raw = raw[3:]
        text = raw.decode("utf-8")
        allowlist = {
            ln.strip().strip("\ufeff")
            for ln in text.splitlines()
            if ln.strip().strip("\ufeff") and not ln.strip().strip("\ufeff").startswith("#")
        }
    max_runtime_seconds = None
    if args.max_runtime_hours is not None:
        max_runtime_seconds = float(args.max_runtime_hours) * 3600.0
    man = run_calibration(
        args.out_dir,
        cfg,
        resume=bool(args.resume),
        max_cells=args.max_cells,
        use_cache=True,  # PERF-02: enable deterministic caching
        max_runtime_seconds=max_runtime_seconds,
        shutdown_margin_seconds=float(args.shutdown_margin_minutes) * 60.0,
        cell_allowlist=allowlist,
    )
    print(
        f"I04-CAL done status={man['status']} rows={man.get('n_rows')} "
        f"elapsed={man.get('elapsed_seconds')}s stopped_for_time={man.get('stopped_for_time')} "
        f"out={args.out_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
