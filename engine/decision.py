"""High‑level decision logic for the SPX put credit spread advisor.

This module combines the individual factor scores to arrive at a final
recommendation.  In v0.1 the logic is intentionally simple and returns
a placeholder result.  When the factor functions are fully implemented,
this module should use the thresholds from ``engine.thresholds`` and the
rules defined in ``docs/Decision_Spec_v0.1.md`` to compute a score and
return a ``DecisionResult`` instance.
"""

from typing import Dict, Optional

from .types import DecisionResult
from . import factors, thresholds
from .explain import build_factor_reasons


def _as_float(value: object) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    return None


def _as_int(value: object) -> Optional[int]:
    if value is None:
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        return int(value)
    return None


def make_decision(data: Dict) -> DecisionResult:
    """Return a ``DecisionResult`` with a recommendation and explanations.

    Args:
        data: A dictionary containing all inputs required by the factor
            functions.  Expected keys include ``market``, ``volatility``,
            ``events`` and ``skew``.  Each value should itself be a
            dictionary matching the expected structure of the corresponding
            factor function.  In the current stub implementation this
            parameter is unused.

    Returns:
        DecisionResult: An object with ``decision`` set to ``"ENTER"`` or
        ``"WAIT"`` and a list of reasons explaining the rationale.
    """
    market_data = data.get("market") or {}
    vol_data = data.get("volatility") or {}
    skew_data = data.get("skew") or {}
    events = data.get("events") or {}
    macro_events = events.get("macro") or {}
    earnings_events = events.get("earnings") or {}

    trend_score = factors.compute_trend_factor(market_data)
    volatility_score = factors.compute_volatility_factor(vol_data)
    event_score = factors.compute_event_factor(
        {
            "macro_days_until_next": macro_events.get("days_until_next"),
            "earnings_days_until_next": earnings_events.get("days_until_next"),
        }
    )
    skew_score = factors.compute_skew_factor(skew_data)

    close = _as_float(market_data.get("close"))
    moving_average = _as_float(market_data.get("moving_average"))
    vix = _as_float(vol_data.get("vix"))
    vix_change_pct = _as_float(vol_data.get("vix_change_pct"))
    macro_days = _as_int(macro_events.get("days_until_next"))
    earnings_days = _as_int(earnings_events.get("days_until_next"))
    skew = _as_float(skew_data.get("skew"))

    missing_flags = {
        "trend": close is None or moving_average is None,
        "volatility": vol_data.get("iv_percentile") is None and vix is None,
        "events": macro_days is None or earnings_days is None,
        "skew": skew is None,
    }
    missing_any = any(missing_flags.values())

    disqualifiers = {
        "macro_event_imminent": (
            macro_days is not None
            and macro_days <= thresholds.MACRO_EVENT_WINDOW_DAYS
        ),
        "earnings_event_imminent": (
            earnings_days is not None
            and earnings_days <= thresholds.EARNINGS_EVENT_WINDOW_DAYS
        ),
        "downtrend": close is not None
        and moving_average is not None
        and close < moving_average,
        "volatility_spike": vix is not None
        and vix_change_pct is not None
        and vix >= thresholds.VIX_EXTREME_LEVEL
        and vix_change_pct >= thresholds.VIX_SPIKE_PERCENT_CHANGE,
        "skew_extreme": skew is not None and skew >= thresholds.SKEW_DISQUALIFY_LEVEL,
        "liquidity_dislocated": bool(
            skew_data.get("liquidity_dislocated")
            or skew_data.get("bid_ask_spread_wide")
            or skew_data.get("trading_halt")
        ),
    }

    score = trend_score + volatility_score + event_score + skew_score
    if missing_any or any(disqualifiers.values()):
        decision = "WAIT"
    else:
        decision = (
            "ENTER" if score >= thresholds.ENTER_SCORE_THRESHOLD else "WAIT"
        )

    reasons = build_factor_reasons(
        market_data=market_data,
        vol_data=vol_data,
        skew_data=skew_data,
        macro_events=macro_events,
        earnings_events=earnings_events,
        factor_scores={
            "trend": trend_score,
            "volatility": volatility_score,
            "events": event_score,
            "skew": skew_score,
        },
        disqualifiers=disqualifiers,
        missing_flags=missing_flags,
        decision=decision,
    )
    return DecisionResult(decision=decision, reasons=reasons)
