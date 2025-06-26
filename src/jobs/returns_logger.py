from src.utils.time import get_current_hour_unix
from src.utils.db import insert_returns_data
import sqlite3

LOOKAHEAD_HOURS = [1, 2, 4]

def get_btc_price_at(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT btc_usd FROM spread_data
        WHERE timestamp = ?
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row[0] if row else None

def get_scored_timestamps_without_returns():
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    # Ensure the returns table exists before we query it
    c.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            timestamp INTEGER PRIMARY KEY,
            return_1h REAL,
            return_2h REAL,
            return_4h REAL
        )
    """)

    # Now run the actual query
    c.execute("""
        SELECT timestamp FROM signals
        WHERE timestamp NOT IN (SELECT timestamp FROM returns)
    """)
    timestamps = [row[0] for row in c.fetchall()]
    conn.close()
    return timestamps


def calculate_returns(timestamp: int):
    price_now = get_btc_price_at(timestamp)
    if not price_now:
        return None

    result = {"timestamp": timestamp}
    for h in LOOKAHEAD_HOURS:
        future_ts = timestamp + h * 3600
        future_price = get_btc_price_at(future_ts)
        if future_price:
            result[f"return_{h}h"] = (future_price - price_now) / price_now
        else:
            result[f"return_{h}h"] = None  # future data not yet available
    return result

def run_returns_logger():
    targets = get_scored_timestamps_without_returns()
    if not targets:
        print("[RETURNS_LOGGER] No new scored timestamps found.")
        return

    for ts in targets:
        row = calculate_returns(ts)
        if row and all(row[f"return_{h}h"] is not None for h in LOOKAHEAD_HOURS):
            insert_returns_data(row)
            print(f"[RETURNS_LOGGER] Logged returns for t={ts}")
        else:
            print(f"[RETURNS_LOGGER] Skipping t={ts} — forward prices incomplete.")

if __name__ == "__main__":
    run_returns_logger()
