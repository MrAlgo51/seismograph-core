import sqlite3
import pandas as pd

def load_signals_and_returns():
    conn = sqlite3.connect("data/seismograph.db")

    # Load signals table (with all score variants)
    signals_df = pd.read_sql_query("SELECT * FROM signals", conn)

    # Load returns table (1h, 2h, 4h forward returns)
    returns_df = pd.read_sql_query("SELECT * FROM returns", conn)

    conn.close()

    # Merge on timestamp (inner join — only aligned rows)
    df = pd.merge(signals_df, returns_df, on="timestamp", how="inner")

    print(f"[ANALYZER] Loaded {len(df)} joined rows")
    return df

if __name__ == "__main__":
    df = load_signals_and_returns()
    print(df.head())  # Show preview
