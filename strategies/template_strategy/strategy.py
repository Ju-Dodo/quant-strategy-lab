"""Gamma Cirques strategy — replace placeholder logic with paper rules."""

from __future__ import annotations

import pandas as pd

from qsl.indicators import simple_moving_average
from qsl.strategies.base import Strategy, StrategyContext


class GammaCirquesStrategy(Strategy):
    """
    Placeholder: dual moving-average long-only on first ticker.

    Update generate_positions once the GResearch Gamma Cirques rules are encoded.
    """

    def generate_positions(self, ctx: StrategyContext) -> pd.DataFrame:
        params = ctx.params or {}
        fast = int(params.get("fast_window", 20))
        slow = int(params.get("slow_window", 50))
        ticker = ctx.prices.columns[0]
        close = ctx.prices[ticker]
        fast_ma = simple_moving_average(close, fast)
        slow_ma = simple_moving_average(close, slow)
        long_signal = (fast_ma > slow_ma).astype(float)
        positions = pd.DataFrame({ticker: long_signal}, index=ctx.prices.index)
        return positions.fillna(0.0)
