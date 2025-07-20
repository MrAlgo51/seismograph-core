import sqlite3

DB_PATH = "data/seismograph.db"

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = [row[0] for row in c.fetchall()]
print("Tables in your database:")
for t in tables:
    print("-", t)
conn.close()
