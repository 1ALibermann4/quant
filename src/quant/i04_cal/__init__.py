"""I04-CAL — Synthetic Structural Calibration (pre-market).

No future market targets. No geometry winners. No PRED/ECON.
"""

from __future__ import annotations

__all__ = ["SPEC_ID", "B_WORLD", "WINDOWS", "QUERY_STRIDE"]

SPEC_ID = "I04-CAL-SPEC-v0.2"
B_WORLD = 32
WINDOWS: tuple[int, ...] = (20, 40, 60)
QUERY_STRIDE = 8
K_NEIGHBORS: tuple[int, ...] = (5, 10, 20)
N_POST_BURNIN = 8192
