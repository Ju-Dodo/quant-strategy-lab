import numpy as np
import pandas as pd

from qsl.backtest.metrics import compute_metrics, compute_turnover


def test_compute_metrics_positive_drift():
    idx = pd.date_range("2020-01-01", periods=252, freq="B")
    returns = pd.Series(0.001, index=idx)
    m = compute_metrics(returns)
    assert m["total_return"] > 0
    assert m["sharpe"] > 0


def test_compute_turnover():
    idx = pd.date_range("2020-01-01", periods=5, freq="B")
    positions = pd.DataFrame({"SPY": [0.0, 1.0, 1.0, 0.0, 1.0]}, index=idx)
    t = compute_turnover(positions)
    assert t > 0
