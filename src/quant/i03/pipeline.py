"""Structural analysis pipeline (synthetic-capable; no market I/O)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

import numpy as np

from quant.i03.blocks import TemporalBlock, build_blocks
from quant.i03.coherence import SurvivalGrid, build_survival_grid
from quant.i03.emnd import EMNDBlockResult, compute_emnd_all
from quant.i03.g0 import build_states_x
from quant.i03.locality import (
    LocalityBlockDiagnostic,
    locality_for_block,
    locality_validity_ok,
)
from quant.i03.n3 import N3BatteryMeta, generate_n3_battery
from quant.i03.n4 import N4ScalePath, generate_n4_battery
from quant.i03.params import DEFAULT_CONFIG, I03Config
from quant.i03.verdict import VerdictInput, VerdictResult, decide_verdict


@dataclass(frozen=True, slots=True)
class I03RunResult:
    """Complete structural run on an in-memory return series."""

    cfg: I03Config
    blocks: tuple[TemporalBlock, ...]
    emnd_obs: tuple[EMNDBlockResult, ...]
    n4_scale: N4ScalePath
    n3_meta: N3BatteryMeta
    locality_obs: tuple[LocalityBlockDiagnostic, ...]
    survival: SurvivalGrid
    V: bool
    E: bool
    verdict: VerdictResult
    B_n4_used: int
    B_n3_used: int


def _x_defined_mask(states: np.ndarray) -> np.ndarray:
    return ~np.isnan(states[:, 0])


def _theta_map(emnd: tuple[EMNDBlockResult, ...]) -> dict[int, dict[int, float]]:
    return {r.period: dict(r.theta_by_k) for r in emnd}


def _emnd_on_returns(
    returns: np.ndarray, blocks: tuple[TemporalBlock, ...], cfg: I03Config
) -> tuple[np.ndarray, np.ndarray, tuple[EMNDBlockResult, ...]]:
    states = build_states_x(returns, cfg)
    defined = _x_defined_mask(states)
    emnd = compute_emnd_all(states, defined, blocks, cfg)
    return states, defined, emnd


def run_structural_analysis(
    returns: np.ndarray,
    cfg: I03Config | None = None,
    *,
    B_n4: int | None = None,
    B_n3: int | None = None,
    compute_locality_on_n4: bool = True,
) -> I03RunResult:
    """Run I03 structural pipeline on a return array (no download).

    ``B_n4`` / ``B_n3`` are **test-only** overrides. Production callers must
    leave them as ``None`` so frozen ``cfg.B_N4`` / ``cfg.B_N3`` apply.
    """

    cfg = cfg or DEFAULT_CONFIG
    r = np.asarray(returns, dtype=np.float64)
    T = r.shape[0]
    blocks = build_blocks(T, cfg)

    states, defined, emnd_obs = _emnd_on_returns(r, blocks, cfg)

    n4_scale, n4_sur = generate_n4_battery(r, cfg, B=B_n4)
    n3_meta, n3_sur = generate_n3_battery(r, cfg, B=B_n3)
    Bn4 = len(n4_sur)
    Bn3 = len(n3_sur)

    theta_n4: list[dict[int, dict[int, float]]] = []
    for rs in n4_sur:
        _s, _d, em = _emnd_on_returns(rs, blocks, cfg)
        theta_n4.append(_theta_map(em))

    theta_n3: list[dict[int, dict[int, float]]] = []
    for rs in n3_sur:
        _s, _d, em = _emnd_on_returns(rs, blocks, cfg)
        theta_n3.append(_theta_map(em))

    survival = build_survival_grid(_theta_map(emnd_obs), theta_n4, theta_n3, cfg)

    # Locality observed
    loc_obs = tuple(
        locality_for_block(states, defined, b, cfg, seed=20_000 + b.period)
        for b in blocks
    )

    loc_n4: list[tuple[LocalityBlockDiagnostic, ...]] = []
    if compute_locality_on_n4 and n4_scale.valid:
        for bi, rs in enumerate(n4_sur, start=1):
            st, df, _ = _emnd_on_returns(rs, blocks, cfg)
            loc_n4.append(
                tuple(
                    locality_for_block(
                        st, df, b, cfg, seed=20_000 + b.period + 1000 * bi
                    )
                    for b in blocks
                )
            )

    V = bool(n4_scale.valid) and locality_validity_ok(loc_obs, loc_n4) if loc_n4 else False
    if not n4_scale.valid:
        V = False
    # If we skipped N4 locality (empty), hard-fail V only when scale invalid;
    # when compute_locality_on_n4 False (unit tests), treat V from hard checks only
    if not compute_locality_on_n4:
        V = all(not d.hard_degenerate and d.Lambda < 1.0 for d in loc_obs)

    E = (
        all(e.n_queries >= cfg.n_min for e in emnd_obs)
        and n4_scale.valid
        and n3_meta.valid
    )

    verdict = decide_verdict(
        VerdictInput(V=V, E=E, C4=survival.C4, C3=survival.C3, F4=survival.F4)
    )

    return I03RunResult(
        cfg=cfg,
        blocks=blocks,
        emnd_obs=emnd_obs,
        n4_scale=n4_scale,
        n3_meta=n3_meta,
        locality_obs=loc_obs,
        survival=survival,
        V=V,
        E=E,
        verdict=verdict,
        B_n4_used=Bn4,
        B_n3_used=Bn3,
    )


def artifact_dict(result: I03RunResult, *, input_hash: str = "") -> dict[str, Any]:
    """Canonical machine-readable artifact (prereg §16)."""

    return {
        "schema": "I03-ARTIFACT-v1",
        "prereg_id": result.cfg.prereg_id,
        "input_hash": input_hash,
        "config": asdict(result.cfg),
        "blocks": [
            {"period": b.period, "start": b.start, "end": b.end, "n": int(b.indices.size)}
            for b in result.blocks
        ],
        "emnd": [
            {
                "period": e.period,
                "n_queries": e.n_queries,
                "n_skipped_undefined_x": e.n_skipped_undefined_x,
                "n_skipped_insufficient_pool": e.n_skipped_insufficient_pool,
                "theta_by_k": e.theta_by_k,
            }
            for e in result.emnd_obs
        ],
        "locality": [
            {
                "period": d.period,
                "Lambda": d.Lambda,
                "Gamma": d.Gamma,
                "hard_degenerate": d.hard_degenerate,
                "DIAGNOSTIC": "NON-PROMOTIONAL",
            }
            for d in result.locality_obs
        ],
        "n4": {
            "valid": result.n4_scale.valid,
            "invalid_reason": result.n4_scale.invalid_reason,
            "Z_frac": float(result.n4_scale.Z_indices.size / max(result.n4_scale.T, 1)),
            "B_used": result.B_n4_used,
            "preserves": "sigma_hat_path_by_construction_on_observed_returns",
            "does_not_claim": "rolling_stdev_recomputed_on_r_star_equals_sigma_hat",
        },
        "n3": {
            "valid": result.n3_meta.valid,
            "invalid_reason": result.n3_meta.invalid_reason,
            "B_requested": result.n3_meta.B_requested,
            "n_converged": result.n3_meta.n_converged,
            "n_nonconverged": result.n3_meta.n_nonconverged,
        },
        "survival": {
            "C4": result.survival.C4,
            "C3": result.survival.C3,
            "F4": result.survival.F4,
            "pvalues": result.survival.pvalues,
            "S": {
                null: {
                    str(p): {str(k): bool(v) for k, v in ks.items()}
                    for p, ks in periods.items()
                }
                for null, periods in result.survival.survival.items()
            },
        },
        "predicates": {"V": result.V, "E": result.E},
        "verdict": {
            "label": result.verdict.label.value,
            "nd_code": result.verdict.nd_code,
            "reason": result.verdict.reason,
        },
    }
