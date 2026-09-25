"""E-MND primary estimand (I03-PREREG-v0.1 §6)."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.blocks import TemporalBlock
from quant.i03.g0 import euclidean_distance
from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class EMNDBlockResult:
    """E-MND results for one block across all k."""

    period: int
    n_queries: int
    n_skipped_undefined_x: int
    n_skipped_insufficient_pool: int
    theta_by_k: dict[int, float]  # k -> Theta_k(p)


def admissible_pool(
    t: int,
    block: TemporalBlock,
    x_defined: np.ndarray,
    cfg: I03Config,
) -> np.ndarray:
    """Intra-block τ-separated indices with X defined (prereg §6.1)."""

    tau = cfg.tau
    members = block.indices
    # |t-s| >= tau and X_s defined
    mask = (np.abs(members.astype(np.int64) - t) >= tau) & x_defined[members]
    return members[mask]


def kth_distance(
    query_x: np.ndarray,
    pool: np.ndarray,
    states: np.ndarray,
    k: int,
) -> float:
    """k-th smallest Euclidean distance with ties broken by s ascending.

    Returns the distance value ``d_(k)`` (1-based k as in prereg).
    """

    if pool.size < k:
        raise ValueError("pool smaller than k")
    # Build (distance, s) and sort
    pairs: list[tuple[float, int]] = []
    for s in pool:
        d = euclidean_distance(query_x, states[s])
        pairs.append((d, int(s)))
    pairs.sort(key=lambda x: (x[0], x[1]))
    return pairs[k - 1][0]


def compute_emnd_block(
    states: np.ndarray,
    x_defined: np.ndarray,
    block: TemporalBlock,
    cfg: I03Config,
) -> EMNDBlockResult:
    """Compute ``Theta_k(p)`` for all ``k in K`` on one block."""

    n_skip_x = 0
    n_skip_pool = 0
    # Collect delta_k per query
    deltas: dict[int, list[float]] = {k: [] for k in cfg.K}

    for t in block.indices:
        if not x_defined[t]:
            n_skip_x += 1
            continue
        pool = admissible_pool(int(t), block, x_defined, cfg)
        if pool.size < cfg.k_max:
            n_skip_pool += 1
            continue
        qx = states[t]
        # Vectorized distances; ties: distance↑ then s↑ via lexsort
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

    return EMNDBlockResult(
        period=block.period,
        n_queries=n_queries,
        n_skipped_undefined_x=n_skip_x,
        n_skipped_insufficient_pool=n_skip_pool,
        theta_by_k=theta_by_k,
    )


def compute_emnd_all(
    states: np.ndarray,
    x_defined: np.ndarray,
    blocks: tuple[TemporalBlock, ...],
    cfg: I03Config,
) -> tuple[EMNDBlockResult, ...]:
    """E-MND for every block."""

    return tuple(compute_emnd_block(states, x_defined, b, cfg) for b in blocks)
