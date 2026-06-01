from __future__ import annotations

import pandas as pd


def simple_moving_average(series: pd.Series, window: int) -> pd.Series:
    if window < 1:
        raise ValueError("window must be >= 1")
    return series.rolling(window=window, min_periods=window).mean()


def momentum(series: pd.Series, lookback: int) -> pd.Series:
    if lookback < 1:
        raise ValueError("lookback must be >= 1")
    return series / series.shift(lookback) - 1.0
