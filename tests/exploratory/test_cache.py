"""Reload UNQUALIFIED cache without a network call."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

from quant.exploratory.adapter import ExploratoryAcquisition, load_latest_cache, write_cache
from quant.exploratory.status import BANNER
from quant.i01.observations import ObservationSeries


def test_load_latest_cache_roundtrip(tmp_path: Path) -> None:
    idx = pd.date_range("1993-01-29", periods=4, freq="B", tz="America/New_York")
    frame = pd.DataFrame(
        {
            "Open": [1.0] * 4,
            "High": [1.0] * 4,
            "Low": [1.0] * 4,
            "Close": [10.0, 10.1, 10.2, 10.3],
            "Adj Close": [1.0, 1.1, 1.2, 1.3],
            "Volume": [1] * 4,
        },
        index=idx,
    )
    acquisition = ExploratoryAcquisition(
        ticker="SPY",
        source="yfinance",
        yfinance_version="1.6.0",
        request_parameters={"auto_adjust": False, "repair": False},
        acquired_at_utc=datetime(2026, 9, 24, 12, 0, 16, tzinfo=timezone.utc),
        series=ObservationSeries(
            sessions=tuple(ts.date() for ts in idx),
            adjusted_price=(1.0, 1.1, 1.2, 1.3),
        ),
        raw_close=(10.0, 10.1, 10.2, 10.3),
        banner=BANNER,
    )
    write_cache(tmp_path, acquisition, frame)
    loaded = load_latest_cache(tmp_path, ticker="SPY")
    assert loaded.series.adjusted_price == acquisition.series.adjusted_price
    assert loaded.request_parameters["auto_adjust"] is False
    assert loaded.yfinance_version == "1.6.0"
