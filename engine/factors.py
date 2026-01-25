"""Factor calculations for the SPX credit spread decision engine.

This module contains functions that evaluate individual factors used in the
decision model.  Each function accepts a dictionary of data (to be
populated by the data provider modules) and returns an integer score:

    +1 → factor supports entering a credit spread
     0 → neutral or unclear
    -1 → factor suggests waiting

The precise rules for each factor are documented in
``docs/Decision_Spec_v0.1.md``.  These implementations are currently
placeholders; they always return ``0``.  Future versions should replace
these stubs with real calculations based on the thresholds defined in
``engine.thresholds``.
"""

from typing import Dict, Optional

from engine import thresholds


def _as_float(value: object) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def compute_trend_factor(market_data: Dict) -> int:
    """Compute the trend factor.

    Evaluates whether the S&P index (or its SPY proxy) is in an uptrend.
    The implementation should compare current prices to moving averages
    (e.g. 200‑day) and return:

    * +1 if the trend is clearly bullish,
    *  0 if the trend is neutral,
    * -1 if the trend is bearish.

    Args:
        market_data: A dictionary containing at least the keys ``close`` (most
            recent close) and ``moving_average`` (long‑term MA).  Additional
            fields may be added later (e.g. slope of MA).

    Returns:
        int: The trend score (+1, 0 or -1).
    """
    close = _as_float(market_data.get("close"))
    moving_average = _as_float(market_data.get("moving_average"))
    if close is None or moving_average is None:
        return 0
    if thresholds.TREND_REQUIRE_ABOVE_MA:
        if close > moving_average:
            return 1
        if close < moving_average:
            return -1
    return 0


def compute_volatility_factor(vol_data: Dict) -> int:
    """Compute the volatility factor.

    Examines implied volatility levels and recent changes.  The function should
    determine whether volatility is elevated and declining, neutral, or low and
    spiking.

    Args:
        vol_data: A dictionary containing metrics such as ``vix`` (current
            VIX value) and ``iv_percentile`` (IV Rank or percentile).  Additional
            fields may be added in the future (e.g. VIX change or VVIX).

    Returns:
        int: The volatility score (+1, 0 or -1).
    """
    vix = _as_float(vol_data.get("vix"))
    iv_percentile = _as_float(vol_data.get("iv_percentile"))
    vix_change_pct = _as_float(vol_data.get("vix_change_pct"))

    if vix_change_pct is not None and vix_change_pct >= thresholds.VIX_SPIKE_PERCENT_CHANGE:
        return -1
    if vix is not None and vix >= thresholds.VIX_EXTREME_LEVEL:
        return -1

    if iv_percentile is None:
        return 0
    if iv_percentile < thresholds.VIX_ELEVATED_PERCENTILE:
        return -1
    if iv_percentile >= thresholds.VIX_ELEVATED_PERCENTILE:
        if vix_change_pct is not None and vix_change_pct < 0:
            return 1
        return 0
    return 0


def compute_event_factor(events: Dict) -> int:
    """Compute the event risk factor.

    Considers the proximity of high‑impact macro and earnings events.  If an
    event is imminent (within the disqualifier windows defined in
    ``engine.thresholds``), the function should return -1.  If the calendar is
    clear, return +1.  Otherwise return 0 for minor or mid‑range events.

    Args:
        events: A dictionary with entries such as ``macro_days_until_next`` and
            ``earnings_days_until_next``, plus optional descriptions.

    Returns:
        int: The event risk score (+1, 0 or -1).
    """
    # TODO: implement real event risk evaluation using events
    return 0


def compute_skew_factor(skew_data: Dict) -> int:
    """Compute the skew and liquidity factor.

    Looks at measures like the SKEW index and proxies for option market
    liquidity.  A normal range returns +1, moderately high skew or minor
    liquidity concerns return 0, and extreme skew or illiquid conditions
    return -1.

    Args:
        skew_data: A dictionary containing at least ``skew`` and potentially
            other sentiment indicators such as put/call ratios or VVIX.

    Returns:
        int: The skew/liquidity score (+1, 0 or -1).
    """
    skew = _as_float(skew_data.get("skew"))
    if skew is None:
        return 0
    if skew >= thresholds.SKEW_DISQUALIFY_LEVEL:
        return -1
    if skew > thresholds.SKEW_CAUTION_LEVEL:
        return 0
    return 1
