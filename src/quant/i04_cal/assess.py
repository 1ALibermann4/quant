"""Assess I04-CAL results.jsonl — raw/distributional reporting (GOV-02).

GOV-02: Unpreregistered numerical thresholds removed from qualification logic.
This module reports raw statistics and distributions only.
Scientific qualification (CAL-PASS/CAL-FAIL) requires governance evaluation
of these distributions against C1–C10 criteria.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def assess(out_dir: Path) -> dict[str, Any]:
    """Generate raw/distributional assessment report (GOV-02 compliant).

    Returns raw statistics, distributions, and quantiles.
    Does NOT enforce unpreregistered numerical thresholds for qualification.
    """
    out_dir = Path(out_dir)
    rows = load_rows(out_dir / "results.jsonl")
    man = json.loads((out_dir / "manifest.json").read_text(encoding="utf-8"))

    by_world: dict[str, list] = defaultdict(list)
    for r in rows:
        if r.get("status") == "OK":
            by_world[r["world_id"]].append(r)

    report: dict[str, Any] = {
        "manifest_status": man.get("status"),
        "n_rows": len(rows),
        "n_ok": sum(1 for r in rows if r.get("status") == "OK"),
        "n_fail_tech": sum(1 for r in rows if r.get("status") == "FAILED_TECHNICAL"),
        "worlds": {},
        "distributions": {},
        "open_governance": [
            "CAL-G2 stronger continuity-preserving overlap-null",
            "S6/S7 observability diagnostic interpretation",
            "G6 diffusion causal comparability (HOLD)",
            "G7 TDA short-window viability vs richer filtrations",
            "Scientific qualification (CAL-PASS/CAL-FAIL) requires governance evaluation of reported distributions",
        ],
        "note": "NO GEOMETRY WINNER — bench assessment only",
        "governance_note": "GOV-02: Raw/distributional reporting; numerical thresholds removed from qualification logic",
    }

    # Helper: extract contrast values
    def contrasts(world: str, geo: str = "G0") -> list[float]:
        vals = []
        for r in by_world.get(world, []):
            if r["gates"]["geometry_id"] != geo:
                continue
            v = r["gates"]["k"]["5"].get("CAL_G1_contrast_median")
            if v is not None:
                vals.append(float(v))
        return vals

    # C1: S0 false structure — report raw contrast distributions
    s0a = contrasts("S0a")
    s0b = contrasts("S0b")
    report["distributions"]["C1_S0_contrast"] = {
        "S0a": {
            "values": s0a,
            "n": len(s0a),
            "median": float(np.median(s0a)) if s0a else None,
            "q10": float(np.quantile(s0a, 0.1)) if s0a else None,
            "q90": float(np.quantile(s0a, 0.9)) if s0a else None,
            "mean": float(np.mean(s0a)) if s0a else None,
            "std": float(np.std(s0a)) if s0a else None,
        },
        "S0b": {
            "values": s0b,
            "n": len(s0b),
            "median": float(np.median(s0b)) if s0b else None,
            "q10": float(np.quantile(s0b, 0.1)) if s0b else None,
            "q90": float(np.quantile(s0b, 0.9)) if s0b else None,
            "mean": float(np.mean(s0b)) if s0b else None,
            "std": float(np.std(s0b)) if s0b else None,
        },
        "note": "Contrast near 1 expected under null; extreme <<1 suggests false structure",
    }

    # C2: S1 nuisance — report raw G_VOL association distributions
    s1_gvol = []
    for r in by_world.get("S1", []):
        if r["gates"]["geometry_id"] != "G0":
            continue
        g5 = r["gates"].get("CAL_G5", {})
        if "dGVOL" in g5:
            s1_gvol.append(abs(float(g5["dGVOL"])))
    report["distributions"]["C2_S1_nuisance_G_VOL"] = {
        "values": s1_gvol,
        "n": len(s1_gvol),
        "median": float(np.median(s1_gvol)) if s1_gvol else None,
        "q10": float(np.quantile(s1_gvol, 0.1)) if s1_gvol else None,
        "q90": float(np.quantile(s1_gvol, 0.9)) if s1_gvol else None,
        "mean": float(np.mean(s1_gvol)) if s1_gvol else None,
        "std": float(np.std(s1_gvol)) if s1_gvol else None,
        "note": "Higher association expected for volatility-dominated world",
    }

    # C3/C4: CAL-6 oracle recovery — report raw distributions
    cal6 = {}
    for world in ("S2", "S3", "S4", "S5"):
        ps = []
        for r in by_world.get(world, []):
            if r["gates"]["geometry_id"] != "G0":
                continue
            c6 = r["gates"].get("CAL_6", {})
            if c6.get("interpretable") and c6.get("P_mean") is not None:
                ps.append(float(c6["P_mean"]) - float(c6.get("chance", 0)))
        cal6[world] = {
            "excess_P_values": ps,
            "n": len(ps),
            "mean_excess_P": float(np.mean(ps)) if ps else None,
            "median_excess_P": float(np.median(ps)) if ps else None,
        }
    report["distributions"]["C3_C4_oracle_recovery_G0"] = cal6

    # C9: Invalid oracle handling — report status only
    invalid_count = 0
    invalid_interpretable_count = 0
    for world in ("S6", "S7"):
        for r in by_world.get(world, []):
            if r.get("oracle_status") == "INVALID":
                invalid_count += 1
                c6 = r["gates"].get("CAL_6", {})
                if c6.get("interpretable") is True:
                    invalid_interpretable_count += 1
    report["distributions"]["C9_invalid_oracle_handling"] = {
        "n_invalid_oracles": invalid_count,
        "n_invalid_treated_interpretable": invalid_interpretable_count,
        "invalid_oracle_worlds": sorted({r["world_id"] for r in rows if r.get("oracle_status") == "INVALID"}),
        "note": "INVALID oracle should NOT be treated as interpretable",
    }

    # Observability diagnostics for S6/S7
    for world in ("S6", "S7"):
        obs_vals = []
        for r in by_world.get(world, []):
            if "observability_spearman" in r.get("latent_notes", []):
                # Extract from notes string like "observability_spearman=0.4321"
                for note in r.get("latent_notes", []):
                    if "observability_spearman=" in str(note):
                        try:
                            val = float(str(note).split("=")[1])
                            obs_vals.append(val)
                        except (ValueError, IndexError):
                            pass
        if obs_vals:
            report["distributions"][f"observability_{world}"] = {
                "values": obs_vals,
                "n": len(obs_vals),
                "median": float(np.median(obs_vals)),
                "q10": float(np.quantile(obs_vals, 0.1)),
                "q90": float(np.quantile(obs_vals, 0.9)),
                "note": "Diagnostic only; no automatic VALID/INVALID threshold (GOV-02)",
            }

    # Completeness status
    complete = man.get("status") == "COMPLETE"
    report["execution_status"] = {
        "complete": complete,
        "manifest_status": man.get("status"),
        "expected_cells": man.get("expected_cells"),
        "n_rows": man.get("n_rows"),
    }

    # Scientific qualification status (GOV-02: pending governance)
    if not complete:
        qualification_status = "CALIBRATION DATA INCOMPLETE"
        qualification_reason = "Execution did not complete"
    else:
        qualification_status = "CALIBRATION DATA COMPLETE"
        qualification_reason = "SCIENTIFIC QUALIFICATION PENDING GOVERNANCE — raw distributions reported for evaluation against C1–C10"

    report["qualification_status"] = qualification_status
    report["qualification_reason"] = qualification_reason

    report["world_summaries"] = {
        w: {
            "n_rows": len(rs),
            "oracle_statuses": sorted({r.get("oracle_status") for r in rs}),
        }
        for w, rs in by_world.items()
    }
    return report


def write_assessment(out_dir: Path) -> dict[str, Any]:
    rep = assess(out_dir)
    path = Path(out_dir) / "assessment.json"
    path.write_text(json.dumps(rep, indent=2) + "\n", encoding="utf-8")
    return rep
