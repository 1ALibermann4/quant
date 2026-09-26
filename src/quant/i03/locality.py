"""Locality validity diagnostics C6-D (I03-PREREG-v0.1 §10).

DIAGNOSTIC — NON-PROMOTIONAL. Not recurrence estimands.

PERF-01 Phase 1A: exact serial kernel optimization (bitwise-equivalent).
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.blocks import TemporalBlock
from quant.i03.emnd import iter_block_query_pools
from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class LocalityBlockDiagnostic:
    """Per-block locality diagnostics."""

    period: int
    Lambda: float
    Gamma: float
    hard_degenerate: bool
    n_queries_used: int


def _query_list(
    block: TemporalBlock,
    x_defined: np.ndarray,
    cfg: I03Config,
) -> list[int]:
    """Admissible query times (ascending). Kept for L1/L2 API compatibility."""

    _, _, queries = iter_block_query_pools(block, x_defined, cfg)
    return [t for t, _ in queries]


def locality_for_block(
    states: np.ndarray,
    x_defined: np.ndarray,
    block: TemporalBlock,
    cfg: I03Config,
    *,
    seed: int,
) -> LocalityBlockDiagnostic:
    """Compute ``Lambda_p``, ``Gamma_p`` with prereg RNG stream."""

    _, _, queries = iter_block_query_pools(block, x_defined, cfg)
    rng = np.random.default_rng(seed)
    lambdas: list[float] = []
    gammas: list[float] = []
    hard = False

    for t, pool in queries:  # increasing order already
        qx = states[t]
        diff = states[pool] - qx
        dists = np.sqrt(np.sum(diff * diff, axis=1))
        order = np.lexsort((pool, dists))
        sorted_d = dists[order]
        d1 = float(sorted_d[0])
        d_kmax = float(sorted_d[cfg.k_max - 1])
        if d1 <= 0.0:
            hard = True
            lambdas.append(float("inf"))
            gammas.append(0.0)
            continue
        m = min(cfg.m_rand, pool.size)
        if pool.size <= m:
            sample = pool
        else:
            sample = rng.choice(pool, size=m, replace=False)
        sdiff = states[sample] - qx
        d_rand = float(np.mean(np.sqrt(np.sum(sdiff * sdiff, axis=1))))
        if d_rand <= 0.0:
            hard = True
            lambdas.append(float("inf"))
        else:
            lambdas.append(d1 / d_rand)
        gammas.append((d_kmax - d1) / d1)

    if not lambdas:
        return LocalityBlockDiagnostic(
            period=block.period,
            Lambda=float("nan"),
            Gamma=float("nan"),
            hard_degenerate=True,
            n_queries_used=0,
        )

    Lam = float(np.median(np.asarray(lambdas, dtype=np.float64)))
    Gam = float(np.median(np.asarray(gammas, dtype=np.float64)))
    if Lam >= 1.0:
        hard = True
    return LocalityBlockDiagnostic(
        period=block.period,
        Lambda=Lam,
        Gamma=Gam,
        hard_degenerate=hard,
        n_queries_used=len(queries),
    )


def locality_validity_ok(
    observed: tuple[LocalityBlockDiagnostic, ...],
    n4_surrogate_locality: list[tuple[LocalityBlockDiagnostic, ...]],
) -> bool:
    """Predicate ``V`` (prereg §10.2)."""

    if not observed:
        return False
    for obs in observed:
        p = obs.period
        if obs.hard_degenerate or not np.isfinite(obs.Lambda) or not np.isfinite(obs.Gamma):
            return False
        if obs.Lambda >= 1.0:
            return False
        gam_s = []
        lam_s = []
        for bat in n4_surrogate_locality:
            for d in bat:
                if d.period == p:
                    gam_s.append(d.Gamma)
                    lam_s.append(d.Lambda)
                    break
        if not gam_s:
            return False
        med_g = float(np.median(np.asarray(gam_s, dtype=np.float64)))
        med_l = float(np.median(np.asarray(lam_s, dtype=np.float64)))
        if obs.Gamma <= med_g and obs.Lambda >= med_l:
            return False
    return True
