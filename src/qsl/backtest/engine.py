from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
import yaml

from qsl.backtest.metrics import compute_metrics, compute_turnover
from qsl.data.loader import load_prices
from qsl.strategies.base import Strategy, StrategyContext


@dataclass
class BacktestResult:
    equity_curve: pd.Series
    returns: pd.Series
    positions: pd.DataFrame
    metrics: dict[str, float]
    config: dict[str, Any]


def _load_config(path: Path | str) -> dict[str, Any]:
    with open(path) as f:
        return yaml.safe_load(f)


def _align_positions(positions: pd.DataFrame, prices: pd.DataFrame) -> pd.DataFrame:
    aligned = positions.reindex(index=prices.index, columns=prices.columns)
    return aligned.fillna(0.0)


def run_backtest(
    strategy: Strategy,
    config: dict[str, Any] | Path | str,
    *,
    repo_root: Path | str | None = None,
) -> BacktestResult:
    """
    Run a vectorized backtest: strategy positions lagged one day vs returns.

    Config keys: tickers, start, end, initial_capital, commission_bps, slippage_bps,
    periods_per_year, risk_free_rate, params (passed to StrategyContext).
    """
    if isinstance(config, (Path, str)):
        cfg = _load_config(Path(config))
    else:
        cfg = config

    tickers: list[str] = list(cfg["tickers"])
    start: str = cfg["start"]
    end: str | None = cfg.get("end")
    initial_capital: float = float(cfg.get("initial_capital", 100_000.0))
    commission_bps: float = float(cfg.get("commission_bps", 0.0))
    slippage_bps: float = float(cfg.get("slippage_bps", 0.0))
    periods_per_year: int = int(cfg.get("periods_per_year", 252))
    risk_free_rate: float = float(cfg.get("risk_free_rate", 0.0))
    params: dict[str, Any] = dict(cfg.get("params", {}))

    cache_dir = cfg.get("cache_dir", "data/cache")
    if repo_root is not None:
        cache_dir = str(Path(repo_root) / cache_dir)

    prices = load_prices(tickers, start, end, cache_dir=cache_dir)
    ctx = StrategyContext(prices=prices, params=params)
    raw_positions = strategy.generate_positions(ctx)
    positions = _align_positions(raw_positions, prices)

    asset_returns = prices.pct_change().fillna(0.0)
    # Positions decided at close t apply to return from t to t+1
    lagged_positions = positions.shift(1).fillna(0.0)
    gross_returns = (lagged_positions * asset_returns).sum(axis=1)

    turnover = lagged_positions.diff().abs().sum(axis=1).fillna(0.0)
    cost_rate = (commission_bps + slippage_bps) / 10_000.0
    costs = turnover * cost_rate
    net_returns = gross_returns - costs

    equity_curve = initial_capital * (1.0 + net_returns).cumprod()
    metrics = compute_metrics(
        net_returns,
        periods_per_year=periods_per_year,
        risk_free_rate=risk_free_rate,
    )
    metrics["turnover"] = compute_turnover(lagged_positions)
    metrics["final_equity"] = float(equity_curve.iloc[-1]) if len(equity_curve) else initial_capital

    return BacktestResult(
        equity_curve=equity_curve,
        returns=net_returns,
        positions=positions,
        metrics=metrics,
        config=cfg,
    )
