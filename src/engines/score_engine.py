import time
from config.weights import weights
import sqlite3
from src.utils.db import (
    get_latest_spread,
    get_latest_usdt_premium,
    get_latest_mempool,
)
# Remove get_hourly_context! Aggregator handles context features.

DB_PATH = "data/seismograph.db"

def update_signal_score(ts, score, extra_fields=None):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    set_fields = "score = ?"
    params = [score]
    if extra_fields:
        for k in extra_fields:
            set_fields += f", {k} = ?"
            params.append(extra_fields[k])
    params.append(ts)
    c.execute(f"UPDATE signals SET {set_fields} WHERE timestamp = ?", params)
    conn.commit()
    conn.close()

class ScoreEngine:
    def __init__(self, timestamp=None):
        # Align to top of hour unless specified
        now = int(time.time())
        self.timestamp = timestamp or (now - (now % 3600))

    def run(self):
        # 1. Make sure the signals row exists for this hour
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM signals WHERE timestamp = ?", (self.timestamp,))
        signal_row = c.fetchone()
        conn.close()
        if not signal_row:
            raise ValueError(f"No signals row found for hour {self.timestamp}. Run the aggregator first!")

        # 2. Fetch additional features for scoring
        spread = get_latest_spread(self.timestamp)
        usdt_premium = get_latest_usdt_premium(self.timestamp)
        mempool = get_latest_mempool(self.timestamp)
        if not all([spread, usdt_premium, mempool]):
            raise ValueError("Missing one or more data sources for scoring.")

        # 3. Build the features dict for scoring
        features = {
            "spread_zscore": spread["spread_zscore"],
            "usdt_premium_zscore": usdt_premium["usdt_premium_zscore"],
            "median_fee_z": mempool["median_fee_z"],
            "unconfirmed_tx_z": mempool["unconfirmed_tx_z"],
            "mempool_size_z": mempool["mempool_size_z"]
        }
        if any(v is None for v in features.values()):
            raise ValueError(f"Missing feature values at {self.timestamp}: {features}")

        # 4. Compute the score
        score = sum(features[k] * weights.get(k, 0) for k in features)

        # 5. Update score (and any extra fields) in signals table for this hour
        update_signal_score(self.timestamp, score, features)
        print(f"[ScoreEngine] Wrote score={score:.3f} at {self.timestamp}")

if __name__ == "__main__":
    try:
        engine = ScoreEngine()
        engine.run()
    except Exception as e:
        print(f"[SCORE_ENGINE] Error: {e}")
