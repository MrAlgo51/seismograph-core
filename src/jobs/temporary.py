import sqlite3
from src.jobs.score_logger import ScoreEngine

DB_PATH = "data/seismograph.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT timestamp FROM signals WHERE score IS NULL OR score = ''")
hours = [row[0] for row in c.fetchall()]
conn.close()

print(f"Scoring {len(hours)} missing hours")
for ts in hours:
    try:
        ScoreEngine(ts).run()
    except Exception as e:
        print(f"Failed to score {ts}: {e}")
