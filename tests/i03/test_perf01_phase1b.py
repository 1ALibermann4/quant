"""PERF-01 Phase 1B — process-parallel surrogate execution tests (non-market)."""

from __future__ import annotations

import math
import time
from typing import Any, Callable

import numpy as np
import pytest

from quant.i03.blocks import build_blocks
from quant.i03.fixture_hat import generate_hat_returns
from quant.i03.n4 import build_n4_scale_path, n4_surrogate_returns
from quant.i03.n3 import generate_n3_battery
from quant.i03.params import DEFAULT_CONFIG
from quant.i03.parallel import (
    ParallelSurrogateError,
    map_surrogate_b,
    reassemble_by_b,
    run_n3_battery_parallel,
    run_n4_battery_parallel,
    _n4_worker,
)
from quant.i03.pipeline import artifact_dict, run_structural_analysis


def _fbits(a: float, b: float) -> bool:
    if math.isnan(a) and math.isnan(b):
        return True
    if math.isinf(a) and math.isinf(b):
        return math.copysign(1.0, a) == math.copysign(1.0, b)
    return a == b


def _theta_eq(
    a: list[dict[int, dict[int, float]]], b: list[dict[int, dict[int, float]]]
) -> bool:
    if len(a) != len(b):
        return False
    for xa, xb in zip(a, b):
        if set(xa) != set(xb):
            return False
        for p in xa:
            if set(xa[p]) != set(xb[p]):
                return False
            for k in xa[p]:
                if not _fbits(xa[p][k], xb[p][k]):
                    return False
    return True


def _loc_eq(a, b) -> bool:
    if len(a) != len(b):
        return False
    for ba, bb in zip(a, b):
        if len(ba) != len(bb):
            return False
        for da, db in zip(ba, bb):
            if (
                da.period != db.period
                or da.hard_degenerate != db.hard_degenerate
                or da.n_queries_used != db.n_queries_used
                or not _fbits(da.Lambda, db.Lambda)
                or not _fbits(da.Gamma, db.Gamma)
            ):
                return False
    return True


def _result_eq(a, b) -> bool:
    """Bitwise structural equivalence of I03RunResult scientific fields."""

    art_a = artifact_dict(a, mode="TEST")
    art_b = artifact_dict(b, mode="TEST")
    # Drop operational execution metadata / implementation noise
    for art in (art_a, art_b):
        art.pop("execution", None)
        art.pop("implementation_id", None)
        art.pop("input_hash", None)
        art.pop("timing", None)
    return art_a == art_b


class _DelayFuture:
    def __init__(self, fn: Callable, b: int, complete_after: float) -> None:
        self._fn = fn
        self._b = b
        self._complete_after = complete_after
        self._result: Any = None
        self._exc: BaseException | None = None
        self._done = False

    def result(self, timeout: float | None = None) -> Any:
        if not self._done:
            time.sleep(self._complete_after)
            try:
                self._result = self._fn(self._b)
            except BaseException as e:  # noqa: BLE001
                self._exc = e
            self._done = True
        if self._exc is not None:
            raise self._exc
        return self._result


class _AdversarialOrderExecutor:
    """Completes even ``b`` before odd ``b`` (not ascending). Spawn-free test double."""

    def __init__(
        self, max_workers: int, initializer=None, initargs: tuple = ()
    ) -> None:
        if initializer is not None:
            initializer(*(initargs or ()))

    def __enter__(self) -> _AdversarialOrderExecutor:
        return self

    def __exit__(self, *args: object) -> None:
        return None

    def submit(self, fn: Callable, b: int) -> _DelayFuture:
        complete_after = 0.0 if (b % 2 == 0) else 0.01
        return _DelayFuture(fn, b, complete_after)


def test_reassemble_fail_closed_missing_duplicate_wrong_family() -> None:
    ok = [{"b": 1, "family": "N4"}, {"b": 2, "family": "N4"}]
    assert [r["b"] for r in reassemble_by_b(ok, B=2, family="N4")] == [1, 2]

    with pytest.raises(ParallelSurrogateError, match="missing"):
        reassemble_by_b([{"b": 1, "family": "N4"}], B=2, family="N4")

    with pytest.raises(ParallelSurrogateError, match="duplicate"):
        reassemble_by_b(
            [{"b": 1, "family": "N4"}, {"b": 1, "family": "N4"}],
            B=2,
            family="N4",
        )

    with pytest.raises(ParallelSurrogateError, match="wrong null family"):
        reassemble_by_b(
            [{"b": 1, "family": "N3"}, {"b": 2, "family": "N4"}],
            B=2,
            family="N4",
        )

    with pytest.raises(ParallelSurrogateError, match="unexpected"):
        reassemble_by_b(
            [{"b": 1, "family": "N4"}, {"b": 9, "family": "N4"}],
            B=2,
            family="N4",
        )

    with pytest.raises(ParallelSurrogateError, match="malformed"):
        reassemble_by_b([{"b": 1}], B=1, family="N4")  # type: ignore[list-item]


