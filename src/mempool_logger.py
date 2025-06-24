from src.utils.mempool import fetch_mempool_data
from src.utils.db import insert_mempool_data
from src.utils.time import get_current_hour_unix

def fetch_and_log_mempool():
    data = fetch_mempool_data()
    if not data:
        print("[MEMPOOL_LOGGER] Mempool fetch failed.")
        return

    entry = {
        "timestamp": get_current_hour_unix(),
        "median_fee": data.get("median_fee"),
        "unconfirmed_tx": data.get("unconfirmed_tx"),
        "mempool_size": data.get("mempool_size"),
        "fee_p10": data.get("fee_p10"),
        "fee_p50": data.get("fee_p50"),
        "fee_p90": data.get("fee_p90"),
        "bucket_low": data.get("bucket_low"),
        "bucket_med": data.get("bucket_med"),
        "bucket_high": data.get("bucket_high")
    }

    insert_mempool_data(entry)
    print(f"[MEMPOOL_LOGGER] fee: {entry['median_fee']} sat/vB, txs: {entry['unconfirmed_tx']}")

if __name__ == "__main__":
    fetch_and_log_mempool()
