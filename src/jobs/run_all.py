# src/jobs/run_all.py

import sys
import traceback

def run_step(label, func):
    print(f"\n[RUN_ALL] Starting {label}...")
    try:
        func()
        print(f"[RUN_ALL] {label} completed successfully.")
    except Exception as e:
        print(f"[RUN_ALL] ERROR in {label}: {e}")
        traceback.print_exc()

def main():
    try:
        from src.jobs.spread_logger import main as run_spread
        from src.jobs.usdt_premium_logger import main as run_usdt_premium
        from src.jobs.mempool_logger import main as run_mempool
        from src.jobs.score_logger import main as run_score
        from src.jobs.returns_logger import main as run_returns
    except ImportError as e:
        print(f"[RUN_ALL] ImportError: {e}")
        sys.exit(1)

    print("\n=== Seismograph Full Pipeline Starting ===")

    steps = [
        ("Spread Logger", run_spread),
        ("USDT Premium Logger", run_usdt_premium),
        ("Mempool Logger", run_mempool),
        ("Score Logger", run_score),
        ("Returns Logger", run_returns),
    ]

    for label, func in steps:
        run_step(label, func)

    print("\n=== Pipeline Complete ===")

if __name__ == "__main__":
    main()
