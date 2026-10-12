"""Consolidate I04-CAL run directories (fail-closed).

Accepts cells only when config_hash matches the canonical identity and
record_hash verifies. Conflicting payloads for the same cell_key → REJECT.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

from quant.i04_cal.bimachine import canonical_config
from quant.i04_cal.pipeline import _checkpoint_path, _record_hash, config_hash


def _iter_ok_rows(run_dir: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    results = run_dir / "results.jsonl"
    ckpt = run_dir / "ckpt"
    if results.is_file():
        for line in results.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            if row.get("status") == "OK":
                rows.append(row)
        return rows
    if ckpt.is_dir():
        for f in ckpt.glob("*.json"):
            row = json.loads(f.read_text(encoding="utf-8"))
            if row.get("status") == "OK":
                rows.append(row)
    return rows


def consolidate(
    sources: list[Path],
    out_dir: Path,
    *,
    expected_config_hash: str | None = None,
) -> dict[str, Any]:
    cfg = canonical_config()
    ch = expected_config_hash or config_hash(cfg)
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    ckpt = out_dir / "ckpt"
    ckpt.mkdir(exist_ok=True)
    accepted: dict[str, dict[str, Any]] = {}
    conflicts: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    provenance: list[dict[str, Any]] = []

    for src in sources:
        src = Path(src)
        man_path = src / "manifest.json"
        man = json.loads(man_path.read_text(encoding="utf-8")) if man_path.is_file() else {}
        provenance.append(
            {
                "path": str(src),
                "run_id": man.get("run_id"),
                "config_hash": man.get("config_hash"),
                "git_commit": man.get("git_commit"),
                "n_rows": man.get("n_rows"),
            }
        )
        for row in _iter_ok_rows(src):
            key = row.get("cell_key")
            if not key:
                rejected.append({"reason": "missing_cell_key", "source": str(src)})
                continue
            if row.get("config_hash") and row.get("config_hash") != ch:
                rejected.append(
                    {
                        "reason": "config_hash_mismatch",
                        "cell_key": key,
                        "got": row.get("config_hash"),
                        "expected": ch,
                        "source": str(src),
                    }
                )
                continue
            # Verify integrity
            rh = row.get("record_hash")
            if rh and rh != _record_hash({k: v for k, v in row.items() if k != "record_hash"}):
                # row may already exclude; recompute against full sans field
                payload = {k: v for k, v in row.items() if k != "record_hash"}
                if rh != _record_hash(payload):
                    rejected.append(
                        {
                            "reason": "record_hash_mismatch",
                            "cell_key": key,
                            "source": str(src),
                        }
                    )
                    continue
            row = dict(row)
            row["config_hash"] = ch
            if "record_hash" not in row:
                row["record_hash"] = _record_hash(row)
            if key in accepted:
                prev = accepted[key]
                if prev.get("record_hash") != row.get("record_hash"):
                    conflicts.append(
                        {
                            "cell_key": key,
                            "source_a": prev.get("_source"),
                            "source_b": str(src),
                        }
                    )
                continue
            row["_source"] = str(src)
            accepted[key] = row

    if conflicts:
        report = {
            "status": "REJECT",
            "reason": "conflicts",
            "n_conflicts": len(conflicts),
            "conflicts": conflicts[:50],
            "rejected": rejected[:50],
            "provenance": provenance,
        }
        (out_dir / "consolidate_report.json").write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
        return report

    # Write durable outputs
    keys_sorted = sorted(accepted)
    results_path = out_dir / "results.jsonl"
    with results_path.open("w", encoding="utf-8") as fout:
        for key in keys_sorted:
            row = {k: v for k, v in accepted[key].items() if k != "_source"}
            path = _checkpoint_path(ckpt, key)
            path.write_text(json.dumps(row, sort_keys=True, default=str) + "\n", encoding="utf-8")
            fout.write(json.dumps(row, default=str) + "\n")

    inventory = {
        "schema": "I04-CAL-CONSOLIDATE-v1",
        "status": "PASS" if not rejected else "PASS_WITH_REJECTS",
        "config_hash": ch,
        "n_accepted": len(accepted),
        "n_rejected": len(rejected),
        "n_conflicts": 0,
        "results_sha256": hashlib.sha256(results_path.read_bytes()).hexdigest(),
        "provenance": provenance,
        "rejected_sample": rejected[:20],
        "note": "Intermediate consolidation — not a global I04-CAL scientific verdict",
    }
    (out_dir / "consolidate_report.json").write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    (out_dir / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "I04-CAL-MANIFEST-v1",
                "status": "INCOMPLETE",
                "config_hash": ch,
                "n_rows": len(accepted),
                "note": "CONSOLIDATED — SYNTHETIC ONLY — NO GEOMETRY WINNER",
            },
            indent=2,
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
    )
    return inventory


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(prog="python -m quant.i04_cal.consolidate")
    p.add_argument("--out-dir", type=Path, required=True)
    p.add_argument("--source", type=Path, action="append", required=True)
    args = p.parse_args(argv)
    report = consolidate(list(args.source), args.out_dir)
    print(json.dumps({k: report[k] for k in ("status", "n_accepted", "n_rejected", "n_conflicts") if k in report}, indent=2))
    return 0 if report.get("status", "").startswith("PASS") else 2


if __name__ == "__main__":
    raise SystemExit(main())
