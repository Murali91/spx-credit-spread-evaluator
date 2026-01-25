"""Macroeconomic events provider stub.

This module contains a function for retrieving information about upcoming
high‑impact macroeconomic events (e.g. Federal Reserve meetings, CPI
releases, jobs reports).  In a real implementation it would fetch
scheduled events from a calendar API.  For v0.1 it returns placeholders.
"""

from typing import Dict, Optional


def get_upcoming_macro_events() -> Dict[str, Optional[int]]:
    """Return a dictionary describing upcoming macro events.

    The returned dictionary may contain:

    - ``days_until_next``: An integer representing the number of trading days
      until the next high‑impact event (e.g. 0 for today, 1 for tomorrow).  If
      unknown, the value should be ``None``.
    - ``description``: A short string describing the next event (e.g.
      "FOMC decision").  May be ``None`` if no event is scheduled.

    Returns:
        Dict[str, Optional[int]]: A dictionary with placeholder values.
    """
    return {"days_until_next": None, "description": None}