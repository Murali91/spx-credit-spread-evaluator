"""Market data provider for SPY price history.

This module fetches daily OHLC data for SPY using Yahoo Finance and
derives basic trend inputs used by the decision engine.
"""

from __future__ import annotations

from datetime import datetime
from functools import lru_cache
from typing import Dict, Optional

import pandas as pd
import yfinance as yf


_SPY_SYMBOL = "SPY"
_LOOKBACK_DAYS = 400
_MOVING_AVG_WINDOW = 200


@lru_cache(maxsize=48)
def _fetch_spy_history(as_of: datetime) -> pd.DataFrame:
    as_of_date = pd.Timestamp(as_of).date()
    start = (pd.Timestamp(as_of_date) - pd.Timedelta(days=_LOOKBACK_DAYS)).date()
    end = (pd.Timestamp(as_of_date) + pd.Timedelta(days=1)).date()
    history = yf.download(
        _SPY_SYMBOL,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
    )
    if history.empty:
        raise ValueError("No SPY history returned from Yahoo Finance.")
    return history.sort_index()


def _calculate_moving_average(close_series: pd.Series) -> Optional[float]:
    if len(close_series) < _MOVING_AVG_WINDOW:
        return None
    return float(close_series.rolling(_MOVING_AVG_WINDOW).mean().iloc[-1])


def get_market_data() -> Dict[str, Optional[float]]:
    """Return a dictionary with market data for SPY.

    Returns:
        Dict[str, Optional[float]]: Market data including latest close and a
        long-term moving average.
    """
    cache_key = pd.Timestamp.utcnow().floor("h").to_pydatetime()
    history = _fetch_spy_history(cache_key)
    close_series = history["Close"].copy()
    latest_close = float(close_series.iloc[-1])
    moving_average = _calculate_moving_average(close_series)
    return {
        "close": latest_close,
        "moving_average": moving_average,
    }
