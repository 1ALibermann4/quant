"""Deterministic k-NN with tie-break ``(distance ↑, s ↑)``."""

from __future__ import annotations

import numpy as np


def select_neighbors(
    library: np.ndarray,
    distances: np.ndarray,
    k: int,
) -> tuple[np.ndarray, np.ndarray]:
    """Select exactly ``k`` neighbors from ``library``.

    Tie policy (prereg §0): ascending distance, then ascending session
    index ``s``. Uniform weights ``1/k`` are applied by the forecast
    layer (not here).

    Returns:
        ``(neighbor_ranks, distances)`` each length ``k``, nearest first.
    """

    library = np.asarray(library, dtype=np.intp)
    distances = np.asarray(distances, dtype=np.float64)
    if library.shape[0] != distances.shape[0]:
        raise ValueError("library and distances length mismatch")
    if library.shape[0] < k:
        raise ValueError(
            f"library size {library.shape[0]} < k={k} "
            "(caller must skip when |A_t| < k)"
        )
    order = np.lexsort((library, distances))
    chosen = order[:k]
    return library[chosen], distances[chosen]
