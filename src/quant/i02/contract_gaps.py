"""I02 L1 contract gaps — status after PREREG-v0.2 gap-closure review.

Historical gap texts are retained. Closed gaps point to the
preregistration sections that supersede them.
"""

from __future__ import annotations


class ImplementationContractGap(RuntimeError):
    """Raised when the frozen contract underspecifies a unique implementation."""


class BlockingImplementationContradiction(RuntimeError):
    """Raised when accepted clauses conflict for a required computation."""


# ---------------------------------------------------------------------------
# Gap A — X inheritance (CLOSED in I02-PREREG-v0.2 §13)
# ---------------------------------------------------------------------------

X_STANDARDIZATION_INHERITANCE_NOTE = """
CLOSED (I02-PREREG-v0.2 §13)

M=252: INHERITED REPRESENTATION CONTRACT (I01 forme X).

epsilon_sigma: NOT inherited. If sigma_hat=0, X is undefined (skip).
If sigma_hat>0, standardize by sigma_hat exactly (no epsilon).

L1 code at 8d05905 still used I01 epsilon — must be patched after
this amendment (readiness C0 until S3 also closed + patch).
"""


# ---------------------------------------------------------------------------
# Gap B — S3 neighbor metric (STILL OPEN — HUMAN DECISION)
# ---------------------------------------------------------------------------

S3_KNN_AGGREGATION_GAP = """
IMPLEMENTATION CONTRACT GAP — S3 kNN distance
Status: OPEN — HUMAN DECISION REQUIRED (I02-PREREG-v0.2 §14)

Affected object: neighbor selection for representation S3 = [RV, Q].

Preserved doctrine:

* S3* = [L, Q]; Q = MA/RV; phi = arccos(Q)
* Shape family {d_Q=|ΔQ|, d_phi=|Δphi|} — NO PRIMARY
* Disagreement => INCONCLUSIVE
* Level: δ_level = |ΔL|
* Aggregation L+form was never frozen (draft OPEN)

Minimal alternatives (see prereg §14.3) — NOT chosen by code:

* S3-A: sqrt((ΔL)^2+(ΔQ)^2) and sqrt((ΔL)^2+(Δphi)^2)
* S3-B: |ΔL|+|ΔQ| and |ΔL|+|Δphi|
* S3-C: shape-only d_Q / d_phi (weak)

Until human decision: S3 kNN / CRPS_S3 / R^(S3) MUST NOT be invented.
"""


# ---------------------------------------------------------------------------
# Gap C — Bootstrap (CLOSED in I02-PREREG-v0.2 §15; code not yet patched)
# ---------------------------------------------------------------------------

BOOTSTRAP_ALGORITHM_GAP = """
FORMERLY: IMPLEMENTATION CONTRACT GAP — moving/block bootstrap
Status: CONTRACT CLOSED in I02-PREREG-v0.2 §15
Implementation: NOT YET PATCHED (still raises until L1 patch)

Frozen algorithm summary:

* non-circular moving block bootstrap on paired valid (Z,R) series
* b* = 40; robustness {20,40,80}
* B = 9999; seed = 42
* percentile CI α=0.05; detectability = CI excludes 0 (CI-dual)
* NOT a separate null-world association-breaking test

See research/I02/I02-preregistration.md §15.
"""
