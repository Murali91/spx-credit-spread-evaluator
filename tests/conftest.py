"""Pytest configuration to ensure repo root is on sys.path."""

from __future__ import annotations

import importlib.util
import os
import sys
import types


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)


if importlib.util.find_spec("yfinance") is None:
    yfinance_stub = types.ModuleType("yfinance")

    def _missing_download(*_args, **_kwargs) -> None:
        raise RuntimeError("yfinance is not installed; tests should mock download.")

    yfinance_stub.download = _missing_download
    sys.modules["yfinance"] = yfinance_stub
