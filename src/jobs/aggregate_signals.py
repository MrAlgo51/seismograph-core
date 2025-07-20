# src/jobs/aggregate_signals.py

import sqlite3
import numpy as np
import time
import logging

DB_PATH = "data/seismograph.db"

logging.basicConfig(
    filename='aggregate_signals.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def get_last_hour_top():
    now = int(time.time())
    return now - (now % 3600)

def fetch_ohlcv_for_hour(ts):
    """Fetch all 5-min bars for the hour ending at ts."""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    start = ts - 3600 + 300
    end = ts
    c.execute(
        "SELECT timestamp, close, volume, vwap FROM ohlcv WHERE timestamp BETWEEN ? AND ? ORDER BY timestamp ASC",
        (start, end)
    )
    rows = c.fetchall()
    conn.close()
    return rows

def get_bar_counts(rows):
    real = sum(1 for r in rows if r[2] > 0)
    dummy = sum(1 for r in rows if r[2] == 0)
    return real, dummy

def get_btc_price(ts):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT close FROM ohlcv WHERE timestamp = ?", (ts,))
    row = c.fetchone()
    conn.close()
    return float(row[0]) if row else None

def volume_zscore(ts, lookback=20):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    hist_vols = []
    for i in range(1, lookback + 1):
        hour_start = ts - i * 3600 + 300
        hour_end = ts - (i - 1) * 3600
        c.execute("SELECT SUM(volume) FROM ohlcv WHERE timestamp BETWEEN ? AND ?", (hour_start, hour_end))
        v = c.fetchone()[0]
        if v is not None:
            hist_vols.append(v)
    conn.close()
    return hist_vols

def aggregate_hour(ts=None):
    ts = ts or get_last_hour_top()
    rows = fetch_ohlcv_for_hour(ts)
    if not rows or len(rows) == 0:
        logging.warning(f"[aggregate_signals] No bars found for hour {ts}")
        print(f"[aggregate_signals] WARNING: No bars found for hour {ts}")
        return False

    closes = [r[1] for r in rows]
    vols = [r[2] for r in rows]
    vwap_numer = np.sum([r[1] * r[2] for r in rows])
    vwap_denom = np.sum(vols)
    hourly_vwap = vwap_numer / vwap_denom if vwap_denom else closes[-1]
    hourly_close = closes[-1]
    vwap_percent_away = ((hourly_close - hourly_vwap) / hourly_vwap) * 100 if hourly_vwap else None
    total_volume = np.sum(vols)

    # Volume Z-Score
    hist_vols = volume_zscore(ts)
    if len(hist_vols) < 5:
        volume_z = None
    else:
        mean = np.mean(hist_vols)
        std = np.std(hist_vols)
        volume_z = (total_volume - mean) / std if std else 0

    btc_price = get_btc_price(ts)
    real_bar_count, dummy_bar_count = get_bar_counts(rows)  # Keep for logging if you want

    # Insert to signals table
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            timestamp INTEGER PRIMARY KEY,
            vwap REAL,
            vwap_percent_away REAL,
            total_volume REAL,
            volume_zscore REAL,
            btc_price REAL,
            score REAL
        )
    ''')
    c.execute('''
        INSERT OR REPLACE INTO signals
        (timestamp, vwap, vwap_percent_away, total_volume, volume_zscore, btc_price)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (ts, float(hourly_vwap), float(vwap_percent_away), float(total_volume),
          float(volume_z) if volume_z is not None else None,
          btc_price))
    conn.commit()
    conn.close()
    # Still print the counts for debug
    logging.info(f"[aggregate_signals] Wrote signal row for {ts}. VWAP: {hourly_vwap:.2f}, Vol: {total_volume:.4f}, Real bars: {real_bar_count}, Dummy bars: {dummy_bar_count}")
    print(f"[aggregate_signals] Wrote signal row for {ts} ({real_bar_count} real, {dummy_bar_count} dummy)")
    return True

def aggregate_signals():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS signals (
            timestamp INTEGER PRIMARY KEY,
            vwap REAL,
            vwap_percent_away REAL,
            total_volume REAL,
            volume_zscore REAL,
            btc_price REAL,
            score REAL
        )
    ''')
    conn.commit()

    c.execute('SELECT DISTINCT timestamp FROM ohlcv')
    all_bars = sorted(r[0] for r in c.fetchall())
    first_bar = min(all_bars)
    last_bar = max(all_bars)
     # Align to hour boundary
    first_hour = first_bar - (first_bar % 3600) + 3600
    last_hour = last_bar - (last_bar % 3600)
    hours = range(first_hour, last_hour + 1, 3600)

    c.execute('SELECT timestamp FROM signals')
    existing = set(r[0] for r in c.fetchall())
    conn.close()
    hours = [h for h in hours if h not in existing]
    wrote = 0
    for h in hours:
        ok = aggregate_hour(h)
        if ok:
            wrote += 1
    print(f"[aggregate_signals] Completed. Total new signals: {wrote}")
    logging.info(f"[aggregate_signals] Completed run. Total new signals: {wrote}")

if __name__ == "__main__":
    aggregate_signals()
