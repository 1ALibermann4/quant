"""I03-E01 exploratory market runner — UNQUALIFIED SPY cache → I03 pipeline.

Operational wiring only. Scientific constants remain frozen (I03-PREREG-v0.1).
Does not import yfinance into the I03 mathematical core; loads the
existing DR-008 exploratory cache via quant.exploratory.adapter.

Allowed E01 labels (mapped from structural verdict):
  EXPL-SUPPORT / EXPL-ABSENT / EXPL-INCONCLUSIVE
Never SCI-PASS / SCI-FAIL / PRED / ECON.
"""

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

from quant.exploratory.adapter import load_latest_cache
from quant.exploratory.status import BANNER
from quant.i01.returns import log_returns
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.pipeline import artifact_dict, run_structural_analysis
from quant.i03.report import render_report

PREREG_ID = "I03-PREREG-v0.1"

# Authorized I01/I02 DR-008 snapshot (must match before science).
AUTHORIZED_PRICE_SHA256 = (
    "sha256:bc0d68b080f1f42c56f01da43820c11425ca1fc3a80bfb0ca32647821c2488d1"
)
AUTHORIZED_RETURNS_SHA256 = (
    "sha256:bde9a3045659bcb6ffdde99c52d7b088662456ed5d42737662f7c8384091c02e"
)
AUTHORIZED_N_SESSIONS = 8470
AUTHORIZED_FIRST = "1993-01-29"
AUTHORIZED_LAST = "2026-09-23"
AUTHORIZED_ACQUIRED = "2026-09-24T12:00:16.920799+00:00"
AUTHORIZED_CACHE_STEM = "UNQUALIFIED_SPY_20260924T120016Z"

STRUCT_TO_EXPL = {
    "PASS": "EXPL-SUPPORT",
    "FAIL": "EXPL-ABSENT",
    "INCONCLUSIVE": "EXPL-INCONCLUSIVE",
}


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


def _qc_returns(returns: np.ndarray) -> dict[str, Any]:
    r = np.asarray(returns, dtype=np.float64)
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
        "adjustment_semantics": (
            "yfinance Adj Close with auto_adjust=False; "
            "dividends/splits reflected in Adj Close column as provided by vendor"
        ),
        "request_parameters": dict(acq.request_parameters),
        "acquired_at_utc": acq.acquired_at_utc.isoformat(),
        "n_sessions": len(acq.series),
        "first_session": acq.series.sessions[0].isoformat(),
        "last_session": acq.series.sessions[-1].isoformat(),
        "calendar_authority": False,
        "cache_dir": str(cache_dir),
        "cache_stem": AUTHORIZED_CACHE_STEM,
        "adjusted_price_sha256": price_hash,
        "log_returns_sha256": ret_hash,
        "qc_returns": _qc_returns(returns),
        "authorized_snapshot_check": {
            "price_sha256_match": price_hash == AUTHORIZED_PRICE_SHA256,
            "returns_sha256_match": ret_hash == AUTHORIZED_RETURNS_SHA256,
            "n_sessions_match": len(acq.series) == AUTHORIZED_N_SESSIONS,
            "first_match": acq.series.sessions[0].isoformat() == AUTHORIZED_FIRST,
            "last_match": acq.series.sessions[-1].isoformat() == AUTHORIZED_LAST,
            "acquired_match": acq.acquired_at_utc.isoformat() == AUTHORIZED_ACQUIRED,
        },
        "note": (
            "Reuse of I01-E01 DR-008 sandbox cache (same as I02-E01). Not C02. "
            "Not confirmatory. Date range not chosen from I03 results."
        ),
    }


