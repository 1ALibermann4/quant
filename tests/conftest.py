"""Fixtures partagées pour tests P0."""

from __future__ import annotations

from datetime import datetime, timezone

import pytest

from quant.contracts.base import (
    DatasetSnapshotRef,
    GateResult,
    GateVerdict,
    MarketStateRef,
    SignalRef,
)
from quant.contracts.dataset_snapshot import DatasetSnapshot, Provenance
from quant.contracts.experiment import Experiment, ExperimentProtocol
from quant.contracts.market_state import FeatureRef, MarketState
from quant.contracts.risk_decision import RiskDecision, RiskVerdict
from quant.contracts.strategy_signal import SignalDirection, StrategySignal

UTC = timezone.utc
T0 = datetime(2024, 1, 15, 16, 0, tzinfo=UTC)
T_START = datetime(2023, 1, 1, tzinfo=UTC)
T_END = datetime(2024, 1, 15, tzinfo=UTC)


@pytest.fixture
def sample_snapshot() -> DatasetSnapshot:
    return DatasetSnapshot(
        snapshot_id="snap-001",
        fingerprint="sha256:abc123",
        as_of=T0,
        availability_cutoff=T0,
        provenance=Provenance(
            source_label="fixture",
            universe_description="TEST_UNIVERSE",
            time_range_start=T_START,
            time_range_end=T_END,
            survivorship_bias_acknowledged=True,
        ),
    )


@pytest.fixture
def sample_market_state(sample_snapshot: DatasetSnapshot) -> MarketState:
    return MarketState(
        market_state_id="ms-001",
        as_of=T0,
        dataset_snapshot_ref=DatasetSnapshotRef(
            snapshot_id=sample_snapshot.snapshot_id,
            fingerprint=sample_snapshot.fingerprint,
        ),
        feature_refs=[
            FeatureRef(name="log_return", version="1.0", value_ref="feat/log_return/001")
        ],
    )


@pytest.fixture
def sample_signal(sample_market_state: MarketState) -> StrategySignal:
    return StrategySignal(
        signal_id="sig-001",
        strategy_id="fixture_strategy",
        strategy_version="0.0.0",
        market_state_ref=MarketStateRef(
            market_state_id=sample_market_state.market_state_id,
            as_of=sample_market_state.as_of,
        ),
        direction=SignalDirection.LONG,
        raw_signal=0.5,
        confidence=0.7,
    )


@pytest.fixture
def sample_experiment(sample_snapshot: DatasetSnapshot) -> Experiment:
    return Experiment(
        experiment_id="I00-fixture",
        hypothesis="Fixture hypothesis for contract tests",
        success_criteria=["structure validates"],
        dataset_snapshot_ref=DatasetSnapshotRef(
            snapshot_id=sample_snapshot.snapshot_id,
            fingerprint=sample_snapshot.fingerprint,
        ),
        baselines=["B0"],
        gates=[
            GateResult(
                gate_id="P0-FIX",
                description="fixture gate",
                verdict=GateVerdict.PASS,
                evidence_ref="tests/conftest.py",
            )
        ],
        protocol=ExperimentProtocol.EXPLORATORY,
    )


@pytest.fixture
def sample_no_trade_decision(sample_signal: StrategySignal) -> RiskDecision:
    return RiskDecision(
        decision_id="rd-001",
        verdict=RiskVerdict.NO_TRADE,
        signal_refs=[
            SignalRef(
                signal_id=sample_signal.signal_id,
                strategy_id=sample_signal.strategy_id,
            )
        ],
        decided_at=T0,
        veto_reason="Insufficient edge after costs — explicit NO_TRADE",
        constraints_applied=["min_edge_not_met"],
    )
