"""Coherence predicates and cell survival grid."""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from quant.i03.inference import left_tail_p, survives
from quant.i03.params import I03Config


@dataclass(frozen=True, slots=True)
class SurvivalGrid:
    """``S_nu(k, p)`` and derived coherence flags."""

    # survival[null][period][k] -> bool ; null in {"N4","N3"}; period 1..P
    survival: dict[str, dict[int, dict[int, bool]]]
    pvalues: dict[str, dict[int, dict[int, float]]]
    C4: bool
    C3: bool
    F4: bool


def build_survival_grid(
    theta_obs: dict[int, dict[int, float]],
    theta_n4: list[dict[int, dict[int, float]]],
    theta_n3: list[dict[int, dict[int, float]]],
    cfg: I03Config,
) -> SurvivalGrid:
    """Build cell p-values and survival indicators.

    ``theta_*`` maps ``period -> k -> Theta``.
    """

    survival: dict[str, dict[int, dict[int, bool]]] = {"N4": {}, "N3": {}}
    pvalues: dict[str, dict[int, dict[int, float]]] = {"N4": {}, "N3": {}}

    periods = sorted(theta_obs.keys())
    for null_name, battery in (("N4", theta_n4), ("N3", theta_n3)):
        for p in periods:
            survival[null_name][p] = {}
            pvalues[null_name][p] = {}
            for k in cfg.K:
                obs = theta_obs[p][k]
                sur = [bat[p][k] for bat in battery]
                ph = left_tail_p(obs, np.asarray(sur, dtype=float))
                pvalues[null_name][p][k] = ph
                survival[null_name][p][k] = survives(ph, cfg.alpha)

    def coherent(null: str) -> bool:
        return all(
            all(survival[null][p][k] for k in cfg.K) for p in periods
        )

    C4 = coherent("N4")
    C3 = coherent("N3")
    F4 = all(not survival["N4"][p][k] for p in periods for k in cfg.K)

    return SurvivalGrid(
        survival=survival, pvalues=pvalues, C4=C4, C3=C3, F4=F4
    )
