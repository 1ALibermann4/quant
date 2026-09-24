"""Homogeneity measures ``H_raw``, ``H_vol``, ``H_shape`` (DEC-03).

These functions return numbers. They do not emit a SCI verdict.
"""

from __future__ import annotations

import numpy as np

from quant.i01.neighbors import pairwise_l2


def _upper_mean(distance_matrix: np.ndarray) -> float:
    k = distance_matrix.shape[0]
    if k < 2:
        raise ValueError("homogeneity requires k >= 2")
    iu = np.triu_indices(k, k=1)
    return float(distance_matrix[iu].mean())


def h_raw(futures: np.ndarray) -> float:
    """Mean pairwise L2 of raw future vectors.

    ``H_raw(N) = 2/(k(k-1)) Σ_{i<j} ||Y_i - Y_j||_2``.
    """

    return _upper_mean(pairwise_l2(futures, futures))


def h_vol(futures: np.ndarray) -> float:
    """Sample variance (``ddof=1``) of future amplitudes ``||Y_j||_2``."""

    amplitudes = np.linalg.norm(futures, axis=1)
    return float(np.var(amplitudes, ddof=1))


def h_shape(futures: np.ndarray, epsilon: float) -> float:
    """Mean pairwise L2 of amplitude-normalized futures."""

    norms = np.linalg.norm(futures, axis=1, keepdims=True)
    hat = futures / (norms + epsilon)
    return _upper_mean(pairwise_l2(hat, hat))


def homogeneity_bundle(futures: np.ndarray, epsilon: float) -> dict[str, float]:
    """Return ``H_raw``, ``H_vol``, ``H_shape`` for one neighborhood."""

    return {
        "H_raw": h_raw(futures),
        "H_vol": h_vol(futures),
        "H_shape": h_shape(futures, epsilon),
    }


def batch_homogeneity(samples: np.ndarray, epsilon: float) -> dict[str, np.ndarray]:
    """Vectorized ``H_*`` over a batch of neighborhoods.

    Args:
        samples: Shape ``(R, k, dim)``.
        epsilon: Shape-normalization floor.

    Returns:
        Mapping of metric name to length-``R`` arrays.
    """

    if samples.ndim != 3:
        raise ValueError("samples must have shape (R, k, dim)")
    _r, k, _dim = samples.shape
    if k < 2:
        raise ValueError("homogeneity requires k >= 2")
    norms2 = np.sum(samples * samples, axis=2)
    gram = np.matmul(samples, np.swapaxes(samples, 1, 2))
    raw = np.sqrt(np.maximum(norms2[:, :, None] + norms2[:, None, :] - 2.0 * gram, 0.0))
    iu = np.triu_indices(k, k=1)
    h_raw_b = raw[:, iu[0], iu[1]].mean(axis=1)
    amplitudes = np.sqrt(norms2)
    h_vol_b = amplitudes.var(axis=1, ddof=1)
    hat = samples / (amplitudes[:, :, None] + epsilon)
    hat_n2 = np.sum(hat * hat, axis=2)
    hat_g = np.matmul(hat, np.swapaxes(hat, 1, 2))
    shp = np.sqrt(np.maximum(hat_n2[:, :, None] + hat_n2[:, None, :] - 2.0 * hat_g, 0.0))
    h_shape_b = shp[:, iu[0], iu[1]].mean(axis=1)
    return {"H_raw": h_raw_b, "H_vol": h_vol_b, "H_shape": h_shape_b}
