"""Skew and sentiment data provider stub.

The functions in this module fetch option skew and sentiment indicators.
In the current stub implementation they return placeholder values.  A
future implementation should query the SKEW index and other sentiment
indicators (e.g. put/call ratios).
"""

from typing import Dict


def get_skew_data() -> Dict[str, float]:
    """Return a dictionary containing skew and sentiment metrics.

    Keys expected by the engine include:

    - ``skew``: The CBOE SKEW index value.
    - ``put_call_ratio``: (Optional) The total market put/call ratio.

    Returns:
        Dict[str, float]: A dictionary with placeholder values.
    """
    return {"skew": None, "put_call_ratio": None}