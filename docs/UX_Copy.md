# UX Copy and Interface Guidelines

This document describes the user‑facing language and layout for the Streamlit application.  The goal is to present the recommendation clearly and concisely, with minimal jargon, and to educate the user about the factors considered.

## App Layout

1. **Title and Introduction**

   - **Title** – “SPX Put Credit Spread Entry Advisor”
   - **Subtitle** – “Rules‑based analysis for bullish put credit spreads”

   Briefly explain what the app does, for example:

   > *This tool evaluates current market conditions to determine whether selling a bull put credit spread on the S&P 500 (or SPY) is favored.  It returns either `ENTER` or `WAIT` along with the reasons behind the recommendation.*

2. **Evaluate Button**

   - Label the button **Evaluate Market**.
   - Description: “Click to refresh data and generate a recommendation.”

3. **Recommendation Display**

   - Display a large, colored word: either `ENTER` (green) or `WAIT` (red).  Use semantic color names for accessibility (e.g. Streamlit’s `st.success` or `st.error`).
   - Below the word, present a bulleted list of three to five points explaining the rationale.  Each bullet corresponds to a factor such as *Market Trend*, *Volatility*, *Event Risk*, or *Skew/Liquidity*.  Keep each explanation to one or two sentences.

   Example bullet:

   ``
   • Volatility is elevated but falling, suggesting rich premium that may decline.
   ``

4. **How It Works / More Info**

   - Provide an expandable section summarizing the four factors evaluated.  Include links or references to `docs/Decision_Spec_v0.1.md` for more details.
   - Clarify that the tool uses free data sources and simple rules, and that future versions will incorporate backtesting and calibration.

5. **Risk Disclaimer**

   - Present a clearly visible disclaimer: *“For educational purposes only.  This tool does not execute trades or provide personalized investment advice.  Options trading involves risk.”*
   - Link to or display the full text from `docs/Risk_Disclaimer.md`.

## Tone and Style

- Use plain language appropriate for retail traders and hobbyists.  Explain jargon where necessary (e.g. define “IV Rank” if referenced).
- Avoid giving investment advice or instructions to trade.  Emphasize that the tool is for learning and timing analysis only.
- Be transparent about limitations and encourage users to do additional research.  If data is unavailable or stale, note this in the output rather than guessing.