# src/score_logger.py

import sqlite3
from src.utils.time import get_current_hour_iso, get_current_hour_unix
from src.config.score_variants import score_configs
from src.utils.scoring import compute_all_scores
from src.utils.db import (
    get_latest_spread,
    get_latest_premium,
    get_latest_mempool,
    get_latest_funding,
    insert_signal_data,
)

def log_score():
    ts_iso = get_current_hour_iso()
    ts_unix = get_current_hour_unix()

    spread = get_latest_spread(ts_unix)
    premium = get_latest_premium(ts_unix)
    mempool = get_latest_mempool(ts_unix)
    funding = get_latest_funding(ts_unix)

    if not spread or not premium or not mempool:
        print("[SCORE_LOGGER] Missing data for current hour.")
        return

    if not funding:
        print("[SCORE_LOGGER] Warning: funding data missing — using 0.0 defaults")

    row = {
        **spread,
        **premium,
        **mempool,
        **(funding or {}),  # safely merge if funding is None
    }

    scores = compute_all_scores(row)

    data = {
        "timestamp": ts_iso,
        "btc_price": premium["btc_usd"],
        "spread_pct": spread["spread_ratio"],
        "spread_z": spread["spread_zscore"],
        "premium_pct": premium["premium_pct"],
        "premium_z": premium["premium_zscore"],
        "median_fee": mempool["median_fee"],
        "unconfirmed_tx": mempool["unconfirmed_tx"],
        "mempool_size": mempool["mempool_size"],
        "funding_rate": funding["funding_rate"] if funding else 0.0,
        "funding_z": funding["funding_z"] if funding else 0.0,
        **scores,
    }

    insert_signal_data(data)
    print(f"[SCORE_LOGGER] Scores logged: {', '.join(scores.keys())}")

if __name__ == "__main__":
    log_score()
