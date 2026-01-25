"""Volatility data provider using Yahoo Finance."""

from __future__ import annotations

from functools import lru_cache
from typing import Dict, Optional

import pandas as pd
import yfinance as yf


_VIX_SYMBOL = "^VIX"
_LOOKBACK_DAYS = 400
_TRADING_DAYS_1Y = 252


@lru_cache(maxsize=4)
def _fetch_vix_history() -> pd.DataFrame:
    start = (pd.Timestamp.utcnow() - pd.Timedelta(days=_LOOKBACK_DAYS)).date()
    end = (pd.Timestamp.utcnow() + pd.Timedelta(days=1)).date()
    history = yf.download(
        _VIX_SYMBOL,
        start=start,
        end=end,
        progress=False,
        auto_adjust=False,
    )
    if history.empty:
        raise ValueError("No VIX history returned from Yahoo Finance.")
    return history.sort_index()


def _calculate_percentile_rank(series: pd.Series) -> Optional[float]:
    if series.empty:
        return None
    percentile = series.rank(pct=True).iloc[-1] * 100
    return float(percentile)


def get_vol_data() -> Dict[str, Optional[float]]:
    """Return a dictionary with volatility metrics derived from VIX data."""
    history = _fetch_vix_history()
    close_series = history["Close"].copy()
    vix_today = float(close_series.iloc[-1])
    window = close_series.tail(_TRADING_DAYS_1Y)
    vix_percentile_1y = _calculate_percentile_rank(window)
    return {
        "vix": vix_today,
        "iv_percentile": vix_percentile_1y,
    }
