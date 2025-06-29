import time
import requests
from src.utils.db import insert_mempool_data, fetch_recent_mempool_data
from src.utils.zscore import compute_z_score

class MempoolEngine:
    def __init__(self, zscore_window=48):
        self.zscore_window = zscore_window
        self.api_fee_url = "https://mempool.space/api/v1/fees/mempool-blocks"
        self.api_size_url = "https://mempool.space/api/mempool"

    def fetch_stats(self):
        r = requests.get(self.api_fee_url)
        data = r.json()
        print("[DEBUG] Fetched mempool block data:", data[:1])  # Optional

        if not data or "medianFee" not in data[0]:
            raise ValueError("Unexpected API response: 'medianFee' missing")

        median_fee = data[0]["medianFee"]
        fee_p10 = data[0]["feeRange"][0]
        fee_p90 = data[0]["feeRange"][-1]
        fee_p50 = (fee_p10 + fee_p90) / 2  # fallback estimate

        buckets = {"low": 0, "med": 0, "high": 0}
        for block in data:
            for fee in block.get("feeRange", []):
                if fee < 10:
                    buckets["low"] += 1
                elif fee < 50:
                    buckets["med"] += 1
                else:
                    buckets["high"] += 1

        return {
            "median_fee": median_fee,
            "fee_p10": fee_p10,
            "fee_p50": fee_p50,
            "fee_p90": fee_p90,
            "bucket_low": buckets["low"],
            "bucket_med": buckets["med"],
            "bucket_high": buckets["high"]
        }

    def fetch_size(self):
        r = requests.get(self.api_size_url)
        data = r.json()
        return {
            "unconfirmed_tx": data["count"],
            "mempool_size": data["vsize"]
        }

    def run(self):
        timestamp = int(time.time())
        stats = self.fetch_stats()
        size = self.fetch_size()

        row = {**stats, **size, "timestamp": timestamp}

        df = fetch_recent_mempool_data(limit=self.zscore_window)
        row["median_fee_z"] = compute_z_score(df["median_fee"], row["median_fee"])
        row["unconfirmed_tx_z"] = compute_z_score(df["unconfirmed_tx"], row["unconfirmed_tx"])
        row["mempool_size_z"] = compute_z_score(df["mempool_size"], row["mempool_size"])

        insert_mempool_data(row)
        print(f"[+] MempoolEngine logged at {timestamp}")
