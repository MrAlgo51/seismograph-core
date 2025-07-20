## Seismograph Data Pipeline: Reference Guide & Flowchart

This document captures the full architecture, reasoning, and logic flow of the Seismograph system — from raw signal capture through return analysis and model-ready data. It is meant to serve as a reference for clarity, onboarding, or development.

---

### 🧭 High-Level Flowchart

```
[1] Raw Market Data (BTC/XMR, mempool, fees, BTC price, etc.)
       |
       v
[2] Signal Normalization
    → z-scores per feature
       |
       v
[3] signals table
    → Stores timestamped z-score values
       |
       v
[4] Return Calculation (features)
    → For each signal: % change in z-score over 1h/2h/4h
       |
       v
[5] returns table
    → Feature returns (e.g. score_return_1h)
       +
    → BTC price returns (btc_price_return_1h, etc.)  ✅ Target
       |
       v
[6] Analyzer
    → Rule testing
    → Bucketed return analysis
    → Model training (X = feature_returns, y = btc_price_return)
```

---

### 🔍 Concepts & Definitions

#### Feature vs Target

* **Feature Return**: Measures how a signal (e.g., score, spread\_zscore) moves over a horizon

  ```
  feature_return = (feature_t+h - feature_t) / feature_t
  ```
* **Target (BTC Return)**: Measures how BTC price moves over the same horizon

  ```
  btc_price_return = (price_t+h - price_t) / price_t
  ```

#### Horizons

* Horizons are future windows you're measuring against: 1h, 2h, 4h (etc.)
* Each horizon generates both feature returns and BTC returns

#### `get_closest_future(ts)`

* A utility function that returns the first available row **at or after** a target timestamp
* Protects against missing/irregular timestamps and ensures aligned return calculation

---

### ✅ Why Only One BTC Price Return Column per Horizon?

* BTC price return is the **shared target** — every feature is trying to predict the same thing
* No need to compute "BTC return for score" and "BTC return for spread" separately — it's the same BTC move

---

### 💥 Summary of Pipeline Purpose

You are:

* Tracking signal abnormality (z-scores)
* Measuring how fast those signals move (feature returns)
* Logging what BTC does afterward (BTC returns)
* Testing whether feature moves predict price moves

This separation between features and target is what allows:

* Rule testing ("if score\_return > X, then...?")
* Predictive modeling (features → BTC outcome)
* Real signal generation

---

### 🧠 Author's Breakthrough

> "My breakthrough was understanding that the returns table was measuring the *change in the features*, not the change in BTC. Once that clicked, the rest of the system made a lot more sense."

This document reflects that conceptual shift and now serves as a canonical map of how the system works.

---

*Stored in `seis/docs/seismograph_pipeline_guide.md`*
