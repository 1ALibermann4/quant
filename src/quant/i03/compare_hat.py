"""Semantic comparison of two I03 artifacts (HAT Run1 vs Run2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


NON_SEMANTIC_PREFIXES = (
    "timing.",
    "environment.",
    "operator.",
)


def _flatten(obj: Any, prefix: str = "") -> dict[str, Any]:
    out: dict[str, Any] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.update(_flatten(v, key))
    elif isinstance(obj, (list, tuple)):
        for i, v in enumerate(obj):
            key = f"{prefix}[{i}]"
            out.update(_flatten(v, key))
    else:
        out[prefix] = obj
    return out


def _is_non_semantic(path: str) -> bool:
    return any(path == p[:-1] or path.startswith(p) for p in NON_SEMANTIC_PREFIXES)


def compare_artifacts(a: dict[str, Any], b: dict[str, Any]) -> dict[str, Any]:
    fa, fb = _flatten(a), _flatten(b)
    keys = sorted(set(fa) | set(fb))
    diffs: list[dict[str, Any]] = []
    for k in keys:
        if _is_non_semantic(k):
            continue
        if k not in fa or k not in fb or fa[k] != fb[k]:
            diffs.append({"path": k, "a": fa.get(k), "b": fb.get(k)})
    return {
        "status": "SEMANTIC_IDENTICAL" if not diffs else "SEMANTIC_DIFFERENCE",
        "n_diffs": len(diffs),
        "diffs": diffs[:50],  # cap report size
    }


def compare_paths(path_a: Path, path_b: Path) -> dict[str, Any]:
    a = json.loads(path_a.read_text(encoding="utf-8"))
    b = json.loads(path_b.read_text(encoding="utf-8"))
    return compare_artifacts(a, b)
