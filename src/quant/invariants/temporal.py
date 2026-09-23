"""Invariant I3 — intégrité temporelle (no look-ahead)."""

from __future__ import annotations

from datetime import datetime

from quant.contracts.dataset_snapshot import DatasetSnapshot
from quant.contracts.market_state import MarketState


def assert_no_look_ahead(
    snapshot: DatasetSnapshot,
    market_state: MarketState,
    *,
    feature_timestamps: dict[str, datetime] | None = None,
) -> None:
    """
    Vérifie qu'aucune information postérieure à availability_cutoff n'est utilisée.

    Raises ValueError si violation détectée.
    """
    cutoff = snapshot.availability_cutoff
    market_state.assert_temporal_integrity(cutoff)

    if feature_timestamps:
        for name, ts in feature_timestamps.items():
            if ts > cutoff:
                raise ValueError(
                    f"look-ahead detected: feature {name!r} timestamp {ts} "
                    f"> availability_cutoff {cutoff}"
                )
