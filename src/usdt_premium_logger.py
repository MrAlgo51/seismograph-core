import time
from src.fetchers.kraken import get_kraken_price
from src.utils.zscore import ZScoreTracker
from src.utils.db import insert_premium_data
from src.utils.time import get_current_hour_unix

zscore_tracker = ZScoreTracker(window_size=48)

def fetch_and_log_usdt_premium():
    btc_usdt = get_kraken_price("BTC/USDT")
    btc_usd = get_kraken_price("BTC/USD")

    if btc_usdt is None or btc_usd is None:
        print("[USDT_PREMIUM] Price fetch failed.")
        return

    premium_pct = ((btc_usdt - btc_usd) / btc_usd) * 100
    premium_z = zscore_tracker.update(premium_pct)

    data = {
        "timestamp": get_current_hour_unix(),  # <-- FIXED
        "btc_usdt": btc_usdt,
        "btc_usd": btc_usd,
        "premium_pct": premium_pct,
        "premium_zscore": premium_z,
    }

    insert_premium_data(data)
    print(f"[USDT_PREMIUM] pct: {premium_pct:.4f}%, z: {premium_z:.2f}")

if __name__ == "__main__":
    fetch_and_log_usdt_premium()