def test_adversarial_completion_order_reassembly() -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    payload = {
        "returns": r,
        "n4_scale": scale,
        "blocks": blocks,
        "cfg": cfg,
        "do_loc_n4": False,
        "include_returns": True,
    }
    raw = map_surrogate_b(
        _n4_worker,
        range(1, 7),
        workers=2,
        initargs=(payload,),
        executor_factory=_AdversarialOrderExecutor,
    )
    ordered_bs = [row["b"] for row in raw]
    assert ordered_bs != list(range(1, 7)), ordered_bs
    ordered = reassemble_by_b(raw, B=6, family="N4")
    assert [row["b"] for row in ordered] == list(range(1, 7))
    # Surrogate identity vs serial generator
    for row in ordered:
        b = row["b"]
        assert row["seed"] == cfg.master_seed + b
        direct = n4_surrogate_returns(r, scale, b, cfg)
        assert np.array_equal(row["returns"], direct, equal_nan=True)


def test_worker_exception_fail_closed_does_not_shrink_b() -> None:
    def boom(b: int) -> dict[str, Any]:
        if b == 3:
            raise RuntimeError("worker boom")
        return {"b": b, "family": "N4"}

    with pytest.raises(RuntimeError, match="worker boom"):
        map_surrogate_b(boom, range(1, 5), workers=1)


@pytest.mark.parametrize("workers", [1, 2, 4])
def test_n4_serial_vs_parallel_bitwise(workers: int) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    B = 8
    th1, loc1 = run_n4_battery_parallel(
        r, scale, cfg, B=B, workers=1, do_loc_n4=True, blocks=blocks
    )
    thN, locN = run_n4_battery_parallel(
        r, scale, cfg, B=B, workers=workers, do_loc_n4=True, blocks=blocks
    )
    assert _theta_eq(th1, thN)
    assert _loc_eq(loc1, locN)


@pytest.mark.parametrize("workers", [1, 2, 4])
def test_n3_serial_vs_parallel_bitwise(workers: int) -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    blocks = build_blocks(len(r), cfg)
    B = 6
    meta1, th1, rows1 = run_n3_battery_parallel(
        r, cfg, B=B, workers=1, blocks=blocks, include_returns=True
    )
    metaN, thN, rowsN = run_n3_battery_parallel(
        r, cfg, B=B, workers=workers, blocks=blocks, include_returns=True
    )
    assert meta1 == metaN
    assert _theta_eq(th1, thN)
    for a, b in zip(rows1, rowsN):
        assert a["b"] == b["b"]
        assert a["seed"] == b["seed"] == 10_000 + a["b"]
        assert a["converged"] == b["converged"]
        assert a["iterations"] == b["iterations"]
        assert np.array_equal(a["returns"], b["returns"], equal_nan=True)
    # Cross-check vs serial generator + flags
    meta_s, sur_s = generate_n3_battery(r, cfg, B=B)
    assert meta_s.converged_flags == meta1.converged_flags
    for i, row in enumerate(rows1):
        assert np.array_equal(row["returns"], sur_s[i], equal_nan=True)


def test_pipeline_workers_bitwise_equivalence(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("I03_ALLOW_TEST_OVERRIDES", "1")
    r = generate_hat_returns()
    cfg = DEFAULT_CONFIG
    serial = run_structural_analysis(
        r, cfg, B_n4=6, B_n3=4, compute_locality_on_n4=True, workers=1
    )
    for w in (2, 4):
        par = run_structural_analysis(
            r, cfg, B_n4=6, B_n3=4, compute_locality_on_n4=True, workers=w
        )
        assert _result_eq(serial, par)
        assert par.workers_requested == w
        assert par.workers_used == w


def test_seed_independent_of_worker_scheduling() -> None:
    cfg = DEFAULT_CONFIG
    r = generate_hat_returns()
    scale = build_n4_scale_path(r, cfg)
    blocks = build_blocks(len(r), cfg)
    payload = {
        "returns": r,
        "n4_scale": scale,
        "blocks": blocks,
        "cfg": cfg,
        "do_loc_n4": False,
        "include_returns": False,
    }
    raw = map_surrogate_b(
        _n4_worker,
        [5, 1, 3],
        workers=2,
        initargs=(payload,),
        executor_factory=_AdversarialOrderExecutor,
    )
    by_b = {row["b"]: row for row in raw}
    assert by_b[1]["seed"] == 42 + 1
    assert by_b[3]["seed"] == 42 + 3
    assert by_b[5]["seed"] == 42 + 5
