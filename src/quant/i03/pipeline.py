"""Structural analysis pipeline (synthetic-capable; no market I/O)."""

from __future__ import annotations

import os
import sys
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
from quant.i03.n4 import N4ScalePath, build_n4_scale_path, generate_n4_battery
from quant.i03.params import DEFAULT_CONFIG, I03Config
from quant.i03.verdict import VerdictInput, VerdictResult, decide_verdict


def _test_overrides_allowed() -> bool:
    return os.environ.get("I03_ALLOW_TEST_OVERRIDES") == "1"


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
    workers_requested: int = 1
    workers_used: int = 1


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
    workers: int = 1,
    checkpoint_dir: str | os.PathLike[str] | None = None,
    resume: bool = False,
) -> I03RunResult:
    """Run I03 structural pipeline on a return array (no download).

    ``B_n4`` / ``B_n3`` / ``compute_locality_on_n4=False`` are **test-only**.
    They require ``I03_ALLOW_TEST_OVERRIDES=1``. Production callers must omit
    overrides so frozen ``cfg.B_N4`` / ``cfg.B_N3`` and full locality apply.

    ``workers`` is **operational only** (PERF-01 Phase 1B).
    ``checkpoint_dir`` / ``resume`` are **operational only** (PERF-01 Phase 1C).
    """

    from pathlib import Path

    from quant.i03.checkpoint import (
        CheckpointError,
        CheckpointStore,
        RunStatus,
        compute_run_id,
        returns_input_sha256,
    )

    cfg = cfg or DEFAULT_CONFIG
    using_overrides = (
        B_n4 is not None or B_n3 is not None or compute_locality_on_n4 is False
    )
    if using_overrides and not _test_overrides_allowed():
        raise RuntimeError(
            "I03 test-only overrides require I03_ALLOW_TEST_OVERRIDES=1"
        )

    workers_req = int(workers)
    if workers_req < 1:
        raise ValueError("workers must be >= 1")

    r = np.asarray(returns, dtype=np.float64)
    T = r.shape[0]
    blocks = build_blocks(T, cfg)

    states, defined, emnd_obs = _emnd_on_returns(r, blocks, cfg)

    n4_scale = build_n4_scale_path(r, cfg)
    Bn4 = cfg.B_N4 if B_n4 is None else int(B_n4)
    Bn3 = cfg.B_N3 if B_n3 is None else int(B_n3)
    if Bn4 < 1 or Bn3 < 1:
        raise ValueError("B must be positive")

    do_loc_n4 = bool(compute_locality_on_n4 and n4_scale.valid)

    ckpt_store = None
    run_id = None
    use_battery_engine = workers_req > 1 or checkpoint_dir is not None
    if checkpoint_dir is not None:
        store = CheckpointStore(Path(checkpoint_dir))
        input_sha = returns_input_sha256(r)
        run_id = compute_run_id(
            input_sha256=input_sha,
            cfg=cfg,
            B_n4=Bn4,
            B_n3=Bn3,
            do_loc_n4=do_loc_n4,
        )
        st = store.status()
        if resume:
            if st in (RunStatus.NEW,):
                raise CheckpointError(
                    "STOP: --resume requested but checkpoint store is NEW/empty"
                )
            if st == RunStatus.INVALID:
                raise CheckpointError("STOP: checkpoint store INVALID")
            store.assert_compatible(
                run_id=run_id,
                input_sha256=input_sha,
                cfg=cfg,
                B_n4=Bn4,
                B_n3=Bn3,
                do_loc_n4=do_loc_n4,
            )
        else:
            if st != RunStatus.NEW:
                raise CheckpointError(
                    "STOP: checkpoint-dir is not empty/NEW; pass --resume "
                    "explicitly to continue a compatible run "
                    f"(status={st.value})"
                )
            store.write_new_manifest(
                run_id=run_id,
                input_sha256=input_sha,
                cfg=cfg,
                B_n4=Bn4,
                B_n3=Bn3,
                do_loc_n4=do_loc_n4,
            )
        ckpt_store = store

    if not use_battery_engine:
        # Phase-1A serial fused path (reference; no checkpoint).
        _, n4_sur = generate_n4_battery(r, cfg, B=Bn4)
        n3_meta, n3_sur = generate_n3_battery(r, cfg, B=Bn3)
        theta_n4: list[dict[int, dict[int, float]]] = []
        loc_n4: list[tuple[LocalityBlockDiagnostic, ...]] = []
        for i, rs in enumerate(n4_sur, start=1):
            st, df, em = _emnd_on_returns(rs, blocks, cfg)
            theta_n4.append(_theta_map(em))
            if do_loc_n4:
                loc_n4.append(
                    tuple(
                        locality_for_block(
                            st, df, b, cfg, seed=20_000 + b.period + 1000 * i
                        )
                        for b in blocks
                    )
                )
            if i == Bn4 or i % 50 == 0:
                print(f"N4 E-MND {i}/{Bn4}", file=sys.stderr, flush=True)
                if do_loc_n4:
                    print(f"N4 locality {i}/{Bn4}", file=sys.stderr, flush=True)

        theta_n3: list[dict[int, dict[int, float]]] = []
        for i, rs in enumerate(n3_sur, start=1):
            _s, _d, em = _emnd_on_returns(rs, blocks, cfg)
            theta_n3.append(_theta_map(em))
            if i == Bn3 or i % 50 == 0:
                print(f"N3 E-MND {i}/{Bn3}", file=sys.stderr, flush=True)
        workers_used = 1
    else:
        from quant.i03.parallel import (
            run_n3_battery_parallel,
            run_n4_battery_parallel,
        )

        print(
            f"N4 battery B={Bn4} workers={workers_req} "
            f"checkpoint={'yes' if ckpt_store else 'no'}",
            file=sys.stderr,
            flush=True,
        )
        theta_n4, loc_n4 = run_n4_battery_parallel(
            r,
            n4_scale,
            cfg,
            B=Bn4,
            workers=workers_req,
            do_loc_n4=do_loc_n4,
            blocks=blocks,
            checkpoint_store=ckpt_store,
            run_id=run_id,
        )
        print(
            f"N3 battery B={Bn3} workers={workers_req} "
            f"checkpoint={'yes' if ckpt_store else 'no'}",
            file=sys.stderr,
            flush=True,
        )
        n3_meta, theta_n3, _ordered_n3 = run_n3_battery_parallel(
            r,
            cfg,
            B=Bn3,
            workers=workers_req,
            blocks=blocks,
            checkpoint_store=ckpt_store,
            run_id=run_id,
        )
        workers_used = workers_req
        if ckpt_store is not None and run_id is not None:
            ckpt_store.mark_complete_if_done(
                run_id=run_id, B_n4=Bn4, B_n3=Bn3
            )

    survival = build_survival_grid(_theta_map(emnd_obs), theta_n4, theta_n3, cfg)

    loc_obs = tuple(
        locality_for_block(states, defined, b, cfg, seed=20_000 + b.period)
        for b in blocks
    )

    V = bool(n4_scale.valid) and locality_validity_ok(loc_obs, loc_n4) if loc_n4 else False
    if not n4_scale.valid:
        V = False
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
        workers_requested=workers_req,
        workers_used=workers_used,
    )


