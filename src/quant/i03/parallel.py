"""PERF-01 Phase 1B — deterministic process-parallel surrogate execution.

Operational parallelism over surrogate index ``b`` only. Seeds remain
``42+b`` (N4) and ``10000+b`` (N3). Worker count is NOT scientific.
"""

from __future__ import annotations

import os
from concurrent.futures import ProcessPoolExecutor, as_completed
from typing import Any, Callable, Sequence, TypeVar

import numpy as np

from quant.i03.blocks import TemporalBlock, build_blocks
from quant.i03.emnd import EMNDBlockResult, compute_emnd_all
from quant.i03.g0 import build_states_x
from quant.i03.iaaft import iaaft
from quant.i03.locality import LocalityBlockDiagnostic, locality_for_block
from quant.i03.n3 import N3BatteryMeta, n3_nonconv_frac_invalid
from quant.i03.n4 import N4ScalePath, n4_surrogate_returns
from quant.i03.params import I03Config

T = TypeVar("T")


class ParallelSurrogateError(RuntimeError):
    """Fail-closed error for surrogate parallel execution / reassembly."""


def _theta_map(emnd: tuple[EMNDBlockResult, ...]) -> dict[int, dict[int, float]]:
    return {r.period: dict(r.theta_by_k) for r in emnd}


def _emnd_on_returns(
    returns: np.ndarray, blocks: tuple[TemporalBlock, ...], cfg: I03Config
) -> tuple[np.ndarray, np.ndarray, tuple[EMNDBlockResult, ...]]:
    states = build_states_x(returns, cfg)
    defined = ~np.isnan(states[:, 0])
    emnd = compute_emnd_all(states, defined, blocks, cfg)
    return states, defined, emnd


def _clamp_blas_threads() -> dict[str, str | None]:
    """Prefer one BLAS thread per process unless the user already set vars.

    Uses ``setdefault`` only — never overrides an explicit user setting.
    """

    keys = (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
    )
    before = {k: os.environ.get(k) for k in keys}
    for k in keys:
        os.environ.setdefault(k, "1")
    return before


# ---------------------------------------------------------------------------
# Worker state (spawn-safe: set by initializer in each child)
# ---------------------------------------------------------------------------

_W: dict[str, Any] = {}


def _init_worker(payload: dict[str, Any]) -> None:
    """Process initializer — receives immutable shared inputs once."""

    _clamp_blas_threads()
    _W.clear()
    _W.update(payload)


def _cfg_from_w() -> I03Config:
    return _W["cfg"]


def _blocks_from_w() -> tuple[TemporalBlock, ...]:
    return _W["blocks"]


def _n4_worker(b: int) -> dict[str, Any]:
    """Evaluate one N4 surrogate ``b`` (generate + E-MND + optional locality)."""

    if b < 1:
        raise ParallelSurrogateError(f"invalid b={b}")
    cfg: I03Config = _cfg_from_w()
    blocks = _blocks_from_w()
    returns: np.ndarray = _W["returns"]
    scale: N4ScalePath = _W["n4_scale"]
    do_loc: bool = _W["do_loc_n4"]
    include_returns: bool = _W.get("include_returns", False)

    seed = int(cfg.master_seed + b)
    rs = n4_surrogate_returns(returns, scale, b, cfg)
    st, df, em = _emnd_on_returns(rs, blocks, cfg)
    loc: list[dict[str, Any]] | None = None
    if do_loc:
        loc = []
        for blk in blocks:
            d = locality_for_block(
                st, df, blk, cfg, seed=20_000 + blk.period + 1000 * b
            )
            loc.append(
                {
                    "period": d.period,
                    "Lambda": d.Lambda,
                    "Gamma": d.Gamma,
                    "hard_degenerate": d.hard_degenerate,
                    "n_queries_used": d.n_queries_used,
                }
            )
    out: dict[str, Any] = {
        "b": int(b),
        "family": "N4",
        "seed": seed,
        "theta": _theta_map(em),
        "locality": loc,
    }
    if include_returns:
        out["returns"] = np.asarray(rs, dtype=np.float64)
    return out


