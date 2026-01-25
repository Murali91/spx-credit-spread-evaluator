"""Tests for factor calculation stubs.

These tests ensure that the factor functions return integers within the
expected range.  The current implementations are stubs that always return
0, but the tests are written to anticipate real scores once the functions
are implemented.
"""

from engine import factors


def test_trend_factor_returns_valid_score() -> None:
    score = factors.compute_trend_factor({})
    assert isinstance(score, int)
    assert score in (-1, 0, 1)


def test_volatility_factor_returns_valid_score() -> None:
    score = factors.compute_volatility_factor({})
    assert isinstance(score, int)
    assert score in (-1, 0, 1)


def test_event_factor_returns_valid_score() -> None:
    score = factors.compute_event_factor({})
    assert isinstance(score, int)
    assert score in (-1, 0, 1)


def test_skew_factor_returns_valid_score() -> None:
    score = factors.compute_skew_factor({})
    assert isinstance(score, int)
    assert score in (-1, 0, 1)