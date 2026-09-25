"""IAAFT surrogate generator (I03-PREREG-v0.1 §9).

Approximately preserves power spectrum and amplitude marginal.
Does not claim exact preservation.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True, slots=True)
class IAAFTResult:
    """One IAAFT surrogate."""

    series: np.ndarray
    converged: bool
    iterations: int


def _power_spectrum(x: np.ndarray) -> np.ndarray:
    """Periodogram magnitudes from rFFT (length of rfft output)."""

    return np.abs(np.fft.rfft(x))


def iaaft(
    series: np.ndarray,
    *,
    seed: int,
    I_max: int = 100,
    eps: float = 1e-8,
) -> IAAFTResult:
    """Iterative amplitude-adjusted Fourier transform surrogate.

    Init: random shuffle of ``series`` (seeded).
    Each iteration: (1) impose original spectrum amplitudes via rFFT;
    (2) impose original amplitude ranks.
    Convergence: max relative change of sorted amplitudes and of spectrum
    bins both ``< eps``.
    """

    x0 = np.asarray(series, dtype=np.float64).copy()
    n = x0.size
    if n == 0:
        return IAAFTResult(series=x0, converged=True, iterations=0)

    # Exclude unused index-0 padding from IAAFT science domain if present:
    # caller passes the full array; we transform the entire length-T vector
    # as prereg §9.1 ("full analysis return series").
    sorted_amp = np.sort(x0)
    target_mag = _power_spectrum(x0)

    rng = np.random.default_rng(seed)
    y = rng.permutation(x0)
    converged = False
    it = 0
    prev_sorted = np.sort(y)
    prev_mag = _power_spectrum(y)

    for it in range(1, I_max + 1):
        # Spectral step
        y_fft = np.fft.rfft(y)
        mag = np.abs(y_fft)
        # avoid div by zero
        scale = np.ones_like(mag)
        nonzero = mag > 0
        scale[nonzero] = target_mag[nonzero] / mag[nonzero]
        y_fft = y_fft * scale
        y = np.fft.irfft(y_fft, n=n)

        # Amplitude rank step
        ranks = np.argsort(np.argsort(y))
        y = sorted_amp[ranks]

        cur_sorted = np.sort(y)
        cur_mag = _power_spectrum(y)

        # Relative changes
        denom_a = np.maximum(np.abs(prev_sorted), 1e-15)
        denom_m = np.maximum(np.abs(prev_mag), 1e-15)
        da = float(np.max(np.abs(cur_sorted - prev_sorted) / denom_a))
        dm = float(np.max(np.abs(cur_mag - prev_mag) / denom_m))
        if da < eps and dm < eps:
            converged = True
            break
        prev_sorted = cur_sorted
        prev_mag = cur_mag

    return IAAFTResult(series=y, converged=converged, iterations=it)
