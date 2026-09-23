"""Tests C03 — MarketState."""

from datetime import datetime, timezone

import pytest

from quant.contracts.base import DatasetSnapshotRef
from quant.contracts.market_state import ExperimentalBranch, MarketState

UTC = timezone.utc


def test_market_state_defaults_classical(sample_snapshot):
    ms = MarketState(
        market_state_id="ms",
        as_of=sample_snapshot.as_of,
        dataset_snapshot_ref=DatasetSnapshotRef(
            snapshot_id=sample_snapshot.snapshot_id,
            fingerprint=sample_snapshot.fingerprint,
        ),
    )
    assert ms.experimental_branch == ExperimentalBranch.CLASSICAL


def test_regime_uncertainty_range(sample_snapshot):
    with pytest.raises(ValueError, match="regime_uncertainty"):
        MarketState(
            market_state_id="ms",
            as_of=sample_snapshot.as_of,
            dataset_snapshot_ref=DatasetSnapshotRef(
                snapshot_id=sample_snapshot.snapshot_id,
                fingerprint=sample_snapshot.fingerprint,
            ),
            regime_uncertainty=1.5,
        )


def test_temporal_integrity_violation(sample_snapshot):
    ms = MarketState(
        market_state_id="ms",
        as_of=datetime(2024, 1, 20, tzinfo=UTC),
        dataset_snapshot_ref=DatasetSnapshotRef(
            snapshot_id=sample_snapshot.snapshot_id,
            fingerprint=sample_snapshot.fingerprint,
        ),
    )
    with pytest.raises(ValueError, match="exceeds"):
        ms.assert_temporal_integrity(sample_snapshot.availability_cutoff)
