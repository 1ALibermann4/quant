"""Synthetic series for I01 component tests."""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pytest

from quant.i01.observations import ObservationSeries
from quant.i01.params import I01Params


@pytest.fixture
def small_params() -> I01Params:
    return I01Params(W=4, M=8, epsilon=1e-8, h=3, k=3, tau=3, L_min=3, B0_R=7, B0_seed=42)


def _weekdays(n: int, start: date = date(2000, 1, 3)) -> tuple[date, ...]:
    days: list[date] = []
    cursor = start
    while len(days) < n:
        if cursor.weekday() < 5:
            days.append(cursor)
        cursor += timedelta(days=1)
    return tuple(days)


@pytest.fixture
def small_series(small_params: I01Params) -> ObservationSeries:
    rng = np.random.default_rng(0)
    n = 48
    log_p = np.cumsum(rng.normal(0.0, 0.01, size=n))
    prices = 100.0 * np.exp(log_p - log_p[0])
    return ObservationSeries(sessions=_weekdays(n), adjusted_price=tuple(float(p) for p in prices))


@pytest.fixture
def leak_series() -> ObservationSeries:
    """Quiet history then a violent jump — a leak would see the jump early."""

    n = 80
    prices = [100.0] * 50 + [100.0 * (1.1**i) for i in range(1, n - 50 + 1)]
    return ObservationSeries(sessions=_weekdays(n), adjusted_price=tuple(prices))
