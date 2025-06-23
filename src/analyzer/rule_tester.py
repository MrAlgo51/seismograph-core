# src/analyzer/rule_tester.py

import pandas as pd

def test_rule(df, rule, return_col="return_1h", threshold=0.0):
    """
    Filters signals by rule string and evaluates forward return stats.

    Args:
        df (pd.DataFrame): The full signals+returns DataFrame.
        rule (str): Filter string, e.g. "score > 0.4 and median_fee > 5".
        return_col (str): Which return column to evaluate, e.g. "return_1h".
        threshold (float): Minimum return to count as a win (e.g. 0.001 = 0.1%).

    Returns:
        dict: Summary stats of the rule test.
    """
    try:
        subset = df.query(rule).dropna(subset=[return_col])
    except Exception as e:
        print(f"❌ Error applying rule: {e}")
        return {}

    total = len(subset)
    if total == 0:
        return {"total_signals": 0}

    wins = subset[subset[return_col] > threshold]
    avg_return = subset[return_col].mean()
    win_rate = len(wins) / total
    std = subset[return_col].std()
    max_loss = subset[return_col].min()
    max_gain = subset[return_col].max()

    return {
        "rule": rule,
        "return_col": return_col,
        "threshold": threshold,
        "total_signals": total,
        "avg_return": round(avg_return, 5),
        "win_rate": round(win_rate, 3),
        "std_dev": round(std, 5),
        "max_gain": round(max_gain, 5),
        "max_loss": round(max_loss, 5),
    }
