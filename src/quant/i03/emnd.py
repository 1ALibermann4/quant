"""E-MND primary estimand (I03-PREREG-v0.1 §6).

PERF-01 Phase 1A: exact serial kernel optimization (bitwise-equivalent).
"""

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
    *,
    members_i64: np.ndarray | None = None,
    defined_on_members: np.ndarray | None = None,
) -> np.ndarray:
    """Intra-block τ-separated indices with X defined (prereg §6.1)."""

    tau = cfg.tau
    members = block.indices if members_i64 is None else members_i64
    if members_i64 is None:
        members = np.asarray(members, dtype=np.int64)
    defined = (
        defined_on_members
        if defined_on_members is not None
        else np.asarray(x_defined[block.indices], dtype=bool)
    )
    mask = (np.abs(members - int(t)) >= tau) & defined
    # Always index the canonical block.indices so dtype/identity match reference.
    return block.indices[mask]


def _block_member_views(
    block: TemporalBlock, x_defined: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    """Per-block index views: members_i64, defined_on_members."""

    members_i64 = np.asarray(block.indices, dtype=np.int64)
    defined_on_members = np.asarray(x_defined[block.indices], dtype=bool)
    return members_i64, defined_on_members


def iter_block_query_pools(
    block: TemporalBlock,
    x_defined: np.ndarray,
    cfg: I03Config,
) -> tuple[int, int, list[tuple[int, np.ndarray]]]:
    """Enumerate admissible E-MND/locality queries in ascending ``t``.

    Returns ``(n_skipped_undefined_x, n_skipped_insufficient_pool, queries)``
    where ``queries`` is a list of ``(t, pool)`` with ``pool.size >= k_max``.
    """

    tau = cfg.tau
    k_max = cfg.k_max
    members_i64, defined_on_members = _block_member_views(block, x_defined)
    members = block.indices
    n_skip_x = 0
    n_skip_pool = 0
    queries: list[tuple[int, np.ndarray]] = []

    for i in range(members_i64.size):
        if not defined_on_members[i]:
            n_skip_x += 1
            continue
        t = int(members_i64[i])
        mask = (np.abs(members_i64 - t) >= tau) & defined_on_members
        pool = members[mask]
        if pool.size < k_max:
            n_skip_pool += 1
            continue
        queries.append((t, pool))
    return n_skip_x, n_skip_pool, queries


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
    pairs: list[tuple[float, int]] = []
    for s in pool:
        d = euclidean_distance(query_x, states[s])
        pairs.append((d, int(s)))
    pairs.sort(key=lambda x: (x[0], x[1]))
    return pairs[k - 1][0]


def _sorted_pool_distances(
    qx: np.ndarray, pool: np.ndarray, states: np.ndarray
) -> np.ndarray:
    """Distances sorted by (dist↑, s↑) — same formula as pre-PERF-01 kernel."""

    diff = states[pool] - qx
    dists = np.sqrt(np.sum(diff * diff, axis=1))
    order = np.lexsort((pool, dists))
    return dists[order]


def compute_emnd_block(
    states: np.ndarray,
    x_defined: np.ndarray,
    block: TemporalBlock,
    cfg: I03Config,
) -> EMNDBlockResult:
    """Compute ``Theta_k(p)`` for all ``k in K`` on one block."""

    n_skip_x, n_skip_pool, queries = iter_block_query_pools(block, x_defined, cfg)
    K = cfg.K
    deltas: dict[int, list[float]] = {k: [] for k in K}

    for t, pool in queries:
        sorted_d = _sorted_pool_distances(states[t], pool, states)
        for k in K:
            deltas[k].append(float(sorted_d[k - 1]))

    n_queries = len(queries)
    theta_by_k: dict[int, float] = {}
    for k in K:
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
