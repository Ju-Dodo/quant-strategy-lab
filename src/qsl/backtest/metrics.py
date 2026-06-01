from __future__ import annotations

import numpy as np
import pandas as pd


def compute_metrics(
    returns: pd.Series,
    *,
    periods_per_year: int = 252,
    risk_free_rate: float = 0.0,
) -> dict[str, float]:
    """Compute standard performance metrics from a return series."""
    r = returns.dropna()
    if r.empty:
        return {
            "cagr": 0.0,
            "sharpe": 0.0,
            "sortino": 0.0,
            "max_drawdown": 0.0,
            "volatility": 0.0,
            "total_return": 0.0,
        }

    equity = (1.0 + r).cumprod()
    total_return = float(equity.iloc[-1] - 1.0)
    n_years = len(r) / periods_per_year
    cagr = float(equity.iloc[-1] ** (1.0 / n_years) - 1.0) if n_years > 0 else 0.0

    excess = r - risk_free_rate / periods_per_year
    vol = float(r.std(ddof=0) * np.sqrt(periods_per_year))
    sharpe = float(excess.mean() / r.std(ddof=0) * np.sqrt(periods_per_year)) if r.std(ddof=0) > 0 else 0.0

    downside = r[r < 0]
    downside_std = downside.std(ddof=0) if len(downside) > 0 else 0.0
    sortino = (
        float(excess.mean() / downside_std * np.sqrt(periods_per_year)) if downside_std > 0 else 0.0
    )

    running_max = equity.cummax()
    drawdown = equity / running_max - 1.0
    max_drawdown = float(drawdown.min())

    return {
        "cagr": cagr,
        "sharpe": sharpe,
        "sortino": sortino,
        "max_drawdown": max_drawdown,
        "volatility": vol,
        "total_return": total_return,
    }


def compute_turnover(positions: pd.DataFrame) -> float:
    """Average daily absolute change in position weights."""
    if positions.empty or len(positions) < 2:
        return 0.0
    delta = positions.diff().abs().sum(axis=1)
    return float(delta.mean())
