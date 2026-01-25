"""Datatypes for the decision engine.

This module defines a simple dataclass used to encapsulate the output of the
decision logic.  The result includes the binary decision and a list of
reasons that explain the rationale.  Keeping the result as a dataclass
supports type checking and future extensibility (e.g. adding confidence
scores or factor values).
"""

from dataclasses import dataclass, field
from typing import List


@dataclass
class DecisionResult:
    """Represents the output of the decision engine.

    Attributes:
        decision: Either ``"ENTER"`` or ``"WAIT"``.  The value is normalised to upper
            case and validated in ``__post_init__``.
        reasons: A list of strings providing explanatory bullet points.  Each entry
            should correspond to a factor considered in the decision logic.
    """

    decision: str
    reasons: List[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        # Normalise decision and validate allowed values
        self.decision = self.decision.upper()
        if self.decision not in ("ENTER", "WAIT"):
            raise ValueError("decision must be 'ENTER' or 'WAIT'")