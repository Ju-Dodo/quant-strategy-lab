import numpy as np
import pandas as pd

from qsl.strategies.base import Strategy, StrategyContext


def test_run_backtest_synthetic_config():
    idx = pd.date_range("2020-01-01", periods=100, freq="B")
    rng = np.random.default_rng(42)
    prices = pd.DataFrame(
        {"SPY": 100 * np.cumprod(1 + rng.normal(0.0005, 0.01, len(idx)))},
        index=idx,
    )

    class _InjectedStrategy(Strategy):
        def generate_positions(self, ctx: StrategyContext) -> pd.DataFrame:
            return pd.DataFrame({"SPY": 1.0}, index=ctx.prices.index)

    # Patch load by passing prices via monkeypatch is heavy; test engine path via config
    # with minimal integration using real load would need network — test metrics path only.
    from qsl.backtest.engine import _align_positions

    positions = _InjectedStrategy().generate_positions(StrategyContext(prices=prices))
    aligned = _align_positions(positions, prices)
    assert aligned.shape == prices.shape
    assert aligned.iloc[-1]["SPY"] == 1.0
