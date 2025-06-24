import time

def get_current_hour_timestamp() -> int:
    """
    Returns the current timestamp rounded down to the top of the hour.
    Example: 14:38 → returns timestamp for 14:00:00
    """
    now = int(time.time())
    return now - (now % 3600)
