# SPX Credit Spread Evaluator

This repository contains the source code for a Streamlit‑based web application that evaluates whether it is a good time to enter a **bullish** put credit spread on the S&P 500 index (SPX) or its liquid ETF proxy SPY.  The tool applies a transparent, rules‑based decision engine to current market data and returns a simple recommendation – `ENTER` or `WAIT` – accompanied by bullet‑point explanations.

The project is intended for educational purposes and to help retail traders and options hobbyists learn how volatility, trend, event risk and option market conditions influence the suitability of a put credit spread.  It **does not** execute trades or provide personalized financial advice.

## Features

- **Rules‑Based Scoring Engine** – Implements the logic described in `docs/Decision_Spec_v0.1.md`, evaluating trend, volatility, macro and earnings calendar risk, and option skew/liquidity to produce a recommendation.
- **Explainable Output** – Returns a binary decision (`ENTER` or `WAIT`) with clear bullet‑point reasons that map to each factor considered by the model.
- **Free‑First Data** – Designed to use freely available data sources for market prices, volatility metrics, skew and event calendars (see `docs/Data_Sources.md`).  Paid services may be added later only if they materially improve reliability.
- **Streamlit Web UI** – A simple user interface built with Streamlit where the user can refresh data and view the recommendation and supporting reasons.
- **Testable Architecture** – Modular engine and factor calculators with accompanying unit tests to facilitate future enhancements and calibrations.

## Getting Started

These instructions assume you have Python 3.9 or higher installed and are working from the repository root.

### Installation

1. Create and activate a virtual environment (recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate   # On Windows use: .venv\Scripts\activate
   ```

2. Install the dependencies:

   ```bash
   pip install -r requirements.txt
   ```

   The main dependencies include [Streamlit](https://streamlit.io) for the UI, `pandas` for data manipulation, and `pytest` for running tests.

### Running the Application

From the repository root, execute the following command to launch the Streamlit app locally:

```bash
streamlit run app/streamlit_app.py
```

The app will open in your default web browser.  Press the **Evaluate Market** button to fetch current data and generate a recommendation.  The output will display a large `ENTER` or `WAIT` followed by explanatory bullet points.  A risk disclaimer and “How it works” section are included in the interface to guide new users.

### Running Tests

To run the unit tests:

```bash
pytest -q
```

Tests reside in the `tests/` directory and cover basic validation of the factor functions and decision logic.  They are intended to ensure the scaffolding behaves as expected and to provide a starting point for further development.

## Project Structure

```
spx-credit-spread-evaluator/
├─ app/                   # Streamlit UI code
│  └─ streamlit_app.py
├─ engine/               # Core decision logic and helper modules
│  ├─ types.py
│  ├─ thresholds.py
│  ├─ factors.py
│  ├─ decision.py
│  └─ explain.py
├─ data/
│  ├─ providers/         # Data provider stubs (market, vol, skew, events, earnings)
│  │  ├─ market_data.py
│  │  ├─ vol_data.py
│  │  ├─ skew_data.py
│  │  ├─ macro_events.py
│  │  └─ earnings_events.py
│  └─ cache.py
├─ docs/
│  ├─ BRD.md
│  ├─ Decision_Spec_v0.1.md
│  ├─ Data_Sources.md
│  ├─ UX_Copy.md
│  └─ Risk_Disclaimer.md
├─ scripts/
│  ├─ run_app.sh
│  └─ run_tests.sh
├─ tests/                # Unit tests and fixtures
│  ├─ test_decision.py
│  └─ test_factors.py
├─ requirements.txt
└─ AGENTS.md
```

For a detailed description of the business requirements, scoring rules and data sources, see the documents in the `docs/` directory.

## License

This project is released under the MIT License.  See the `LICENSE` file for details.