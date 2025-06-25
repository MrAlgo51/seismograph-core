import sqlite3
from src.config.score_variants import score_configs

conn = sqlite3.connect("data/seismograph.db")
c = conn.cursor()

# Loop through all score variant names
for score_name in score_configs.keys():
    try:
        c.execute(f"ALTER TABLE signals ADD COLUMN {score_name} REAL;")
        print(f"✅ Added column: {score_name}")
    except sqlite3.OperationalError as e:
        print(f"⚠️ Skipped {score_name}: {e}")

conn.commit()
conn.close()
