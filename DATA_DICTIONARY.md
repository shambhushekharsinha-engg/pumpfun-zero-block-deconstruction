# Data Dictionary

This document represents the Phase 1 read-only schema audit of the real Kaggle dataset files.

## 1. `bought_deploy_txs_index.parquet`
Target bot's positive label universe (Tokens it actually bought).
- **Rows**: 15,927

| Field | Meaning | Type | Nulls | Time Semantics | Usable? |
|-------|---------|------|-------|----------------|---------|
| `tx_hash` | Transaction signature | String | 0% | Fixed at deployment | ✅ |
| `line_number` | Pointer to JSONL file | Int64 | 0% | N/A | ✅ |
| `blockTime` | Unix timestamp | Int64 | 0% | `t_deployment` | ✅ |
| `blockSlot` | Solana slot number | Int64 | 0% | `t_decision` | ✅ |
| `token_address` | Mint address | String | 0% | N/A | ✅ |
| `tx_signer` | Deployer's wallet address | String | 0% | N/A | ✅ |
| `creator_address` | Alternate creator field | String | 99.99% | N/A | ❌ |

## 2. `deploy_txs.jsonl`
Deep transaction payloads for the 15,927 bought deployments.
- **Rows**: 15,927 (Matches index)

| Field | Meaning | Type | Time Semantics | Usable? |
|-------|---------|------|----------------|---------|
| `blockTime` | Unix timestamp | Int | `t_deployment` | ✅ |
| `slot` | Solana slot number | Int | `t_decision` | ✅ |
| `meta` | tx metadata (fees, CUs, inner ix) | Dict | Available at `t_decision` | ✅ |
| `transaction` | Full tx payload (Jito tip, instructions) | Dict | Available at `t_decision` | ✅ |

## 3. `bought_deployers_activity.parquet`
Historical activity and trades for the deployers who launched the 16k bought tokens. Contains 411,137 token `launch` events out of ~4.9M total rows.
- **Rows**: 4,912,125

| Field | Meaning | Type | Nulls | Time Semantics | Usable? |
|-------|---------|------|-------|----------------|---------|
| `wallet` | Deployer address | String | 0% | N/A | ✅ |
| `event_type` | Action (launch, buy, sell, burn) | String | 0% | Event time | ✅ |
| `timestamp` | Unix time of event | Int64 | 0% | `t_activity` | ✅ |
| `tx_hash` | Transaction signature | String | 0% | Event time | ✅ |
| `token_address` | Token involved | String | 0% | N/A | ✅ |
| `price_usd` / `cost_usd` | Market price data | String | ~0% | Post-deployment | ⚠️ (Only for outcomes/P&L) |
| `priority_fee` / `tip_fee`| Tx fee data | String | ~0% | Event time | ✅ |

### Universe Discovery
The target positives are the 15,927 tokens in `bought_deploy_txs_index`. The universe of *candidates* (negatives) must be derived from the 411,137 `launch` events in `bought_deployers_activity.parquet` that were NOT bought by the bot. This gives us ~411k negative samples for training, which is less than the ~5M assumed initially, but perfectly maps the domain of these specific deployers.
