"""Tests C02 — DatasetSnapshot."""

from datetime import datetime, timezone

import pytest

from quant.contracts.dataset_snapshot import DatasetSnapshot, Provenance

UTC = timezone.utc


def test_snapshot_valid(sample_snapshot):
    assert sample_snapshot.contract_id == "C02"
    assert sample_snapshot.fingerprint.startswith("sha256:")


def test_availability_cutoff_after_as_of_rejected():
    t = datetime(2024, 1, 15, tzinfo=UTC)
    with pytest.raises(ValueError, match="availability_cutoff"):
        DatasetSnapshot(
            snapshot_id="bad",
            fingerprint="sha256:x",
            as_of=t,
            availability_cutoff=datetime(2024, 1, 16, tzinfo=UTC),
            provenance=Provenance(
                source_label="x",
                universe_description="u",
                time_range_start=datetime(2023, 1, 1, tzinfo=UTC),
                time_range_end=t,
                survivorship_bias_acknowledged=False,
            ),
        )


def test_invalid_time_range():
    t = datetime(2024, 1, 15, tzinfo=UTC)
    with pytest.raises(ValueError, match="time_range"):
        DatasetSnapshot(
            snapshot_id="bad",
            fingerprint="sha256:x",
            as_of=t,
            availability_cutoff=t,
            provenance=Provenance(
                source_label="x",
                universe_description="u",
                time_range_start=t,
                time_range_end=t,
                survivorship_bias_acknowledged=False,
            ),
        )
