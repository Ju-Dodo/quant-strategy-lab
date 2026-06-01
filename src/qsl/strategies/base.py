from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

import pandas as pd


@dataclass
class StrategyContext:
    """Aligned market data and backtest parameters for a strategy."""

    prices: pd.DataFrame
    volumes: pd.DataFrame | None = None
    params: dict[str, Any] | None = None


class Strategy(ABC):
    """Strategy contract: map context to target position weights."""

    @abstractmethod
    def generate_positions(self, ctx: StrategyContext) -> pd.DataFrame:
        """
        Return a DataFrame of position weights aligned to ctx.prices.index/columns.

        Values are fractions of portfolio (e.g. 1.0 = 100% long that asset).
        Use 0 for flat; negative for short if supported by the backtest config.
        """
