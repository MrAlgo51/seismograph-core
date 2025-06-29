# src/utils/zscore.py

import numpy as np

def compute_z_score(series, current_value):
    if len(series) < 2:
        return 0.0  # Avoid divide-by-zero
    mean = np.mean(series)
    std = np.std(series)
    return (current_value - mean) / std if std else 0.0

