import time
import requests
from src.utils.db import insert_spread_data, get_latest_spread
from src.utils.zscore import compute_z_score

class SpreadEngine:
    def __init__(self, zscore_window=48):
        self.zscore_window = zscore_window
        self.btc_url = "https://api.kraken.com/0/public/Ticker?pair=BTCUSD"
        self.xmr_url = "https://api.kraken.com/0/public/Ticker?pair=XMRUSD"

    def fetch_price(self, url):
        r = requests.get(url)
        data = r.json()
        result = list(data["result"].values())[0]
        return float(result["c"][0])  # last trade close price

    def run(self):
        timestamp = int(time.time())
        btc_usd = self.fetch_price(self.btc_url)
        xmr_usd = self.fetch_price(self.xmr_url)

        spread_ratio = btc_usd / xmr_usd

        # Pull recent ratios
        recent = []
        for i in range(self.zscore_window):
            offset = 60 * i
            prior = get_latest_spread(timestamp - offset)
            if prior:
                recent.append(prior["spread_ratio"])

        spread_z = compute_z_score(recent, spread_ratio)

        row = {
            "timestamp": timestamp,
            "btc_usd": btc_usd,
            "xmr_usd": xmr_usd,
            "spread_ratio": spread_ratio,
            "spread_zscore": spread_z
        }

        insert_spread_data(row)
        print(f"[+] SpreadEngine logged at {timestamp}")
