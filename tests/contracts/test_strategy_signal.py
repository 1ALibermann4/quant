"""Tests C04 — StrategySignal."""

import pytest

from quant.contracts.base import MarketStateRef
from quant.contracts.strategy_signal import SignalDirection, StrategySignal


def test_abstain_requires_reason(sample_market_state):
    with pytest.raises(ValueError, match="abstain_reason"):
        StrategySignal(
            signal_id="s",
            strategy_id="st",
            strategy_version="0",
            market_state_ref=MarketStateRef(
                market_state_id=sample_market_state.market_state_id,
                as_of=sample_market_state.as_of,
            ),
            direction=SignalDirection.ABSTAIN,
        )


def test_abstain_with_reason(sample_market_state):
    sig = StrategySignal(
        signal_id="s",
        strategy_id="st",
        strategy_version="0",
        market_state_ref=MarketStateRef(
            market_state_id=sample_market_state.market_state_id,
            as_of=sample_market_state.as_of,
        ),
        direction=SignalDirection.ABSTAIN,
        abstain_reason="Regime unknown",
    )
    assert sig.direction == SignalDirection.ABSTAIN


def test_confidence_range(sample_market_state):
    with pytest.raises(ValueError, match="confidence"):
        StrategySignal(
            signal_id="s",
            strategy_id="st",
            strategy_version="0",
            market_state_ref=MarketStateRef(
                market_state_id=sample_market_state.market_state_id,
                as_of=sample_market_state.as_of,
            ),
            direction=SignalDirection.LONG,
            confidence=1.5,
        )
