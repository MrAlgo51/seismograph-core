import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from src.engines.mempool_engine import MempoolEngine

if __name__ == "__main__":
    engine = MempoolEngine(zscore_window=48)
    engine.run()
