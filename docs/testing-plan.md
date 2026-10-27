# Testing & CI Plan

Adapted to this repo's actual layout (`pipeline/`, `tests/`, `dashboard/`, `data/`).

## 1. Make the code easy to test first

Each pipeline stage should be a plain function that takes a DataFrame and returns a
DataFrame, separate from file reading and from the Dash app:

```
finance-dashboard/
├── pipeline/
│   ├── ingest.py      # load_transactions(path) -> DataFrame (loading + column check only)
│   ├── validate.py    # enforce_types(df), check_nulls(df)
│   ├── clean.py       # remove_duplicates(df)
│   ├── transform.py   # aggregations (monthly, by category)
│   ├── anomalies.py   # flag_anomalies(df, threshold=2.0)
│   └── load.py        # write to SQLite
├── dashboard/app.py   # Dash only; calls the functions above
├── tests/
│   ├── conftest.py    # shared fixtures (sample DataFrames)
│   ├── fixtures/      # small sample CSVs: clean, messy, empty
│   └── test_*.py      # one test file per module
├── requirements.txt
└── requirements-dev.txt   # pytest, pytest-cov, ruff
```

## 2. What to test, stage by stage

**Ingest**
- A valid CSV loads with the right columns and row count.
- An empty or header-only CSV is handled without crashing.
- A CSV with a missing required column raises a clear error.
- Write test CSVs with pytest's `tmp_path` fixture instead of real files.

**Validate (nulls and types)**
- Rows with missing amount or date are dropped or flagged (whichever the code does).
- Amounts like "$1,200.50" or "abc" are converted or rejected correctly.
- Bad dates ("2026-13-45") are caught.
- Use `@pytest.mark.parametrize` to run one test over many bad inputs.

**Clean (duplicates)**
- Exact duplicate rows are removed.
- Similar but non-duplicate rows (same amount, different date) are kept.
- The function doesn't mutate the DataFrame passed in.

**Transform**
- Monthly and category totals match hand-computed values on a tiny fixture.

**Anomaly detection**
- One obvious outlier (nine $20 purchases and one $5,000) gets flagged.
- Normal data produces no flags.
- All amounts identical (std == 0) produces no flags and no crash. The current code
  already guards this, so it is a regression test, not a bug found.
- Very small inputs (1–2 rows) don't crash.
- Changing the threshold changes which rows get flagged.

**Load**
- Data written to a temporary SQLite file can be read back with the same row count.

**End-to-end (integration)**
- Run a messy sample CSV through the whole pipeline (ingest → validate → clean →
  transform/anomalies → load) and check the final row count and flagged rows.
  Only call these "integration tests" if this test exists.

**Dashboard**
- One smoke test that the Dash app's layout builds without errors. Don't unit-test charts.

**Tools:** `conftest.py` fixtures, `pandas.testing.assert_frame_equal`, `pytest.raises(...)`.

## 3. Measure coverage

```
pytest --cov=pipeline --cov-report=term-missing
```

Aim for 80%+ on `pipeline/`. Don't chase 100%, and leave the dashboard out of the number.

## 4. GitHub Actions workflow

`.github/workflows/ci.yml`:

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ["3.12", "3.13"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}
          cache: pip
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: ruff check .
      - run: pytest --cov=pipeline --cov-report=term-missing --cov-fail-under=80
```

Then:
- Add a CI status badge to the README.
- Turn on branch protection for `main` (require the CI check to pass before merging),
  and make changes through pull requests from then on.
- Add a short "Running tests" section to the README.

## 5. Record real results when done

- Number of tests (pytest prints it at the end)
- Coverage % on `pipeline/`
- Python versions tested in CI
- Bugs the tests actually found, and what they were
- Whether CI blocks merges

Accuracy rules: say "integration tests" only if the end-to-end test exists, say "linting"
only if the ruff step is in CI, and use the real numbers.
