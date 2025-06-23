# src/scoring.py

# Define scoring rules as: {field: [(threshold, score)]}
scoring_rules = {
    "premium_z": [(-1.0, 0.3), (-1.3, 0.5)],
    "spread_z": [(-1.0, 0.2)],
    "median_fee": [(8, 0.2)],
    "funding_rate": [(0.01, 0.2), (-0.005, 0.3)]
}

def calculate_score(data, rules=scoring_rules):
    """
    Calculates a signal score based on threshold rules.

    Parameters:
        data (dict): keys are signal names, values are actual values
        rules (dict): scoring rules

    Returns:
        float: total score
    """
    score = 0.0
    for key, conditions in rules.items():
        value = data.get(key)
        if value is None:
            continue
        for threshold, weight in conditions:
            if (threshold > 0 and value > threshold) or (threshold < 0 and value < threshold):
                score += weight
    return round(score, 4)
