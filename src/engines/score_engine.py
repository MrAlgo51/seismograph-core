import time
from config.weights import weights
from src.utils.zscore import compute_z_score
from src.utils.db import (
    get_latest_spread,
    get_latest_usdt_premium,
    get_latest_mempool,
    insert_signal_data
)

class ScoreEngine:
    def __init__(self):
        self.timestamp = int(time.time())

    def run(self):
        spread = get_latest_spread(self.timestamp)
        usdt_premium = get_latest_usdt_premium(self.timestamp)
        mempool = get_latest_mempool(self.timestamp)

        if not all([spread, usdt_premium, mempool]):
            raise ValueError("Missing one or more data sources")

        # Build feature vector with correct keys
        features = {
            "spread_zscore": spread["spread_zscore"],
            "usdt_premium_zscore": usdt_premium["usdt_premium_zscore"],  # updated
            "median_fee_z": mempool["median_fee_z"],
            "unconfirmed_tx_z": mempool["unconfirmed_tx_z"],
            "mempool_size_z": mempool["mempool_size_z"]
        }

        # Compute weighted score
        score = sum(features[k] * weights.get(k, 0) for k in features)

        row = {
            "timestamp": self.timestamp,
            "btc_price": spread["btc_usd"],
            **features,
            "score": score
        }

        insert_signal_data(row)
        print(f"[+] ScoreEngine logged at {self.timestamp}")
