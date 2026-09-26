"""I03 operational runtime — canonical operator entry for HAT / future E01.

Scientific constants are frozen (I03-PREREG-v0.1). CLI exposes only operational
paths. No tuning of W, M, tau, K, P, B, alpha, nulls.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

from quant.i03.fixture_hat import fixture_sha256, load_fixture, write_fixture
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis
from quant.i03.report import render_report

PREREG_ID = "I03-PREREG-v0.1"


def _git_head() -> str | None:
    try:
        out = subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            stderr=subprocess.DEVNULL,
            text=True,
        )
        return out.strip()
    except (subprocess.CalledProcessError, FileNotFoundError, OSError):
        return None


def _json_default(obj: Any) -> Any:
    if isinstance(obj, (np.floating, np.integer)):
        return obj.item()
    if isinstance(obj, np.ndarray):
        return obj.tolist()
    raise TypeError(f"not JSON serializable: {type(obj)}")


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m quant.i03",
        description="I03 structural recurrence runtime (frozen prereg).",
    )
    p.add_argument(
        "--mode",
        choices=("hat", "e01", "produce-canonical"),
        required=True,
        help=(
            "hat=synthetic HAT; e01=exploratory market; "
            "produce-canonical=Amendment B local producer (no science)."
        ),
    )
    p.add_argument(
        "--fixture-dir",
        type=Path,
        default=None,
        help="HAT: directory containing fixture_v1.npy + fixture_v1.meta.json",
    )
    p.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("data/exploratory"),
        help="E01 CSV path / produce-canonical: authorized snapshot directory",
    )
    p.add_argument(
        "--canonical-dir",
        type=Path,
        default=None,
        help="E01 Amendment B: directory with returns.npy + manifest.json",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        required=True,
        help="Output directory for artifact.json / report.md / canonical artifact",
    )
    p.add_argument(
        "--prepare-fixture",
        action="store_true",
        help="HAT: write/overwrite the synthetic HAT fixture into --fixture-dir",
    )
    p.add_argument(
        "--workers",
        type=int,
        default=1,
        help=(
            "Operational process workers for surrogate batteries (PERF-01 Phase 1B). "
            "Not a scientific parameter. Default 1 = serial reference."
        ),
    )
    p.add_argument(
        "--checkpoint-dir",
        type=Path,
        default=None,
        help=(
            "PERF-01 Phase 1C: directory for deterministic per-b checkpoints. "
            "Operational only. Empty/NEW required unless --resume."
        ),
    )
    p.add_argument(
        "--resume",
        action="store_true",
        help=(
            "PERF-01 Phase 1C: resume a compatible incomplete checkpoint run. "
            "Fail-closed if identity mismatches."
        ),
    )
    return p


def _run_hat(args: argparse.Namespace) -> int:
    if args.fixture_dir is None:
        raise SystemExit("--fixture-dir is required for --mode hat")
    fixture_dir: Path = args.fixture_dir
    out_dir: Path = args.out_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.prepare_fixture:
        meta = write_fixture(fixture_dir)
        print(f"Prepared fixture {meta['fixture_id']} hash={meta['sha256']}")

    returns, meta = load_fixture(fixture_dir)
    digest = fixture_sha256(returns)
    assert digest == meta["sha256"]

    cfg = DEFAULT_CONFIG
    workers = int(getattr(args, "workers", 1))
    if workers < 1:
        raise SystemExit("--workers must be >= 1")
    ckpt = getattr(args, "checkpoint_dir", None)
    resume = bool(getattr(args, "resume", False))
    if resume and ckpt is None:
        raise SystemExit("--resume requires --checkpoint-dir")
    t0 = time.perf_counter()
    # Official HAT: full frozen B=999, full locality — no scientific overrides
    result = run_structural_analysis(
        returns,
        cfg,
        workers=workers,
        checkpoint_dir=ckpt,
        resume=resume,
    )
    elapsed = time.perf_counter() - t0

    impl = _git_head() or "unknown"
    timing = {
        "total_seconds": round(elapsed, 3),
        "workers_requested": workers,
        "workers_used": result.workers_used,
        "logical_cpus": os.cpu_count(),
        "checkpoint_dir": str(ckpt) if ckpt else None,
        "resume": resume,
        "note": "engineering observation only; no scientific performance gate",
    }
    artifact = artifact_dict(
        result,
        input_hash=digest,
        implementation_id=impl,
        mode="SYNTHETIC_HAT",
        timing=timing,
        fixture_id=meta["fixture_id"],
    )
    artifact["environment"] = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "executable": sys.executable,
    }
    artifact["operator"] = {
        "command": "python -m quant.i03 --mode hat ...",
        "prereg_id": PREREG_ID,
        "B_N4": cfg.B_N4,
        "B_N3": cfg.B_N3,
        "test_overrides_enabled": False,
    }

    art_path = out_dir / "artifact.json"
    rep_path = out_dir / "report.md"
    art_path.write_text(
        json.dumps(artifact, indent=2, default=_json_default) + "\n",
        encoding="utf-8",
    )
    rep_path.write_text(render_report(artifact), encoding="utf-8")

    env_path = out_dir / "environment.json"
    env_path.write_text(
        json.dumps(
            {
                **artifact["environment"],
                "elapsed_seconds": elapsed,
                "fixture": meta,
                "exit": 0,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"I03 HAT complete: verdict={result.verdict.label.value} "
        f"elapsed={elapsed:.1f}s out={out_dir}"
    )
    return 0


def main(argv: list[str] | None = None) -> int:
    # Production path must not inherit test overrides
    if os.environ.get("I03_ALLOW_TEST_OVERRIDES") == "1":
        print(
            "WARNING: I03_ALLOW_TEST_OVERRIDES=1 is set; production path clears it.",
            file=sys.stderr,
        )
        del os.environ["I03_ALLOW_TEST_OVERRIDES"]

    args = build_parser().parse_args(argv)
    if args.mode == "produce-canonical":
        from quant.i03.canonical_input import (
            CanonicalInputError,
            produce_authorized_canonical,
        )

        try:
            man = produce_authorized_canonical(
                cache_dir=args.cache_dir, out_dir=args.out_dir
            )
        except CanonicalInputError as e:
            print(f"STOP: canonical produce failed: {e}", file=sys.stderr)
            return 2
        print(
            f"I03 canonical input written: payload={man['return_payload_sha256']} "
            f"out={args.out_dir}"
        )
        return 0
    if args.mode == "e01":
        from quant.i03.e01 import run_e01

        workers = int(getattr(args, "workers", 1))
        if workers < 1:
            raise SystemExit("--workers must be >= 1")
        ckpt = getattr(args, "checkpoint_dir", None)
        resume = bool(getattr(args, "resume", False))
        if resume and ckpt is None:
            raise SystemExit("--resume requires --checkpoint-dir")
        common = {
            "out_dir": args.out_dir,
            "workers": workers,
            "checkpoint_dir": ckpt,
            "resume": resume,
        }
        if args.canonical_dir is not None:
            return run_e01(
                canonical_dir=args.canonical_dir,
                cache_dir=None,
                **common,
            )
        return run_e01(cache_dir=args.cache_dir, **common)
    return _run_hat(args)


if __name__ == "__main__":
    raise SystemExit(main())
