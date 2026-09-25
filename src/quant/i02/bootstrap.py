"""Non-circular moving block bootstrap (I02-PREREG-v0.2/v0.3 §15).

CI-dual detectability: percentile CI excludes 0.
This is **not** a dependence-preserving H0 randomization test.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i02.params import DEFAULT_PARAMS, I02Params
from quant.i02.spearman import spearman_rho
from quant.i02.types import SkipReason


@dataclass(slots=True)
class MBBResult:
    """Bootstrap inference for one Spearman association."""

    rho_hat: float
    ci_low: float | None
    ci_high: float | None
    detectable: bool | None
    n_valid: int
    n_finite_replicates: int
    b: int
    inconclusive: bool
    reason: SkipReason | None = None


def frozen_block_lengths(
    params: I02Params = DEFAULT_PARAMS,
) -> tuple[int, tuple[int, ...]]:
    return params.b_star, params.b_sensitivity


def _percentile_ci(
    samples: np.ndarray, alpha: float
) -> tuple[float, float]:
    lo = float(np.quantile(samples, alpha / 2.0, method="linear"))
    hi = float(np.quantile(samples, 1.0 - alpha / 2.0, method="linear"))
    return lo, hi


def moving_block_bootstrap_indices(
    n: int,
    b: int,
    B: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """Return bootstrap index arrays of shape ``(B, n)`` (non-circular MBB).

    Block starts drawn uniformly from ``{0, …, n-b}``. Blocks concatenated
    then truncated to length ``n``.
    """

    if n < b:
        raise ValueError("n < b")
    max_start = n - b
    out = np.empty((B, n), dtype=np.intp)
    for r in range(B):
        idx: list[int] = []
        while len(idx) < n:
            start = int(rng.integers(0, max_start + 1))
            idx.extend(range(start, start + b))
        out[r] = np.asarray(idx[:n], dtype=np.intp)
    return out


def mbb_spearman_ci(
    z: np.ndarray,
    r: np.ndarray,
    *,
    b: int,
    params: I02Params = DEFAULT_PARAMS,
    seed: int | None = None,
) -> MBBResult:
    """Percentile CI for Spearman ρ via non-circular MBB on paired series.

    Only finite pairs are kept (time order preserved). If ``n < b``,
    returns inconclusive. Degenerate replicates (undefined ρ) are dropped;
    if fewer than ``ceil(0.8 B)`` finite replicates remain → inconclusive.
    """

    z = np.asarray(z, dtype=np.float64)
    r = np.asarray(r, dtype=np.float64)
    mask = np.isfinite(z) & np.isfinite(r)
    z_v = z[mask]
    r_v = r[mask]
    n = int(z_v.shape[0])
    rho_hat = spearman_rho(z_v, r_v) if n >= 2 else float("nan")

    if n < b:
        return MBBResult(
            rho_hat=rho_hat,
            ci_low=None,
            ci_high=None,
            detectable=None,
            n_valid=n,
            n_finite_replicates=0,
            b=b,
            inconclusive=True,
            reason=SkipReason.BOOTSTRAP_INSUFFICIENT_N,
        )

    seed = params.bootstrap_seed if seed is None else int(seed)
    rng = np.random.default_rng(seed)
    B = params.bootstrap_B
    index_draws = moving_block_bootstrap_indices(n, b, B, rng)

    rhos: list[float] = []
    for row in index_draws:
        rho_star = spearman_rho(z_v[row], r_v[row])
        if np.isfinite(rho_star):
            rhos.append(float(rho_star))

    n_fin = len(rhos)
    min_req = int(np.ceil(0.8 * B))
    if n_fin < min_req:
        return MBBResult(
            rho_hat=rho_hat,
            ci_low=None,
            ci_high=None,
            detectable=None,
            n_valid=n,
            n_finite_replicates=n_fin,
            b=b,
            inconclusive=True,
            reason=SkipReason.BOOTSTRAP_DEGENERATE,
        )

    samples = np.asarray(rhos, dtype=np.float64)
    lo, hi = _percentile_ci(samples, params.alpha)
    detectable = not (lo <= 0.0 <= hi)
    return MBBResult(
        rho_hat=rho_hat,
        ci_low=lo,
        ci_high=hi,
        detectable=detectable,
        n_valid=n,
        n_finite_replicates=n_fin,
        b=b,
        inconclusive=False,
        reason=None,
    )


def mbb_spearman_robustness(
    z: np.ndarray,
    r: np.ndarray,
    *,
    params: I02Params = DEFAULT_PARAMS,
) -> dict[int, MBBResult]:
    """Run identical MBB for each ``b ∈ {20,40,80}``; no best-b selection."""

    return {
        b: mbb_spearman_ci(z, r, b=b, params=params)
        for b in params.b_sensitivity
    }
