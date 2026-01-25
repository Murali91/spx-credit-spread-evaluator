"""Helper functions for formatting decision explanations.

This module contains utilities to convert a ``DecisionResult`` into user‑
friendly text.  Although not strictly necessary for a minimal v0.1 release,
providing a separate explanation builder makes it easier to adjust the
presentation in future versions and to reuse the same logic in tests and the
Streamlit app.
"""

from .types import DecisionResult


def build_explanation_text(result: DecisionResult) -> str:
    """Concatenate the reasons in a ``DecisionResult`` into a single string.

    Each reason will be prefixed with a bullet (``•``).  The returned
    string is suitable for use in markdown or plain text displays.

    Args:
        result: A populated ``DecisionResult`` instance.

    Returns:
        str: A string containing the bullet‑point explanations separated by
            newlines.
    """
    return "\n".join(f"• {reason}" for reason in result.reasons)