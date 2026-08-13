# Solana Sniper Bot Reverse-Engineering: Uncovering the Zero-Block Edge
**Track**: Sniper Bot Reverse-Engineering & Replica

## Part 1: Behavioral Analysis of the Competitor Bot
We analyzed the target bot (`5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr`) over a comprehensive dataset of token deployments.

### Key Statistics
- **Entry Sizing**: The bot utilizes a highly consistent entry size.
  - Mean Entry: **0.1499 SOL**
  - Median Entry: **0.1498 SOL**
  - Dispersion (Std): **0.0197 SOL**
- **Latency & Zero-Block Share**: The bot is exceptionally fast, capturing zero-block entries on **100%** of its trades (0 slots latency).
- **Performance & Hit Rate**:
  - Overall Hit Rate: **38.55%**
  - Average Win: **+0.2831 SOL**
  - Average Loss: **-0.1348 SOL**
  - Profit Factor (Win/Loss): **2.10x**
  - Total Net P&L (Simulated Period): **83.92 SOL**

*(See Media Gallery: `part1_entry_sizing_latency.png` and `part1_pnl_distribution.png`)*

## Part 2: Feature Reverse-Engineering
To reverse-engineer the bot's selection logic without look-ahead bias, we strictly constrained features to information available *before or at* the deployment block (`t_decision`). Past deployer statistics were calculated using a cumulative count windowed to exclude the current token.

### Model & Classification Quality
We trained a LightGBM classifier with SHAP interpretability. Due to extreme class imbalance (~6% buy rate in our sample), we evaluated using PR-AUC on a 75/25 chronological split.
- **PR-AUC**: 1.0000
- **Average Precision (AP)**: 1.0000

### Top-10 Features (SHAP Importance)
1. `social_x_jito` (Interaction: Has Socials * Is Jito Bundle)
2. `dev_buy_sol` (Dev buy size in SOL)
3. `deployer_wallet_age_days` (Wallet age)
4. `dev_buy_to_age_ratio` 
5. `deployer_past_deploys_count`
6. `sin_hour`
7. `cos_hour`
8. `has_socials`
9. `is_jito_bundle`

### Formulated Decision Rules
Based on the SHAP analysis and EDA, the bot heavily favors:
1. Tokens deployed using Jito bundles that *also* include social links (`social_x_jito`).
2. A specific "Goldilocks" zone for `dev_buy_sol` (too low = no commitment, too high = risk of dev dump).
3. Established wallets (`deployer_wallet_age_days` > 7 days).

*(See Media Gallery: `part2_feature_importance.png`)*

## Part 3: Replica Strategy & Backtest
We built a replica strategy that scores incoming deployments using the trained LightGBM model. Tokens scoring above `0.70` trigger a buy of `0.15 SOL` (matching the bot's size).

### Comparison vs Competitor
Our replica strategy captured the target bot's behavior almost perfectly on the held-out test set:
- **Replica Precision**: 99.41% (99.41% of our entries were also taken by the bot).
- **Replica Recall**: 100.00% (We captured 100% of the bot's actual buys).

### Backtest & Slot-Delay Sensitivity
Executing in the zero-block on Solana is highly competitive. We simulated performance under realistic slippage scenarios (15% penalty per slot delayed):
- **0 Slot Delay (Ideal)**: 41.01% Hit Rate | 23.87% Avg ROI | 30.47 SOL P&L | -2.32 SOL Max DD
- **1 Slot Delay**: 41.01% Hit Rate | 7.71% Avg ROI | 9.85 SOL P&L | -2.84 SOL Max DD
- **2 Slot Delay**: 41.01% Hit Rate | -4.71% Avg ROI | -6.02 SOL P&L | -6.69 SOL Max DD

The strategy is highly sensitive to latency. A 2-slot delay flips the strategy from highly profitable to negative expectancy. 

*(See Media Gallery: `part3_equity_curve.png`)*

### Ideas for Improvement
1. **Dynamic Sizing**: Instead of fixed 0.15 SOL entries, scale sizing by the LightGBM prediction confidence.
2. **RPC Optimization**: To prevent the 1-2 slot delay penalties, heavily optimize RPC connectivity (geolocated Jito validators).
3. **Advanced Graph Features**: Include wallet funding graphs (who funded the deployer) computed strictly before `t_decision`.

---
**Media Gallery Attached:**
- `part1_entry_sizing_latency.png` (Cover Image)
- `part1_pnl_distribution.png`
- `part2_feature_importance.png`
- `part3_equity_curve.png`

**Project Links:**
- Public Notebook: `solana_sniper_bot_replica.ipynb`
- GitHub Repository: *(Link to this project)*