def _n3_worker(b: int) -> dict[str, Any]:
    """Evaluate one N3 surrogate ``b`` (IAAFT + E-MND). No retry on non-convergence."""

    if b < 1:
        raise ParallelSurrogateError(f"invalid b={b}")
    cfg: I03Config = _cfg_from_w()
    blocks = _blocks_from_w()
    returns: np.ndarray = _W["returns"]
    include_returns: bool = _W.get("include_returns", False)

    seed = 10_000 + b
    ia = iaaft(
        returns,
        seed=seed,
        I_max=cfg.iaaft_I_max,
        eps=cfg.iaaft_eps,
    )
    st, df, em = _emnd_on_returns(ia.series, blocks, cfg)
    out: dict[str, Any] = {
        "b": int(b),
        "family": "N3",
        "seed": seed,
        "converged": bool(ia.converged),
        "iterations": int(ia.iterations),
        "theta": _theta_map(em),
    }
    if include_returns:
        out["returns"] = np.asarray(ia.series, dtype=np.float64)
    return out


def reassemble_by_b(
    results: Sequence[dict[str, Any]],
    *,
    B: int,
    family: str,
) -> list[dict[str, Any]]:
    """Canonical ascending-``b`` reassembly with fail-closed identity checks."""

    if B < 1:
        raise ParallelSurrogateError("B must be positive")
    by_b: dict[int, dict[str, Any]] = {}
    for raw in results:
        if not isinstance(raw, dict):
            raise ParallelSurrogateError(f"malformed worker result: {type(raw)}")
        if "b" not in raw or "family" not in raw:
            raise ParallelSurrogateError("malformed worker result: missing b/family")
        b = int(raw["b"])
        fam = raw["family"]
        if fam != family:
            raise ParallelSurrogateError(
                f"wrong null family: expected {family}, got {fam!r} for b={b}"
            )
        if b < 1 or b > B:
            raise ParallelSurrogateError(f"unexpected b={b} (B={B})")
        if b in by_b:
            raise ParallelSurrogateError(f"duplicate b={b}")
        by_b[b] = raw
    ordered: list[dict[str, Any]] = []
    for b in range(1, B + 1):
        if b not in by_b:
            raise ParallelSurrogateError(f"missing b={b}")
        ordered.append(by_b[b])
    if len(by_b) != B:
        raise ParallelSurrogateError(
            f"result cardinality mismatch: got {len(by_b)}, expected {B}"
        )
    return ordered


def map_surrogate_b(
    worker: Callable[[int], dict[str, Any]],
    bs: Sequence[int],
    *,
    workers: int,
    initargs: tuple[Any, ...] | None = None,
    executor_factory: Callable[..., Any] | None = None,
) -> list[dict[str, Any]]:
    """Map ``worker`` over ``bs`` with process pool (or serial if workers==1).

    Completion order is undefined; caller must ``reassemble_by_b``.
    Worker exceptions propagate (fail closed — do not shrink B).
    """

    workers = int(workers)
    if workers < 1:
        raise ParallelSurrogateError("workers must be >= 1")
    bs_list = [int(b) for b in bs]
    if workers == 1:
        # Serial path: same worker function, no pool (reference execution).
        if initargs is not None:
            _init_worker(initargs[0])
        return [worker(b) for b in bs_list]

    factory = executor_factory or ProcessPoolExecutor
    results: list[dict[str, Any]] = []
    with factory(
        max_workers=workers,
        initializer=_init_worker,
        initargs=initargs if initargs is not None else ({},),
    ) as ex:
        futs = [ex.submit(worker, b) for b in bs_list]
        # Real ProcessPoolExecutor futures support as_completed.
        # Test doubles may expose an intentional completion key `_complete_after`.
        if futs and all(hasattr(f, "_complete_after") for f in futs):
            for fut in sorted(futs, key=lambda f: f._complete_after):
                results.append(fut.result())
        else:
            for fut in as_completed(futs):
                results.append(fut.result())
    return results


