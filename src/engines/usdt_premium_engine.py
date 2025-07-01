import time
import requests
from src.utils.db import insert_usdt_premium_data, get_latest_usdt_premium
from src.utils.zscore import compute_z_score

class USDTPremiumEngine:
    def __init__(self, zscore_window=48):
        self.zscore_window = zscore_window
        self.api_usdt_url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSDT"
        self.api_usd_url = "https://api.kraken.com/0/public/Ticker?pair=XBTUSD"

    def fetch_price(self, url):
        r = requests.get(url)
        data = r.json()
        result = list(data["result"].values())[0]
        return float(result["c"][0])

    def run(self):
        timestamp = int(time.time())
        btc_usdt = self.fetch_price(self.api_usdt_url)
        btc_usd = self.fetch_price(self.api_usd_url)

        premium_pct = ((btc_usdt - btc_usd) / btc_usd) * 100

        # Fetch recent premiums for z-score calculation
        recent = []
        for i in range(self.zscore_window):
           offset = 3600 * i
           prior = get_latest_usdt_premium(timestamp - offset)
           if prior:
             recent.append(prior["usdt_premium_pct"])


        premium_z = compute_z_score(recent, premium_pct)

        row = {
            "timestamp": timestamp,
            "btc_usdt": btc_usdt,
            "btc_usd": btc_usd,
            "usdt_premium_pct": premium_pct,
            "usdt_premium_zscore": premium_z
        }

        insert_usdt_premium_data(row)
        print(f"[+] USDTPremiumEngine logged at {timestamp}")
