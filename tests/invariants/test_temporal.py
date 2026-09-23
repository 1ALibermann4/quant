"""Tests invariant I3 — no look-ahead."""

from datetime import datetime, timezone

import pytest

from quant.invariants.temporal import assert_no_look_ahead

UTC = timezone.utc


def test_no_look_ahead_passes(sample_snapshot, sample_market_state):
    assert_no_look_ahead(sample_snapshot, sample_market_state)


def test_no_look_ahead_feature_violation(sample_snapshot, sample_market_state):
    future = datetime(2024, 1, 20, tzinfo=UTC)
    with pytest.raises(ValueError, match="look-ahead"):
        assert_no_look_ahead(
            sample_snapshot,
            sample_market_state,
            feature_timestamps={"log_return": future},
        )
