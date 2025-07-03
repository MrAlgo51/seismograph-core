<<<<<<< HEAD
# Seismograph Core

Seismograph Core is a modular Python project for collecting, scoring, and analyzing on-chain and market signals for BTC swing trading research. It’s designed for independent, data-driven signal development—no external dependencies, no web dashboards, just raw logs, SQLite, and code you can trust.

## What It Does

- **Logs key data**: BTC mempool stats, funding rates, USDT premium, BTC/XMR spread, and synthetic signals, all on an hourly schedule.
- **Calculates feature scores**: Uses domain-specific z-scores and custom scoring logic to produce research-grade signals.
- **Computes forward returns**: Matches every signal with its 1h, 2h, and 4h “future” and logs all returns for offline analysis.
- **Modular pipeline**: Every logging step is its own script. Easy to audit, debug, or adapt.
- **Visualizes**: Notebooks and scripts for quick review and deeper research.
- **Zero SaaS, zero tracking, zero bullshit.** All code is local and open.

## Why This Exists

Crypto signal research is full of hype and overfitted “AI.” This repo is for rigorous, old-school, statistically honest, *offline* alpha mining—with total control. You own the code, the data, and the pipeline.

## Project Structure

See `tree` output below (cleaned up):


## Requirements

- Python 3.9+  
- `sqlite3` (included in stdlib)  
- `requests`, `numpy`, `pandas`, etc. (see `requirements.txt` if present)

## How To Use

1. **Clone the repo** and install dependencies.
2. **Edit config** in `modules/config.py` if needed.
3. **Run logger scripts** (from root directory) to pull fresh data:
    ```sh
    python jobs/mempool_logger.py
    python jobs/usdt_premium_logger.py
    python jobs/spread_logger.py
    python jobs/returns_logger.py
    ```
4. **Explore signals and returns** with Jupyter (`visualizations/analysis.ipynb`) or your favorite Python tool.

**Tip:** The project is 100% batch/offline—no web server, no Flask/FastAPI, no cron by default.  
Use `run_logger.py` or write a simple shell script for orchestration.

## Extending/Modifying

- Add new jobs to `jobs/`.
- Add new scoring features in `modules/scoring.py`.
- Patch or backup data in `scripts/`.
- Visualize results in `visualizations/`.

## Philosophy

- **No vendor lock-in.** All source, all raw.
- **Audit-friendly.** Every signal is reproducible and logged.
- **Built for tinkerers.** The point is learning and finding real edge.

---

> Questions, improvements, or want to fork for a different asset?  
> Open an issue or just clone and go wild.  
> No guarantees, no hand-holding, just code.

=======
<pre>seismograph-core/                 # Top-level project folder
│
├── README.md                    # Main project documentation (start here!)
│
├── .gitignore                   # Git: files to exclude from version control
│
├── labels.md                    # Markdown: label definitions/documentation
├── notes.md                     # Markdown: general project notes
│
├── run_logger.py                # Script: runs main logging process (core signals logger)
├── run_usdt_premium_logger.py   # Script: runs the USDT premium logger
├── run_xmr_spread_logger.py     # Script: runs the XMR spread logger
│
├── data/                        # Data directory (SQLite DBs, CSVs, etc)
│   ├── seismograph.db           # Main SQLite database (signals, returns, etc.)
│   └── (other data files…)      # (Other .db or .csv files if present)
│
├── jobs/                        # Scheduled or batch job scripts
│   ├── funding_logger.py        # Logs funding rate data to DB
│   ├── mempool_logger.py        # Logs mempool stats to DB
│   ├── returns_logger.py        # Computes forward returns and logs them to DB
│   ├── score_logger.py          # Computes signal scores and logs them to DB
│   ├── spread_logger.py         # Logs XMR/BTC spread data to DB
│   ├── usdt_premium_logger.py   # Logs USDT premium data to DB
│   └── (other job scripts…)     # Any other batch loggers or updaters
│
├── modules/                     # Python modules (utility functions, API wrappers, scoring logic)
│   ├── __init__.py              # Python package marker
│   ├── config.py                # Stores config, keys, or DB paths
│   ├── scoring.py               # Scoring logic for signal calculation
│   ├── utils.py                 # Utility/helper functions
│   └── (other modules…)         # Any other shared code for import
│
├── scripts/                     # Utility/data migration scripts (rarely run, not core pipeline)
│   ├── backup_db.py             # Script: backs up the database (manual or scheduled)
│   └── (other scripts…)         # Any migration/export/fixup scripts
│
├── visualizations/              # Notebooks and scripts for visualization/analysis
│   ├── analysis.ipynb           # Jupyter notebook for interactive analysis
│   ├── plot_returns.py          # Python script for plotting returns
│   └── (other visualization…)   # Any other .ipynb or plot scripts
│
└── tests/                       # Unit tests or test scripts (if present)
    └── (test files…)            # Test code to validate pipeline</pre>
>>>>>>> e7f3235de598b4fb548a60375ab1b042a55eef99

