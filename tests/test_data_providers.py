"""Tests for market/volatility/skew data providers."""

from __future__ import annotations

from datetime import datetime, timedelta
import json
from typing import Dict

import pandas as pd

from data.providers import macro_events, market_data, skew_data, vol_data


def _build_history(rows: int) -> pd.DataFrame:
    dates = pd.date_range(end=pd.Timestamp.utcnow().normalize(), periods=rows, freq="B")
    values = pd.Series(range(1, rows + 1), index=dates, dtype="float")
    return pd.DataFrame(
        {
            "Open": values + 0.1,
            "High": values + 0.2,
            "Low": values - 0.2,
            "Close": values,
        }
    )


def test_get_market_data_returns_close_and_moving_average(monkeypatch) -> None:
    history = _build_history(260)

    def fake_download(*_args, **_kwargs) -> pd.DataFrame:
        return history

    market_data._fetch_spy_history.cache_clear()
    monkeypatch.setattr(market_data.yf, "download", fake_download)

    result = market_data.get_market_data()

    assert result["close"] == float(history["Close"].iloc[-1])
    assert result["moving_average"] == float(history["Close"].rolling(200).mean().iloc[-1])
    assert set(result.keys()) == {"close", "moving_average"}


def test_fetch_spy_history_cache_varies_by_date(monkeypatch) -> None:
    history = _build_history(10)
    calls: Dict[str, int] = {"count": 0}

    def fake_download(*_args, **_kwargs) -> pd.DataFrame:
        calls["count"] += 1
        return history

    market_data._fetch_spy_history.cache_clear()
    monkeypatch.setattr(market_data.yf, "download", fake_download)

    morning = datetime(2024, 1, 1, 10, 0, 0)
    evening = morning + timedelta(hours=8)

    market_data._fetch_spy_history(morning)
    market_data._fetch_spy_history(morning)
    market_data._fetch_spy_history(evening)

    assert calls["count"] == 2


def test_get_vol_data_computes_metrics_and_caches(monkeypatch) -> None:
    history = _build_history(260)
    calls: Dict[str, int] = {"count": 0}
    fixed_now = pd.Timestamp(2024, 1, 1, 10, 0, 0)

    def fake_download(*_args, **_kwargs) -> pd.DataFrame:
        calls["count"] += 1
        return history

    vol_data._fetch_vix_history.cache_clear()
    monkeypatch.setattr(
        vol_data.pd.Timestamp, "utcnow", lambda *args, **kwargs: fixed_now
    )
    monkeypatch.setattr(vol_data.yf, "download", fake_download)

    result = vol_data.get_vol_data()
    second_result = vol_data.get_vol_data()

    assert calls["count"] == 1
    assert result == second_result
    assert result["vix"] == float(history["Close"].iloc[-1])
    assert result["iv_percentile"] == 1.0


def test_fetch_vix_history_cache_varies_by_date(monkeypatch) -> None:
    history = _build_history(10)
    calls: Dict[str, int] = {"count": 0}

    def fake_download(*_args, **_kwargs) -> pd.DataFrame:
        calls["count"] += 1
        return history

    vol_data._fetch_vix_history.cache_clear()
    monkeypatch.setattr(vol_data.yf, "download", fake_download)

    morning = datetime(2024, 1, 1, 10, 0, 0)
    evening = morning + timedelta(hours=8)

    vol_data._fetch_vix_history(morning)
    vol_data._fetch_vix_history(morning)
    vol_data._fetch_vix_history(evening)

    assert calls["count"] == 2


def test_get_skew_data_computes_percentile(monkeypatch) -> None:
    history = _build_history(260)

    def fake_download(*_args, **_kwargs) -> pd.DataFrame:
        return history

    skew_data._fetch_skew_history.cache_clear()
    monkeypatch.setattr(skew_data.yf, "download", fake_download)

    result = skew_data.get_skew_data()

    assert result["skew"] == float(history["Close"].iloc[-1])
    assert result["skew_percentile_1y"] == 1.0


def test_fetch_skew_history_cache_varies_by_date(monkeypatch) -> None:
    history = _build_history(10)
    calls: Dict[str, int] = {"count": 0}

    def fake_download(*_args, **_kwargs) -> pd.DataFrame:
        calls["count"] += 1
        return history

    skew_data._fetch_skew_history.cache_clear()
    monkeypatch.setattr(skew_data.yf, "download", fake_download)

    morning = datetime(2024, 1, 1, 10, 0, 0)
    evening = morning + timedelta(hours=8)

    skew_data._fetch_skew_history(morning)
    skew_data._fetch_skew_history(morning)
    skew_data._fetch_skew_history(evening)

    assert calls["count"] == 2


def test_get_upcoming_macro_events_returns_nearest_trading_day_event(
    monkeypatch, tmp_path
) -> None:
    calendar = [
        {"date": "2024-01-15", "description": "Macro event"},
        {"date": "2024-01-19", "description": "CPI release"},
    ]
    calendar_path = tmp_path / "macro_events.json"
    calendar_path.write_text(json.dumps(calendar), encoding="utf-8")
    monkeypatch.setattr(macro_events, "CALENDAR_PATH", calendar_path)

    result = macro_events.get_upcoming_macro_events(today=datetime(2024, 1, 12).date())

    assert result == {"days_until_next": 1, "description": "Macro event"}


def test_get_upcoming_macro_events_handles_missing_or_invalid_file(
    monkeypatch, tmp_path
) -> None:
    monkeypatch.setattr(macro_events, "CALENDAR_PATH", tmp_path / "does-not-exist.json")

    result = macro_events.get_upcoming_macro_events(today=datetime(2024, 1, 1).date())

    assert result == {"days_until_next": None, "description": None}
