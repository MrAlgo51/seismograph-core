import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.engines.spread_engine import SpreadEngine

def main():
    try:
        engine = SpreadEngine()
        engine.run()
    except Exception as e:
        print(f"[SPREAD_LOGGER] Error: {e}")

if __name__ == "__main__":
    main()