def _locality_from_dicts(
    rows: list[dict[str, Any]] | None,
) -> tuple[LocalityBlockDiagnostic, ...] | None:
    if rows is None:
        return None
    return tuple(
        LocalityBlockDiagnostic(
            period=int(r["period"]),
            Lambda=float(r["Lambda"]),
            Gamma=float(r["Gamma"]),
            hard_degenerate=bool(r["hard_degenerate"]),
            n_queries_used=int(r["n_queries_used"]),
        )
        for r in rows
    )


def run_n4_battery_parallel(
    returns: np.ndarray,
    scale: N4ScalePath,
    cfg: I03Config,
    *,
    B: int,
    workers: int,
    do_loc_n4: bool,
    blocks: tuple[TemporalBlock, ...] | None = None,
    include_returns: bool = False,
    executor_factory: Callable[..., Any] | None = None,
) -> tuple[list[dict[int, dict[int, float]]], list[tuple[LocalityBlockDiagnostic, ...]]]:
    """N4 generate+E-MND(+locality) for ``b=1..B`` with canonical reassembly."""

    r = np.asarray(returns, dtype=np.float64)
    blocks = blocks if blocks is not None else build_blocks(r.shape[0], cfg)
    payload = {
        "returns": r,
        "n4_scale": scale,
        "blocks": blocks,
        "cfg": cfg,
        "do_loc_n4": bool(do_loc_n4),
        "include_returns": bool(include_returns),
    }
    raw = map_surrogate_b(
        _n4_worker,
        range(1, B + 1),
        workers=workers,
        initargs=(payload,),
        executor_factory=executor_factory,
    )
    ordered = reassemble_by_b(raw, B=B, family="N4")
    theta: list[dict[int, dict[int, float]]] = []
    loc_n4: list[tuple[LocalityBlockDiagnostic, ...]] = []
    for row in ordered:
        theta.append(row["theta"])
        if do_loc_n4:
            loc = _locality_from_dicts(row["locality"])
            if loc is None:
                raise ParallelSurrogateError(f"missing locality for b={row['b']}")
            loc_n4.append(loc)
    return theta, loc_n4


def run_n3_battery_parallel(
    returns: np.ndarray,
    cfg: I03Config,
    *,
    B: int,
    workers: int,
    blocks: tuple[TemporalBlock, ...] | None = None,
    include_returns: bool = False,
    executor_factory: Callable[..., Any] | None = None,
) -> tuple[N3BatteryMeta, list[dict[int, dict[int, float]]], list[dict[str, Any]]]:
    """N3 IAAFT+E-MND for ``b=1..B`` with canonical reassembly."""

    r = np.asarray(returns, dtype=np.float64)
    blocks = blocks if blocks is not None else build_blocks(r.shape[0], cfg)
    payload = {
        "returns": r,
        "blocks": blocks,
        "cfg": cfg,
        "include_returns": bool(include_returns),
    }
    raw = map_surrogate_b(
        _n3_worker,
        range(1, B + 1),
        workers=workers,
        initargs=(payload,),
        executor_factory=executor_factory,
    )
    ordered = reassemble_by_b(raw, B=B, family="N3")
    flags = tuple(bool(row["converged"]) for row in ordered)
    n_non = sum(1 for f in flags if not f)
    invalid = n3_nonconv_frac_invalid(n_non, B, cfg.iaaft_nonconv_frac)
    meta = N3BatteryMeta(
        B_requested=B,
        n_converged=B - n_non,
        n_nonconverged=n_non,
        valid=not invalid,
        invalid_reason="N3_IAAFT_NONCONV_FRAC" if invalid else None,
        converged_flags=flags,
    )
    theta = [row["theta"] for row in ordered]
    return meta, theta, ordered
