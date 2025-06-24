# src/fetchers/kraken.py

import requests

def get_kraken_price(pair: str) -> float | None:
    pair_map = {
        "BTC/USD": "XXBTZUSD",
        "BTC/USDT": "XBTUSDT",
        "XMR/USD": "XXMRZUSD",
    }

    kraken_pair = pair_map.get(pair)
    if not kraken_pair:
        print(f"[KRAKEN] Unsupported pair: {pair}")
        return None

    url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_pair}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        result = data["result"][kraken_pair]
        price = float(result["c"][0])
        return price
    except Exception as e:
        print(f"[KRAKEN] Failed to fetch {pair}: {e}")
        return None
