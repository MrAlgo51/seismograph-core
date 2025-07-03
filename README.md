# seismograph-core
Next-gen Bitcoin stress signal system. Modular, logged, and built for edge.

<pre>seismograph-core/                 # Top-level project folder
│
├── .gitignore                   # Git: files to exclude from version control
├── fix_funding_table.py         # (One-off) Script to fix/patch the funding table in the database
├── fix_premium_table.py         # (One-off) Script to fix/patch the USDT premium table
├── fix_signals_table.py         # (One-off) Script to fix/patch the signals table
├── fix_spread_table.py          # (One-off) Script to fix/patch the spread table
├── labels.md                    # Markdown notes: probably label definitions or documentation
├── notes.md                     # Markdown notes: your general project notes
├── README.md                    # Main project documentation (start here!)
├── runall.log                   # Log file output from a previous pipeline run
├── run_logger.py                # Script: runs main logging process (core signals logger)
├── run_usdt_premium_logger.py   # Script: runs the USDT premium logger
├── run_xmr_spread_logger.py     # Script: runs the XMR spread logger
│
├── .git/                        # (Hidden) Git repository metadata (ignore)
│
├── data/                        # Data directory (contains SQLite DBs and possibly CSVs)
│   ├── seismograph.db           # Main SQLite database with all signals, returns, etc.
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
│   ├── (other modules…)         # Any other shared code for import
│
├── scripts/                     # One-off, utility, or data migration scripts
│   ├── backup_db.py             # Backs up the database (manual or scheduled)
│   └── (other scripts…)         # Any other migration, export, or fixup scripts
│
├── visualizations/              # Notebooks and scripts for visualization/analysis
│   ├── analysis.ipynb           # Jupyter notebook for interactive analysis
│   ├── plot_returns.py          # Python script for plotting returns
│   ├── (other visualization…)   # Any other .ipynb or plot scripts
│
└── tests/                       # Unit tests or test scripts (if present)
    └── (test files…)            # Test code to validate pipeline</pre>
