"""Tests C05 — RiskDecision."""

from datetime import datetime, timezone

import pytest

from quant.contracts.base import AuthorizedExposure, SignalRef
from quant.contracts.risk_decision import RiskDecision, RiskVerdict

UTC = timezone.utc
T0 = datetime(2024, 1, 15, tzinfo=UTC)


def test_no_trade_requires_veto_reason(sample_signal):
    with pytest.raises(ValueError, match="veto_reason"):
        RiskDecision(
            decision_id="d",
            verdict=RiskVerdict.NO_TRADE,
            signal_refs=[
                SignalRef(
                    signal_id=sample_signal.signal_id,
                    strategy_id=sample_signal.strategy_id,
                )
            ],
            decided_at=T0,
        )


def test_no_trade_no_exposure(sample_no_trade_decision):
    assert sample_no_trade_decision.is_no_trade
    assert sample_no_trade_decision.authorized_exposure is None
    assert sample_no_trade_decision.veto_reason


def test_reduce_requires_factor(sample_signal):
    with pytest.raises(ValueError, match="reduce_factor"):
        RiskDecision(
            decision_id="d",
            verdict=RiskVerdict.REDUCE,
            signal_refs=[
                SignalRef(
                    signal_id=sample_signal.signal_id,
                    strategy_id=sample_signal.strategy_id,
                )
            ],
            decided_at=T0,
        )


def test_authorise_with_exposure(sample_signal):
    d = RiskDecision(
        decision_id="d",
        verdict=RiskVerdict.AUTHORISE,
        signal_refs=[
            SignalRef(
                signal_id=sample_signal.signal_id,
                strategy_id=sample_signal.strategy_id,
            )
        ],
        decided_at=T0,
        authorized_exposure=AuthorizedExposure(gross=0.1, net=0.1),
        constraints_applied=["max_position"],
    )
    assert d.verdict == RiskVerdict.AUTHORISE
