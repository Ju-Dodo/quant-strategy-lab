# Gamma Cirques

## Status

`research`

## Thesis

Strategy derived from the GResearch GRiddles puzzle *Gamma Cirques* (Andrew Smith). See [references/](references/) for the source PDF.

## Signal rules

**Current implementation:** placeholder dual SMA crossover on SPY (long when fast MA > slow MA). Replace with puzzle-specific rules in `strategy.py` as the write-up progresses.

| Rule | Code |
|------|------|
| Fast/slow windows | `config.yaml` → `params.fast_window`, `params.slow_window` |
| Position | `strategy.py` → `GammaCirquesStrategy.generate_positions` |

## Universe and data

- Single-name proxy: `SPY` daily adjusted close via yfinance
- Cache: repo-root `data/cache/`

## Backtest configuration

See [config.yaml](config.yaml).

## Results

Run from repo root:

```bash
python strategies/gamma_cirques/run_backtest.py
```

Metrics and curves are written to `results/` (gitignored).

## Promotion

When promoted to live trading:

1. Add `logic.md` with deterministic rules for the Rust port
2. Implement `deploy/crates/gamma_cirques/`
3. Update status to `promoted` and link deployment notes here
