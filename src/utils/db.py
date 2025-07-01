import sqlite3
import os
import pandas as pd

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


def insert_usdt_premium_data(data: dict):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usdt_premium_data (
            timestamp INTEGER PRIMARY KEY,
            btc_usdt REAL,
            btc_usd REAL,
            usdt_premium_pct REAL,
            usdt_premium_zscore REAL
        )
    """)
    c.execute("""
        INSERT OR REPLACE INTO usdt_premium_data (
            timestamp, btc_usdt, btc_usd, usdt_premium_pct, usdt_premium_zscore
        ) VALUES (
            :timestamp, :btc_usdt, :btc_usd, :usdt_premium_pct, :usdt_premium_zscore
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
            bucket_high INTEGER,
            median_fee_z REAL,
            unconfirmed_tx_z REAL,
            mempool_size_z REAL
        )
    """)
    c.execute("""
        INSERT OR REPLACE INTO mempool (
            timestamp, median_fee, unconfirmed_tx, mempool_size,
            fee_p10, fee_p50, fee_p90,
            bucket_low, bucket_med, bucket_high,
            median_fee_z, unconfirmed_tx_z, mempool_size_z
        ) VALUES (
            :timestamp, :median_fee, :unconfirmed_tx, :mempool_size,
            :fee_p10, :fee_p50, :fee_p90,
            :bucket_low, :bucket_med, :bucket_high,
            :median_fee_z, :unconfirmed_tx_z, :mempool_size_z
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
        timestamp INTEGER PRIMARY KEY,
        btc_price REAL,
        spread_zscore REAL,
        usdt_premium_zscore REAL,
        median_fee_z REAL,
        unconfirmed_tx_z REAL,
        mempool_size_z REAL,
        score REAL
    )
    """)
    c.execute("""
        INSERT OR REPLACE INTO signals (
            timestamp, btc_price,
            spread_zscore, usdt_premium_zscore,
            median_fee_z, unconfirmed_tx_z, mempool_size_z,
            score
        ) VALUES (
            :timestamp, :btc_price,
            :spread_zscore, :usdt_premium_zscore,
            :median_fee_z, :unconfirmed_tx_z, :mempool_size_z,
            :score
        )
    """, data)

    conn.commit()
    conn.close()


# === FETCH FUNCTIONS ===

def get_latest_spread(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    # Ensure table exists
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
        SELECT * FROM spread_data
        WHERE timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row and dict(zip([d[0] for d in c.description], row))



def get_latest_usdt_premium(timestamp: int):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usdt_premium_data (
            timestamp INTEGER PRIMARY KEY,
            btc_usdt REAL,
            btc_usd REAL,
            usdt_premium_pct REAL,
            usdt_premium_zscore REAL
        )
    """)
    c.execute("""
        SELECT * FROM usdt_premium_data
        WHERE timestamp <= ?
        ORDER BY timestamp DESC
        LIMIT 1
    """, (timestamp,))
    row = c.fetchone()
    conn.close()
    return row and dict(zip([d[0] for d in c.description], row))



def fetch_recent_mempool_data(limit=48):
    conn = sqlite3.connect("data/seismograph.db")
    c = conn.cursor()

    # Ensure table exists before querying
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
            bucket_high INTEGER,
            median_fee_z REAL,
            unconfirmed_tx_z REAL,
            mempool_size_z REAL
        )
    """)

    query = """
        SELECT timestamp, median_fee, unconfirmed_tx, mempool_size
        FROM mempool
        ORDER BY timestamp DESC
        LIMIT ?
    """
    df = pd.read_sql_query(query, conn, params=(limit,))
    conn.close()
    return df.sort_values("timestamp")




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

