# Deploy (Rust)

Cargo workspace for live trading on [Alpaca Markets](https://alpaca.markets/).

## Layout

| Crate | Purpose |
|-------|---------|
| `crates/alpaca-broker` | Shared REST client and config |
| `crates/qsl-types` | Shared types (optional) |
| `crates/<slug>/` | One binary per promoted strategy |

## Setup

1. Copy repo-root `.env.example` to `.env` and set Alpaca keys.
2. `cd deploy && cargo build`

## Promoting a strategy

1. Meet gates in Python backtest (`strategies/<slug>/`).
2. Write `strategies/<slug>/logic.md` (deterministic rules).
3. `cargo new --bin crates/<slug>` and depend on `alpaca-broker`.
