"""Invariants I1, I2 — souveraineté du Risk Engine et NO_TRADE."""

from __future__ import annotations

from quant.contracts.risk_decision import RiskDecision, RiskVerdict
from quant.contracts.strategy_signal import StrategySignal


def assert_risk_sovereignty(
    decision: RiskDecision,
    signals: list[StrategySignal],
    *,
    proposed_gross_exposure: float | None = None,
) -> None:
    """
    Vérifie que la décision risque ne dépasse pas les propositions
    et que NO_TRADE est explicite.

    Raises ValueError si violation.
    """
    if decision.verdict == RiskVerdict.NO_TRADE:
        if not decision.veto_reason:
            raise ValueError("NO_TRADE requires explicit veto_reason (I2)")
        if decision.authorized_exposure is not None:
            raise ValueError("NO_TRADE must not carry authorized_exposure (I2)")

    if decision.verdict == RiskVerdict.VETO and decision.authorized_exposure is not None:
        raise ValueError("VETO must not carry authorized_exposure (I1)")

    if (
        proposed_gross_exposure is not None
        and decision.authorized_exposure is not None
        and decision.authorized_exposure.gross > proposed_gross_exposure
    ):
        raise ValueError(
            "authorized_exposure exceeds proposed exposure — risk sovereignty violated (I1)"
        )

    # Confidence élevée ne doit pas être interprétée comme autorisation implicite
    for signal in signals:
        if signal.confidence is not None and signal.confidence > 0.99:
            if decision.verdict == RiskVerdict.AUTHORISE and not decision.constraints_applied:
                # Autorisation sans contraintes malgré signal très confiant — acceptable
                # mais on vérifie qu'une exposure explicite existe
                if decision.authorized_exposure is None:
                    raise ValueError(
                        "AUTHORISE requires explicit authorized_exposure regardless of confidence"
                    )
