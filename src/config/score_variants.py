# src/config/score_variants.py

score_configs = {
    "score_urgency_only": {
        "median_fee": 0.4,
        "unconfirmed_tx": 0.3,
        "premium_z": 0.3
    },

    "score_direction_only": {
        "spread_z": 1.0
    },

    "score_combined_basic": {
        "spread_z": 0.5,
        "premium_z": 0.5
    },

    "score_combined_weighted": {
        "spread_z": 0.2,
        "premium_z": 0.6,
        "median_fee": 0.2
    },

    "score_urgency_then_direction": {
        "premium_z": 0.3,
        "median_fee": 0.3,
        "spread_z": 0.4
    }
}

