"""Documented implementation contract gaps for I02 L1.

Per L1 mandate: do **not** invent missing scientific rules.
Other components may proceed independently.
"""

from __future__ import annotations


class ImplementationContractGap(RuntimeError):
    """Raised when the frozen contract underspecifies a unique implementation."""


class BlockingImplementationContradiction(RuntimeError):
    """Raised when accepted clauses conflict for a required computation."""


# ---------------------------------------------------------------------------
# S3 neighbor metric / L+form aggregation
# ---------------------------------------------------------------------------

S3_KNN_AGGREGATION_GAP = """
IMPLEMENTATION CONTRACT GAP — S3 kNN distance

Affected object: neighbor selection for representation S3 = [RV, Q].

Conflicting / open clauses:

1. Representations accepted (draft §9.13.3): S3(t) = [RV_t, Q_t].
2. Level proximity (draft §9.14.1 ACCEPTED): δ_level = |ΔL| on RV > 0.
3. Metric robustness set (draft §9.16.2 ACCEPTED):
      M_S3 = {d_Q, d_φ} with NO primary between |ΔQ| and |Δφ|.
4. Explicit OPEN (draft §9.16 / §16): exact aggregation of L+form
      inside the kNN operator remains OPEN.
5. Preregistration §0 lists a single comparator S3 for the evidence
      grid — not two metric variants as primary estimands.

Minimal decision required (human / prereg bump class C):

* Choose the unique primary distance for S3 neighbor selection
  (how δ_level combines with d_Q and/or d_φ), OR
* Expand the preregistered evidence unit to named S3 metric variants.

Until then: S3 features (RV, Q, L) may be computed; S3 kNN / CRPS_S3 /
R^(S3) MUST NOT be silently invented.
"""


# ---------------------------------------------------------------------------
# Bootstrap algorithm uniqueness
# ---------------------------------------------------------------------------

BOOTSTRAP_ALGORITHM_GAP = """
IMPLEMENTATION CONTRACT GAP — moving/block bootstrap inference

Affected object: dependence-aware inference for Spearman(Z^(m), R^(S)).

Frozen:

* family = moving/block bootstrap (Gate 6 / §14M);
* b* = 40 primary; diagnostic b ∈ {20, 40, 80};
* no best-p / no ACF-tuned b;
* seed must be explicit when RNG is used.

NOT uniquely specified in the preregistration:

* number of bootstrap replicates B;
* overlapping moving-block vs non-overlapping partition;
* circular wrapping at series ends;
* whether resampling is applied to the paired (Z, R) series only
  or to an underlying return path;
* how two-sided uncertainty / p-values are formed from replicates.

Minimal decision required: preregister the unique bootstrap algorithm
and (if applicable) mark B as an execution parameter with a frozen
default.

Until then: do not invent a bootstrap CI / p-value procedure.
Block-length constants remain available as frozen scientific params.
"""


# ---------------------------------------------------------------------------
# X standardization inheritance note (non-blocking if accepted as I01 form)
# ---------------------------------------------------------------------------

X_STANDARDIZATION_INHERITANCE_NOTE = """
CONTRACT NOTE — X standardization parameters

I02 freezes W_X = 20 and inherits the I01 geometric form of X as
standardized causal log-returns (draft héritage / I01 state_X).

I01 parameters used for that form (not listed in I02 prereg §0 table):

* M = 252 causal μ/σ window;
* x_sigma_epsilon = 1e-8 floor on σ̂ (I01 standardization only —
  distinct from the I02 ban on ε for RV=0 / CRPS_S=0).

If this inheritance is rejected, treat as IMPLEMENTATION CONTRACT GAP
and bump the preregistration before scientific runs.
"""
