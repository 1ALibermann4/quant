"""Soft-DTW kernels for I04-CAL G1.

Reference pure-Python implementation preserved for numerical qualification.
Optional Numba JIT path must match reference within float64 contract.
"""

from __future__ import annotations

import math

import numpy as np

_HAS_NUMBA = False
try:
    from numba import njit

    _HAS_NUMBA = True
except ImportError:  # pragma: no cover
    njit = None  # type: ignore[assignment]


def softmin3(r0: float, r1: float, r2: float, gamma: float) -> float:
    """Numerically stable softmin of three values."""
    m = r0
    if r1 < m:
        m = r1
    if r2 < m:
        m = r2
    return float(
        -gamma
        * math.log(
            math.exp(-(r0 - m) / gamma)
            + math.exp(-(r1 - m) / gamma)
            + math.exp(-(r2 - m) / gamma)
        )
        - m
    )


def soft_dtw_ref(x: np.ndarray, y: np.ndarray, gamma: float, band: int | None = None) -> float:
    """Reference Soft-DTW (Sakoe-Chiba band). Scientific contract implementation."""
    x = np.asarray(x, dtype=np.float64)
    y = np.asarray(y, dtype=np.float64)
    n, m = x.size, y.size
    if band is None:
        band = max(2, max(n, m) // 4)
    R = np.full((n + 2, m + 2), np.inf, dtype=np.float64)
    R[0, 0] = 0.0
    for i in range(1, n + 1):
        j0 = max(1, i - band)
        j1 = min(m, i + band)
        xi = x[i - 1]
        for j in range(j0, j1 + 1):
            cost = (xi - y[j - 1]) ** 2
            R[i, j] = cost + softmin3(R[i - 1, j], R[i, j - 1], R[i - 1, j - 1], gamma)
    return float(R[n, m])


if _HAS_NUMBA:

    @njit(cache=True)
    def _softmin3_jit(r0: float, r1: float, r2: float, gamma: float) -> float:
        m = r0
        if r1 < m:
            m = r1
        if r2 < m:
            m = r2
        return (
            -gamma
            * math.log(
                math.exp(-(r0 - m) / gamma)
                + math.exp(-(r1 - m) / gamma)
                + math.exp(-(r2 - m) / gamma)
            )
            - m
        )

    @njit(cache=True)
    def _soft_dtw_jit(x: np.ndarray, y: np.ndarray, gamma: float, band: int) -> float:
        n = x.shape[0]
        m = y.shape[0]
        R = np.empty((n + 2, m + 2), dtype=np.float64)
        for i in range(n + 2):
            for j in range(m + 2):
                R[i, j] = np.inf
        R[0, 0] = 0.0
        for i in range(1, n + 1):
            j0 = i - band
            if j0 < 1:
                j0 = 1
            j1 = i + band
            if j1 > m:
                j1 = m
            xi = x[i - 1]
            for j in range(j0, j1 + 1):
                cost = (xi - y[j - 1]) * (xi - y[j - 1])
                R[i, j] = cost + _softmin3_jit(
                    R[i - 1, j], R[i, j - 1], R[i - 1, j - 1], gamma
                )
        return R[n, m]

else:  # pragma: no cover

    def _soft_dtw_jit(x, y, gamma, band):  # type: ignore[misc]
        raise RuntimeError("numba not available")


def soft_dtw(
    x: np.ndarray,
    y: np.ndarray,
    gamma: float,
    band: int | None = None,
    *,
    backend: str = "auto",
) -> float:
    """Soft-DTW with optional Sakoe-Chiba band.

    backend:
      - \"ref\": pure Python reference
      - \"numba\": JIT path (requires numba)
      - \"auto\": numba if available else ref
    """
    x = np.ascontiguousarray(np.asarray(x, dtype=np.float64))
    y = np.ascontiguousarray(np.asarray(y, dtype=np.float64))
    n, m = x.size, y.size
    if band is None:
        band = max(2, max(n, m) // 4)
    if backend == "ref" or (backend == "auto" and not _HAS_NUMBA):
        return soft_dtw_ref(x, y, gamma, band)
    if backend in ("numba", "auto"):
        if not _HAS_NUMBA:
            raise RuntimeError("numba backend requested but numba is not installed")
        return float(_soft_dtw_jit(x, y, float(gamma), int(band)))
    raise ValueError(f"unknown soft_dtw backend: {backend}")


# Self-term cache (representation-local; deterministic within process)
_SDTW_SELF_CACHE: dict[tuple[bytes, float], float] = {}


def clear_sdtw_self_cache() -> None:
    _SDTW_SELF_CACHE.clear()


def _sdtw_self_term(x: np.ndarray, gamma: float) -> float:
    key = (x.tobytes(), float(gamma))
    if key not in _SDTW_SELF_CACHE:
        _SDTW_SELF_CACHE[key] = soft_dtw(x, x, gamma)
    return _SDTW_SELF_CACHE[key]


def soft_dtw_divergence(x: np.ndarray, y: np.ndarray, gamma: float) -> float:
    """Soft-DTW divergence with cached self-terms."""
    return (
        soft_dtw(x, y, gamma)
        - 0.5 * _sdtw_self_term(x, gamma)
        - 0.5 * _sdtw_self_term(y, gamma)
    )
