"""Post-run HAT gate validation H1–H20 (synthetic; no market data)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from quant.i03.compare_hat import compare_paths


def _recon_verdict_independent(art: dict[str, Any]) -> tuple[str, str | None]:
    """Independent encoding of prereg §14 — does NOT call decide_verdict."""

    V = bool(art["predicates"]["V"])
    E = bool(art["predicates"]["E"])
    C4 = bool(art["survival"]["C4"])
    C3 = bool(art["survival"]["C3"])
    F4 = bool(art["survival"]["F4"])
    if not V:
        return "INCONCLUSIVE", None
    if not E:
        return "INCONCLUSIVE", None
    if C4 and C3:
        return "PASS", "ND-1"
    if F4:
        return "FAIL", "ND-4"
    if C4 and not C3:
        return "INCONCLUSIVE", "ND-2"
    if C3 and not C4:
        return "INCONCLUSIVE", "ND-3"
    return "INCONCLUSIVE", "ND-5"


def evaluate_gates(
    *,
    run1: Path,
    run2: Path,
    fixture_meta: dict[str, Any],
    exit1: int,
) -> dict[str, Any]:
    art1 = json.loads((run1 / "artifact.json").read_text(encoding="utf-8"))
    art2 = json.loads((run2 / "artifact.json").read_text(encoding="utf-8"))
    cfg = art1["config"]
    cs = art1["contract_surface"]
    gates: dict[str, bool] = {}

    gates["H1"] = exit1 == 0 and (run1 / "artifact.json").exists()
    gates["H2"] = art1.get("input_hash") == fixture_meta.get("sha256")
    gates["H3"] = art1.get("mode") == "SYNTHETIC_HAT" and not art1.get("operator", {}).get(
        "test_overrides_enabled", True
    )
    gates["H4"] = cfg.get("W_X") == 20 and cfg.get("M") == 252 and cfg.get("W_sigma") == 20
    gates["H5"] = len(art1.get("blocks", [])) == 3 and cs.get("P") == 3
    gates["H6"] = cs.get("tau") == 20
    gates["H7"] = list(cfg.get("K", [])) == [10, 25, 50]
    gates["H8"] = all("n_queries" in e for e in art1.get("emnd", []))
    gates["H9"] = all(
        set(e.get("theta_by_k", {}),) >= {"10", "25", "50"}
        or set(int(k) for k in e.get("theta_by_k", {})) >= {10, 25, 50}
        for e in art1.get("emnd", [])
    )
    # theta keys may be int when loaded from json become str
    def _has_all_k(e: dict) -> bool:
        keys = {int(k) for k in e.get("theta_by_k", {})}
        return keys >= {10, 25, 50}

    gates["H9"] = all(_has_all_k(e) for e in art1.get("emnd", []))
    gates["H10"] = len(art1.get("locality", [])) == 3
    n4 = art1.get("n4", {})
    gates["H11"] = (
        n4.get("W_sigma") == 20
        and n4.get("B_used") == 999
        and "42" in str(n4.get("seed_doctrine", ""))
    )
    gates["H12"] = "valid" in n4 and "Z_frac" in n4
    n3 = art1.get("n3", {})
    gates["H13"] = (
        n3.get("method") == "IAAFT"
        and n3.get("B_requested") == 999
        and n3.get("I_max") == 100
        and float(n3.get("epsilon", -1)) == 1e-8
        and "10000" in str(n3.get("seed_doctrine", ""))
    )
    gates["H14"] = "n_converged" in n3 and "n_nonconverged" in n3
    # p-values for 3 periods × 3 k × 2 nulls
    pvals = art1.get("survival", {}).get("pvalues", {})
    n_cells = 0
    for null in ("N4", "N3"):
        for p, ks in pvals.get(null, {}).items():
            n_cells += len(ks)
    gates["H15"] = n_cells == 18
    surv = art1.get("survival", {})
    gates["H16"] = all(k in surv for k in ("C4", "C3", "F4"))
    gates["H17"] = all(k in art1.get("verdict", {}) for k in ("label", "nd_code", "reason"))
    recon_label, recon_nd = _recon_verdict_independent(art1)
    gates["H18"] = (
        recon_label == art1["verdict"]["label"]
        and recon_nd == art1["verdict"].get("nd_code")
    )
    report = (run1 / "report.md").read_text(encoding="utf-8")
    gates["H19"] = (
        "SYNTHETIC HAT" in report
        and "NOT MARKET EVIDENCE" in report
        and "NOT SCIENTIFIC EVIDENCE" in report
        and art1["verdict"]["label"] in report
    )
    cmp = compare_paths(run1 / "artifact.json", run2 / "artifact.json")
    gates["H20"] = cmp["status"] == "SEMANTIC_IDENTICAL"

    return {
        "gates": gates,
        "all_pass": all(gates.values()),
        "recon": {"label": recon_label, "nd_code": recon_nd},
        "semantic_compare": cmp,
        "n_inference_cells": n_cells,
        "synthetic_verdict": art1.get("verdict"),
        "block_queries": [e.get("n_queries") for e in art1.get("emnd", [])],
        "n4": n4,
        "n3": n3,
        "timing_run1": art1.get("timing"),
        "timing_run2": art2.get("timing"),
    }
