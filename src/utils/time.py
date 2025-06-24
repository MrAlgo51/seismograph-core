from datetime import datetime, timezone

def get_current_hour_unix() -> int:
    """Returns current UTC hour as UNIX timestamp (integer)."""
    return int(datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0).timestamp())

def get_current_hour_iso() -> str:
    """Returns current UTC hour as ISO string (e.g. '2025-06-24T18:00:00+00:00')."""
    return datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat()
