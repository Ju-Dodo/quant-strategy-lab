import importlib.util
import sys
from pathlib import Path

import pandas as pd

from qsl.strategies.base import Strategy, StrategyContext

REPO_ROOT = Path(__file__).resolve().parents[2]
STRATEGY_DIR = REPO_ROOT / "strategies" / "gamma_cirques"


def _load_strategy_class():
    spec = importlib.util.spec_from_file_location("gamma_strategy", STRATEGY_DIR / "strategy.py")
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module.GammaCirquesStrategy


def test_gamma_cirques_positions_shape():
    idx = pd.date_range("2019-01-01", periods=120, freq="B")
    prices = pd.DataFrame({"SPY": range(100, 220)}, index=idx, dtype=float)
    strategy = _load_strategy_class()()
    positions = strategy.generate_positions(
        StrategyContext(prices=prices, params={"fast_window": 10, "slow_window": 30})
    )
    assert positions.shape == prices.shape
    assert positions.min().min() >= 0.0
    assert positions.max().max() <= 1.0
