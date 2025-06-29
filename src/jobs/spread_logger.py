import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.engines.spread_engine import SpreadEngine

if __name__ == "__main__":
    engine = SpreadEngine(zscore_window=48)
    engine.run()
