import requests
import sqlite3
import os
import logging
from datetime import datetime, timezone
import time

DB_PATH = "data/seismograph.db"

logging.basicConfig(filename='run_ohlcv.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s: %(message)s')

def create_ohlcv_table():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ohlcv (
            timestamp INTEGER PRIMARY KEY,
            open REAL,
            high REAL,
            low REAL,
            close REAL,
            volume REAL,
            vwap REAL
        )
    ''')
    conn.commit()
    conn.close()

def get_last_timestamp():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT MAX(timestamp) FROM ohlcv")
    last_ts = c.fetchone()[0]
    conn.close()
    return last_ts

def fetch_kraken_ohlcv(since):
    pair = "XBTUSD"
    interval = 5  # 5-minute bars
    url = "https://api.kraken.com/0/public/OHLC"
    params = {"pair": pair, "interval": interval, "since": since}
    try:
        resp = requests.get(url, params=params, timeout=15)
        resp.raise_for_status()
        data = resp.json()
        key = list(data["result"].keys())[0]
        ohlc = data["result"][key]
        return ohlc
    except Exception as e:
        logging.error(f"Error fetching OHLCV data from Kraken: {e}")
        return []

def validate_and_log_bars(bars):
    if not bars:
        return
    to_insert = []
    for bar in bars:
        try:
            ts = int(bar[0])
            o = float(bar[1])
            h = float(bar[2])
            l = float(bar[3])
            cl = float(bar[4])
            vwap = float(bar[5])
            volume = float(bar[6])
            # Ensure timestamp is multiple of 300 (5 min)
            if ts % 300 != 0:
                continue
            # Only insert if volume > 0
            if volume <= 0:
                continue
            to_insert.append((ts, o, h, l, cl, volume, vwap))
        except Exception as e:
            logging.error(f"Error processing bar {bar}: {e}")
    if to_insert:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.executemany('''
            INSERT OR REPLACE INTO ohlcv (timestamp, open, high, low, close, volume, vwap)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', to_insert)
        conn.commit()
        conn.close()
        logging.info(f"Inserted {len(to_insert)} new OHLCV bars.")
    else:
        logging.info("No valid bars to insert.")

def fill_missing_ohlcv_bars():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT timestamp, close FROM ohlcv ORDER BY timestamp ASC")
    bars = c.fetchall()
    if not bars:
        conn.close()
        print("[fill_missing_ohlcv_bars] No OHLCV data found.")
        return

    prev_ts, prev_close = bars[0]
    filled = 0
    for row in bars[1:]:
        curr_ts, curr_close = row
        expected_ts = prev_ts + 300
        while expected_ts < curr_ts:
            # Insert dummy bar
            c.execute('''
                INSERT OR IGNORE INTO ohlcv
                (timestamp, open, high, low, close, volume, vwap)
                VALUES (?, ?, ?, ?, ?, 0, ?)
            ''', (expected_ts, prev_close, prev_close, prev_close, prev_close, prev_close))
            log_time = datetime.fromtimestamp(expected_ts, tz=timezone.utc)
            print(f"[fill_missing_ohlcv_bars] Inserted dummy bar for {expected_ts} ({log_time})")
            logging.info(f"Inserted dummy (zero-volume) bar for {expected_ts} ({log_time})")
            filled += 1
            expected_ts += 300
        prev_ts, prev_close = curr_ts, curr_close
    conn.commit()
    conn.close()
    if filled:
        print(f"[fill_missing_ohlcv_bars] Filled {filled} missing 5-min bars.")
        logging.info(f"Filled {filled} missing 5-min bars with zero-volume dummies.")
    else:
        print("[fill_missing_ohlcv_bars] No gaps found.")
        logging.info("No gaps found.")

def get_latest_complete_bar():
    now = int(time.time())
    return now - (now % 300) - 300

def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    create_ohlcv_table()

    last_ts = get_last_timestamp()
    # Kraken since param: fetch bars after this timestamp (INCLUSIVE!)
    since = last_ts if last_ts else int(time.time()) - 86400    # 24h ago

    latest_complete_bar = get_latest_complete_bar()

    # DO NOT skip bars at latest_complete_bar! Allow up to and including latest_complete_bar.
    print(f"Last timestamp in DB: {last_ts}")
    print(f"Fetching OHLCV data since: {since}")
    print(f"Latest complete 5-min bar: {latest_complete_bar}")

    bars = fetch_kraken_ohlcv(since)
    # Only keep bars at or before latest_complete_bar
    bars = [bar for bar in bars if int(bar[0]) <= latest_complete_bar]

    print(f"Number of bars fetched: {len(bars)}")
    if bars:
        print(f"First bar sample: {bars[0]}")
        validate_and_log_bars(bars)
    else:
        logging.info("No new OHLCV bars fetched.")

    fill_missing_ohlcv_bars()

if __name__ == "__main__":
    main()
