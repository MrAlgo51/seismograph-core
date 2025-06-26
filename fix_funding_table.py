import sqlite3
import time

conn = sqlite3.connect("data/seismograph.db")
c = conn.cursor()

# Create funding table if it doesn't exist
c.execute("""
    CREATE TABLE IF NOT EXISTS funding (
        timestamp INTEGER PRIMARY KEY,
        funding_rate REAL,
        funding_z REAL
    )
""")

# Insert dummy row (current hour)
timestamp = int(time.time()) // 3600 * 3600
c.execute("""
    INSERT OR REPLACE INTO funding (
        timestamp, funding_rate, funding_z
    ) VALUES (
        ?, ?, ?
    )
""", (timestamp, 0.0001, 0.5))

conn.commit()
conn.close()
print(f"? Funding table created with dummy row at {timestamp}")
