import sqlite3

conn = sqlite3.connect("data/seismograph.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE premium_data ADD COLUMN premium_z REAL;")
    print("✅ premium_z column added to premium_data.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Already exists or failed: {e}")

conn.commit()
conn.close()
