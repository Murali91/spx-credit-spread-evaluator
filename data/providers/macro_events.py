"""Macroeconomic events provider backed by a local JSON calendar."""

from __future__ import annotations

import json
from datetime import date, datetime
from pathlib import Path
from typing import Dict, Optional, Tuple

CALENDAR_PATH = Path(__file__).resolve().parents[1] / "calendar" / "macro_events.json"


def _trading_days_until(start: date, end: date) -> int:
    """Count weekday trading days between ``start`` and ``end`` inclusive of end.

    A same-day event returns 0. Weekends are excluded.
    """
    if end <= start:
        return 0

    days = 0
    current = start
    while current < end:
        current = current.fromordinal(current.toordinal() + 1)
        if current.weekday() < 5:
            days += 1
    return days


def _parse_event(raw_event: Dict[str, str]) -> Optional[Tuple[date, str]]:
    event_date_raw = raw_event.get("date")
    description = raw_event.get("description")
    if not event_date_raw or not description:
        return None
    try:
        event_date = datetime.strptime(event_date_raw, "%Y-%m-%d").date()
    except ValueError:
        return None
    return event_date, description


def get_upcoming_macro_events(today: Optional[date] = None) -> Dict[str, Optional[object]]:
    """Return days until the next high-impact macro event and its description."""
    current_day = today or date.today()

    try:
        with CALENDAR_PATH.open("r", encoding="utf-8") as handle:
            raw_events = json.load(handle)
    except (FileNotFoundError, json.JSONDecodeError):
        return {"days_until_next": None, "description": None}

    if not isinstance(raw_events, list):
        return {"days_until_next": None, "description": None}

    upcoming = []
    for raw_event in raw_events:
        if not isinstance(raw_event, dict):
            continue
        parsed = _parse_event(raw_event)
        if not parsed:
            continue
        event_date, description = parsed
        if event_date < current_day:
            continue
        days_until = _trading_days_until(current_day, event_date)
        upcoming.append((days_until, description))

    if not upcoming:
        return {"days_until_next": None, "description": None}

    days_until_next, description = min(upcoming, key=lambda event: event[0])
    return {"days_until_next": days_until_next, "description": description}
