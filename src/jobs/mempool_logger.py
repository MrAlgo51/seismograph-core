from src.fetchers.mempool_api import fetch_mempool_data
from src.utils.db import insert_mempool_data, fetch_recent_mempool_data
from src.utils.time import get_current_hour_unix
import pandas as pd

ROLLING_WINDOW = 48  # number of recent data points (e.g., hours) for z-score calculation

def compute_zscore(series):
    if len(series) < 2 or series.std() == 0:
        return 0.0
    return (series.iloc[-1] - series.mean()) / series.std()

def fetch_and_log_mempool():
    data = fetch_mempool_data()
    if not data:
        print("[MEMPOOL_LOGGER] Mempool fetch failed.")
        return

    timestamp = get_current_hour_unix()

    # Fetch recent mempool data for z-score calculation
    recent_df = fetch_recent_mempool_data(limit=ROLLING_WINDOW)
    
    # Append current values to recent_df to compute z-scores correctly
    # If recent_df is empty, create new DataFrame with current values
    if recent_df is None or recent_df.empty:
        recent_df = pd.DataFrame([{
            "median_fee": data.get("median_fee"),
            "unconfirmed_tx": data.get("unconfirmed_tx"),
            "mempool_size": data.get("mempool_size")
        }])
    else:
        recent_df = pd.concat([
            recent_df,
            pd.DataFrame([{
                "median_fee": data.get("median_fee"),
                "unconfirmed_tx": data.get("unconfirmed_tx"),
                "mempool_size": data.get("mempool_size")
            }])
        ]).tail(ROLLING_WINDOW)

    median_fee_z = compute_zscore(recent_df["median_fee"])
    unconfirmed_tx_z = compute_zscore(recent_df["unconfirmed_tx"])
    mempool_size_z = compute_zscore(recent_df["mempool_size"])

    entry = {
        "timestamp": timestamp,
        "median_fee": data.get("median_fee"),
        "unconfirmed_tx": data.get("unconfirmed_tx"),
        "mempool_size": data.get("mempool_size"),
        "fee_p10": data.get("fee_p10"),
        "fee_p50": data.get("fee_p50"),
        "fee_p90": data.get("fee_p90"),
        "bucket_low": data.get("bucket_low"),
        "bucket_med": data.get("bucket_med"),
        "bucket_high": data.get("bucket_high"),
        "median_fee_z": median_fee_z,
        "unconfirmed_tx_z": unconfirmed_tx_z,
        "mempool_size_z": mempool_size_z
    }

    insert_mempool_data(entry)
    print(f"[MEMPOOL_LOGGER] fee: {entry['median_fee']} sat/vB, txs: {entry['unconfirmed_tx']}")

if __name__ == "__main__":
    fetch_and_log_mempool()
