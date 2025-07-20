import sqlite3
import datetime

DB_PATH = "data/seismograph.db"

def unix_to_human(ts):
    return datetime.datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d %H:%M')

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()

# Get all ohlcv timestamps in order
c.execute("SELECT timestamp FROM ohlcv ORDER BY timestamp ASC")
rows = [r[0] for r in c.fetchall()]

# Group by top-of-hour
from collections import defaultdict
hours = defaultdict(list)
for ts in rows:
    hour_top = ts - (ts % 3600)
    hours[hour_top].append(ts)

# Print hours missing bars
print(f"{'Hour':<20}{'#Bars':<6}{'Expected':<10}")
for hour, ts_list in sorted(hours.items()):
    count = len(ts_list)
    missing = count < 12
    print(f"{unix_to_human(hour):<20}{count:<6}{'(MISSING)' if missing else ''}")

# Optionally, print the most recent hour
if hours:
    last_hour = max(hours.keys())
    print(f"\nMost recent hour in ohlcv: {unix_to_human(last_hour)} — Bars: {len(hours[last_hour])}")

conn.close()
