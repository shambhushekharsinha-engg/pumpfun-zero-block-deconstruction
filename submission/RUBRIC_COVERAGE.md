# Rubric Coverage Matrix — Zero-Block Deconstruction

## Data Availability Decision

> **Outcome-data gate: NOT AVAILABLE**
>
> The supplied competition archive available to this project did not contain the post-deployment
> outcome files referenced by the rubric (`pumpfun_trades.parquet`, `mcap_candles.parquet`).
> Consequently, the corresponding economic metrics are not empirically observable from the supplied assets.
>
> **Decision: No synthetic economics are included in the competition results.**

---

## What the Missing Data Prevents vs. What We Can Establish

```text
AVAILABLE (Supplied Archive)
    ↓
bought_deploy_txs_index.parquet
bought_deployers_activity.parquet
deploy_txs.jsonl
    ↓
Decision reconstruction
    ↓
PR-AUC / Recall / Precision
    ↓
Replica selection efficiency
Unseen-deployer generalization
Two-regime discovery

─────────────────────────────────────────

MISSING (Not in supplied archive)
    ↓
pumpfun_trades.parquet / mcap_candles.parquet
    ↓
Exact execution price at entry
Exit timing and sell structure
Hold time distribution
Per-trade ROI
Cumulative P&L
Max drawdown
Head-to-head economic comparison
```

---

## Rubric Coverage Table

| Rubric | Requirement | Evidence / Artifact | Status | Limitation |
| :--- | :--- | :--- | :---: | :--- |
| **Part 1** | Entry size (mean/median/dispersion) | `OBSERVABILITY.md` | ⚠️ | Bot buy tx size absent from supplied archive |
| **Part 1** | Latency in slots/seconds | Phase 2A analysis | ⚠️ | Separate bot buy tx timestamps absent |
| **Part 1** | Zero-block share | Phase 2A analysis | ⚠️ | Requires bot buy tx with slot reference |
| **Part 1** | In-block position | `OBSERVABILITY.md` | ⚠️ | Requires full block tx ordering data |
| **Part 1** | Hold time / exit structure | `OBSERVABILITY.md` | ❌ | No bot sell history in supplied archive |
| **Part 1** | Hit rate / win-loss | `OBSERVABILITY.md` | ❌ | Requires exit prices (not supplied) |
| **Part 1** | P&L distribution | `OBSERVABILITY.md` | ❌ | No complete exit/trade stream supplied |
| **Part 2** | Point-in-time features (t_decision firewall) | `features_v1` / leakage gate | ✅ | — |
| **Part 2** | No post-deployment data in features | Three-layer leakage firewall | ✅ | — |
| **Part 2** | Interpretable model | LightGBM | ✅ | — |
| **Part 2** | Top-10 features by importance | SHAP values + decision tree | ✅ | — |
| **Part 2** | Hypothesized bot decision rules | Two-regime analysis | ✅ | — |
| **Part 2** | Time-based train/test split | Chronological 70/15/15 | ✅ | — |
| **Classification** | Precision | `final_metrics` | ✅ | 31.7% @ Top-5% |
| **Classification** | Recall | `final_metrics` | ✅ | 47.8% @ Top-5% |
| **Classification** | F1 | `final_metrics` | ✅ | Computed on frozen test set |
| **Classification** | PR-AUC | `final_metrics` | ✅ | 0.286 frozen / 0.396 unseen deployers |
| **Classification** | Correct imbalance handling | PR-AUC primary metric | ✅ | — |
| **Part 3** | Replica scoring model / entry rules | Frozen Top-5% policy | ✅ | — |
| **Part 3** | Entry feasibility assessment | Evidence boundary documented | ✅ | Economic outcome unavailable |
| **Part 3** | 0/1/2-slot delay sensitivity (economics) | — | ⚠️ | Required market/price data absent |
| **Part 3** | ROI / hit rate / max drawdown / total P&L | — | ⚠️ | Required outcome data not supplied |
| **Competitor** | Token selection overlap (precision/recall) | Counterfactual analysis | ✅ | 1,388 shared / 1,536 bot-only |
| **Competitor** | Selection ratio | `final_metrics` | ✅ | 1.50× |
| **Competitor** | P&L / hit rate / drawdown comparison | — | ⚠️ | Required outcome data not supplied |
| **Reproducibility** | Public notebook | CI + notebook | ✅ | — |
| **Reproducibility** | Repository with setup instructions | GitHub | ✅ | — |
| **Reproducibility** | t_decision truncation explicitly enforced | Leakage gate + tests | ✅ | — |
| **Reproducibility** | Metrics recomputable by judges | Golden inference vector | ✅ | 100% floating-point equivalence |
| **Integrity** | No fabricated economic assumptions | `REPRODUCTION_CONTRACT.md` | ✅ | Fabricated economic assumptions: 0 |
| **Required** | Writeup under 3,000 words | `Kaggle_Writeup.md` | ✅ | ~650 words |
| **Required** | Cover image | `project_logo.png` | ✅ | — |
| **Required** | Public notebook attached | GitHub repo | ✅ | — |
| **Required** | Repository link | GitHub | ✅ | — |

---

## Legend

| Symbol | Meaning |
| :---: | :--- |
| ✅ | Fully satisfied by supplied evidence |
| ⚠️ | Partially satisfied — specific limitation documented above |
| ❌ | Not observable from supplied competition assets |

---

## Scientific Integrity Statement

Every ✅ result in this matrix is directly supported by the supplied competition data.
Every ⚠️ and ❌ entry reflects an explicit, deliberate decision not to fabricate the missing evidence.

This submission optimizes for evidentiary validity: every reported result is supported by the supplied data, while every unobservable quantity is explicitly left unclaimed.
