"""Synthetic fixtures for I03 L1 (no market data)."""

from __future__ import annotations

import numpy as np
import pytest

from quant.i03.params import DEFAULT_CONFIG, I03Config


@pytest.fixture
def cfg() -> I03Config:
    return DEFAULT_CONFIG


@pytest.fixture
def synthetic_returns() -> np.ndarray:
    """Deterministic returns; index 0 unused (I02/I03 convention).

    Length chosen so each of P=3 blocks can satisfy n_min=250 queries
    after G0 warm-up (M=252) in block 1.
    """

    rng = np.random.default_rng(7)
    n = 2400
    r = np.full(n, np.nan, dtype=np.float64)
    vol = 0.01 + 0.005 * np.sin(np.linspace(0, 12, n - 1))
    r[1:] = rng.normal(0.0, 1.0, size=n - 1) * vol
    return r
