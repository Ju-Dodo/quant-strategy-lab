from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pandas as pd
import yfinance as yf

DEFAULT_CACHE_DIR = Path("data/cache")


def _cache_key(tickers: list[str], start: str, end: str | None) -> str:
    payload = json.dumps({"tickers": sorted(tickers), "start": start, "end": end}, sort_keys=True)
    return hashlib.sha256(payload.encode()).hexdigest()[:16]


def _normalize_prices(raw: pd.DataFrame, tickers: list[str]) -> pd.DataFrame:
    if raw.empty:
        raise ValueError("No price data returned for the requested universe and date range.")

    if isinstance(raw.columns, pd.MultiIndex):
        if "Adj Close" in raw.columns.get_level_values(0):
            prices = raw["Adj Close"].copy()
        elif "Close" in raw.columns.get_level_values(0):
            prices = raw["Close"].copy()
        else:
            raise ValueError("Downloaded data missing Adj Close / Close columns.")
    else:
        col = "Adj Close" if "Adj Close" in raw.columns else "Close"
        prices = raw[[col]].copy()
        prices.columns = [tickers[0]]

    prices.index = pd.to_datetime(prices.index)
    prices = prices.sort_index()
    return prices.astype(float)


def load_prices(
    tickers: list[str],
    start: str,
    end: str | None = None,
    *,
    cache_dir: Path | str | None = DEFAULT_CACHE_DIR,
    use_cache: bool = True,
) -> pd.DataFrame:
    """Load adjusted close prices for tickers, with optional disk cache."""
    if not tickers:
        raise ValueError("tickers must be a non-empty list")

    cache_path: Path | None = None
    if cache_dir is not None and use_cache:
        cache_root = Path(cache_dir)
        cache_root.mkdir(parents=True, exist_ok=True)
        cache_path = cache_root / f"prices_{_cache_key(tickers, start, end)}.csv"
        if cache_path.exists():
            return pd.read_csv(cache_path, index_col=0, parse_dates=True)

    raw = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
        group_by="column",
    )
    prices = _normalize_prices(raw, tickers)

    if cache_path is not None:
        prices.to_csv(cache_path)

    return prices
