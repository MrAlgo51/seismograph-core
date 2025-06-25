# src/score_logger.py

import sqlite3
from src.utils.time import get_current_hour_iso, get_current_hour_unix
from src.config.score_variants import score_configs
from src.utils.scoring import compute_scores

def log_score():
    ts = get_current_hour_iso()
    unix_ts = get_current_hour_unix()

    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    # Fetch spread data
    c.execute("SELECT spread_ratio, spread_z FROM spread_data WHERE timestamp = ?", (unix_ts,))
    spread = c.fetchone()

    # Fetch premium data
    c.execute("SELECT premium_pct, premium_z, btc_usd FROM premium_data WHERE timestamp = ?", (unix_ts,))
    premium = c.fetchone()

    # Fetch mempool data
    c.execute("SELECT median_fee, unconfirmed_tx FROM mempool WHERE timestamp = ?", (unix_ts,))
    mempool = c.fetchone()

    if not (spread and premium and mempool):
        print("[SCORE_LOGGER] Missing data for current hour.")
        return

    # Extract values
    spread_ratio, spread_z = spread
    premium_pct, premium_z, btc_price = premium
    median_fee, unconfirmed_tx = mempool

    # Build input row for scoring
    input_row = {
        "spread_z": spread_z,
        "premium_z": premium_z,
        "median_fee": median_fee,
        "unconfirmed_tx": unconfirmed_tx
    }

    # Compute all score variants
    score_dict = compute_scores(input_row)

    # Base columns
    data = {
        "timestamp": ts,
        "btc_price": btc_price,
        "spread_pct": spread_ratio,
        "spread_z": spread_z,
        "premium_pct": premium_pct,
        "premium_z": premium_z,
    }

    # Add each score to the data dict
    data.update(score_dict)

    # Build CREATE TABLE with dynamic score columns
    score_columns = ",\n".join([f"{name} REAL" for name in score_dict.keys()])
    c.execute(f"""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT PRIMARY KEY,
            btc_price REAL,
            spread_pct REAL,
            spread_z REAL,
            premium_pct REAL,
            premium_z REAL,
            {score_columns}
        )
    """)

    # Build dynamic insert query
    all_columns = ", ".join(data.keys())
    placeholders = ", ".join([f":{k}" for k in data.keys()])
    c.execute(f"""
        INSERT OR REPLACE INTO signals (
            {all_columns}
        ) VALUES (
            {placeholders}
        )
    """, data)

    conn.commit()
    conn.close()
    print(f"[SCORE_LOGGER] Scores logged: {', '.join(score_dict.keys())}")

if __name__ == "__main__":
    log_score()
