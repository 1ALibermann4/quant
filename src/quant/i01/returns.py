"""Log-returns from an observation series."""

from __future__ import annotations

import numpy as np

from quant.i01.observations import ObservationSeries


def log_returns(series: ObservationSeries) -> np.ndarray:
    """Return ``r`` of length ``n`` with ``r[0] = nan`` and ``r[t] = ln(P_t/P_{t-1})``.

    Index ``t`` is the session rank of ``P_t``. ``r_t`` is known after the close
    of session ``t`` (DEC-04).
    """

    prices = np.asarray(series.adjusted_price, dtype=np.float64)
    out = np.empty(prices.shape[0], dtype=np.float64)
    out[0] = np.nan
    out[1:] = np.log(prices[1:] / prices[:-1])
    return out
