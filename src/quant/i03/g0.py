"""G0 state construction for I03 — reuse I02 X contract (prereg §3).

CONTRACT MATCH: ``quant.i02.states_x`` implements causal μ/σ with M=252,
W_X=20, ddof=1, no ε, σ=0 → undefined. Indexing: returns[0] unused.
"""

from __future__ import annotations

import numpy as np

from quant.i02.params import DEFAULT_PARAMS as I02_PARAMS
from quant.i02.params import I02Params
from quant.i02.states_x import (
    XUndefinedError,
    all_state_vectors_x,
    causal_mu_sigma,
    first_valid_x_index,
    state_vector_x,
    x_is_defined,
)
from quant.i03.params import I03Config


def _i02_params_compatible(cfg: I03Config) -> I02Params:
    """Return I02 params after asserting G0 constants match I03."""

    if cfg.W_X != I02_PARAMS.W_X or cfg.M != I02_PARAMS.M:
        raise RuntimeError("L1-I5: I02 G0 params diverge from I03 config")
    return I02_PARAMS


def build_states_x(returns: np.ndarray, cfg: I03Config) -> np.ndarray:
    """Stack ``X_t``; NaN rows where undefined (prereg §3)."""

    return all_state_vectors_x(returns, _i02_params_compatible(cfg))


def euclidean_distance(a: np.ndarray, b: np.ndarray) -> float:
    """``d_0 = ||a-b||_2``."""

    d = a - b
    return float(np.sqrt(np.dot(d, d)))


__all__ = [
    "XUndefinedError",
    "build_states_x",
    "causal_mu_sigma",
    "euclidean_distance",
    "first_valid_x_index",
    "state_vector_x",
    "x_is_defined",
]
