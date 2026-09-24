"""Independent component tests for the I01 core."""

from __future__ import annotations

import math

import numpy as np
import pytest

from quant.i01.candidates import admissible_candidates, evaluation_indices
from quant.i01.futures import future_vector
from quant.i01.homogeneity import h_raw, h_shape, h_vol
from quant.i01.neighbors import l2_neighbors, pairwise_l2
from quant.i01.observations import ObservationSeries
from quant.i01.params import I01Params
from quant.i01.pipeline import run_geometry
from quant.i01.returns import log_returns
from quant.i01.standardization import causal_mu_sigma, standardize_window
from quant.i01.states import state_vector


def test_log_returns_match_definition(small_series: ObservationSeries) -> None:
    r = log_returns(small_series)
    prices = np.asarray(small_series.adjusted_price)
    assert math.isnan(r[0])
    np.testing.assert_allclose(r[1:], np.log(prices[1:] / prices[:-1]))


def test_standardization_window_length(small_series: ObservationSeries, small_params: I01Params) -> None:
    r = log_returns(small_series)
    t = small_params.M
    x = standardize_window(r, t, small_params)
    assert x.shape == (small_params.W,)
    mu, sigma = causal_mu_sigma(r, t, small_params)
    expected = (r[t - small_params.W + 1 : t + 1] - mu) / (sigma + small_params.epsilon)
    np.testing.assert_allclose(x, expected)


def test_future_starts_at_t_plus_1(small_series: ObservationSeries, small_params: I01Params) -> None:
    r = log_returns(small_series)
    t = 10
    y = future_vector(r, t, small_params)
    np.testing.assert_array_equal(y, r[t + 1 : t + 1 + small_params.h])


def test_admissible_candidates_invariants(
    small_series: ObservationSeries, small_params: I01Params
) -> None:
    t = 20
    library = admissible_candidates(t, len(small_series), small_params)
    assert library.size >= small_params.L_min
    assert np.all(library < t)
    assert np.all((t - library) > small_params.tau)
    assert np.all(library + small_params.h <= t)
    assert np.all(library >= small_params.M)


def test_l2_neighbors_tie_breaks_oldest() -> None:
    states = np.array(
        [
            [0.0, 0.0],
            [1.0, 0.0],
            [1.0, 0.0],
            [3.0, 0.0],
        ],
        dtype=np.float64,
    )
    library = np.array([1, 2, 3], dtype=np.intp)
    ranks, distances = l2_neighbors(np.array([0.0, 0.0]), states, library, k=2)
    assert list(ranks) == [1, 2]
    np.testing.assert_allclose(distances, [1.0, 1.0])


def test_h_raw_identical_futures_is_zero() -> None:
    y = np.ones((4, 3))
    assert h_raw(y) == 0.0
    assert h_shape(y, 1e-8) == 0.0
    assert h_vol(y) == 0.0


def test_pairwise_l2_matches_numpy() -> None:
    rng = np.random.default_rng(1)
    a = rng.normal(size=(5, 3))
    b = rng.normal(size=(4, 3))
    got = pairwise_l2(a, b)
    expected = np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2)
    np.testing.assert_allclose(got, expected, atol=1e-12)


def test_run_geometry_small(small_series: ObservationSeries, small_params: I01Params) -> None:
    result = run_geometry(small_series, small_params)
    assert result.n_eval == len(evaluation_indices(len(small_series), small_params))
    assert result.example is not None
    assert len(result.example.x_t) == small_params.W
    assert len(result.example.neighbor_ranks) == small_params.k
    assert set(result.mean_geo) == {"H_raw", "H_vol", "H_shape"}
    assert set(result.mean_delta) == {"H_raw", "H_vol", "H_shape"}


def test_observation_series_rejects_non_increasing() -> None:
    with pytest.raises(ValueError, match="strictly increasing"):
        ObservationSeries(
            sessions=(__import__("datetime").date(2000, 1, 3), __import__("datetime").date(2000, 1, 3)),
            adjusted_price=(1.0, 1.1),
        )


def test_state_vector_is_standardize_window(
    small_series: ObservationSeries, small_params: I01Params
) -> None:
    r = log_returns(small_series)
    t = small_params.M + 2
    np.testing.assert_array_equal(
        state_vector(r, t, small_params), standardize_window(r, t, small_params)
    )
