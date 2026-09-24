"""L2 geometric neighborhood. Selection is a function of ``X`` only (AF-08)."""

from __future__ import annotations

import numpy as np


def pairwise_l2(a: np.ndarray, b: np.ndarray) -> np.ndarray:
    """Euclidean distances between each row of ``a`` and each row of ``b``.

    Args:
        a: Shape ``(n, d)``.
        b: Shape ``(m, d)``.

    Returns:
        Array of shape ``(n, m)``.
    """

    a = np.asarray(a, dtype=np.float64)
    b = np.asarray(b, dtype=np.float64)
    a_norm = np.sum(a * a, axis=1)
    b_norm = np.sum(b * b, axis=1)
    d2 = a_norm[:, None] + b_norm[None, :] - 2.0 * (a @ b.T)
    return np.sqrt(np.maximum(d2, 0.0))


def l2_neighbors(
    x_t: np.ndarray,
    states: np.ndarray,
    library: np.ndarray,
    k: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Select ``k`` nearest library ranks to ``x_t``.

    Ties break toward the **oldest** session (smallest rank). ``Y`` is not used.

    Returns:
        ``(neighbor_ranks, distances)`` each of length ``k``, nearest first.
    """

    if library.shape[0] < k:
        raise ValueError(f"library size {library.shape[0]} < k={k}")
    distances = pairwise_l2(x_t.reshape(1, -1), states[library])[0]
    order = np.lexsort((library, distances))
    chosen = order[:k]
    return library[chosen], distances[chosen]
