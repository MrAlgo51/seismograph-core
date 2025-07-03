import sqlite3

FEATURES = [
    "spread_zscore",
    "usdt_premium_zscore",
    "median_fee_z",
    "unconfirmed_tx_z",
    "mempool_size_z",
    "score"
]
LOOKAHEADS = [1, 2, 4]  # hours

def get_signal_at(ts):
    # You don't need this anymore, but keeping it for reference
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT *, ABS(timestamp - ?) AS diff
        FROM signals
        WHERE timestamp BETWEEN ? AND ?
        ORDER BY diff ASC
        LIMIT 1
    """, (ts, ts - 600, ts + 600))
    row = c.fetchone()
    columns = [desc[0] for desc in c.description[:-1]]
    conn.close()
    return dict(zip(columns, row)) if row else None

def get_signal_after(ts, max_window=600):
    # max_window = 600 seconds (10 min) is reasonable for hourly data.
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    min_future = ts
    max_future = ts + max_window
    c.execute("""
        SELECT *
        FROM signals
        WHERE timestamp >= ? AND timestamp <= ?
        ORDER BY timestamp ASC
        LIMIT 1
    """, (min_future, max_future))
    row = c.fetchone()
    columns = [desc[0] for desc in c.description]
    conn.close()
    return dict(zip(columns, row)) if row else None


def get_targets():
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT timestamp FROM signals
        WHERE timestamp NOT IN (SELECT timestamp FROM returns)
    """)
    timestamps = [row[0] for row in c.fetchall()]
    conn.close()
    return timestamps

def calc_return(now, fut):
    if now is None or fut is None or now == 0:
        return None
    return (fut - now) / now

def calculate_returns(ts):
    now = get_signal_at(ts)
    if not now:
        print(f"No 'now' for ts={ts}")
        return None

    result = {"timestamp": ts}
    for feat in FEATURES:
        now_val = now.get(feat)
        for h in LOOKAHEADS:
            future_ts = ts + h * 3600
            # Diagnostic print - window you’re searching
            print(f"For ts={ts}, h={h}, search window: [{future_ts}, {future_ts+600}]")
            fut = get_signal_after(future_ts, max_window=600)
            # Diagnostic print - did you find a future row?
            if fut:
                print(f"  Found future at ts={fut['timestamp']}")
            else:
                print(f"  No future row within window for ts={ts}, h={h}")
            fut_val = fut.get(feat) if fut else None
            result[f"{feat}_return_{h}h"] = calc_return(now_val, fut_val)
    return result


    


def main():
    # Create/upgrade returns table if needed
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            timestamp INTEGER PRIMARY KEY,
            spread_zscore_return_1h REAL,
            spread_zscore_return_2h REAL,
            spread_zscore_return_4h REAL,
            usdt_premium_zscore_return_1h REAL,
            usdt_premium_zscore_return_2h REAL,
            usdt_premium_zscore_return_4h REAL,
            median_fee_z_return_1h REAL,
            median_fee_z_return_2h REAL,
            median_fee_z_return_4h REAL,
            unconfirmed_tx_z_return_1h REAL,
            unconfirmed_tx_z_return_2h REAL,
            unconfirmed_tx_z_return_4h REAL,
            mempool_size_z_return_1h REAL,
            mempool_size_z_return_2h REAL,
            mempool_size_z_return_4h REAL,
            score_return_1h REAL,
            score_return_2h REAL,
            score_return_4h REAL
        )
    """)
    conn.commit()
    conn.close()

    targets = get_targets()
    if not targets:
        print("[RETURNS_ENGINE] No new scored timestamps found.")
        return

    for ts in targets:
        row = calculate_returns(ts)
        # Insert row if at least one return value is not None (besides timestamp)
        if row and any(v is not None for k, v in row.items() if k != "timestamp"):
            conn = sqlite3.connect("data/seismograph.db")
            c = conn.cursor()
            cols = ", ".join(row.keys())
            placeholders = ", ".join([f":{k}" for k in row.keys()])
            c.execute(
                f"INSERT OR REPLACE INTO returns ({cols}) VALUES ({placeholders})",
                row
            )
            conn.commit()
            conn.close()
            print(f"[RETURNS_ENGINE] Logged returns for t={ts}")
        else:
            missing = [k for k, v in row.items() if v is None and k != "timestamp"] if row else []
            print(f"[RETURNS_ENGINE] Skipping t={ts} — all returns missing. Missing: {missing}")

if __name__ == "__main__":
    main()
