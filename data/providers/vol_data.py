"""Volatility data provider stub.

This module defines a function that returns implied volatility metrics
required by the decision engine.  In a real implementation this would
query a data source for VIX values and calculate percentile rankings.
For v0.1 it returns ``None`` placeholders.
"""

from typing import Dict


def get_vol_data() -> Dict[str, float]:
    """Return a dictionary with volatility metrics.

    Keys expected by the engine include:

    - ``vix``: The current VIX index value.
    - ``iv_percentile``: The percentile rank of implied volatility over
      a look‑back period (e.g. the past year).

    Returns:
        Dict[str, float]: A dictionary with placeholder values (all ``None``).
    """
    return {"vix": None, "iv_percentile": None}