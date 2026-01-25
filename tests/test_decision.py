"""Tests for the decision engine.

These tests verify that the ``make_decision`` function returns a ``DecisionResult``
instance with the expected structure.  At this stage the decision logic is
placeholder, so we focus on validating types and output fields.
"""

from engine.decision import make_decision
from engine.types import DecisionResult


def test_make_decision_returns_decision_result() -> None:
    result = make_decision({})
    assert isinstance(result, DecisionResult)
    assert result.decision in ("ENTER", "WAIT"), "decision must be ENTER or WAIT"
    assert isinstance(result.reasons, list), "reasons must be a list"