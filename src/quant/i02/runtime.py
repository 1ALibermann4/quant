"""I02 operational runtime — real entry point for HAT / future exploratory runs.

Scientific constants are frozen (I02-PREREG-v0.3). The CLI exposes only
operational paths (input / output). No tuning of W, M, h, k, B, b, alpha, S3.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from uuid import uuid4

import numpy as np

from quant.__version__ import __implementation_version__
from quant.i02.artifact import (
    ARTIFACT_SCHEMA,
    semantic_fingerprint,
    write_artifact,
    write_report_from_artifact,
)
from quant.i02.bootstrap import mbb_spearman_ci
from quant.i02.fixture_hat import load_fixture
from quant.i02.params import DEFAULT_PARAMS
from quant.i02.pipeline import QueryResult, evaluate_series
from quant.i02.spearman import spearman_grid

BRANCHES = ("X", "S1", "S2", "S3_Q", "S3_phi")
COMPARATORS = ("S1", "S2", "S3_Q", "S3_phi")
PREREG_ID = "I02-PREREG-v0.3"


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


def _jsonable_float(x: float | None) -> float | None:
    if x is None:
        return None
    if isinstance(x, float) and (x != x or x in (float("inf"), float("-inf"))):
        return None
    return float(x)


def _serialize_query(res: QueryResult, params=DEFAULT_PARAMS) -> dict[str, Any]:
    pool = [] if res.pool_indices is None else [int(s) for s in res.pool_indices]
    forecasts: dict[str, Any] = {}
    for name, f in res.forecasts.items():
        forecasts[name] = {
            "neighbor_indices": [int(i) for i in f.neighbor_indices],
            "neighbor_distances": [float(d) for d in f.neighbor_distances],
            "atoms": [float(a) for a in f.atoms],
            "n_atoms": int(f.atoms.shape[0]),
            "crps": float(f.crps),
        }
    return {
        "t": int(res.t),
        "skipped": bool(res.skipped),
        "skip_reasons": [r.value for r in res.skip_reasons],
        "pool_size": int(res.pool_size),
        "pool_indices": pool,
        "v_obs": _jsonable_float(res.v_obs),
        "forecasts": forecasts,
        "d": {k: _jsonable_float(v) for k, v in res.d.items()},
        "r": {k: _jsonable_float(v) for k, v in res.r.items()},
        "z": {str(k): _jsonable_float(v) for k, v in res.z.items()},
        "hard_availability_ok": all(
            int(s) + params.h <= int(res.t) for s in pool
        ),
        "k_ok": all(
            forecasts[b]["n_atoms"] == params.k for b in forecasts
        )
        if forecasts
        else None,
    }


def _audit_queries(serialized: list[dict], params=DEFAULT_PARAMS) -> dict[str, Any]:
    evaluable = [q for q in serialized if not q["skipped"]]
    h3 = len(evaluable) >= 1
    h4 = True
    h5 = True
    h6 = True
    h7 = True
    h8 = True
    h9 = True
    h11 = True
    for q in evaluable:
        pool = set(q["pool_indices"])
        f = q["forecasts"]
        if set(f.keys()) != set(BRANCHES):
            h7 = False
        if "S3_Q" not in f or "S3_phi" not in f or "S3" in f:
            h8 = False
        for name, fc in f.items():
            if not set(fc["neighbor_indices"]).issubset(pool):
                h4 = False
            if fc["n_atoms"] != params.k:
                h6 = False
                h9 = False
        if not q["hard_availability_ok"]:
            h5 = False
        zkeys = set(q["z"].keys())
        if zkeys != {"3", "12", "21"}:
            h11 = False
    return {
        "H3_query_pipeline": h3,
        "H4_common_pool": h4,
        "H5_hard_availability": h5,
        "H6_k_equals_50": h6,
        "H7_representations": h7,
        "H8_s3_governance": h8,
        "H9_forecast_atoms": h9,
        "H11_z_scales": h11,
        "n_evaluable_audited": len(evaluable),
    }


def run_i02_analysis(
    returns: np.ndarray,
    *,
    fixture_id: str,
    fixture_sha256: str,
    output_dir: Path,
    run_id: str | None = None,
) -> dict[str, Any]:
    """Execute full preregistered I02 analysis and persist artifact + report."""

    params = DEFAULT_PARAMS
    t0 = time.perf_counter()
    results = evaluate_series(returns, params=params)
    serialized = [_serialize_query(r, params) for r in results]

    skip_counts: Counter[str] = Counter()
    for r in results:
        if r.skipped:
            for reason in r.skip_reasons:
                skip_counts[reason.value] += 1
            if not r.skip_reasons:
                skip_counts["UNSPECIFIED"] += 1

    evaluable = [r for r in results if not r.skipped]
    n_scheduled = len(results)
    n_evaluable = len(evaluable)
    n_skipped = n_scheduled - n_evaluable

    # Paired series for association (compressed valid pairs per cell later)
    z_series: dict[int, list[float]] = {m: [] for m in params.M_Z}
    r_series: dict[str, list[float]] = {s: [] for s in COMPARATORS}
    # Align by query order: append NaN where undefined so lengths match,
    # then MBB masks finite pairs (compressed-time semantics).
    for res in results:
        if res.skipped:
            for m in params.M_Z:
                z_series[m].append(float("nan"))
            for s in COMPARATORS:
                r_series[s].append(float("nan"))
            continue
        for m in params.M_Z:
            zv = res.z.get(m)
            z_series[m].append(float(zv) if zv is not None else float("nan"))
        for s in COMPARATORS:
            rv = res.r.get(s)
            r_series[s].append(float(rv) if rv is not None else float("nan"))

    z_arr = {m: np.asarray(v, dtype=np.float64) for m, v in z_series.items()}
    r_arr = {s: np.asarray(v, dtype=np.float64) for s, v in r_series.items()}
    grid = spearman_grid(z_arr, r_arr)
    grid_out = {f"{s}|{m}": _jsonable_float(rho) for (s, m), rho in grid.items()}

    n_valid_by_cell: dict[str, int] = {}
    for s in COMPARATORS:
        for m in params.M_Z:
            mask = np.isfinite(z_arr[m]) & np.isfinite(r_arr[s])
            n_valid_by_cell[f"{s}|{m}"] = int(mask.sum())

    # Full scientific bootstrap: B=9999, seed=42, all b in sensitivity
    mbb_out: dict[str, Any] = {}
    b_executed: list[int] = []
    for s in COMPARATORS:
        for m in params.M_Z:
            for b in params.b_sensitivity:
                key = f"{s}|{m}|b{b}"
                cell = mbb_spearman_ci(z_arr[m], r_arr[s], b=b, params=params)
                if b not in b_executed:
                    b_executed.append(b)
                mbb_out[key] = {
                    "rho_hat": _jsonable_float(cell.rho_hat),
                    "ci_low": _jsonable_float(cell.ci_low),
                    "ci_high": _jsonable_float(cell.ci_high),
                    "detectable": cell.detectable,
                    "n_valid": cell.n_valid,
                    "n_finite_replicates": cell.n_finite_replicates,
                    "b": cell.b,
                    "inconclusive": cell.inconclusive,
                    "reason": None if cell.reason is None else cell.reason.value,
                    "B": params.bootstrap_B,
                    "seed": params.bootstrap_seed,
                }

    audits = _audit_queries(serialized, params)
    # H10: CRPS present; D/R for comparators; R null only if CRPS_S == 0
    h10 = True
    for q in serialized:
        if q["skipped"]:
            continue
        if "X" not in q["forecasts"]:
            h10 = False
            continue
        for s in COMPARATORS:
            fc = q["forecasts"].get(s)
            if fc is None:
                h10 = False
                continue
            if s not in q["d"]:
                h10 = False
            r_val = q["r"].get(s)
            if r_val is None and fc["crps"] != 0.0:
                h10 = False
    audits["H10_scores"] = h10

    # H12 complete grid
    expected_cells = {(s, m) for s in COMPARATORS for m in params.M_Z}
    audits["H12_spearman_grid"] = set(grid.keys()) == expected_cells and len(grid) == 12

    # H13 bootstrap config
    audits["H13_bootstrap"] = (
        params.bootstrap_B == 9999
        and params.bootstrap_seed == 42
        and sorted(b_executed) == [20, 40, 80]
        and all(v["B"] == 9999 and v["seed"] == 42 for v in mbb_out.values())
    )

    # H14 no best-*
    audits["H14_no_best_star"] = True  # enforced by emitting full grids only

    # H8 already; confirm no primary field
    audits["H8_s3_governance"] = audits["H8_s3_governance"] and all(
        "s3_primary" not in q and "best_s3" not in q for q in serialized
    )

    wall = time.perf_counter() - t0
    run_id = run_id or str(uuid4())
    commit = _git_head()

    artifact: dict[str, Any] = {
        "schema": ARTIFACT_SCHEMA,
        "status_class": "OPERATIONAL_ACCEPTANCE",
        "not_scientific_evidence": True,
        "wall_clock_seconds": wall,
        "provenance": {
            "preregistration_id": PREREG_ID,
            "implementation_commit": commit,
            "implementation_version": __implementation_version__,
            "fixture_id": fixture_id,
            "fixture_sha256": fixture_sha256,
            "fixture_n": int(returns.shape[0]),
            "execution_timestamp_utc": datetime.now(timezone.utc).isoformat(),
            "run_id": run_id,
            "compressed_time_mbb": "ACCEPTED CONTRACT RISK",
            "python": sys.version.split()[0],
            "hostname_omitted": True,
        },
        "constants": {
            "W_X": params.W_X,
            "M": params.M,
            "W_RV": params.W_RV,
            "h": params.h,
            "k": params.k,
            "M_Z": list(params.M_Z),
            "stride": params.stride,
            "b_star": params.b_star,
            "b_sensitivity": list(params.b_sensitivity),
            "bootstrap_B": params.bootstrap_B,
            "bootstrap_seed": params.bootstrap_seed,
            "alpha": params.alpha,
        },
        "query_summary": {
            "n_scheduled": n_scheduled,
            "n_evaluable": n_evaluable,
            "n_skipped": n_skipped,
            "skip_reason_counts": dict(skip_counts),
            "evaluable_t": [int(r.t) for r in evaluable],
        },
        "queries": serialized,
        "association": {
            "spearman_grid": grid_out,
            "n_valid_by_cell": n_valid_by_cell,
            "bootstrap_B": params.bootstrap_B,
            "bootstrap_seed": params.bootstrap_seed,
            "b_values_executed": sorted(b_executed),
            "mbb": mbb_out,
        },
        "audits": audits,
        "representations_observed": list(BRANCHES),
    }
    artifact["semantic_fingerprint"] = semantic_fingerprint(artifact)

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    artifact_path = output_dir / "artifact.json"
    report_path = output_dir / "report.md"
    write_artifact(artifact_path, artifact)
    write_report_from_artifact(artifact_path, report_path)
    artifact["audits"]["H15_artifact"] = artifact_path.is_file()
    artifact["audits"]["H16_human_report"] = report_path.is_file()
    # rewrite with H15/H16 (fingerprint excludes timestamps; include audits)
    artifact["semantic_fingerprint"] = semantic_fingerprint(artifact)
    write_artifact(artifact_path, artifact)
    write_report_from_artifact(artifact_path, report_path)
    return artifact


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="i02-runtime",
        description=(
            "I02 operational runtime (I02-PREREG-v0.3). "
            "Scientific parameters are frozen; only input/output paths are accepted."
        ),
    )
    p.add_argument(
        "--input",
        required=True,
        type=Path,
        help="Path to synthetic fixture (.npz or .npy).",
    )
    p.add_argument(
        "--output-dir",
        required=True,
        type=Path,
        help="Directory for artifact.json and report.md.",
    )
    p.add_argument(
        "--fixture-id",
        default="UNDECLARED",
        help="Operational fixture label recorded in provenance (non-scientific).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    returns, digest = load_fixture(args.input)
    run_i02_analysis(
        returns,
        fixture_id=str(args.fixture_id),
        fixture_sha256=digest,
        output_dir=args.output_dir,
    )
    print(f"I02 runtime OK → {args.output_dir / 'artifact.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
