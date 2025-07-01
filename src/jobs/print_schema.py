import sqlite3
conn = sqlite3.connect('data/seismograph.db')
c = conn.cursor()

for table in ["spread_data", "premium_data", "mempool", "signals", "returns"]:
    print(f"--- {table} ---")
    c.execute(f"PRAGMA table_info({table})")
    for row in c.fetchall():
        print(row)
    print()

conn.close()
