"""Tests invariants I1, I2 — risk sovereignty."""

import pytest

from quant.contracts.base import AuthorizedExposure, SignalRef
from quant.contracts.risk_decision import RiskDecision, RiskVerdict
from quant.invariants.risk import assert_risk_sovereignty


def test_no_trade_sovereignty(sample_signal, sample_no_trade_decision):
    assert_risk_sovereignty(
        sample_no_trade_decision,
        [sample_signal],
    )


def test_exposure_cannot_exceed_proposed(sample_signal):
    decision = RiskDecision(
        decision_id="d",
        verdict=RiskVerdict.AUTHORISE,
        signal_refs=[
            SignalRef(
                signal_id=sample_signal.signal_id,
                strategy_id=sample_signal.strategy_id,
            )
        ],
        decided_at=sample_signal.market_state_ref.as_of,
        authorized_exposure=AuthorizedExposure(gross=1.0, net=1.0),
        constraints_applied=["test"],
    )
    with pytest.raises(ValueError, match="sovereignty"):
        assert_risk_sovereignty(
            decision,
            [sample_signal],
            proposed_gross_exposure=0.5,
        )
