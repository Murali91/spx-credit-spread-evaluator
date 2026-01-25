# Decision/Scoring Specification (v0.1)

This document defines the rule‑based logic used to decide whether to **ENTER** a put credit spread or **WAIT**.  The goal is to provide a transparent, explainable framework that maps directly to the Business Requirements Document.

## Factors and Weights

The decision engine evaluates four primary factors and assigns them approximate weights that reflect their importance in the scoring system:

| Factor | Weight | Description |
|-------|--------|-------------|
| **Market Trend Regime** | 30% | Determines if SPX/SPY is in an uptrend based on moving averages (e.g. above its 200‑day MA).  A bullish or stable trend is required for a positive score. |
| **Volatility Regime** | 25% | Measures the level and direction of implied volatility (VIX or IV Rank).  High and declining volatility yields a positive score; low or spiking vol yields a negative score. |
| **Event Risk** | 25% | Checks for upcoming high‑impact macro events (Fed meetings, CPI, jobs report) and earnings releases of top S&P companies.  An event within the next few trading days disqualifies an entry. |
| **Option Market Conditions** | 20% | Evaluates skew and liquidity via the SKEW index and proxies like put/call ratios or VVIX.  Normal conditions are mildly positive; extreme skew or illiquidity triggers caution or disqualification. |

Weights are approximate and serve as guidance for the initial implementation; they may be adjusted in future versions via backtesting.

## High Conviction Criteria

A recommendation of **ENTER** requires that all of the following are satisfied:

- **Bullish Trend** – The index is in an uptrend (e.g. price above its 200‑day moving average).
- **Elevated, Declining Volatility** – Implied volatility is high relative to recent history but showing signs of reversal (e.g. VIX at a high percentile and turning down).
- **Clear Calendar** – No high‑impact macroeconomic events or major earnings releases in the next few trading days.
- **Normal Skew & Liquidity** – Option skew and liquidity are in a normal range (e.g. SKEW around 115–130).

When these conditions are met, the engine should output `ENTER` and list bullet reasons noting the positive factors.

## Disqualifiers (Automatic WAIT)

Regardless of scores, the engine must recommend **WAIT** if any of the following holds:

- A major macro event (FOMC, CPI, NFP, etc.) is within 2–3 trading days.
- A top S&P 500 company has an earnings release within the next day.
- The index is in a confirmed downtrend (price below its long‑term moving average and momentum negative).
- Volatility is spiking sharply (e.g. VIX ≥ 30 and rising more than 20 % in a day), signalling a crisis.
- The SKEW index exceeds an extreme threshold (e.g. 145), indicating unusually high tail‑risk pricing.
- Option market liquidity appears dislocated (e.g. extremely wide bid–ask spreads or trading halts).

In any of these scenarios the engine must output `WAIT` with a clear reason such as “Upcoming Fed meeting – high event risk” or “Trend breakdown: market in downtrend”.

## Scoring Logic

When no disqualifiers are present, compute an integer score by evaluating each factor:

- **Trend** – +1 if bullish, 0 if neutral, –1 if bearish.
- **Volatility** – +1 if elevated and falling, 0 if unclear, –1 if low or spiking.
- **Event Risk** – +1 if calendar is clear for at least roughly three trading days, 0 for minor events within 4–7 days, –1 for significant events imminently.
- **Skew/Liquidity** – +1 if conditions are normal, 0 if moderately high, –1 if extreme.

Sum the scores.  Output `ENTER` if the sum ≥ 3; otherwise output `WAIT`.  This threshold yields a conservative bias.  In future versions these weights and thresholds may be tuned using historical backtesting.

## Examples

- **High & Falling Volatility, Bullish Trend, Clear Calendar** – A strong uptrend with VIX in the 70th percentile but declining, and no major events in the next two weeks yields a high total score.  The engine should return `ENTER` with reasons noting the elevated vol contraction, bullish trend, clear calendar and normal skew.
- **Low Volatility, Big Event Tomorrow** – A bullish trend but VIX at historic lows and a Fed meeting tomorrow triggers a disqualifier.  The engine outputs `WAIT` and cites the imminent event and unattractive premium as reasons.

These examples illustrate how the logic balances multiple inputs and prioritizes safety by avoiding high‑risk scenarios.