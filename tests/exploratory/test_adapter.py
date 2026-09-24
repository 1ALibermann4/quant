"""Adapter tests use a fake frame — no network in CI."""

from __future__ import annotations

import sys
from datetime import datetime, timezone
from types import SimpleNamespace

import pandas as pd
import pytest

from quant.exploratory.adapter import (
    EXPLICIT_HISTORY_PARAMS,
    PINNED_YFINANCE_VERSION,
    acquire_spy,
)
from quant.exploratory.status import BANNER


def _frame() -> pd.DataFrame:
    idx = pd.date_range("1993-01-22", periods=5, freq="B", tz="America/New_York")
    return pd.DataFrame(
        {
            "Open": [1.0] * 5,
            "High": [1.0] * 5,
            "Low": [1.0] * 5,
            "Close": [10.0, 10.1, 10.2, 10.3, 10.4],
            "Adj Close": [1.0, 1.1, 1.2, 1.3, 1.4],
            "Volume": [1] * 5,
        },
        index=idx,
    )


def test_explicit_params_include_auto_adjust_and_repair() -> None:
    assert EXPLICIT_HISTORY_PARAMS["auto_adjust"] is False
    assert EXPLICIT_HISTORY_PARAMS["repair"] is False
    assert EXPLICIT_HISTORY_PARAMS["interval"] == "1d"


def test_acquire_spy_maps_adj_close(monkeypatch: pytest.MonkeyPatch) -> None:
    calls: list[dict] = []

    class FakeTicker:
        def __init__(self, ticker: str) -> None:
            self.ticker = ticker

        def history(self, **kwargs):
            calls.append(kwargs)
            return _frame()

    fake_yf = SimpleNamespace(__version__=PINNED_YFINANCE_VERSION, Ticker=FakeTicker)
    monkeypatch.setitem(sys.modules, "yfinance", fake_yf)

    acquisition = acquire_spy(end="1993-02-01")
    assert acquisition.banner == BANNER
    assert acquisition.series.adjusted_price[0] == pytest.approx(1.0)
    assert acquisition.raw_close[0] == pytest.approx(10.0)
    assert calls[0]["auto_adjust"] is False
    assert calls[0]["repair"] is False
    assert calls[0]["start"] == "1993-01-22"
    assert calls[0]["end"] == "1993-02-01"
    assert acquisition.acquired_at_utc.tzinfo == timezone.utc
    assert isinstance(acquisition.acquired_at_utc, datetime)
