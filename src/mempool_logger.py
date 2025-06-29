# src/jobs/mempool_logger.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

import time
import requests
import pandas as pd
from src.utils.db import insert_mempool_data, fetch_recent_mempool_data
from src.utils.zscore import compute_z_score

def fetch_mempool_stats():
    response = requests.get("https://mempool.space/api/v1/fees/mempool-blocks")
    data = response.json()

    median_fee = data[0]["feeMedian"]
    fee_p10 = data[0]["feeRange"][0]
    fee_p90 = data[0]["feeRange"][-1]
    fee_p50 = data[0]["fees"][len(data[0]["fees"]) // 2]

    buckets = {"low": 0, "med": 0, "high": 0}
    for block in data:
        for fee in block["fees"]:
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

def fetch_mempool_size():
    response = requests.get("https://mempool.space/api/mempool")
    data = response.json()
    return {
        "unconfirmed_tx": data["count"],
        "mempool_size": data["vsize"]
    }

def log_mempool_data():
    timestamp = int(time.time())

    stats = fetch_mempool_stats()
    size_data = fetch_mempool_size()
    full_data = {**stats, **size_data, "timestamp": timestamp}

    df = fetch_recent_mempool_data(limit=48)

    full_data["median_fee_z"] = compute_z_score(df["median_fee"], full_data["median_fee"])
    full_data["unconfirmed_tx_z"] = compute_z_score(df["unconfirmed_tx"], full_data["unconfirmed_tx"])
    full_data["mempool_size_z"] = compute_z_score(df["mempool_size"], full_data["mempool_size"])

    insert_mempool_data(full_data)
    print(f"[+] Logged mempool data at {timestamp}")

if __name__ == "__main__":
    log_mempool_data()
