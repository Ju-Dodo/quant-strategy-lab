#!/usr/bin/env python3
"""Scaffold a new strategy folder under strategies/<slug>/."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
STRATEGIES_DIR = REPO_ROOT / "strategies"

SLUG_RE = re.compile(r"^[a-z][a-z0-9_]*$")

CONFIG_YAML = """tickers:
  - SPY
start: "2015-01-01"
end: null
initial_capital: 100000
commission_bps: 1.0
slippage_bps: 1.0
periods_per_year: 252
risk_free_rate: 0.0
cache_dir: data/cache
params: {}
"""

STRATEGY_PY = '''"""{title} strategy implementation."""

from __future__ import annotations

import pandas as pd

from qsl.indicators import simple_moving_average
from qsl.strategies.base import Strategy, StrategyContext


class {class_name}Strategy(Strategy):
    """Placeholder: replace with rules from references/ and README."""

    def generate_positions(self, ctx: StrategyContext) -> pd.DataFrame:
        params = ctx.params or {{}}
        fast = int(params.get("fast_window", 20))
        slow = int(params.get("slow_window", 50))
        ticker = ctx.prices.columns[0]
        close = ctx.prices[ticker]
        fast_ma = simple_moving_average(close, fast)
        slow_ma = simple_moving_average(close, slow)
        long_signal = (fast_ma > slow_ma).astype(float)
        positions = pd.DataFrame({{ticker: long_signal}}, index=ctx.prices.index)
        return positions.fillna(0.0)
'''

RUN_BACKTEST_PY = '''#!/usr/bin/env python3
"""Run backtest for {slug} strategy."""

import sys
from pathlib import Path

STRATEGY_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(STRATEGY_DIR))

from qsl.backtest import run_backtest
from qsl.reporting import save_backtest_results

from strategy import {class_name}Strategy

REPO_ROOT = STRATEGY_DIR.parents[1]


def main() -> None:
    config_path = STRATEGY_DIR / "config.yaml"
    results_dir = STRATEGY_DIR / "results"
    strategy = {class_name}Strategy()
    result = run_backtest(strategy, config_path, repo_root=REPO_ROOT)
    summary = save_backtest_results(result, results_dir)
    print("Metrics:", result.metrics)
    print("Summary written to", summary)


if __name__ == "__main__":
    main()
'''

README_MD = """# {title}

## Status

`research`

## Thesis

<!-- Summarize the academic idea and link to references/ -->

## Signal rules

<!-- Plain English + mapping to strategy.py -->

## Universe and data

<!-- Tickers, frequency, adjustments — see config.yaml -->

## Backtest configuration

See [config.yaml](config.yaml).

## Results

<!-- Paste key metrics after running run_backtest.py; full output in results/ -->

## Promotion

When promoted to live trading:

1. Add `logic.md` with deterministic rules for the Rust port
2. Implement `deploy/crates/{slug}/`
3. Update status to `promoted` and link deployment notes here
"""


def slug_to_class_name(slug: str) -> str:
    return "".join(part.capitalize() for part in slug.split("_"))


def slug_to_title(slug: str) -> str:
    return slug.replace("_", " ").title()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new strategy scaffold")
    parser.add_argument("slug", help="snake_case strategy name, e.g. momentum_12_1")
    args = parser.parse_args()
    slug: str = args.slug

    if not SLUG_RE.match(slug):
        print("slug must be snake_case (lowercase letters, digits, underscores)", file=sys.stderr)
        return 1

    strategy_dir = STRATEGIES_DIR / slug
    if strategy_dir.exists():
        print(f"already exists: {strategy_dir}", file=sys.stderr)
        return 1

    class_name = slug_to_class_name(slug)
    title = slug_to_title(slug)

    (strategy_dir / "references").mkdir(parents=True)
    (strategy_dir / "notebooks").mkdir(exist_ok=True)
    (strategy_dir / "results").mkdir(exist_ok=True)

    (strategy_dir / "config.yaml").write_text(CONFIG_YAML)
    (strategy_dir / "strategy.py").write_text(
        STRATEGY_PY.format(title=title, class_name=class_name)
    )
    (strategy_dir / "run_backtest.py").write_text(
        RUN_BACKTEST_PY.format(slug=slug, class_name=class_name)
    )
    (strategy_dir / "README.md").write_text(README_MD.format(title=title, slug=slug))

    print(f"Created {strategy_dir}")
    print("Next: add paper to references/, edit README.md and strategy.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
