"""Streamlit application for the SPX Credit Spread Evaluator.

This script defines the user interface and coordinates data retrieval and
decision making.  It relies on the engine modules for business logic and
the data provider stubs for fetching market information.  The UI is kept
minimal to emphasise the recommendation and the explanatory bullets.
"""

import streamlit as st
import os
import sys

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)
from engine.decision import make_decision
from engine.explain import build_explanation_text
from data.providers import (
    market_data,
    vol_data,
    skew_data,
    macro_events,
    earnings_events,
)


def _safe_provider_call(label: str, fetcher, fallback):
    try:
        return fetcher()
    except Exception:
        st.warning(f"{label} data unavailable; using placeholders for now.")
        return fallback


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(page_title="SPX Put Credit Spread Entry Advisor", page_icon="📈")

    # Title and introduction
    st.title("SPX Put Credit Spread Entry Advisor")
    st.write(
        "This tool evaluates current market conditions to determine whether "
        "selling a bull put credit spread on the S&P 500 (or SPY) is favoured. "
        "It returns either **ENTER** or **WAIT** along with the reasons behind "
        "the recommendation."
    )

    # Evaluate button
    evaluate = st.button("Evaluate Market")

    if evaluate:
        # Gather data from providers.  In v0.1 these return None placeholders.
        data = {
            "market": _safe_provider_call(
                "Market",
                market_data.get_market_data,
                {"close": None, "moving_average": None},
            ),
            "volatility": _safe_provider_call(
                "Volatility",
                vol_data.get_vol_data,
                {"vix": None, "iv_percentile": None},
            ),
            "skew": _safe_provider_call(
                "Skew",
                skew_data.get_skew_data,
                {"skew": None, "skew_percentile_1y": None},
            ),
            "events": {
                "macro": macro_events.get_upcoming_macro_events(),
                "earnings": earnings_events.get_upcoming_earnings_events(),
            },
        }
        result = make_decision(data)

        # Display the recommendation prominently
        if result.decision == "ENTER":
            st.success(result.decision)
        else:
            st.warning(result.decision)

        # Show the explanatory bullets
        st.markdown(build_explanation_text(result))
    else:
        st.info("Click **Evaluate Market** to fetch data and generate a recommendation.")

    # Optional expanded sections for more information
    with st.expander("How it works"):
        st.markdown(
            """
            The decision engine analyses four factors:

            - **Market Trend** – is the index in an uptrend or downtrend?
            - **Volatility Regime** – are implied volatilities high and falling, or low and rising?
            - **Event Risk** – are there significant macro events (e.g. Fed meetings, CPI reports) or major earnings announcements imminent?
            - **Option Market Conditions** – are option skew and liquidity within normal ranges?

            Each factor contributes to a score that determines whether a bullish put credit spread is favourable now.  See `docs/Decision_Spec_v0.1.md` for the full specification.
            """
        )

    with st.expander("Risk Disclaimer"):
        try:
            with open("docs/Risk_Disclaimer.md", "r", encoding="utf-8") as f:
                disclaimer = f.read()
        except FileNotFoundError:
            disclaimer = (
                "Risk disclaimer file not found.  Please ensure `docs/Risk_Disclaimer.md` "
                "exists in the repository."
            )
        st.markdown(disclaimer)


if __name__ == "__main__":
    main()
