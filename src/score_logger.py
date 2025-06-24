# src/score_logger.py

import sqlite3
from src.utils.time import get_current_hour_iso
from src.config.weights import weights

def compute_score(spread_z, premium_z):
    return (
        spread_z * weights.get("spread_zscore", 0) +
        premium_z * weights.get("premium_zscore", 0)
    )

def log_score():
    ts = get_current_hour_iso()
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    # Fetch spread data
    c.execute("SELECT spread_ratio, spread_zscore FROM spread_data WHERE timestamp = (SELECT MAX(timestamp) FROM spread_data)")
    spread = c.fetchone()

    # Fetch premium data
    c.execute("SELECT premium_pct, premium_zscore FROM premium_data WHERE timestamp = (SELECT MAX(timestamp) FROM premium_data)")
    premium = c.fetchone()

    if not spread or not premium:
        print("[SCORE_LOGGER] Missing data.")
        return

    spread_ratio, spread_z = spread
    premium_pct, premium_z = premium

    score = compute_score(spread_z, premium_z)

    # Get current BTC price (can use premium's btc_usd as proxy)
    c.execute("SELECT btc_usd FROM premium_data ORDER BY timestamp DESC LIMIT 1")
    btc_row = c.fetchone()
    btc_price = btc_row[0] if btc_row else None

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

    # Insert or update signal row
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
