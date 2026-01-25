"""Threshold and parameter definitions for the decision engine.

This module centralises the numeric values used by the decision logic.
Modifying these values allows tuning the behaviour of the model without
changing the logic in ``engine.decision``.  See ``docs/Decision_Spec_v0.1.md``
for details on how these thresholds correspond to the rules.
"""

# Trend thresholds
TREND_LONG_MA_PERIOD: int = 200  # length of the long‑term moving average in days
TREND_REQUIRE_ABOVE_MA: bool = True  # require price above MA to be considered bullish

# Volatility thresholds
VIX_ELEVATED_PERCENTILE: float = 0.50  # 50% IV Percentile or above counts as elevated
VIX_SPIKE_PERCENT_CHANGE: float = 0.20  # 20% daily increase constitutes a volatility spike
VIX_EXTREME_LEVEL: float = 30.0  # absolute VIX level considered extremely high

# Event risk thresholds
MACRO_EVENT_WINDOW_DAYS: int = 3    # disqualify entry within this many trading days of a macro event
EARNINGS_EVENT_WINDOW_DAYS: int = 1  # disqualify entry within this many days of a top earnings release

# Skew thresholds
SKEW_CAUTION_LEVEL: float = 130.0    # caution if skew exceeds this level
SKEW_DISQUALIFY_LEVEL: float = 145.0  # disqualify entry if skew exceeds this level

# Decision scoring
ENTER_SCORE_THRESHOLD: int = 3  # minimum score required to recommend ENTER when no disqualifiers present