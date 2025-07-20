#!/usr/bin/env python3
import sqlite3

DB_PATH    = "data/seismograph.db"
MAX_DRIFT  = 600          # +/- 10 min wiggle
LOOKAHEADS = [3600,7200,14400]  # 1h, 2h, 4h in seconds
FEATURES   = [
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

def get_signal_at(conn, ts):
    c = conn.cursor()
    c.execute("""
        SELECT *, ABS(timestamp - ?) AS diff
          FROM signals
         WHERE timestamp BETWEEN ? AND ?
      ORDER BY diff
         LIMIT 1
    """, (ts, ts-MAX_DRIFT, ts+MAX_DRIFT))
    row = c.fetchone()
    if not row: return None
    cols = [d[0] for d in c.description[:-1]]
    return dict(zip(cols, row))

def calc_return(now, fut):
    if now is None or fut is None or now == 0:
        return None
    return (fut - now) / now

def calculate_returns(conn, ts):
    now = get_signal_at(conn, ts)
    if not now:
        print(f"[diag] no 'now' row for ts={ts}")
        return None
    if 'total_volume' in now and now['total_volume'] == 0:
        print(f"[diag] skipping dummy/no-volume signal at ts={ts}")
        return None
    result = {"timestamp": ts}
    for feat in FEATURES:
        now_val = now.get(feat)
        for offset in LOOKAHEADS:
            fut = get_signal_at(conn, ts+offset)
            fut_val = fut.get(feat) if fut else None
            result[f"{feat}_return_{offset//3600}h"] = calc_return(now_val, fut_val)
    return result

def get_backfill_targets(conn):
    c = conn.cursor()
    c.execute("""
    SELECT s.timestamp
      FROM signals AS s
 LEFT JOIN returns AS r
        ON s.timestamp = r.timestamp
     WHERE r.score_return_4h IS NULL
    """)
    return [row[0] for row in c.fetchall()]

def main():
    conn = sqlite3.connect(DB_PATH)
    targets = get_backfill_targets(conn)
    if not targets:
        print("✅ backfill: nothing to do, all 4h returns present.")
        return
    print(f"🛠️  backfill: {len(targets)} timestamps to process…")
    for ts in targets:
        row = calculate_returns(conn, ts)
        some_4h = any(row.get(f"{feat}_return_4h") is not None for feat in FEATURES)
        if row and some_4h:
            cols = ", ".join(row.keys())
            placeholders = ", ".join("?" for _ in row)
            conn.execute(
                f"INSERT OR REPLACE INTO returns ({cols}) VALUES ({placeholders})",
                tuple(row.values())
            )
            print(f"  ✓ backfilled {ts}")
        else:
            print(f"  • skipping {ts} (no 4h returns available)")
    conn.commit()
    conn.close()
    print("✅ backfill complete.")

if __name__ == "__main__":
    main()
