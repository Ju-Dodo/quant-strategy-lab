#!/usr/bin/env python3
"""Run backtest for gamma_cirques strategy."""

import sys
from pathlib import Path

STRATEGY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STRATEGY_DIR))

from qsl.backtest import run_backtest
from qsl.reporting import save_backtest_results

from strategy import GammaCirquesStrategy

REPO_ROOT = STRATEGY_DIR.parents[1]


def main() -> None:
    config_path = STRATEGY_DIR / "config.yaml"
    results_dir = STRATEGY_DIR / "results"
    strategy = GammaCirquesStrategy()
    result = run_backtest(strategy, config_path, repo_root=REPO_ROOT)
    summary = save_backtest_results(result, results_dir)
    print("Metrics:", result.metrics)
    print("Summary written to", summary)


if __name__ == "__main__":
    main()
