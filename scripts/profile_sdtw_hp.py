"""I04-CAL HP profiling — Soft-DTW ref vs Numba (engineering only)."""

from __future__ import annotations

import json
import time
from pathlib import Path

import numpy as np

from quant.i04_cal.sdtw import _HAS_NUMBA, soft_dtw, soft_dtw_ref


def main() -> None:
    out = Path("research/I04/perf/HP-OPT-PROFILE.json")
    out.parent.mkdir(parents=True, exist_ok=True)
    rng = np.random.default_rng(0)
    report: dict = {"has_numba": _HAS_NUMBA, "windows": {}, "note": "engineering only"}
    for W in (20, 40, 60):
        pairs = [(rng.normal(size=W), rng.normal(size=W)) for _ in range(80)]
        # warmup
        if _HAS_NUMBA:
            soft_dtw(pairs[0][0], pairs[0][1], 1.0, backend="numba")
        t0 = time.perf_counter()
        for x, y in pairs:
            soft_dtw_ref(x, y, 1.0)
        t_ref = time.perf_counter() - t0
        t_jit = None
        max_abs = None
        if _HAS_NUMBA:
            t0 = time.perf_counter()
            for x, y in pairs:
                soft_dtw(x, y, 1.0, backend="numba")
            t_jit = time.perf_counter() - t0
            diffs = [
                abs(soft_dtw_ref(x, y, 1.0) - soft_dtw(x, y, 1.0, backend="numba"))
                for x, y in pairs[:20]
            ]
            max_abs = float(max(diffs))
        report["windows"][str(W)] = {
            "n_pairs": len(pairs),
            "t_ref_s": t_ref,
            "t_numba_s": t_jit,
            "speedup": (t_ref / t_jit) if t_jit else None,
            "max_abs_diff_20": max_abs,
            "s_per_pair_ref": t_ref / len(pairs),
            "s_per_pair_numba": (t_jit / len(pairs)) if t_jit else None,
        }
        print(W, report["windows"][str(W)])
    out.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print("wrote", out)


if __name__ == "__main__":
    main()
