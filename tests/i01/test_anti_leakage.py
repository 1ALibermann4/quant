"""Anti-leakage tests. A deliberate leak must be detectable on the synthetic series."""

from __future__ import annotations

from datetime import date, timedelta

import numpy as np
import pytest

from quant.i01.candidates import admissible_candidates, evaluation_indices
from quant.i01.futures import future_vector
from quant.i01.observations import ObservationSeries
from quant.i01.params import I01Params
from quant.i01.returns import log_returns
from quant.i01.standardization import causal_mu_sigma, standardize_window
from quant.i01.states import state_vector


def _truncate(series: ObservationSeries, last_inclusive: int) -> ObservationSeries:
    return ObservationSeries(
        sessions=series.sessions[: last_inclusive + 1],
        adjusted_price=series.adjusted_price[: last_inclusive + 1],
    )


def leaky_standardize_uses_future(
    returns: np.ndarray, t: int, params: I01Params
) -> np.ndarray:
    """Incorrect implementation: μ/σ window includes ``r_{t+1}``."""

    start = t - params.M + 2
    window = returns[start : t + 2]
    mu = float(np.mean(window))
    sigma = float(np.std(window, ddof=1))
    x_start = t - params.W + 1
    body = returns[x_start : t + 1]
    return (body - mu) / (sigma + params.epsilon)


def test_x_t_identical_on_truncated_series(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    t = 20
    full = state_vector(log_returns(leak_series), t, params)
    truncated = state_vector(log_returns(_truncate(leak_series, t)), t, params)
    np.testing.assert_allclose(full, truncated)


def test_standardization_does_not_read_past_t(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    r = log_returns(leak_series)
    t = 20
    _mu, _sigma = causal_mu_sigma(r, t, params)
    x = standardize_window(r, t, params)
    r_poisoned = r.copy()
    r_poisoned[t + 1 :] = 50.0
    x_poisoned = standardize_window(r_poisoned, t, params)
    np.testing.assert_allclose(x, x_poisoned)


def test_detector_catches_leaky_standardization(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    r = log_returns(leak_series)
    t = 49  # last flat price; r_{t+1} is the first jump
    clean = standardize_window(r, t, params)
    leaked = leaky_standardize_uses_future(r, t, params)
    assert not np.allclose(clean, leaked)


def test_candidate_time_strictly_before_query(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    for t in evaluation_indices(len(leak_series), params):
        library = admissible_candidates(int(t), len(leak_series), params)
        assert np.all(library < t), "candidate_time < query_time"


def test_candidate_future_end_leq_query_cutoff(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    for t in evaluation_indices(len(leak_series), params):
        library = admissible_candidates(int(t), len(leak_series), params)
        future_end = library + params.h
        assert np.all(future_end <= t), "candidate.future_end <= query.information_cutoff"


def test_y_t_uses_only_future_returns(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    r = log_returns(leak_series)
    t = 20
    y = future_vector(r, t, params)
    assert y[0] == pytest.approx(r[t + 1])
    poisoned = r.copy()
    poisoned[: t + 1] = 0.0
    y2 = future_vector(poisoned, t, params)
    np.testing.assert_array_equal(y, y2)


def test_no_shared_return_in_x_windows(leak_series: ObservationSeries) -> None:
    params = I01Params(W=4, M=8, h=3, k=3, tau=3, L_min=3, B0_R=2)
    t = int(evaluation_indices(len(leak_series), params)[0])
    for s in admissible_candidates(t, len(leak_series), params):
        query = set(range(t - params.W + 1, t + 1))
        cand = set(range(int(s) - params.W + 1, int(s) + 1))
        assert query.isdisjoint(cand)


def test_weekday_construction_is_not_a_calendar_authority() -> None:
    """The synthetic fixture uses weekdays for convenience, not as NYSE truth."""

    sessions = []
    cursor = date(2000, 1, 3)
    while len(sessions) < 5:
        if cursor.weekday() < 5:
            sessions.append(cursor)
        cursor += timedelta(days=1)
    series = ObservationSeries(sessions=tuple(sessions), adjusted_price=(1.0, 1.1, 1.2, 1.3, 1.4))
    assert len(series) == 5
