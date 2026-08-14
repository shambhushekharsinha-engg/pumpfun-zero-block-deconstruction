# Final Frozen Results — v1.1.0-final

> ⚠️ These results are frozen. The model, threshold, and test set are locked.

## Scientific Checkpoint

| Metric | Value |
|:---|:---:|
| Dataset: Total eligible deployments | 411,137 |
| Dataset: Mapped positive labels | 13,818 |
| Dataset: Unknown labels excluded | 2,109 |
| Dataset: Confirmed negative labels | 395,210 |
| Features | 5 (point-in-time) |
| Model | LightGBM |
| Split | Chronological 70/15/15 |
| Threshold source | Validation set only |
| Leakage violations | 0 |
| **Frozen test PR-AUC** | **0.286104** |
| **Unseen-deployer PR-AUC** | **0.396** |
| **Bot capture @ Top-5%** | **47.8%** |
| **Precision @ Top-5%** | **31.7%** |
| **Selection ratio** | **1.50×** |
| Fabricated economic assumptions | 0 |

## Economic Backtest

| Metric | Status |
|:---|:---:|
| Entry size | NOT OBSERVABLE |
| Hold time | NOT OBSERVABLE |
| Exit structure | NOT OBSERVABLE |
| P&L distribution | NOT OBSERVABLE |
| ROI | NOT OBSERVABLE |
| Max drawdown | NOT OBSERVABLE |

Reason: The supplied competition archive did not contain pumpfun_trades.parquet or mcap_candles.parquet.
