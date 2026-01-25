"""Earnings events provider stub.

This module provides functions to determine when major S&P 500 constituents
report earnings.  In a real implementation it would query an earnings
calendar API or scrape dates for the largest companies (e.g. Apple,
Microsoft).  For v0.1 it returns placeholders.
"""

from typing import Dict, Optional


def get_upcoming_earnings_events() -> Dict[str, Optional[int]]:
    """Return a dictionary describing upcoming earnings events.

    The returned dictionary may include:

    - ``days_until_next``: The number of days until the next major earnings
      release among the top S&P 500 constituents.  ``None`` if unknown.
    - ``description``: A short description (e.g. "Apple earnings").  ``None``
      if there are no imminent earnings.

    Returns:
        Dict[str, Optional[int]]: A dictionary with placeholder values.
    """
    return {"days_until_next": None, "description": None}