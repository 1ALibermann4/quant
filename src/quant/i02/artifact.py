"""I02 HAT / operational artifact serialization and Markdown rendering.

JSON is canonical. Markdown is derived from JSON only (no recompute).
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ARTIFACT_SCHEMA = "I02-HAT-ARTIFACT-v1"
NON_SCIENTIFIC_META_KEYS = frozenset(
    {
        "execution_timestamp_utc",
        "run_id",
        "wall_clock_seconds",
        "hostname_omitted",
    }
)


def _json_default(obj: Any) -> Any:
    if isinstance(obj, float):
        if obj != obj:  # NaN
            return None
        return obj
    raise TypeError(f"not JSON-serializable: {type(obj)!r}")


def canonical_artifact_bytes(artifact: dict) -> bytes:
    """Stable UTF-8 JSON for hashing (sorted keys, compact separators)."""

    return json.dumps(
        artifact,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        default=_json_default,
    ).encode("utf-8")


def semantic_payload(artifact: dict) -> dict:
    """Drop explicitly non-scientific metadata for reproducibility compare."""

    out = json.loads(json.dumps(artifact, default=_json_default))
    prov = dict(out.get("provenance", {}))
    for k in NON_SCIENTIFIC_META_KEYS:
        prov.pop(k, None)
    out["provenance"] = prov
    # wall clock may also live at top level
    out.pop("wall_clock_seconds", None)
    return out


def semantic_fingerprint(artifact: dict) -> str:
    payload = canonical_artifact_bytes(semantic_payload(artifact))
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def write_artifact(path: Path, artifact: dict) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(artifact, indent=2, sort_keys=True, default=_json_default)
    path.write_text(text + "\n", encoding="utf-8")


def load_artifact(path: Path) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def render_markdown_from_artifact(artifact: dict) -> str:
    """Human-readable summary derived solely from the canonical artifact."""

    p = artifact.get("provenance", {})
    q = artifact.get("query_summary", {})
    audits = artifact.get("audits", {})
    assoc = artifact.get("association", {})
    lines: list[str] = []
    lines.append("# I02 HAT — operational report (derived)")
    lines.append("")
    lines.append("> **NOT SCIENTIFIC EVIDENCE** — synthetic operational acceptance only.")
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"- Schema: `{artifact.get('schema')}`")
    lines.append(f"- Prereg: `{p.get('preregistration_id')}`")
    lines.append(f"- Implementation commit: `{p.get('implementation_commit')}`")
    lines.append(f"- Fixture: `{p.get('fixture_id')}` / `{p.get('fixture_sha256')}`")
    lines.append(f"- Execution UTC: `{p.get('execution_timestamp_utc')}`")
    lines.append(f"- Semantic fingerprint: `{artifact.get('semantic_fingerprint')}`")
    lines.append(
        f"- Compressed-time MBB: `{p.get('compressed_time_mbb')}`"
    )
    lines.append("")
    lines.append("## Query summary")
    lines.append("")
    lines.append(f"- Total scheduled: **{q.get('n_scheduled')}**")
    lines.append(f"- Evaluable: **{q.get('n_evaluable')}**")
    lines.append(f"- Skipped: **{q.get('n_skipped')}**")
    lines.append(f"- Skip reasons: `{q.get('skip_reason_counts')}`")
    lines.append("")
    lines.append("## Structural audits (H-criteria)")
    lines.append("")
    for key in sorted(audits.keys()):
        lines.append(f"- `{key}`: **{audits[key]}**")
    lines.append("")
    lines.append("## Association (structural)")
    lines.append("")
    grid = assoc.get("spearman_grid", {})
    lines.append(f"- Spearman cells: **{len(grid)}**")
    lines.append(f"- Grid keys: `{sorted(grid.keys())}`")
    mbb = assoc.get("mbb", {})
    lines.append(f"- MBB cells: **{len(mbb)}**")
    lines.append(
        f"- Bootstrap config: B={assoc.get('bootstrap_B')}, "
        f"seed={assoc.get('bootstrap_seed')}, "
        f"b_values={assoc.get('b_values_executed')}"
    )
    lines.append("")
    lines.append("## Constants (frozen)")
    lines.append("")
    lines.append(f"```json\n{json.dumps(artifact.get('constants', {}), indent=2, sort_keys=True)}\n```")
    lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append(
        "This Markdown is generated from the canonical JSON artifact. "
        "Do not interpret synthetic ρ / CI as scientific evidence."
    )
    lines.append("")
    return "\n".join(lines)


def write_report_from_artifact(artifact_path: Path, report_path: Path) -> None:
    artifact = load_artifact(artifact_path)
    report_path = Path(report_path)
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(render_markdown_from_artifact(artifact), encoding="utf-8")
