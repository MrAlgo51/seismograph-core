# src/analyzer/return_generator.py

import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def load_signals(db_path="data/seismograph.db"):
    """Loads the full signals table as a DataFrame."""
    conn = sqlite3.connect(db_path)
    df = pd.read_sql("SELECT * FROM signals", conn, parse_dates=["timestamp"])
    conn.close()
    return df.sort_values("timestamp")

def add_forward_returns(df, price_col="btc_price", horizons=[1, 2, 4]):
    """
    Adds forward return columns to the dataframe.

    Args:
        df (pd.DataFrame): Signals with a timestamp and price.
        price_col (str): Name of BTC price column.
        horizons (list): List of hours to calculate forward returns for.

    Returns:
        pd.DataFrame: Original + return_Xh columns
    """
    df = df.copy()
    df.set_index("timestamp", inplace=True)

    for h in horizons:
        df[f"return_{h}h"] = (
            df[price_col].shift(-h) - df[price_col]
        ) / df[price_col]

    df.reset_index(inplace=True)
    return df
