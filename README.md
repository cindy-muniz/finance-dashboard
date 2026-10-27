# Personal Finance Data Pipeline & Dashboard

An end-to-end ETL pipeline in Python. It ingests and validates raw transaction data,
transforms it (aggregations and per-category z-score anomaly detection), loads it into
SQLite, and will visualize it with a Plotly Dash dashboard.

> Work in progress. See the roadmap below for what is done.

## Project layout

```
finance-dashboard/
├── data/
│   ├── generate_mock_data.py   # 200 seeded mock transactions -> data/transactions.csv
│   └── transactions.csv
├── pipeline/
│   ├── ingest.py               # load_transactions(filepath)
│   └── transform.py            # aggregations + flag_anomalies
├── tests/
├── dashboard/
└── docs/testing-plan.md
```

## Setup

Requires Python 3.13.

```bash
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -r requirements.txt
python data/generate_mock_data.py
```

## Roadmap

- [x] Mock data generator (`data/generate_mock_data.py`)
- [x] Ingestion with column validation, null/duplicate handling (`pipeline/ingest.py`)
- [ ] **1. Get on GitHub:** `.gitignore`, package `__init__.py` files, README, first push
- [ ] **2.** Run and fix `pipeline/transform.py`; write `pipeline/load.py` (SQLite)
- [ ] **3.** Refactor into testable stages: `ingest`, `validate`, `clean`, `anomalies`
- [ ] **4.** pytest suite, coverage, and GitHub Actions CI (see `docs/testing-plan.md`)
- [ ] **5.** Plotly Dash dashboard (`dashboard/app.py`) reading from SQLite, plus a smoke test
- [ ] **6.** README polish (CI badge, running tests), branch protection, deployment
