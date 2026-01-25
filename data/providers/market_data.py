"""Market data provider stub.

This module defines a function that returns the latest market price and
trend data needed by the decision engine.  In a real implementation this
would call an API such as Yahoo Finance or Alpha Vantage to fetch
SPY/SPX prices and compute moving averages.  For v0.1 this function
returns ``None`` values as placeholders.
"""

from typing import Dict


def get_market_data() -> Dict[str, float]:
    """Return a dictionary with market data for SPY/SPX.

    Keys expected by the engine include:

    - ``close``: The most recent closing price.
    - ``moving_average``: A long‑term moving average (e.g. 200‑day MA).

    In this stub implementation all values are ``None``.  Replace this
    function with real data retrieval in a later version.

    Returns:
        Dict[str, float]: A dictionary containing placeholder values.
    """
    return {"close": None, "moving_average": None}