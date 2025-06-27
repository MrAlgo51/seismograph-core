import sys
import os

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.jobs.usdt_premium_logger import fetch_and_log_usdt_premium

if __name__ == "__main__":
    fetch_and_log_usdt_premium()
