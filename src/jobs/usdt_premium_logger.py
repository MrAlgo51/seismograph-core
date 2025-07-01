from src.engines.usdt_premium_engine import USDTPremiumEngine

def main():
    try:
        engine = USDTPremiumEngine()
        engine.run()
    except Exception as e:
        print(f"[USDT_PREMIUM_LOGGER] Error: {e}")

if __name__ == "__main__":
    main()
