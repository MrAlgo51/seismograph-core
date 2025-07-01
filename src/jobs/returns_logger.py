import sqlite3

FEATURES = [
    "spread_zscore",
    "usdt_premium_zscore",   # updated here
    "median_fee_z",
    "unconfirmed_tx_z",
    "mempool_size_z",
    "score"
]
LOOKAHEADS = [1, 2, 4]

def get_signal_at(ts):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("SELECT * FROM signals WHERE timestamp = ?", (ts,))
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
        return None

    result = {"timestamp": ts}
    for feat in FEATURES:
        now_val = now.get(feat)
        for h in LOOKAHEADS:
            fut = get_signal_at(ts + h * 3600)
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
            usdt_premium_zscore_return_1h REAL,     -- updated here
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
        if row and all(row[f"score_return_{h}h"] is not None for h in LOOKAHEADS):
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
            print(f"[RETURNS_ENGINE] Skipping t={ts} — forward returns incomplete.")

if __name__ == "__main__":
    main()
