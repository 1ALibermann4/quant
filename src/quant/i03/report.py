"""I03 Markdown report from artifact (HAT / operator output)."""

from __future__ import annotations

from typing import Any


def render_report(artifact: dict[str, Any]) -> str:
    """Human-readable report. Scientific claims only if present in artifact."""

    lines: list[str] = []
    lines.append("# I03 HAT — operational report (derived)")
    lines.append("")
    lines.append("> **NOT SCIENTIFIC EVIDENCE** — synthetic operational acceptance only.")
    lines.append(">")
    lines.append("> ```text")
    lines.append("> SYNTHETIC HAT")
    lines.append("> NOT MARKET EVIDENCE")
    lines.append("> NOT SCIENTIFIC EVIDENCE")
    lines.append("> ```")
    lines.append("")
    lines.append("## Provenance")
    lines.append("")
    lines.append(f"- Schema: `{artifact.get('schema')}`")
    lines.append(f"- Prereg: `{artifact.get('prereg_id')}`")
    lines.append(f"- Input hash: `{artifact.get('input_hash')}`")
    lines.append(f"- Implementation: `{artifact.get('implementation_id', 'n/a')}`")
    lines.append(f"- Mode: `{artifact.get('mode', 'n/a')}`")
    lines.append("")
    cfg = artifact.get("config", {})
    lines.append("## Frozen config (from artifact)")
    lines.append("")
    for key in (
        "W_X",
        "M",
        "W_sigma",
        "tau",
        "K",
        "P",
        "B_N4",
        "B_N3",
        "alpha",
        "n_min",
        "iaaft_I_max",
        "iaaft_eps",
    ):
        if key in cfg:
            lines.append(f"- `{key}` = `{cfg[key]}`")
    lines.append("")
    lines.append("## Blocks")
    lines.append("")
    for b in artifact.get("blocks", []):
        lines.append(
            f"- period {b['period']}: [{b['start']}, {b['end']}] n={b['n']}"
        )
    lines.append("")
    lines.append("## E-MND")
    lines.append("")
    for e in artifact.get("emnd", []):
        lines.append(
            f"- period {e['period']}: n_queries={e['n_queries']} "
            f"skip_x={e['n_skipped_undefined_x']} "
            f"skip_pool={e['n_skipped_insufficient_pool']} "
            f"theta={e['theta_by_k']}"
        )
    lines.append("")
    lines.append("## Locality (DIAGNOSTIC — NON-PROMOTIONAL)")
    lines.append("")
    for d in artifact.get("locality", []):
        lines.append(
            f"- period {d['period']}: Lambda={d['Lambda']} Gamma={d['Gamma']} "
            f"hard={d['hard_degenerate']}"
        )
    lines.append("")
    lines.append("## Null batteries")
    lines.append("")
    n4 = artifact.get("n4", {})
    n3 = artifact.get("n3", {})
    lines.append(f"- N4 valid={n4.get('valid')} reason={n4.get('invalid_reason')} "
                 f"B={n4.get('B_used')} Z_frac={n4.get('Z_frac')}")
    lines.append(f"- N3 valid={n3.get('valid')} reason={n3.get('invalid_reason')} "
                 f"B_req={n3.get('B_requested')} "
                 f"converged={n3.get('n_converged')} "
                 f"nonconv={n3.get('n_nonconverged')}")
    lines.append("")
    lines.append("## Predicates / coherence")
    lines.append("")
    pred = artifact.get("predicates", {})
    surv = artifact.get("survival", {})
    lines.append(f"- V={pred.get('V')} E={pred.get('E')}")
    lines.append(
        f"- C4={surv.get('C4')} C3={surv.get('C3')} F4={surv.get('F4')}"
    )
    lines.append("")
    lines.append("## Verdict (synthetic — not market evidence)")
    lines.append("")
    v = artifact.get("verdict", {})
    lines.append(f"- label: **{v.get('label')}**")
    lines.append(f"- nd_code: `{v.get('nd_code')}`")
    lines.append(f"- reason: `{v.get('reason')}`")
    lines.append("")
    if "timing" in artifact:
        lines.append("## Timing (engineering only)")
        lines.append("")
        for k, val in artifact["timing"].items():
            lines.append(f"- {k}: {val}")
        lines.append("")
    lines.append("## Note")
    lines.append("")
    lines.append(
        "This Markdown is generated from the canonical JSON artifact. "
        "Do not interpret the synthetic verdict as market evidence."
    )
    lines.append("")
    return "\n".join(lines)
