from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from qsl.backtest.engine import BacktestResult


def save_backtest_results(result: BacktestResult, output_dir: Path | str) -> Path:
    """Write equity curve, returns, positions, and metrics to output_dir."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)

    result.equity_curve.to_frame("equity").to_csv(out / "equity_curve.csv")
    result.returns.to_frame("return").to_csv(out / "returns.csv")
    result.positions.to_csv(out / "positions.csv")

    summary_path = out / "summary.json"
    with open(summary_path, "w") as f:
        json.dump(result.metrics, f, indent=2)

    return summary_path
