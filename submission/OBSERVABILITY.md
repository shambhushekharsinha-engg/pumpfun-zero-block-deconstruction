# Observability Manifest — Zero-Block Deconstruction

## Data Availability Gate

Outcome-data gate: NOT AVAILABLE

The supplied competition archive did not contain:
- `pumpfun_trades.parquet` — required for entry size, latency, hold time, P&L
- `mcap_candles.parquet` — required for market prices and ROI calculation

Decision: No synthetic economics are included in the competition results.

## Observability Matrix

| Metric | Observable? | Reason |
|:---|:---:|:---|
| Deployment event timestamps | ✅ Yes | In bought_deploy_txs_index.parquet |
| Deployer historical activity | ✅ Yes | In bought_deployers_activity.parquet |
| Bot selection labels | ✅ Yes | In bought_deploy_txs_index.parquet |
| Point-in-time behavioral features | ✅ Yes | Derived at t_decision |
| Target bot buy entry size | ❌ No | Bot buy tx details absent |
| Target bot buy latency (slots) | ❌ No | Bot buy tx absent |
| Zero-block entry position | ❌ No | Requires full block tx ordering |
| Bot exit/sell transactions | ❌ No | Not in supplied archive |
| Hold time per token | ❌ No | No sell data |
| Per-trade ROI | ❌ No | No execution prices |
| Realized P&L | ❌ No | No exit prices |
| Max drawdown | ❌ No | No trade stream |
