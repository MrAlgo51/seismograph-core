from datetime import datetime, timezone

def get_current_hour_iso() -> str:
    """
    Returns an ISO8601 UTC timestamp snapped to the top of the current hour.
    Example: '2025-06-24T18:00:00+00:00'
    """
    return datetime.now(timezone.utc).replace(minute=0, second=0, microsecond=0).isoformat()
