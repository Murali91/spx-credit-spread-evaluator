# Data Sources

This document summarizes the data requirements for the SPX Put Credit Spread Entry Advisor and suggests free and paid sources.  The application is designed to use free data first; paid services should only be adopted if they demonstrably improve reliability or coverage.

## Summary Matrix

| Data Requirement | Free Sources | Paid/Upgraded Sources |
|-----------------|--------------|-----------------------|
| **Index level & trend** | Yahoo Finance API via [`yfinance`], Alpha Vantage (daily quotes), Federal Reserve FRED series for S&P 500 | Polygon.io or Alpha Vantage premium for intraday data, institutional feeds such as Bloomberg or Refinitiv |
| **Volatility metrics (VIX, IV)** | CBOE VIX (ticker `^VIX` on Yahoo), FRED VIX series, local computation of IV Rank using a year of VIX history | OptionMetrics, IVolatility, TradingView, Ivrank.com for exact implied volatilities and percentiles |
| **Volatility skew & sentiment** | CBOE SKEW Index (`^SKEW` on Yahoo), CBOE put/call ratio daily figures | OptionMetrics or other providers of the full option surface |
| **Economic calendar (macro events)** | Government websites (e.g. Federal Reserve, Bureau of Labor Statistics), community calendars like Investing.com or Forex Factory, Financial Modeling Prep’s free calendar | Trading Economics API, Finnhub.io calendar, other commercial economic calendar services |
| **Earnings calendar (top stocks)** | Yahoo Finance `Ticker.nextEarningsDate`, Nasdaq investor relations pages, community‑maintained calendars for S&P constituents | Polygon.io earnings API, IEX Cloud and other commercial earnings feeds |
| **Market data for indicators** | Yahoo Finance or Alpha Vantage for SPY price history, FRED for other series (e.g. SP500 dividend yields) | Real‑time feeds via Quandl, Nasdaq Data Link and other subscription services |
| **Option chain data (if needed)** | *Not used in v0.1*; there is no reliable free real‑time source | Broker APIs (Tradier, TD Ameritrade), OptionMetrics or ORATS for comprehensive chains |

## Notes

- For v0.1 the app uses only free sources to fetch daily data for prices, volatility indices, skew and simple calendars.  See the individual provider stubs under `data/providers/` for how to integrate these sources.
- If an API fails or data is unavailable, the app should handle the failure gracefully and notify the user rather than crashing.
- Before integrating a paid data source, update this document and discuss the trade‑off between cost and benefit.  Free solutions often suffice for end‑of‑day analysis and educational purposes.