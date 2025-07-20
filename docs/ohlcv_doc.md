Script Name           | Path                          | Schedule            | Purpose / Output
----------------------|-------------------------------|---------------------|----------------------------------------
run_ohlcv.py          | src/jobs/run_ohlcv.py         | Every 5 min (task)  | Fetch 5-min OHLCV → ohlcv table
aggregate_signals.py  | src/jobs/aggregate_signals.py | 1st in run_all.py   | 5-min → hourly signals
spread_logger.py      | src/jobs/spread_logger.py     | run_all.py (hourly) | Log spread_zscore → spread_data
usdt_premium_logger.py| src/jobs/usdt_premium_logger.py| run_all.py (hourly)| Log usdt_premium_zscore → usdt_premium
mempool_logger.py     | src/jobs/mempool_logger.py    | run_all.py (hourly) | Log mempool congestion → mempool_data
score_logger.py       | src/jobs/score_logger.py      | run_all.py (hourly) | Join signals + metrics → signals (score)
returns_logger.py     | src/jobs/returns_logger.py    | run_all.py (hourly) | Forward returns on features → returns