def artifact_dict(
    result: I03RunResult,
    *,
    input_hash: str = "",
    implementation_id: str = "",
    mode: str = "STRUCTURAL",
    timing: dict[str, Any] | None = None,
    fixture_id: str = "",
) -> dict[str, Any]:
    """Canonical machine-readable artifact (prereg §16)."""

    cfg = result.cfg
    art: dict[str, Any] = {
        "schema": "I03-ARTIFACT-v1",
        "prereg_id": cfg.prereg_id,
        "input_hash": input_hash,
        "implementation_id": implementation_id,
        "mode": mode,
        "fixture_id": fixture_id,
        "config": {**asdict(cfg), "K": list(cfg.K)},
        "contract_surface": {
            "W_X": cfg.W_X,
            "M": cfg.M,
            "W_sigma": cfg.W_sigma,
            "tau": cfg.tau,
            "K": list(cfg.K),
            "P": cfg.P,
            "B_N4": cfg.B_N4,
            "B_N3": cfg.B_N3,
            "alpha": cfg.alpha,
            "n_min": cfg.n_min,
            "iaaft_I_max": cfg.iaaft_I_max,
            "iaaft_eps": cfg.iaaft_eps,
            "n4_seed_doctrine": "42 + b (b=1..B_N4)",
            "n3_seed_doctrine": "10000 + b (b=1..B_N3)",
            "validity_seed_doctrine": "20000 + p (+ 1000*b for N4 surrogates)",
        },
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
            "W_sigma": cfg.W_sigma,
            "seed_doctrine": "42 + b",
            "preserves": "sigma_hat_path_by_construction_on_observed_returns",
            "does_not_claim": "rolling_stdev_recomputed_on_r_star_equals_sigma_hat",
        },
        "n3": {
            "valid": result.n3_meta.valid,
            "invalid_reason": result.n3_meta.invalid_reason,
            "B_requested": result.n3_meta.B_requested,
            "n_converged": result.n3_meta.n_converged,
            "n_nonconverged": result.n3_meta.n_nonconverged,
            "method": "IAAFT",
            "I_max": cfg.iaaft_I_max,
            "epsilon": cfg.iaaft_eps,
            "seed_doctrine": "10000 + b",
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
        "execution": {
            "workers_requested": result.workers_requested,
            "workers_used": result.workers_used,
            "logical_cpus": os.cpu_count(),
            "note": "workers is operational only; not a scientific parameter",
        },
    }
    if timing is not None:
        art["timing"] = timing
    return art
