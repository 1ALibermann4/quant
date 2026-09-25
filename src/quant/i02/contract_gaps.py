"""I02 L1/L1-patch contract gap status (I02-PREREG-v0.3).

Historical gap texts retained; closed gaps superseded by prereg §§13–15 / §14 S3-A.
"""

from __future__ import annotations


class ImplementationContractGap(RuntimeError):
    """Raised when the frozen contract underspecifies a unique implementation."""


class BlockingImplementationContradiction(RuntimeError):
    """Raised when accepted clauses conflict for a required computation."""


X_STANDARDIZATION_INHERITANCE_NOTE = """
CLOSED (I02-PREREG-v0.2 §13, implemented in L1 patch)

M=252: INHERITED REPRESENTATION CONTRACT.
epsilon_sigma: NOT used. sigma_hat=0 => X undefined (X_SIGMA_ZERO).
sigma_hat>0 => exact division by sigma_hat.
"""

S3_KNN_AGGREGATION_GAP = """
CLOSED (I02-PREREG-v0.3) — human decision S3-A ACCEPTED BEFORE DATA

d_S3,Q   = sqrt((ΔL)^2 + (ΔQ)^2)
d_S3,phi = sqrt((ΔL)^2 + (Δφ)^2), φ=arccos(Q)
NO PRIMARY; both S3_Q and S3_phi reported; disagreement => INCONCLUSIVE.
S3-B and S3-C rejected.
"""

BOOTSTRAP_ALGORITHM_GAP = """
CLOSED (I02-PREREG-v0.2 §15) — implemented in L1 patch

Non-circular MBB; B=9999; seed=42; percentile CI α=0.05;
detectability = CI excludes 0 (CI-dual, not H0 randomization test).
"""
