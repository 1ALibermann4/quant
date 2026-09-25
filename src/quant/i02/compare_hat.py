"""Compare two I02 HAT artifacts for semantic reproducibility (H17)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from quant.i02.artifact import load_artifact, semantic_fingerprint, semantic_payload


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="I02 HAT semantic reproducibility compare")
    p.add_argument("artifact_a", type=Path)
    p.add_argument("artifact_b", type=Path)
    args = p.parse_args(argv)
    a = load_artifact(args.artifact_a)
    b = load_artifact(args.artifact_b)
    fa = semantic_fingerprint(a)
    fb = semantic_fingerprint(b)
    print(f"A: {fa}")
    print(f"B: {fb}")
    if fa != fb:
        print("MISMATCH")
        return 1
    # Extra structural equality on semantic payload
    if semantic_payload(a) != semantic_payload(b):
        print("FINGERPRINT COLLISION OR PAYLOAD DRIFT")
        return 1
    print("SEMANTIC_IDENTICAL")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
