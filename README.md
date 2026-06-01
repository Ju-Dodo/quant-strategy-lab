# quant-strategy-lab

Strategy lab for quantitative research: shared Python library (`qsl`), per-strategy folders, and Rust deployment for promoted strategies.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"
```

Locked dependencies for CI/reproducibility live in [requirements.txt](requirements.txt). After changing [pyproject.toml](pyproject.toml), refresh the lock:

```bash
pip install -e ".[dev]"
pip freeze | grep -E '^(numpy|scipy|pandas|yfinance|pyyaml|qsl|pytest|ruff)' > requirements.txt
```

## Layout

| Path | Purpose |
|------|---------|
| `src/qsl/` | Shared library — data, backtest, indicators, reporting |
| `strategies/<slug>/` | One strategy per folder (write-up, config, backtest) |
| `deploy/` | Rust workspace for live trading via Alpaca |
| `data/cache/` | Shared price cache (gitignored) |
| `scripts/` | Scaffolding and utilities |

## Run a backtest

```bash
python strategies/gamma_cirques/run_backtest.py
```

## New strategy

```bash
python scripts/new_strategy.py my_strategy_slug
```

## Promotion to live trading

When a strategy passes your research gates, document rules in `strategies/<slug>/logic.md` and add a crate under `deploy/crates/<slug>/`. See each strategy README for status (`research` → `candidate` → `promoted`).
