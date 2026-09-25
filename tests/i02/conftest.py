"""Synthetic fixtures for I02 L1 (no market data)."""

from __future__ import annotations

import numpy as np
import pytest

from quant.i02.params import DEFAULT_PARAMS, I02Params


@pytest.fixture
def params() -> I02Params:
    return DEFAULT_PARAMS


@pytest.fixture
def synthetic_returns() -> np.ndarray:
    """Long enough for M=252, W=20, h=10, k=50 with non-zero RV.

    Deterministic PRNG; no market data.
    """

    rng = np.random.default_rng(0)
    n = 800
    r = np.full(n, np.nan, dtype=np.float64)
    r[1:] = rng.normal(0.0, 0.01, size=n - 1)
    return r


@pytest.fixture
def constant_abs_returns() -> np.ndarray:
    """All |r| equal after index 0 → Q=1 when defined; useful edge cases."""

    n = 400
    r = np.full(n, np.nan, dtype=np.float64)
    r[1:] = 0.01
    return r
