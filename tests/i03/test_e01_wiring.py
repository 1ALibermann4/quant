"""I03-E01 wiring tests — no market download; no full B=999."""

from __future__ import annotations

import os
from pathlib import Path

import numpy as np
import pytest

from quant.i03.e01 import (
    AUTHORIZED_RETURNS_SHA256,
    STRUCT_TO_EXPL,
    _dataset_record,
    run_e01,
)


def test_structural_to_exploratory_mapping() -> None:
    assert STRUCT_TO_EXPL["PASS"] == "EXPL-SUPPORT"
    assert STRUCT_TO_EXPL["FAIL"] == "EXPL-ABSENT"
    assert STRUCT_TO_EXPL["INCONCLUSIVE"] == "EXPL-INCONCLUSIVE"


def test_e01_refuses_mismatched_snapshot(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    """Gate must STOP before science if returns hash ≠ authorized."""

    from datetime import date, datetime, timezone

    class FakeSeries:
        sessions = tuple(date(1993, 1, 29) for _ in range(10))
        adjusted_price = tuple(float(i) for i in range(10))

        def __len__(self) -> int:
            return len(self.sessions)

    class FakeAcq:
        ticker = "SPY"
        source = "yfinance"
        yfinance_version = "1.6.0"
        request_parameters = {"start": "1993-01-22", "end": "2026-09-25"}
        acquired_at_utc = datetime.fromisoformat("2026-09-24T12:00:16.920799+00:00")
        series = FakeSeries()

    monkeypatch.setattr("quant.i03.e01.load_latest_cache", lambda *a, **k: FakeAcq())
    monkeypatch.setattr(
        "quant.i03.e01.log_returns",
        lambda series: np.array([np.nan] + [0.01] * 9, dtype=np.float64),
    )
    called = {"science": False}

    def boom(*a, **k):
        called["science"] = True
        raise AssertionError("science must not run on mismatch")

    monkeypatch.setattr("quant.i03.e01.run_structural_analysis", boom)
    rc = run_e01(cache_dir=tmp_path, out_dir=tmp_path / "out")
    assert rc == 2
    assert called["science"] is False
    assert not (tmp_path / "out" / "artifact.json").exists()


def test_authorized_constants_match_i02_record() -> None:
    assert AUTHORIZED_RETURNS_SHA256.startswith("sha256:bde9a304")
