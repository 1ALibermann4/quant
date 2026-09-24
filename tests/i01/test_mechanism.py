"""E03 past-vol diagnostic — not a B0, frozen I01 parameters."""

from __future__ import annotations

import numpy as np

from quant.i01.candidates import admissible_candidates, evaluation_indices
from quant.i01.mechanism import (
    past_window_features,
    run_vol_mechanism,
    scalar_neighbors,
    summarize_mechanism,
)
from quant.i01.params import DEFAULT_PARAMS
from quant.i01.returns import log_returns
from quant.i01.states import all_state_vectors


def test_parameters_still_frozen() -> None:
    assert DEFAULT_PARAMS.W == 20
    assert DEFAULT_PARAMS.k == 50
    assert DEFAULT_PARAMS.h == 10
    assert DEFAULT_PARAMS.B0_R == 200
    assert DEFAULT_PARAMS.B0_seed == 42


def test_scalar_neighbors_closest_then_oldest() -> None:
    values = np.array([0.0, 0.50, 0.10, 0.10, 0.40, 0.11])
    library = np.array([1, 2, 3, 4, 5], dtype=np.intp)
    ranks, distances = scalar_neighbors(0.10, values, library, k=3)
    np.testing.assert_array_equal(ranks, np.array([2, 3, 5]))
    np.testing.assert_allclose(distances, [0.0, 0.0, 0.01])


def test_past_features_ignore_future(small_series, small_params) -> None:
    returns = log_returns(small_series)
    states = all_state_vectors(returns, small_params)
    t = int(evaluation_indices(len(small_series), small_params)[0])
    clean = past_window_features(returns, states, small_params)
    poisoned = returns.copy()
    poisoned[t + 1 :] = 0.5
    dirty_states = all_state_vectors(poisoned, small_params)
    dirty = past_window_features(poisoned, dirty_states, small_params)
    assert clean.rv_w[t] == dirty.rv_w[t]
    assert clean.sigma_m[t] == dirty.sigma_m[t]
    assert clean.x_norm[t] == dirty.x_norm[t]


def test_vol_control_stays_inside_library_and_ignores_y(small_series, small_params) -> None:
    result = run_vol_mechanism(small_series, small_params)
    assert result.n_eval > 0
    assert "not B0" in result.note

    returns = log_returns(small_series)
    states = all_state_vectors(returns, small_params)
    features = past_window_features(returns, states, small_params)
    t = int(evaluation_indices(len(small_series), small_params)[0])
    library = admissible_candidates(t, len(small_series), small_params)
    ctrl, _ = scalar_neighbors(float(features.rv_w[t]), features.rv_w, library, small_params.k)
    assert set(int(s) for s in ctrl).issubset(set(int(s) for s in library))

    poisoned = returns.copy()
    poisoned[t + 1 :] = 0.5
    dirty_states = all_state_vectors(poisoned, small_params)
    dirty = past_window_features(poisoned, dirty_states, small_params)
    ctrl2, _ = scalar_neighbors(float(dirty.rv_w[t]), dirty.rv_w, library, small_params.k)
    np.testing.assert_array_equal(ctrl, ctrl2)


def test_summarize_has_no_sci_verdict(small_series, small_params) -> None:
    result = run_vol_mechanism(small_series, small_params)
    bundle = summarize_mechanism(result)
    assert "mean_H_volctrl" in bundle
    assert "not a SCI gate" in bundle["note"]
    text = str(bundle).lower()
    assert "sci-pass" not in text
    assert "sci-fail" not in text
