"""Helper functions for formatting decision explanations."""

from typing import Dict, List, Optional

from .types import DecisionResult


def _format_days(days: Optional[int]) -> str:
    if days is None:
        return "unknown"
    if days == 0:
        return "today"
    if days == 1:
        return "1 trading day"
    return f"{days} trading days"


def _format_description(description: Optional[str]) -> str:
    if description:
        return f" ({description})"
    return ""


def build_factor_reasons(
    *,
    market_data: Dict,
    vol_data: Dict,
    skew_data: Dict,
    macro_events: Dict,
    earnings_events: Dict,
    factor_scores: Dict[str, int],
    disqualifiers: Dict[str, bool],
    missing_flags: Dict[str, bool],
    decision: str,
) -> List[str]:
    """Build bullet-ready explanations for each factor."""
    reasons: List[str] = []

    if missing_flags.get("trend"):
        trend_reason = "Market trend data unavailable; defaulting to WAIT."
    elif disqualifiers.get("downtrend"):
        trend_reason = "Market trend is bearish (price below long-term average)."
    elif factor_scores.get("trend") == 1:
        trend_reason = "Market trend is bullish (price above long-term average)."
    else:
        trend_reason = "Market trend is mixed; not a strong uptrend."
    reasons.append(f"Market Trend: {trend_reason}")

    if missing_flags.get("volatility"):
        vol_reason = "Volatility data incomplete; cannot confirm a decline."
    elif disqualifiers.get("volatility_spike"):
        vol_reason = (
            "Volatility is spiking (VIX elevated and up sharply), signaling risk."
        )
    elif factor_scores.get("volatility") == 1:
        vol_reason = "Volatility is elevated and falling, supporting premium collection."
    elif factor_scores.get("volatility") == -1:
        vol_reason = "Volatility is low or rising, reducing attractive premium."
    else:
        vol_reason = "Volatility is elevated but not clearly declining."
    reasons.append(f"Volatility: {vol_reason}")

    if missing_flags.get("events"):
        event_reason = "Event calendar data unavailable; defaulting to WAIT."
    else:
        macro_days = macro_events.get("days_until_next")
        earnings_days = earnings_events.get("days_until_next")
        macro_desc = _format_description(macro_events.get("description"))
        earnings_desc = _format_description(earnings_events.get("description"))
        if disqualifiers.get("macro_event_imminent") and disqualifiers.get(
            "earnings_event_imminent"
        ):
            event_reason = (
                "High-impact events imminent: macro event in "
                f"{_format_days(macro_days)}{macro_desc} and earnings in "
                f"{_format_days(earnings_days)}{earnings_desc}."
            )
        elif disqualifiers.get("macro_event_imminent"):
            event_reason = (
                "High-impact macro event in "
                f"{_format_days(macro_days)}{macro_desc}."
            )
        elif disqualifiers.get("earnings_event_imminent"):
            event_reason = (
                "Major earnings in "
                f"{_format_days(earnings_days)}{earnings_desc}."
            )
        elif factor_scores.get("events") == 1:
            event_reason = "Calendar is clear for the next several trading days."
        else:
            event_reason = "Events are on the horizon; staying cautious."
    reasons.append(f"Event Risk: {event_reason}")

    if missing_flags.get("skew"):
        skew_reason = "Skew/liquidity data unavailable; defaulting to WAIT."
    elif disqualifiers.get("liquidity_dislocated"):
        skew_reason = "Option market liquidity appears dislocated."
    elif disqualifiers.get("skew_extreme"):
        skew_reason = "Skew is extreme, indicating elevated tail-risk pricing."
    elif factor_scores.get("skew") == 1:
        skew_reason = "Skew and liquidity are in a normal range."
    else:
        skew_reason = "Skew is elevated; risk pricing is less favorable."
    reasons.append(f"Skew/Liquidity: {skew_reason}")

    if decision == "ENTER" and len(reasons) < 3:
        reasons.append("Conditions align with the high-conviction criteria.")

    return reasons


def build_explanation_text(result: DecisionResult) -> str:
    """Concatenate the reasons in a ``DecisionResult`` into a single string."""
    return "\n".join(f"• {reason}" for reason in result.reasons)
