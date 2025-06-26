import sqlite3
import pandas as pd
from src.fetchers.kraken import get_kraken_price
from src.utils.db import insert_premium_data
from src.utils.time import get_current_hour_unix

DB_PATH = "data/seismograph.db"
ROLLING_WINDOW = 48  # hours

def compute_zscore(series):
    if len(series) < 2:
        return 0.0
    return (series.iloc[-1] - series.mean()) / series.std()

def fetch_premium_history():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        f"SELECT timestamp, premium_pct FROM premium_data ORDER BY timestamp DESC LIMIT {ROLLING_WINDOW - 1}",
        conn
    )
    conn.close()
    return df.sort_values("timestamp")

def fetch_and_log_usdt_premium():
    btc_usdt = get_kraken_price("BTC/USDT")
    btc_usd = get_kraken_price("BTC/USD")

    if btc_usdt is None or btc_usd is None:
        print("[USDT_PREMIUM] Price fetch failed.")
        return

    premium_pct = ((btc_usdt - btc_usd) / btc_usd) * 100
    df = fetch_premium_history()
    df = df.append({"timestamp": get_current_hour_unix(), "premium_pct": premium_pct}, ignore_index=True)

    premium_z = compute_zscore(df["premium_pct"])

    data = {
        "timestamp": get_current_hour_unix(),
        "btc_usdt": btc_usdt,
        "btc_usd": btc_usd,
        "premium_pct": premium_pct,
        "premium_zscore": premium_z
    }

    insert_premium_data(data)
    print(f"[USDT_PREMIUM] pct: {premium_pct:.4f}%, z: {premium_z:.2f}")

if __name__ == "__main__":
    fetch_and_log_usdt_premium()
