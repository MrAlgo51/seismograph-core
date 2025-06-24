# Seismograph: Scoring Engine Plan

This document outlines the strategy for building and maintaining the scoring engine used in Seismograph.

---

## Purpose

The scoring engine assigns a numeric value ("score") to each signal timestamp. This score reflects the confidence or strength of a potential trade setup based on multiple z-scored or raw metrics.

The score is used for:
- Filtering trades
- Backtesting signal combinations
- Rule-based logic (e.g. "only enter if score > 0.5")

---

## Goals

✅ Make scoring logic transparent  
✅ Use a centralized config file for weights  
✅ Keep everything modular and debuggable  
✅ Prevent hardcoded logic or hidden math  
✅ Allow fast iteration and tuning

---

## Architecture

- `config/weights.py` defines signal weights:

```python
weights = {
    "spread_zscore": 0.6,
    "premium_zscore": 0.4,
    # Add more signals later
}
