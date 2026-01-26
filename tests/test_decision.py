"""Tests for the decision engine."""

from engine.decision import make_decision


def _base_data() -> dict:
    return {
        "market": {"close": 5100.0, "moving_average": 5000.0},
        "volatility": {"vix": 22.0, "iv_percentile": 0.7, "vix_change_pct": -0.05},
        "skew": {"skew": 120.0},
        "events": {
            "macro": {"days_until_next": 10, "description": "FOMC meeting"},
            "earnings": {"days_until_next": 10, "description": "Apple earnings"},
        },
    }


def test_enter_when_all_factors_positive() -> None:
    data = _base_data()
    result = make_decision(data)
    assert result.decision == "ENTER"
    assert len(result.reasons) == 4
    assert all(isinstance(reason, str) for reason in result.reasons)


def test_wait_when_score_below_threshold() -> None:
    data = _base_data()
    data["volatility"]["iv_percentile"] = 0.2
    data["volatility"]["vix_change_pct"] = 0.03
    data["market"]["close"] = data["market"]["moving_average"]
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("Volatility" in reason for reason in result.reasons)


def test_wait_on_macro_event_disqualifier() -> None:
    data = _base_data()
    data["events"]["macro"]["days_until_next"] = 2
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("Event Risk" in reason for reason in result.reasons)


def test_wait_on_earnings_disqualifier() -> None:
    data = _base_data()
    data["events"]["earnings"]["days_until_next"] = 1
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("earnings" in reason.lower() for reason in result.reasons)


def test_wait_on_downtrend_disqualifier() -> None:
    data = _base_data()
    data["market"]["close"] = 4800.0
    data["market"]["moving_average"] = 5000.0
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("bearish" in reason.lower() for reason in result.reasons)


def test_wait_on_volatility_spike_disqualifier() -> None:
    data = _base_data()
    data["volatility"]["vix"] = 32.0
    data["volatility"]["vix_change_pct"] = 0.25
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("spiking" in reason.lower() for reason in result.reasons)


def test_wait_on_skew_disqualifier() -> None:
    data = _base_data()
    data["skew"]["skew"] = 150.0
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("skew" in reason.lower() for reason in result.reasons)


def test_wait_on_missing_data() -> None:
    data = _base_data()
    data["market"]["moving_average"] = None
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("unavailable" in reason.lower() for reason in result.reasons)


def test_wait_on_partial_event_data_missing() -> None:
    data = _base_data()
    data["events"]["macro"]["days_until_next"] = None
    result = make_decision(data)
    assert result.decision == "WAIT"
    assert any("event calendar data unavailable" in reason.lower() for reason in result.reasons)
