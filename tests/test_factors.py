"""Tests for factor calculations."""

from unittest.mock import Mock

import pytest

from engine import factors, thresholds


def _mock_provider_data(payload: dict) -> Mock:
    mock_data = Mock(spec=dict)
    mock_data.get.side_effect = lambda key, default=None: payload.get(key, default)
    return mock_data


@pytest.mark.parametrize(
    ("market_data", "expected"),
    [
        ({"close": 410.0, "moving_average": 400.0}, 1),
        ({"close": 390.0, "moving_average": 400.0}, -1),
        ({"close": None, "moving_average": 400.0}, 0),
    ],
)
def test_trend_factor_from_market_data(market_data: dict, expected: int) -> None:
    assert factors.compute_trend_factor(_mock_provider_data(market_data)) == expected


def test_volatility_factor_flags_spike() -> None:
    vol_data = _mock_provider_data(
        {"vix": thresholds.VIX_EXTREME_LEVEL - 1, "iv_percentile": 0.75, "vix_change_pct": 0.25}
    )
    score = factors.compute_volatility_factor(vol_data)
    assert score == -1


def test_volatility_factor_flags_low_vol() -> None:
    vol_data = _mock_provider_data({"vix": 15.0, "iv_percentile": 0.2})
    score = factors.compute_volatility_factor(vol_data)
    assert score == -1


def test_volatility_factor_positive_when_elevated_and_declining() -> None:
    vol_data = _mock_provider_data({"vix": 22.0, "iv_percentile": 0.7, "vix_change_pct": -0.05})
    score = factors.compute_volatility_factor(vol_data)
    assert score == 1


def test_volatility_factor_neutral_when_missing_change() -> None:
    vol_data = _mock_provider_data({"vix": 22.0, "iv_percentile": 0.7})
    score = factors.compute_volatility_factor(vol_data)
    assert score == 0


def test_skew_factor_disqualify_level() -> None:
    skew_data = _mock_provider_data({"skew": thresholds.SKEW_DISQUALIFY_LEVEL})
    score = factors.compute_skew_factor(skew_data)
    assert score == -1


def test_skew_factor_caution_range() -> None:
    skew_data = _mock_provider_data({"skew": thresholds.SKEW_CAUTION_LEVEL + 1})
    score = factors.compute_skew_factor(skew_data)
    assert score == 0


def test_skew_factor_normal() -> None:
    skew_data = _mock_provider_data({"skew": thresholds.SKEW_CAUTION_LEVEL - 1})
    score = factors.compute_skew_factor(skew_data)
    assert score == 1
