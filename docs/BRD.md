# Business Requirements Document (BRD)

## Objective

Develop a Streamlit application that determines whether current market conditions favor entering a **bull put credit spread** on the S&P 500 (SPX), outputting either **ENTER** or **WAIT** along with bullet‑point reasons.  The tool is for educational use and does not execute trades or provide personalized advice.

## Users

- **Retail traders and options hobbyists** seeking a clear, rules‑based market timing signal.
- **Learners** who want to understand how volatility, trend, macro events and options market sentiment affect the suitability of a credit spread.

## Functional Requirements

1. **Binary Recommendation** – The application must return exactly one of two recommendations: `ENTER` or `WAIT`.  There is no third option.
2. **Explanatory Reasons** – Each recommendation must be accompanied by 3–5 bullet points explaining the decision, with one bullet per factor (e.g. volatility regime, trend, event risk, skew/liquidity).
3. **Factor Evaluation**
   - **Trend Regime** – Analyse whether SPX (or SPY) is in an uptrend by comparing the current price to moving averages (e.g. 200‑day).  A bullish trend is a prerequisite for a high‑conviction entry.
   - **Volatility Regime** – Assess implied volatility (VIX or IV Rank).  A high and declining volatility environment is favorable; low or spiking volatility is unfavorable.
   - **Event Risk** – Detect upcoming macroeconomic events (Fed meetings, CPI, NFP) and major earnings announcements (top S&P constituents).  If a high‑impact event is imminent (within a few trading days), the tool should recommend WAIT regardless of other factors.
   - **Option Market Conditions** – Evaluate option skew (e.g. SKEW index) and liquidity proxies.  Extremely high skew or illiquidity is a red flag.
4. **Free Data Usage** – Use free data sources wherever possible (see `docs/Data_Sources.md`).  Paid APIs may be added later only if they materially improve accuracy or reliability.
5. **Explainable Logic** – Implement the decision logic as explicit rules and thresholds (see `docs/Decision_Spec_v0.1.md`), not a black‑box model.
6. **No Trade Execution** – The app must not connect to brokerage APIs or perform any transactions.

## Non‑Functional Requirements

- **Usability** – Present the recommendation prominently with a simple UI: a button to evaluate the market and a section for results and explanations.
- **Performance** – Compute the decision within a few seconds using end‑of‑day or near real‑time data; handle API failures gracefully.
- **Transparency** – Provide documentation and an expandable “How it works” section that explains the factors and logic.
- **Maintainability** – Encapsulate factor calculations and thresholds in separate modules for ease of tuning and testing.
- **Educational Focus** – Include clear risk warnings and avoid giving personalized advice.

## Acceptance Criteria

The v0.1 release shall be considered complete when:

- The app displays either `ENTER` or `WAIT` along with bullet explanations reflecting the four factors.
- The logic follows the decision specification and automatically declines entry when any disqualifying event risk or trend breakdown is present.
- The app uses only free data sources and handles missing data gracefully.
- Unit tests for the engine and factor stubs pass.
- The UI contains a visible risk disclaimer and an explanatory “How it works” section.

## Out of Scope

- **Executing or managing trades**, including brokerage integration.
- **Personalized advice** or portfolio management.
- **Advanced machine‑learning models** or optimizations (deferred to future versions).
