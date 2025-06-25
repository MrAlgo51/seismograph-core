import sqlite3

conn = sqlite3.connect("data/seismograph.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE spread_data ADD COLUMN spread_z REAL;")
    print("✅ spread_z column added to spread_data.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Already exists or failed: {e}")

conn.commit()
conn.close()
