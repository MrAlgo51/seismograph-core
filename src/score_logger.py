# src/score_logger.py

import sqlite3
from src.utils.time import get_current_hour_iso, get_current_hour_unix
from src.config.weights import weights

def compute_score(spread_z, premium_z):
    return (
        spread_z * weights.get("spread_zscore", 0) +
        premium_z * weights.get("premium_zscore", 0)
    )

def log_score():
    ts = get_current_hour_iso()     # ISO for signals table
    unix_ts = get_current_hour_unix()  # INT for joins

    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    # Pull hourly-matched spread data
    c.execute("SELECT spread_ratio, spread_zscore FROM spread_data WHERE timestamp = ?", (unix_ts,))
    spread = c.fetchone()

    # Pull hourly-matched premium data
    c.execute("SELECT premium_pct, premium_zscore, btc_usd FROM premium_data WHERE timestamp = ?", (unix_ts,))
    premium = c.fetchone()

    if not spread or not premium:
        print("[SCORE_LOGGER] Missing data for current hour.")
        return

    spread_ratio, spread_z = spread
    premium_pct, premium_z, btc_price = premium

    score = compute_score(spread_z, premium_z)

    data = {
        "timestamp": ts,
        "btc_price": btc_price,
        "spread_pct": spread_ratio,
        "spread_z": spread_z,
        "premium_pct": premium_pct,
        "premium_z": premium_z,
        "score": score
    }

    # Create table if needed
    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT PRIMARY KEY,
            btc_price REAL,
            spread_pct REAL,
            spread_z REAL,
            premium_pct REAL,
            premium_z REAL,
            score REAL
        )
    """)

    # Insert or update row
    c.execute("""
        INSERT OR REPLACE INTO signals (
            timestamp, btc_price, spread_pct, spread_z, premium_pct, premium_z, score
        ) VALUES (
            :timestamp, :btc_price, :spread_pct, :spread_z, :premium_pct, :premium_z, :score
        )
    """, data)

    conn.commit()
    conn.close()
    print(f"[SCORE_LOGGER] Score logged: {score:.4f}")

if __name__ == "__main__":
    log_score()
