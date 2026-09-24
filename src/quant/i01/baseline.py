"""Baseline B0: uniform draws from ``L_t``, independent of distance."""

from __future__ import annotations

import numpy as np

from quant.i01.homogeneity import homogeneity_bundle
from quant.i01.params import I01Params


def b0_mean_homogeneity(
    futures: np.ndarray,
    library: np.ndarray,
    params: I01Params,
    rng: np.random.Generator,
) -> dict[str, float]:
    """Monte-Carlo mean of ``H_*`` over ``R`` uniform k-subsets of ``library``.

    B0 does not look at ``X`` or at geometric distance.
    """

    if library.shape[0] < params.k:
        raise ValueError("B0 library smaller than k")
    acc = {"H_raw": 0.0, "H_vol": 0.0, "H_shape": 0.0}
    for _ in range(params.B0_R):
        pick = rng.choice(library, size=params.k, replace=False)
        bundle = homogeneity_bundle(futures[pick], params.epsilon)
        for key in acc:
            acc[key] += bundle[key]
    scale = 1.0 / params.B0_R
    return {key: value * scale for key, value in acc.items()}
