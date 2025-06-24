import sqlite3
import os

# Ensure the data/ folder exists
os.makedirs("data", exist_ok=True)

# Connect to the new database file
conn = sqlite3.connect("data/seismograph.db")
cursor = conn.cursor()

# Create the clean V2 signals table
cursor.execute("""
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
    score REAL
)
""")

def insert_spread_data(data: dict):
    conn = sqlite3.connect("seismograph.db")
    c = conn.cursor()

    # Create spread_data table if it doesn't exist
    c.execute("""
        CREATE TABLE IF NOT EXISTS spread_data (
            timestamp INTEGER PRIMARY KEY,
            btc_usd REAL,
            xmr_usd REAL,
            spread_ratio REAL,
            spread_zscore REAL
        )
    """)

    # Insert data
    c.execute("""
        INSERT OR REPLACE INTO spread_data (
            timestamp, btc_usd, xmr_usd, spread_ratio, spread_zscore
        ) VALUES (
            :timestamp, :btc_usd, :xmr_usd, :spread_ratio, :spread_zscore
        )
    """, data)

    conn.commit()
    conn.close()


print("✅ Seismograph signals table created successfully.")
