import sys
import os

# Add the project root to Python's import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '')))

# Now we can import using src. like a real package
from src.jobs.mempool_logger import fetch_and_log_mempool

if __name__ == "__main__":
    fetch_and_log_mempool()
