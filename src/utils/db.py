import sqlite3
import os

# Ensure the data folder exists
os.makedirs("data", exist_ok=True)

# === INSERT FUNCTIONS ===

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


def insert_mempool_data(data: dict):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS mempool (
            timestamp INTEGER PRIMARY KEY,
            median_fee REAL,
            unconfirmed_tx INTEGER,
            mempool_size INTEGER,
            fee_p10 REAL,
            fee_p50 REAL,
            fee_p90 REAL,
            bucket_low INTEGER,
            bucket_med INTEGER,
            bucket_high INTEGER
        )
    """)
    c.execute("""
        INSERT OR REPLACE INTO mempool (
            timestamp, median_fee, unconfirmed_tx, mempool_size,
            fee_p10, fee_p50, fee_p90,
            bucket_low, bucket_med, bucket_high
        ) VALUES (
            :timestamp, :median_fee, :unconfirmed_tx, :mempool_size,
            :fee_p10, :fee_p50, :fee_p90,
            :bucket_low, :bucket_med, :bucket_high
        )
    """, data)
    conn.commit()
    conn.close()


def insert_returns_data(data: dict):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS returns (
            timestamp INTEGER PRIMARY KEY,
            return_1h REAL,
            return_2h REAL,
            return_4h REAL
        )
    """)
    c.execute("""
        INSERT OR REPLACE INTO returns (
            timestamp, return_1h, return_2h, return_4h
        ) VALUES (
            :timestamp, :return_1h, :return_2h, :return_4h
        )
    """, data)
    conn.commit()
    conn.close()


def insert_signal_data(data: dict):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS signals (
            timestamp TEXT PRIMARY KEY,
            btc_price REAL,
            spread_pct REAL,
            spread_z REAL,
            premium_pct REAL,
            premium_z REAL,
            median_fee REAL,
            unconfirmed_tx INTEGER,
            mempool_size INTEGER,
            funding_rate REAL,
            funding_z REAL,
            score_urgency_only REAL,
            score_direction_only REAL,
            score_combined_basic REAL,
            score_combined_weighted REAL,
            score_urgency_then_direction REAL
        )
    """)
    c.execute("""
        INSERT OR REPLACE INTO signals (
            timestamp, btc_price, spread_pct, spread_z, premium_pct, premium_z,
            median_fee, unconfirmed_tx, mempool_size, funding_rate, funding_z,
            score_urgency_only, score_direction_only, score_combined_basic,
            score_combined_weighted, score_urgency_then_direction
        ) VALUES (
            :timestamp, :btc_price, :spread_pct, :spread_z, :premium_pct, :premium_z,
            :median_fee, :unconfirmed_tx, :mempool_size, :funding_rate, :funding_z,
            :score_urgency_only, :score_direction_only, :score_combined_basic,
            :score_combined_weighted, :score_urgency_then_direction
        )
    """, data)
    conn.commit()
    conn.close()

# === FETCH FUNCTIONS ===

def get_latest_spread(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT * FROM spread_data
        WHERE timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row and dict(zip([d[0] for d in c.description], row))


def get_latest_premium(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT * FROM premium_data
        WHERE timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row and dict(zip([d[0] for d in c.description], row))


def get_latest_mempool(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT * FROM mempool
        WHERE timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row and dict(zip([d[0] for d in c.description], row))


def get_latest_funding(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        SELECT * FROM funding
        WHERE timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row and dict(zip([d[0] for d in c.description], row))
