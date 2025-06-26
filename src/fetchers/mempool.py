# src/fetchers/mempool_api.py

import requests

def fetch_mempool_data():
    try:
        mempool_url = "https://mempool.space/api/v1/fees/recommended"
        stats_url = "https://mempool.space/api/mempool"

        fees = requests.get(mempool_url).json()
        stats = requests.get(stats_url).json()

        return {
            "median_fee": fees.get("halfHourFee"),
            "unconfirmed_tx": stats.get("count"),
            "mempool_size": stats.get("vsize"),
            "fee_p10": fees.get("minimumFee"),      # approx low
            "fee_p50": fees.get("hourFee"),         # middle range
            "fee_p90": fees.get("fastestFee"),      # upper range
            "bucket_low": int(stats.get("count", 0) * 0.5),
            "bucket_med": int(stats.get("count", 0) * 0.33),
            "bucket_high": int(stats.get("count", 0) * 0.17)
        }

    except Exception as e:
        print(f"[FETCH_ERROR] {e}")
        return None
