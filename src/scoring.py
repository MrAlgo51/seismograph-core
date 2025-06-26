from src.config.score_variants import score_configs

def compute_all_scores(row):
    scores = {}
    for score_name, weights in score_configs.items():
        score = 0.0
        for var, weight in weights.items():
            val = row.get(var)
            if val is not None:
                score += val * weight
        scores[score_name] = score
    return scores
