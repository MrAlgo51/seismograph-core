def log_ohlcv_batch(bars):
    """
    Inserts a batch of OHLCV bars into the database.
    Skips bars with volume <= 0, timestamp misaligned, or duplicates.
    Expects bars as list of dicts or lists in Kraken format.
    """
    import sqlite3
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    inserted = 0

    for bar in bars:
        try:
            # Supports both list (Kraken) and dict (custom) bars
            if isinstance(bar, dict):
                ts = int(bar["timestamp"])
                o = float(bar["open"])
                h = float(bar["high"])
                l = float(bar["low"])
                cl = float(bar["close"])
                vwap = float(bar["vwap"])
                volume = float(bar["volume"])
            else:  # Kraken raw list
                ts = int(bar[0])
                o = float(bar[1])
                h = float(bar[2])
                l = float(bar[3])
                cl = float(bar[4])
                vwap = float(bar[5])
                volume = float(bar[6])

            if ts % 300 != 0 or volume <= 0:
                continue  # skip bad/misaligned/zero bars

            # Fast duplicate skip (primary key will also enforce, but avoids error log)
            c.execute("SELECT 1 FROM ohlcv WHERE timestamp = ?", (ts,))
            if c.fetchone():
                continue

            c.execute('''
                INSERT OR IGNORE INTO ohlcv (timestamp, open, high, low, close, volume, vwap)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (ts, o, h, l, cl, volume, vwap))
            inserted += 1
        except Exception as e:
            logging.error(f"Error logging bar at {bar}: {e}")

    conn.commit()
    conn.close()
    print(f"[ohlcv_logger] Batch insert complete. Inserted {inserted} bars.")
    return inserted
