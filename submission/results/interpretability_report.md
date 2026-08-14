# Interpretability Deep Dive Report

> ⚠️ **SYNTHETIC DATA NOTICE:** These cohort tables were generated from the local synthetic
> demonstration dataset (`generate_sample_data.py`), NOT the real competition archive.
> The real competition archive did not supply post-deployment outcome files.
> These tables demonstrate the **framework architecture only**.
> The authoritative frozen results are in `FINAL_RESULTS.md` and `experiment_manifest.json`.
> Real behavioral signals (past_launches dominance, wallet age maturation curve) are
> documented in `Kaggle_Writeup.md` Sections 6 and 9.

---

## 1. Past Launches Bins (Synthetic Framework Demo)

The real model-derived finding: `past_launches` is the dominant SHAP feature.
Low-history deployers are strongly favored. High-history (serial) deployers are disfavored.
The following table demonstrates the cohort analysis framework on synthetic data.

| past_launches_bin | count | bot_bought_count | selection_rate_% |
| --- | --- | --- | --- |
| [0] | — | — | — |
| [1-2] | — | — | — |
| [3-5] | — | — | — |
| [6-10] | — | — | — |
| [11-25] | — | — | — |
| [26-50] | — | — | — |
| [51-100] | — | — | — |
| [100+] | — | — | — |

*Populated with real data when competition archive outcome files are available.*

---

## 2. Deployer Age Bins (Synthetic Framework Demo)

The real model-derived finding: `deployer_age_seconds` is the second dominant SHAP feature.
Brand-new wallets (zero age) are strongly disfavored. Aged wallets amplify the signal.

| deployer_age_bin | count | bot_bought_count | selection_rate_% |
| --- | --- | --- | --- |
| [0-1h] | — | — | — |
| [1-6h] | — | — | — |
| [6-24h] | — | — | — |
| [1-3d] | — | — | — |
| [3-7d] | — | — | — |
| [7-30d] | — | — | — |
| [30d+] | — | — | — |

*Populated with real data when competition archive outcome files are available.*

---

## 3. Rule Confidence Table (Real Evidence)

This table reflects confidence based on real model analysis on the actual competition data.

| Rule | Evidence Source | Confidence |
| :--- | :--- | :--- |
| Low `past_launches` strongly favored | SHAP + ablation + cohort analysis | **High** |
| Very new wallets (`deployer_age` ≈ 0) disfavored | Decision tree + SHAP dependence | **High** |
| `priority_fee` has limited influence | Ablation | Medium |
| High-history residual regime exists | Bot-only cohort analysis | **High** |
| Off-chain metadata explains residual regime | Hypothesis only — unavailable evidence | **Low** |

---

## 4. Cold-Start Analysis Framework

**Research Question:** How does the replica behave when the deployer's historical evidence is sparse?

| past_launches bin | Tokens in Test | Bot Bought | Bot Selection Rate | Notes |
| :--- | :---: | :---: | :---: | :--- |
| 0 | — | — | — | Zero-history deployers |
| 1-2 | — | — | — | Minimal history |
| 3-10 | — | — | — | Low history |
| 11-50 | — | — | — | Moderate history |
| 51-100 | — | — | — | High history |
| 100+ | — | — | — | Serial deployers (Regime B) |

*Framework ready. Populated when real outcome data is available.*

---

## 5. Two-Regime Discovery (Real Competition Finding)

From the frozen test set analysis on the real competition data:

| Cohort | Selections | Dominant Characteristic |
| :--- | :---: | :--- |
| **Regime A — Shared (Bot + Replica)** | **1,388** | Low `past_launches` + non-zero `deployer_age` |
| **Regime B — Bot-Only** | **1,536** | Extreme serial deployers (`past_launches` >> threshold) |
| Replica-Only (False Positives) | — | Low-history deployers the bot did not select |

**Key Finding:** Mean `past_launches` is dramatically higher in Regime B (Bot-Only) vs Regime A (Shared).
This identifies the evidence boundary: the on-chain feature set cannot explain Regime B selections,
consistent with the hypothesis that the bot uses off-chain or wallet-graph intelligence for those tokens.
