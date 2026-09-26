"""CLI entry for I04-CAL."""

from __future__ import annotations

import argparse
import os
from pathlib import Path

from quant.i04_cal.params import DEFAULT_CAL_CONFIG, CalConfig, WINDOWS, K_NEIGHBORS
from quant.i04_cal.pipeline import run_calibration


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="python -m quant.i04_cal")
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--workers", type=int, default=1)
    p.add_argument("--resume", action="store_true")
    p.add_argument(
        "--max-cells",
        type=int,
        default=None,
        help="TEST ONLY; requires I04_CAL_ALLOW_TEST_OVERRIDES=1",
    )
    p.add_argument("--worlds", type=str, default=None)
    p.add_argument("--geometries", type=str, default=None)
    p.add_argument("--B", type=int, default=None, help="Override B (TEST ONLY)")
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    worlds = DEFAULT_CAL_CONFIG.worlds
    geos = DEFAULT_CAL_CONFIG.geometries
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
        k_neighbors=K_NEIGHBORS,
        workers=int(args.workers),
        worlds=worlds,
        geometries=geos,
    )
    man = run_calibration(
        args.out_dir, cfg, resume=bool(args.resume), max_cells=args.max_cells
    )
    print(
        f"I04-CAL done status={man['status']} rows={man.get('n_rows')} "
        f"elapsed={man.get('elapsed_seconds')}s out={args.out_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
