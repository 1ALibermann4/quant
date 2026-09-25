"""N4 volatility-preserving surrogate (I03-PREREG-v0.1 §8).

CRITICAL SEMANTICS
==================
N4 preserves **by construction** the path ``sigma_hat_t`` computed on the
**observed** return series. Surrogate returns are

    r*_t = sigma_hat_t(obs) * z*_t

Recomputing sample stdev on ``r*`` is **not** required to recover the same
path and must not be claimed as preserved.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class N4ScalePath:
    """Observed N4 scale path and residual domain."""

    sigma: np.ndarray  # float; NaN where undefined
    z: np.ndarray  # float; NaN where not in Z
    Z_indices: np.ndarray  # intp indices in Z
    T: int
    valid: bool
    invalid_reason: str | None


def n4_sigma_at(returns: np.ndarray, t: int, cfg: I03Config) -> float | None:
    """Causal sample stdev on ``[t-W_sigma+1, t]``, denominator ``W_sigma-1``.

    Returns ``None`` if warm-up incomplete. Returns ``0.0`` if window constant.
    Distinct from I02 RMS ``RV_t``.
    """

    W = cfg.W_sigma
    start = t - W + 1
    # I02/I03 indexing: scientific returns start at index 1
    if start < 1 or t >= len(returns):
        return None
    window = np.asarray(returns[start : t + 1], dtype=np.float64)
    if window.shape[0] != W or np.isnan(window).any():
        return None
    return float(np.std(window, ddof=1))


def build_n4_scale_path(returns: np.ndarray, cfg: I03Config) -> N4ScalePath:
    """Compute ``sigma_hat``, ``z``, and validity flags on observed returns."""

    T = len(returns)
    sigma = np.full(T, np.nan, dtype=np.float64)
    z = np.full(T, np.nan, dtype=np.float64)
    Z_list: list[int] = []
    for t in range(T):
        s = n4_sigma_at(returns, t, cfg)
        if s is None:
            continue
        sigma[t] = s
        if s > 0.0:
            z[t] = float(returns[t]) / s
            Z_list.append(t)
    Z_indices = np.asarray(Z_list, dtype=np.intp)
    invalid_reason = None
    valid = True
    if T == 0 or (len(Z_indices) / T) < cfg.n4_z_frac_min:
        valid = False
        invalid_reason = "N4_Z_FRAC"
    elif len(Z_indices) > 0:
        sig_z = sigma[Z_indices]
        if float(np.var(sig_z)) == 0.0:
            valid = False
            invalid_reason = "N4_SIGMA_VAR_ZERO"
    else:
        valid = False
        invalid_reason = "N4_Z_EMPTY"
    return N4ScalePath(
        sigma=sigma,
        z=z,
        Z_indices=Z_indices,
        T=T,
        valid=valid,
        invalid_reason=invalid_reason,
    )


def n4_surrogate_returns(
    returns: np.ndarray,
    scale: N4ScalePath,
    b: int,
    cfg: I03Config,
) -> np.ndarray:
    """Build one N4 surrogate return path for replicate ``b`` (1..B).

    Seed: ``42 + b`` per prereg §8.5.
    """

    if b < 1:
        raise ValueError("surrogate index b is 1-based")
    rng = np.random.default_rng(cfg.master_seed + b)
    r_star = np.array(returns, dtype=np.float64, copy=True)
    Z = scale.Z_indices
    if Z.size == 0:
        return r_star
    z_vals = scale.z[Z].copy()
    perm = rng.permutation(Z.size)
    z_star = z_vals[perm]
    # Map: position i in Z gets z from permuted order
    for i, t in enumerate(Z):
        r_star[t] = scale.sigma[t] * z_star[i]
    # t not in Z: already copied from returns
    return r_star


def generate_n4_battery(
    returns: np.ndarray,
    cfg: I03Config,
    B: int | None = None,
) -> tuple[N4ScalePath, list[np.ndarray]]:
    """Generate N4 surrogate return series.

    ``B`` defaults to ``cfg.B_N4``. Tests may pass a smaller ``B``; production
    entrypoints must omit ``B`` so the frozen size is used.
    """

    scale = build_n4_scale_path(returns, cfg)
    n = cfg.B_N4 if B is None else int(B)
    if n < 1:
        raise ValueError("B must be positive")
    surrogates = [n4_surrogate_returns(returns, scale, b, cfg) for b in range(1, n + 1)]
    return scale, surrogates
