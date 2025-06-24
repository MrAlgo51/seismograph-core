import requests

def get_binance_price(symbol: str) -> float | None:
    url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        return float(data["price"])
    except Exception as e:
        print(f"[BINANCE] Failed to fetch {symbol}: {e}")
        return None
