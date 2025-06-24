# src/xmr_spread_logger.py

import time
from src.fetchers.kraken import get_kraken_price
from src.utils.zscore import ZScoreTracker
from src.utils.db import insert_spread_data
from src.utils.time import get_current_hour_timestamp

zscore_tracker = ZScoreTracker(window_size=48)

def fetch_and_log_xmr_spread():
    btc_usd = get_kraken_price("BTC/USD")
    xmr_usd = get_kraken_price("XMR/USD")

    if btc_usd is None or xmr_usd is None:
        print("[XMR_SPREAD] Price fetch failed.")
        return

    spread_ratio = btc_usd / xmr_usd
    spread_z = zscore_tracker.update(spread_ratio)

    data = {
        "timestamp": get_current_hour_timestamp(),
        "btc_usd": btc_usd,
        "xmr_usd": xmr_usd,
        "spread_ratio": spread_ratio,
        "spread_zscore": spread_z,
    }

    insert_spread_data(data)
    print(f"[XMR_SPREAD] ratio: {spread_ratio:.4f}, z: {spread_z:.2f}")

if __name__ == "__main__":
    fetch_and_log_xmr_spread()
