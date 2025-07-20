# src/jobs/returns_logger.py

import sqlite3
import logging

DB_PATH = "data/seismograph.db"

logging.basicConfig(
    filename='returns_logger.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

FEATURES = [
    "score",
    "vwap_percent_away",
    "volume_zscore",
    "spread_zscore",
    "usdt_premium_zscore",
    "median_fee_z",
    "unconfirmed_tx_z",
    "mempool_size_z",
    "btc_price"
]

LOOKAHEADS = [1, 2, 4]  # 1h, 2h, 4h returns

def get_signal(ts):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM signals WHERE timestamp = ?", (ts,))
    row = c.fetchone()
    columns = [desc[0] for desc in c.description] if row else []
    conn.close()
    return dict(zip(columns, row)) if row else None

def get_future_signal(ts, lookahead):
    """Finds the first signal >= target_ts (within a window of +10 minutes)."""
    target_ts = ts + lookahead * 3600
    window = 600  # 10 minutes
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(
        "SELECT * FROM signals WHERE timestamp >= ? AND timestamp <= ? ORDER BY timestamp ASC LIMIT 1",
        (target_ts, target_ts + window)
    )
    row = c.fetchone()
    columns = [desc[0] for desc in c.description] if row else []
    conn.close()
    return dict(zip(columns, row)) if row else None

def get_targets():
    """Returns timestamps from signals table that are missing from returns table."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT timestamp FROM signals
        WHERE timestamp NOT IN (SELECT timestamp FROM returns)
    """)
    targets = [row[0] for row in c.fetchall()]
    conn.close()
    return targets

def calc_return(now_val, fut_val):
    if now_val is None or fut_val is None or now_val == 0:
        return None
    return (fut_val - now_val) / now_val

def get_all_signal_timestamps():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp FROM signals ORDER BY timestamp")
    all_ts = [row[0] for row in c.fetchall()]
    conn.close()
    return all_ts

def main():
    # ... create table logic as before ...
    all_timestamps = get_all_signal_timestamps()
    for ts in all_timestamps:
        now = get_signal(ts)
        if not now:
            print(f"[RETURNS_LOGGER] No 'now' row for {ts}, skipping.")
            continue

        result = {"timestamp": ts}
        for feat in FEATURES:
            now_val = now.get(feat)
            for h in LOOKAHEADS:
                future = get_future_signal(ts, h)
                fut_val = future.get(feat) if future else None
                result[f"{feat}_return_{h}h"] = calc_return(now_val, fut_val)

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        cols = ", ".join(result.keys())
        placeholders = ", ".join([f":{k}" for k in result.keys()])
        c.execute(
            f"INSERT OR REPLACE INTO returns ({cols}) VALUES ({placeholders})",
            result
        )
        conn.commit()
        conn.close()
        print(f"[RETURNS_LOGGER] Wrote/updated returns for {ts}")

if __name__ == "__main__":
    main()
