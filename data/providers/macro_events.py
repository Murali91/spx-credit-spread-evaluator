"""Macroeconomic events provider backed by a local JSON calendar."""

from __future__ import annotations

import json
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, TypedDict, Tuple


class MacroEventResult(TypedDict):
    days_until_next: Optional[int]
    description: Optional[str]
CALENDAR_PATH = Path(__file__).resolve().parents[1] / "calendar" / "macro_events.json"


def _trading_days_until(start: date, end: date) -> int:
    """Count weekday trading days from ``start`` to ``end``.

    A same-day event returns ``0``. Weekend days are excluded.
    """
    if end <= start:
        return 0

    days = 0
    current = start
    while current < end:
        current += timedelta(days=1)
        if current.weekday() < 5:
            days += 1
    return days


def _parse_event(raw_event: Dict[str, object]) -> Optional[Tuple[date, str]]:
    event_date_raw = raw_event.get("date")
    description_raw = raw_event.get("description")
    if not isinstance(event_date_raw, str) or not isinstance(description_raw, str):
        return None

    description = description_raw.strip()
    if not description:
        return None

    try:
        event_date = datetime.strptime(event_date_raw, "%Y-%m-%d").date()
    except ValueError:
        return None

    return event_date, description


def get_upcoming_macro_events(today: Optional[date] = None) -> MacroEventResult:
    """Return the next macro event as ``{days_until_next, description}``."""
    current_day = today or date.today()

    try:
        with CALENDAR_PATH.open("r", encoding="utf-8") as handle:
            raw_events = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return {"days_until_next": None, "description": None}

    if not isinstance(raw_events, list):
        return {"days_until_next": None, "description": None}

    upcoming: list[Tuple[int, str]] = []
    for raw_event in raw_events:
        if not isinstance(raw_event, dict):
            continue
        parsed = _parse_event(raw_event)
        if parsed is None:
            continue

        event_date, description = parsed
        if event_date < current_day:
            continue

        upcoming.append((_trading_days_until(current_day, event_date), description))

    if not upcoming:
        return {"days_until_next": None, "description": None}

    days_until_next, description = min(upcoming, key=lambda event: event[0])
    return {"days_until_next": days_until_next, "description": description}
