import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.engines.mempool_engine import MempoolEngine

def main():
    try:
        engine = MempoolEngine()
        engine.run()
    except Exception as e:
        print(f"[MEMPOOL_LOGGER] Error: {e}")

if __name__ == "__main__":
    main()

