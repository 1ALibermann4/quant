"""Frozen Phase-1A reference oracles for E-MND / locality (test-only).

Exact copy of the pre-PERF-01 serial kernels. Production must not import this
for runtime paths — tests compare REFERENCE vs OPTIMIZED.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.blocks import TemporalBlock
from quant.i03.g0 import euclidean_distance
from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class RefEMNDBlockResult:
    period: int
    n_queries: int
    n_skipped_undefined_x: int
    n_skipped_insufficient_pool: int
    theta_by_k: dict[int, float]


@dataclass(frozen=True, slots=True)
class RefLocalityBlockDiagnostic:
    period: int
    Lambda: float
    Gamma: float
    hard_degenerate: bool
    n_queries_used: int


def ref_admissible_pool(
    t: int,
    block: TemporalBlock,
    x_defined: np.ndarray,
    cfg: I03Config,
) -> np.ndarray:
    tau = cfg.tau
    members = block.indices
    mask = (np.abs(members.astype(np.int64) - t) >= tau) & x_defined[members]
    return members[mask]


def ref_compute_emnd_block(
    states: np.ndarray,
    x_defined: np.ndarray,
    block: TemporalBlock,
    cfg: I03Config,
) -> RefEMNDBlockResult:
    n_skip_x = 0
    n_skip_pool = 0
    deltas: dict[int, list[float]] = {k: [] for k in cfg.K}

    for t in block.indices:
        if not x_defined[t]:
            n_skip_x += 1
            continue
        pool = ref_admissible_pool(int(t), block, x_defined, cfg)
        if pool.size < cfg.k_max:
            n_skip_pool += 1
            continue
        qx = states[t]
        diff = states[pool] - qx
        dists = np.sqrt(np.sum(diff * diff, axis=1))
        order = np.lexsort((pool, dists))
        sorted_d = dists[order]
        for k in cfg.K:
            deltas[k].append(float(sorted_d[k - 1]))

    n_queries = len(deltas[cfg.K[0]])
    theta_by_k: dict[int, float] = {}
    for k in cfg.K:
        if n_queries == 0:
            theta_by_k[k] = float("nan")
        else:
            theta_by_k[k] = float(np.mean(np.asarray(deltas[k], dtype=np.float64)))

    return RefEMNDBlockResult(
        period=block.period,
        n_queries=n_queries,
        n_skipped_undefined_x=n_skip_x,
        n_skipped_insufficient_pool=n_skip_pool,
        theta_by_k=theta_by_k,
    )


def ref_compute_emnd_all(
    states: np.ndarray,
    x_defined: np.ndarray,
    blocks: tuple[TemporalBlock, ...],
    cfg: I03Config,
) -> tuple[RefEMNDBlockResult, ...]:
    return tuple(ref_compute_emnd_block(states, x_defined, b, cfg) for b in blocks)


def ref_query_list(
    block: TemporalBlock,
    x_defined: np.ndarray,
    cfg: I03Config,
) -> list[int]:
    out: list[int] = []
    for t in block.indices:
        if not x_defined[t]:
            continue
        pool = ref_admissible_pool(int(t), block, x_defined, cfg)
        if pool.size >= cfg.k_max:
            out.append(int(t))
    return out


def ref_locality_for_block(
    states: np.ndarray,
    x_defined: np.ndarray,
    block: TemporalBlock,
    cfg: I03Config,
    *,
    seed: int,
) -> RefLocalityBlockDiagnostic:
    queries = ref_query_list(block, x_defined, cfg)
    rng = np.random.default_rng(seed)
    lambdas: list[float] = []
    gammas: list[float] = []
    hard = False

    for t in queries:
        pool = ref_admissible_pool(t, block, x_defined, cfg)
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
        return RefLocalityBlockDiagnostic(
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
    return RefLocalityBlockDiagnostic(
        period=block.period,
        Lambda=Lam,
        Gamma=Gam,
        hard_degenerate=hard,
        n_queries_used=len(queries),
    )
