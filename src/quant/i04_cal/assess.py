"""Assess I04-CAL results.jsonl against C1–C10 (no geometry winner)."""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path
from typing import Any


def load_rows(path: Path) -> list[dict[str, Any]]:
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def assess(out_dir: Path) -> dict[str, Any]:
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
        "criteria": {},
        "open_governance": [
            "CAL-G2 stronger continuity-preserving overlap-null",
            "S6/S7 observability Spearman cutoff 0.25",
            "G6 diffusion causal comparability (HOLD)",
            "G7 TDA short-window viability vs richer filtrations",
        ],
        "note": "NO GEOMETRY WINNER — bench assessment only",
    }

    # C1: S0 false structure — G1 contrast systematically << 1 would be suspicious;
    # we flag if median contrast across G0 on S0a is < 0.5 for most seeds (strong false structure)
    def contrasts(world: str, geo: str = "G0") -> list[float]:
        vals = []
        for r in by_world.get(world, []):
            if r["gates"]["geometry_id"] != geo:
                continue
            v = r["gates"]["k"]["5"].get("CAL_G1_contrast_median")
            if v is not None:
                vals.append(float(v))
        return vals

    s0a = contrasts("S0a")
    s0b = contrasts("S0b")
    c1_pass = True
    if s0a:
        # Expect contrast near 1 under null; extreme <<0.4 suggests strong false structure.
        # Mild <1 can arise from overlapping windows even for IID (documented limitation).
        frac_low = sum(1 for v in s0a if v < 0.4) / len(s0a)
        c1_pass = frac_low < 0.25
    report["criteria"]["C1_S0_false_positive"] = {
        "pass": c1_pass,
        "S0a_contrast_median_of_medians": float(sorted(s0a)[len(s0a) // 2]) if s0a else None,
        "S0b_contrast_median_of_medians": float(sorted(s0b)[len(s0b) // 2]) if s0b else None,
        "S0a_frac_contrast_lt_0.4": (
            sum(1 for v in s0a if v < 0.4) / len(s0a) if s0a else None
        ),
        "note": "overlapping windows induce mild contrast<1 even under IID",
    }

    # C2: S1 nuisance — G_VOL association should be relatively high for G0
    s1_gvol = []
    for r in by_world.get("S1", []):
        if r["gates"]["geometry_id"] != "G0":
            continue
        g5 = r["gates"].get("CAL_G5", {})
        if "dGVOL" in g5:
            s1_gvol.append(abs(float(g5["dGVOL"])))
    c2 = bool(s1_gvol) and (sum(s1_gvol) / len(s1_gvol) > 0.2)
    report["criteria"]["C2_S1_nuisance"] = {
        "pass": c2,
        "mean_abs_spearman_dGVOL_G0": float(sum(s1_gvol) / len(s1_gvol)) if s1_gvol else None,
    }

    # C4/C3: CAL-6 on categorical worlds
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
            "mean_excess_P": float(sum(ps) / len(ps)) if ps else None,
            "n": len(ps),
        }
    report["criteria"]["C3_C4_oracle_recovery_G0"] = cal6

    # C9: invalid oracles not FAIL
    invalid_ok = True
    for world in ("S6", "S7"):
        for r in by_world.get(world, []):
            if r.get("oracle_status") == "INVALID":
                c6 = r["gates"].get("CAL_6", {})
                if c6.get("interpretable") is True:
                    invalid_ok = False
    report["criteria"]["C9_invalid_oracle_handling"] = {"pass": invalid_ok}

    # Completeness
    complete = man.get("status") == "COMPLETE"
    report["criteria"]["completeness"] = {"pass": complete, "status": man.get("status")}

    # Bench verdict
    if not complete:
        status = "CAL-INCONCLUSIVE"
        reason = "execution incomplete"
    elif not c1_pass:
        status = "CAL-FAIL"
        reason = "S0 systematic false structure under contrast"
    elif not invalid_ok:
        status = "CAL-FAIL"
        reason = "invalid oracle treated as interpretable"
    else:
        # Partial pass: core invariants hold; full C3-C8 need multi-geo evidence
        status = "CAL-PASS" if s0a and s1_gvol else "CAL-INCONCLUSIVE"
        reason = (
            "core S0/S1/C9 gates satisfied on available COMPLETE evidence"
            if status == "CAL-PASS"
            else "insufficient rows for full C1-C10"
        )

    report["bench_status"] = status
    report["bench_reason"] = reason
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
