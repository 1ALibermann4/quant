"""yfinance → :class:`ObservationSeries`. The I01 core never imports this module."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date, datetime, timezone
from pathlib import Path
from typing import Any

from quant.exploratory.status import BANNER, stamp
from quant.i01.observations import ObservationSeries

PINNED_YFINANCE_VERSION = "1.6.0"
DEFAULT_TICKER = "SPY"
# Exclusive end is filled at acquisition time (UTC calendar date + 1 day).
DEFAULT_START = "1993-01-22"

# Every history() argument is set here. Do not omit a key to inherit a default.
EXPLICIT_HISTORY_PARAMS: dict[str, Any] = {
    "interval": "1d",
    "prepost": False,
    "actions": True,
    "auto_adjust": False,
    "back_adjust": False,
    "repair": False,
    "keepna": False,
    "rounding": False,
    "timeout": 30,
    "raise_errors": True,
}


@dataclass(frozen=True, slots=True)
class ExploratoryAcquisition:
    """Traceable UNQUALIFIED download. Not a C02 snapshot."""

    ticker: str
    source: str
    yfinance_version: str
    request_parameters: dict[str, Any]
    acquired_at_utc: datetime
    series: ObservationSeries
    raw_close: tuple[float, ...]
    banner: str = BANNER


def _session_date(index_value: Any) -> date:
    ts = index_value
    if getattr(ts, "tzinfo", None) is not None:
        try:
            from zoneinfo import ZoneInfo

            ts = ts.tz_convert(ZoneInfo("America/New_York"))
        except Exception:
            ts = ts.tz_convert("America/New_York")
    return ts.date() if hasattr(ts, "date") else date.fromisoformat(str(ts)[:10])


def acquire_spy(
    *,
    ticker: str = DEFAULT_TICKER,
    start: str = DEFAULT_START,
    end: str | None = None,
    cache_dir: Path | None = None,
) -> ExploratoryAcquisition:
    """Download daily bars with explicit yfinance parameters.

    The price fed to I01 is the ``Adj Close`` column. ``Close`` is stored only
    as raw trace. Rows are not treated as an official market calendar.
    """

    import yfinance as yf

    installed = getattr(yf, "__version__", "unknown")
    if installed != PINNED_YFINANCE_VERSION:
        raise RuntimeError(
            f"yfinance {PINNED_YFINANCE_VERSION} is pinned for I01-E01; found {installed}"
        )

    acquired_at = datetime.now(timezone.utc)
    if end is None:
        # yfinance treats ``end`` as exclusive.
        end = date.fromisoformat(acquired_at.date().isoformat()).isoformat()
        # Use tomorrow UTC so today's bar can appear if already published.
        from datetime import timedelta

        end = (acquired_at.date() + timedelta(days=1)).isoformat()

    params = {
        **EXPLICIT_HISTORY_PARAMS,
        "start": start,
        "end": end,
    }
    frame = yf.Ticker(ticker).history(**params)
    if frame is None or frame.empty:
        raise RuntimeError(f"yfinance returned no rows for {ticker}")
    if "Adj Close" not in frame.columns or "Close" not in frame.columns:
        raise RuntimeError(
            "auto_adjust=False must yield both Close and Adj Close; refusing implicit Close"
        )

    sessions = tuple(_session_date(idx) for idx in frame.index)
    adj = tuple(float(v) for v in frame["Adj Close"].tolist())
    raw = tuple(float(v) for v in frame["Close"].tolist())
    series = ObservationSeries(sessions=sessions, adjusted_price=adj)
    acquisition = ExploratoryAcquisition(
        ticker=ticker,
        source="yfinance",
        yfinance_version=installed,
        request_parameters=params,
        acquired_at_utc=acquired_at,
        series=series,
        raw_close=raw,
    )
    if cache_dir is not None:
        write_cache(cache_dir, acquisition, frame)
    return acquisition


def write_cache(cache_dir: Path, acquisition: ExploratoryAcquisition, frame: Any) -> Path:
    """Persist the UNQUALIFIED download outside git."""

    cache_dir = Path(cache_dir)
    cache_dir.mkdir(parents=True, exist_ok=True)
    stamp_name = acquisition.acquired_at_utc.strftime("%Y%m%dT%H%M%SZ")
    base = cache_dir / f"UNQUALIFIED_{acquisition.ticker}_{stamp_name}"
    csv_path = base.with_suffix(".csv")
    meta_path = Path(str(base) + ".meta.json")
    frame.to_csv(csv_path)
    meta = {
        **stamp(),
        "ticker": acquisition.ticker,
        "source": acquisition.source,
        "yfinance_version": acquisition.yfinance_version,
        "request_parameters": acquisition.request_parameters,
        "acquired_at_utc": acquisition.acquired_at_utc.isoformat(),
        "n_sessions": len(acquisition.series),
        "first_session": acquisition.series.sessions[0].isoformat(),
        "last_session": acquisition.series.sessions[-1].isoformat(),
        "price_field_used_by_i01": "Adj Close",
        "calendar_authority": False,
        "csv": str(csv_path),
    }
    meta_path.write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
    readme = cache_dir / "README_UNQUALIFIED.txt"
    readme.write_text(
        f"{BANNER}\n"
        "This directory is a sandbox cache. Do not commit. Do not treat as C02.\n"
        "Do not treat row dates as an official NYSE calendar.\n",
        encoding="utf-8",
    )
    return csv_path


def load_latest_cache(cache_dir: Path, ticker: str = DEFAULT_TICKER) -> ExploratoryAcquisition:
    """Reload the newest UNQUALIFIED CSV so E02 diagnoses the same bars as E01."""

    cache_dir = Path(cache_dir)
    metas = sorted(cache_dir.glob(f"UNQUALIFIED_{ticker}_*.meta.json"))
    if not metas:
        raise FileNotFoundError(
            f"no UNQUALIFIED {ticker} cache in {cache_dir}; run I01-E01 first"
        )
    meta_path = metas[-1]
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    csv_path = Path(meta["csv"])
    if not csv_path.is_file():
        csv_path = meta_path.with_suffix("").with_suffix(".csv")
        if not csv_path.is_file():
            raise FileNotFoundError(f"cache csv missing for {meta_path}")
    import pandas as pd

    frame = pd.read_csv(csv_path, index_col=0, parse_dates=True)
    if "Adj Close" not in frame.columns or "Close" not in frame.columns:
        raise RuntimeError("cached frame must contain Close and Adj Close")
    sessions = tuple(_session_date(idx) for idx in frame.index)
    acquired_at = datetime.fromisoformat(meta["acquired_at_utc"])
    return ExploratoryAcquisition(
        ticker=str(meta["ticker"]),
        source=str(meta["source"]),
        yfinance_version=str(meta["yfinance_version"]),
        request_parameters=dict(meta["request_parameters"]),
        acquired_at_utc=acquired_at,
        series=ObservationSeries(
            sessions=sessions,
            adjusted_price=tuple(float(v) for v in frame["Adj Close"].tolist()),
        ),
        raw_close=tuple(float(v) for v in frame["Close"].tolist()),
    )
