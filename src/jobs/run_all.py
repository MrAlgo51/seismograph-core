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

def backfill_all_scores():
    import sqlite3
    from src.jobs.score_logger import ScoreEngine

    DB_PATH = "data/seismograph.db"
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp FROM signals WHERE score IS NULL OR score = ''")
    hours = [row[0] for row in c.fetchall()]
    conn.close()

    if hours:
        print(f"[RUN_ALL] Backfilling scores for {len(hours)} signals...")
        for ts in hours:
            try:
                ScoreEngine(ts).run()
            except Exception as e:
                print(f"[RUN_ALL] Failed to score {ts}: {e}")
    else:
        print("[RUN_ALL] No missing scores to backfill.")

def main():
    try:
        from src.jobs.aggregate_signals import aggregate_signals
        from src.jobs.spread_logger import main as run_spread
        from src.jobs.usdt_premium_logger import main as run_usdt_premium
        from src.jobs.mempool_logger import main as run_mempool
        from src.jobs.score_logger import main as run_score
        from src.jobs.returns_logger import main as run_returns
        from src.jobs.backfill_returns import main as run_backfill_returns   # <--- THE MISSING IMPORT!
    except ImportError as e:
        print(f"[RUN_ALL] ImportError: {e}")
        sys.exit(1)

    print("\n=== Seismograph Full Pipeline Starting ===")

    steps = [
        ("Aggregate Signals", aggregate_signals),
        ("Spread Logger", run_spread),
        ("USDT Premium Logger", run_usdt_premium),
        ("Mempool Logger", run_mempool),
        ("Backfill All Scores", backfill_all_scores),   # Make sure all scores filled
        ("Score Logger", run_score),                    # Fill new scores (if missed)
        ("Backfill Returns", run_backfill_returns),     # Make sure all returns filled
        ("Returns Logger", run_returns),                # Fill new returns (if missed)
    ]

    for label, func in steps:
        run_step(label, func)

    print("\n=== Pipeline Complete ===")

if __name__ == "__main__":
    main()
