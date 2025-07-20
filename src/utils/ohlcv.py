import sqlite3
import numpy as np
import logging

DB_PATH = "data/seismograph.db"

logging.basicConfig(
    filename='ohlcv_utils.log',
    level=logging.INFO,
    format='%(asctime)s %(levelname)s: %(message)s'
)

def get_hourly_context(ts, lookback=20, min_bars=8):
    """
    Aggregates OHLCV for the last hour ending at timestamp ts (inclusive).
    Only uses bars with volume > 0.
    Returns dict with keys: vwap, vwap_percent_away, total_volume, volume_zscore.
    """
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        # Find the hour's range (e.g., for 11:00:00, gets 10:05...11:00 inclusive)
        end = ts
        start = ts - 3600 + 300  # Assumes 5-min bars
        c.execute(
            "SELECT timestamp, close, volume, vwap FROM ohlcv "
            "WHERE timestamp BETWEEN ? AND ? AND volume > 0 "
            "ORDER BY timestamp ASC",
            (start, end)
        )
        rows = c.fetchall()
        real_bar_count = len(rows)
        if real_bar_count < min_bars:
            logging.warning(
                f"[get_hourly_context] Not enough real bars for hour ending {ts}. Got {real_bar_count} (need {min_bars})."
            )
            conn.close()
            return {
                "vwap": None,
                "vwap_percent_away": None,
                "total_volume": None,
                "volume_zscore": None,
                "real_bar_count": real_bar_count
            }

        vols = np.array([r[2] for r in rows])
        closes = np.array([r[1] for r in rows])
        vwaps = np.array([r[3] for r in rows])
        hourly_vwap = np.sum(closes * vols) / np.sum(vols) if np.sum(vols) else closes[-1]
        hourly_close = closes[-1]
        vwap_percent_away = ((hourly_close - hourly_vwap) / hourly_vwap * 100) if hourly_vwap else None
        total_volume = np.sum(vols)

        # --- Volume Z-score using lookback ---
        hist_vols = []
        for i in range(1, lookback + 1):
            hour_start = ts - i * 3600 + 300
            hour_end = ts - (i - 1) * 3600
            c.execute(
                "SELECT SUM(volume) FROM ohlcv WHERE timestamp BETWEEN ? AND ? AND volume > 0",
                (hour_start, hour_end)
            )
            v = c.fetchone()[0]
            if v is not None:
                hist_vols.append(v)
        conn.close()
        if len(hist_vols) < 5:
            volume_z = None
            logging.info(f"[get_hourly_context] Not enough history for z-score at ts {ts} (got {len(hist_vols)}).")
        else:
            mean = np.mean(hist_vols)
            std = np.std(hist_vols)
            volume_z = (total_volume - mean) / std if std else 0

        result = {
            "vwap": float(hourly_vwap),
            "vwap_percent_away": float(vwap_percent_away),
            "total_volume": float(total_volume),
            "volume_zscore": float(volume_z) if volume_z is not None else None,
            "real_bar_count": real_bar_count
        }
        logging.info(f"[get_hourly_context] {ts}: {result}")
        return result

    except Exception as e:
        logging.error(f"Error in get_hourly_context for ts {ts}: {e}")
        return {
            "vwap": None,
            "vwap_percent_away": None,
            "total_volume": None,
            "volume_zscore": None,
            "real_bar_count": 0
        }

# Example usage:
if __name__ == "__main__":
    import time
    # Test for the last complete hour
    now = int(time.time())
    last_hour = now - (now % 3600)
    print(get_hourly_context(last_hour))
