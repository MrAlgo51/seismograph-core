import requests

def fetch_btc_price():
    """
    Fetches the current BTC/USD price using Coingecko API (no auth needed).

    Returns:
        dict: {"btc_price": float} or {} on error
    """
    try:
        url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
        res = requests.get(url, timeout=5)
        data = res.json()
        return {"btc_price": float(data["bitcoin"]["usd"])}
    except Exception as e:
        print(f"❌ fetch_btc_price() failed: {e}")
        return {}
