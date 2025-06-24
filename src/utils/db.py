import sqlite3
import os

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

def insert_spread_data(data: dict):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS spread_data (
            timestamp INTEGER PRIMARY KEY,
            btc_usd REAL,
            xmr_usd REAL,
            spread_ratio REAL,
            spread_zscore REAL
        )
    """)

    c.execute("""
        INSERT OR REPLACE INTO spread_data (
            timestamp, btc_usd, xmr_usd, spread_ratio, spread_zscore
        ) VALUES (
            :timestamp, :btc_usd, :xmr_usd, :spread_ratio, :spread_zscore
        )
    """, data)

    conn.commit()
    conn.close()


def insert_premium_data(data: dict):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS premium_data (
            timestamp INTEGER PRIMARY KEY,
            btc_usdt REAL,
            btc_usd REAL,
            premium_pct REAL,
            premium_zscore REAL
        )
    """)

    c.execute("""
        INSERT OR REPLACE INTO premium_data (
            timestamp, btc_usdt, btc_usd, premium_pct, premium_zscore
        ) VALUES (
            :timestamp, :btc_usdt, :btc_usd, :premium_pct, :premium_zscore
        )
    """, data)

    conn.commit()
    conn.close()
