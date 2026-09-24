"""Vendor-agnostic daily observations.

The I01 core consumes only session dates and a strictly positive price used as
adjusted close. It must not import a data vendor.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True, slots=True)
class ObservationSeries:
    """Ordered daily prices. This is **not** a market calendar.

    Missing calendar days among the rows are just missing rows. Absence of a
    row is not evidence that the market was closed (DR-005).

    Attributes:
        sessions: Strictly increasing session dates, one per price.
        adjusted_price: Positive prices used to form log-returns.
    """

    sessions: tuple[date, ...]
    adjusted_price: tuple[float, ...]

    def __post_init__(self) -> None:
        if len(self.sessions) != len(self.adjusted_price):
            raise ValueError("sessions and adjusted_price must have the same length")
        if len(self.sessions) < 2:
            raise ValueError("ObservationSeries needs at least two sessions")
        previous: date | None = None
        for session, price in zip(self.sessions, self.adjusted_price, strict=True):
            if previous is not None and session <= previous:
                raise ValueError("sessions must be strictly increasing")
            previous = session
            if not (price > 0.0) or price != price:  # NaN check
                raise ValueError("adjusted_price must be finite and strictly positive")

    def __len__(self) -> int:
        return len(self.sessions)
