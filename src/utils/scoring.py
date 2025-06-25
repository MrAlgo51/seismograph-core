# src/utils/scoring.py

from src.config.score_variants import score_configs

def compute_scores(row: dict) -> dict:
    """
    Given a dict of signal inputs, compute all score variants.
    Returns a dict: {score_name: score_value}
    """
    scores = {}

    for score_name, weights in score_configs.items():
        score = 0.0
        for key, weight in weights.items():
            value = row.get(key)
            if value is not None:
                score += value * weight
        scores[score_name] = score

    return scores
