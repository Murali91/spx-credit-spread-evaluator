"""High‑level decision logic for the SPX put credit spread advisor.

This module combines the individual factor scores to arrive at a final
recommendation.  In v0.1 the logic is intentionally simple and returns
a placeholder result.  When the factor functions are fully implemented,
this module should use the thresholds from ``engine.thresholds`` and the
rules defined in ``docs/Decision_Spec_v0.1.md`` to compute a score and
return a ``DecisionResult`` instance.
"""

from typing import Dict

from .types import DecisionResult
from . import factors


def make_decision(data: Dict) -> DecisionResult:
    """Return a ``DecisionResult`` with a recommendation and explanations.

    Args:
        data: A dictionary containing all inputs required by the factor
            functions.  Expected keys include ``market``, ``volatility``,
            ``events`` and ``skew``.  Each value should itself be a
            dictionary matching the expected structure of the corresponding
            factor function.  In the current stub implementation this
            parameter is unused.

    Returns:
        DecisionResult: An object with ``decision`` set to ``"ENTER"`` or
        ``"WAIT"`` and a list of reasons explaining the rationale.
    """
    # TODO: implement real decision logic using factors and thresholds
    # For now, return WAIT with a single generic reason.
    return DecisionResult(decision="WAIT", reasons=["Decision engine not yet implemented."])