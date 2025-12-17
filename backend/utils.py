from datetime import datetime, timezone
from typing import Optional, Union
from zoneinfo import ZoneInfo


def utcnow() -> datetime:
    """Return timezone-aware UTC now."""
    return datetime.now(timezone.utc)


def ensure_utc(value: Optional[Union[str, datetime]]) -> Optional[datetime]:
    """Ensure the input is a timezone-aware datetime in UTC.

    Accepts datetime objects or ISO datetime strings. If `value` is None,
    returns None so callers can decide to substitute a default.
    """
    if value is None:
        return None
    if isinstance(value, str):
        try:
            s = value.strip()
            # Accept Zulu-style UTC designator by converting it to +00:00
            if s.endswith('Z'):
                s = s[:-1] + '+00:00'
            value = datetime.fromisoformat(s)
        except Exception as e:
            raise ValueError(f"Invalid datetime string: {value}") from e
    if not isinstance(value, datetime):
        raise ValueError("Value is not a datetime or ISO datetime string")
    if value.tzinfo is None:
        # Treat naive datetimes as local wall-clock time, then convert to UTC.
        # Use the process-wide local timezone obtained from an aware datetime.
        local_tz = datetime.now().astimezone().tzinfo or ZoneInfo('UTC')
        value = value.replace(tzinfo=local_tz)
        return value.astimezone(timezone.utc)
    return value.astimezone(timezone.utc)
