# src/score_logger.py
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))


import sqlite3
from datetime import datetime, timezone
from scoring import calculate_score

from fetchers.fetch_btc_price import fetch_btc_price
from fetchers.fetch_fees import fetch_fee_data
from scoring import calculate_score


# Initialize clean data dict
data = {
    "timestamp": datetime.now(timezone.utc).isoformat()
}

# Merge in live data from each fetcher
data.update(fetch_btc_price())
data.update(fetch_fee_data())

# Calculate score
data["score"] = calculate_score(data)


# Connect to the SQLite DB
conn = sqlite3.connect("data/seismograph.db")
cursor = conn.cursor()

# Insert into signals table
cursor.execute("""
INSERT OR REPLACE INTO signals (
    timestamp, btc_price, spread_pct, spread_z,
    premium_pct, premium_z, median_fee, unconfirmed_tx,
    mempool_size, funding_rate, funding_z, score
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    data["timestamp"],
    data.get("btc_price"),
    data.get("spread_pct"),
    data.get("spread_z"),
    data.get("premium_pct"),
    data.get("premium_z"),
    data.get("median_fee"),
    data.get("unconfirmed_tx"),
    data.get("mempool_size"),
    data.get("funding_rate"),
    data.get("funding_z"),
    data.get("score")
))


conn.commit()
conn.close()

print(f"✅ Signal logged at {data['timestamp']} with score {data['score']}")