def run_e01(*, cache_dir: Path, out_dir: Path) -> int:
    """Execute one I03-E01 exploratory market run. Returns process exit code."""

    if os.environ.get("I03_ALLOW_TEST_OVERRIDES") == "1":
        print(
            "WARNING: I03_ALLOW_TEST_OVERRIDES=1 is set; E01 clears it for production path.",
            file=sys.stderr,
        )
        del os.environ["I03_ALLOW_TEST_OVERRIDES"]

    print(BANNER)
    acq = load_latest_cache(cache_dir, ticker="SPY")
    returns = log_returns(acq.series)
    dataset = _dataset_record(acq, returns, cache_dir)

    checks = dataset["authorized_snapshot_check"]
    if not all(checks.values()):
        print("STOP: exploratory dataset does not match authorized I02-E01 snapshot.", file=sys.stderr)
        print(json.dumps(checks, indent=2), file=sys.stderr)
        print(
            f"got price={dataset['adjusted_price_sha256']} returns={dataset['log_returns_sha256']}",
            file=sys.stderr,
        )
        print(
            "Note: log-returns SHA-256 is platform-sensitive (Win MSC vs Linux GCC numpy). "
            "Use the same platform as I02-E01 (Windows py -3.12) for bit-identical returns.",
            file=sys.stderr,
        )
        return 2

    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "dataset.json").write_text(
        json.dumps(dataset, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    cfg = DEFAULT_CONFIG
    t0 = time.perf_counter()
    result = run_structural_analysis(returns, cfg)
    elapsed = time.perf_counter() - t0

    impl = _git_head() or "unknown"
    structural = result.verdict.label.value
    expl = STRUCT_TO_EXPL[structural]

    artifact = artifact_dict(
        result,
        input_hash=dataset["log_returns_sha256"],
        implementation_id=impl,
        mode="E01_EXPLORATORY_UNQUALIFIED",
        timing={
            "total_seconds": round(elapsed, 3),
            "note": "engineering observation only; no scientific performance gate",
        },
        fixture_id=f"EXPLORATORY-SPY-{acq.acquired_at_utc.strftime('%Y%m%dT%H%M%SZ')}",
    )
    artifact["dataset"] = dataset
    artifact["environment"] = {
        "python": sys.version.replace("\n", " "),
        "platform": platform.platform(),
        "executable": sys.executable,
        "numpy": np.__version__,
    }
    artifact["operator"] = {
        "command": "python -m quant.i03 --mode e01 ...",
        "prereg_id": PREREG_ID,
        "B_N4": cfg.B_N4,
        "B_N3": cfg.B_N3,
        "test_overrides_enabled": False,
    }
    artifact["run_class"] = "I03-E01-EXPLORATORY-UNQUALIFIED"
    artifact["not_scientific_evidence_promotable"] = True
    artifact["exploratory_verdict"] = {
        "label": expl,
        "structural_label": structural,
        "structural_nd_code": result.verdict.nd_code,
        "structural_reason": result.verdict.reason,
        "mapping": (
            "PASS→EXPL-SUPPORT; FAIL→EXPL-ABSENT; INCONCLUSIVE→EXPL-INCONCLUSIVE"
        ),
        "explicit": {
            "EXPL-SUPPORT_ne_SCI-PASS": True,
            "EXPL-ABSENT_ne_SCI-FAIL": True,
            "EXPL-INCONCLUSIVE_ne_evidence_of_absence": True,
        },
    }

    (out_dir / "artifact.json").write_text(
        json.dumps(artifact, indent=2, default=_json_default) + "\n",
        encoding="utf-8",
    )
    (out_dir / "report.md").write_text(render_report(artifact), encoding="utf-8")
    (out_dir / "environment.json").write_text(
        json.dumps(
            {
                **artifact["environment"],
                "elapsed_seconds": elapsed,
                "dataset": {
                    "cache_stem": dataset["cache_stem"],
                    "log_returns_sha256": dataset["log_returns_sha256"],
                    "adjusted_price_sha256": dataset["adjusted_price_sha256"],
                },
                "exploratory_verdict": expl,
                "structural_verdict": structural,
                "exit": 0,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(
        f"I03 E01 complete: structural={structural} exploratory={expl} "
        f"elapsed={elapsed:.1f}s out={out_dir}"
    )
    return 0
