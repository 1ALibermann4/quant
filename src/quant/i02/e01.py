"""I02-E01 exploratory runner — UNQUALIFIED SPY cache → I02 runtime.

Operational wiring only. Scientific constants remain frozen (v0.3).
Does not import yfinance into the I02 mathematical core; loads the
existing DR-008 exploratory cache via quant.exploratory.adapter.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

import numpy as np

from quant.exploratory.adapter import load_latest_cache
from quant.exploratory.status import BANNER
from quant.i01.returns import log_returns
from quant.i02.runtime import run_i02_analysis


def _qc_returns(returns: np.ndarray) -> dict[str, Any]:
    r = np.asarray(returns, dtype=np.float64)
    finite = np.isfinite(r)
    # r[0] is intentionally NaN
    body = r[1:]
    return {
        "n": int(r.shape[0]),
        "n_finite_including_r0_nan_slot": int(np.isfinite(r[1:]).sum()),
        "r0_is_nan": bool(np.isnan(r[0])) if r.size else None,
        "n_nonfinite_body": int((~np.isfinite(body)).sum()) if body.size else 0,
        "n_zero_body": int(np.sum(body == 0.0)) if body.size else 0,
        "min_body": float(np.nanmin(body)) if body.size and np.isfinite(body).any() else None,
        "max_body": float(np.nanmax(body)) if body.size and np.isfinite(body).any() else None,
    }


def _dataset_record(acq, returns: np.ndarray, cache_dir: Path) -> dict[str, Any]:
    prices = np.asarray(acq.series.adjusted_price, dtype=np.float64)
    price_hash = "sha256:" + hashlib.sha256(prices.tobytes(order="C")).hexdigest()
    ret_hash = "sha256:" + hashlib.sha256(
        np.asarray(returns, dtype=np.float64).tobytes(order="C")
    ).hexdigest()
    return {
        "data_class": "EXPLORATORY",
        "qualification": "UNQUALIFIED",
        "scientifically_promotable": False,
        "banner": BANNER,
        "source": acq.source,
        "ticker": acq.ticker,
        "yfinance_version": acq.yfinance_version,
        "price_field": "Adj Close",
        "request_parameters": dict(acq.request_parameters),
        "acquired_at_utc": acq.acquired_at_utc.isoformat(),
        "n_sessions": len(acq.series),
        "first_session": acq.series.sessions[0].isoformat(),
        "last_session": acq.series.sessions[-1].isoformat(),
        "calendar_authority": False,
        "cache_dir": str(cache_dir),
        "adjusted_price_sha256": price_hash,
        "log_returns_sha256": ret_hash,
        "qc_returns": _qc_returns(returns),
        "note": (
            "Reuse of I01-E01 DR-008 sandbox cache. Not C02. "
            "Not confirmatory. Date range not chosen from I02 results."
        ),
    }


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="i02-e01",
        description=(
            "I02-E01 exploratory run (UNQUALIFIED). "
            "Frozen I02-PREREG-v0.3; no scientific knobs."
        ),
    )
    p.add_argument(
        "--cache-dir",
        type=Path,
        default=Path("data/exploratory"),
        help="Directory containing UNQUALIFIED_SPY_*.meta.json cache.",
    )
    p.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory for artifact.json / report.md / dataset.json.",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(BANNER)
    acq = load_latest_cache(args.cache_dir, ticker="SPY")
    returns = log_returns(acq.series)
    dataset = _dataset_record(acq, returns, args.cache_dir)

    out = Path(args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "dataset.json").write_text(
        json.dumps(dataset, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    artifact = run_i02_analysis(
        returns,
        fixture_id=f"EXPLORATORY-SPY-{acq.acquired_at_utc.strftime('%Y%m%dT%H%M%SZ')}",
        fixture_sha256=dataset["log_returns_sha256"],
        output_dir=out,
        store_full_queries=False,
    )
    # Attach dataset block without recomputing science
    artifact["dataset"] = dataset
    artifact["run_class"] = "I02-E01-EXPLORATORY-UNQUALIFIED"
    artifact["not_scientific_evidence_promotable"] = True
    from quant.i02.artifact import semantic_fingerprint, write_artifact, write_report_from_artifact

    artifact["semantic_fingerprint"] = semantic_fingerprint(artifact)
    write_artifact(out / "artifact.json", artifact)
    write_report_from_artifact(out / "artifact.json", out / "report.md")
    print(f"I02-E01 runtime OK -> {out / 'artifact.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
