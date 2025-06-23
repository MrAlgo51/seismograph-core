# src/fetchers/fetch_fees.py

import requests

def fetch_fee_data():
    """
    Fetches current Bitcoin network congestion data from mempool.space

    Returns:
        dict: {
            "median_fee": float (sats/vByte),
            "unconfirmed_tx": int,
            "mempool_size": int (bytes)
        }
    """
    try:
        fees_res = requests.get("https://mempool.space/api/v1/fees/recommended", timeout=5)
        stats_res = requests.get("https://mempool.space/api/mempool", timeout=5)

        fees = fees_res.json()
        stats = stats_res.json()

        return {
            "median_fee": fees["halfHourFee"],
            "unconfirmed_tx": stats["count"],
            "mempool_size": stats["vsize"] * 1000  # convert to bytes
        }

    except Exception as e:
        print(f"❌ fetch_fee_data() failed: {e}")
        return {}
