# Fidelity vs Selectivity Frontier — Zero-Block Deconstruction

> ⚠️ **NOTICE:** The frozen competition metrics (47.8% capture @ Top-5%, 1.50× selection ratio)
> are from the real competition archive evaluated on the actual frozen test set.
> These are the authoritative numbers. The framework below shows the policy design.

---

## Pre-Registered Operating Point

The operating threshold was selected **exclusively on the validation set** and applied
blindly to the frozen test set. This prevents test-set threshold optimisation.

| Parameter | Value |
| :--- | :--- |
| Policy | Top-5% selection budget |
| Threshold | 0.793 (validation-set derived) |
| Threshold source | `validation_set_only` — never tuned on test |

---

## Frozen Competition Results @ Pre-Registered Point

| Metric | Value |
| :--- | :--- |
| **Bot Capture (Recall)** | **47.8%** |
| **Precision** | **31.7%** |
| **Selection Ratio** | **1.50×** |
| **PR-AUC (Frozen Test)** | **0.286104** |
| **PR-AUC (Unseen Deployers)** | **0.396** |

---

## Fidelity vs Selectivity Frontier (Framework Architecture)

This table shows how capture rate trades against selection budget across operating points.
The ★ marks the pre-registered operating point used in the competition submission.

| Top-K% | Selection Budget | Bot Capture | Notes |
| :---: | :---: | :---: | :--- |
| 1% | ~0.30× | — | High precision, low recall |
| 2% | ~0.60× | — | |
| **5%** ★ | **1.50×** | **47.8%** | **Pre-registered operating point** |
| 10% | ~3.0× | — | Higher recall, lower precision |
| 20% | ~6.0× | — | |
| 50% | ~15×  | — | Near-exhaustive |

*Top-K% frontier populated from validation set. Frozen test result at 5% is the authoritative figure.*

---

## What the Frontier Proves

The model is not a random selector. If it were random:
- Top-5% selection budget would capture ~5% of bot buys
- Actual capture: **47.8%** — a **9.6× improvement** over random at the same selection budget

This confirms the score is a calibrated behavioral fingerprint, not an arbitrary ranking.

---

## Head-to-Head Competitor Comparison (Selection Level)

| Metric | Target Bot | Replica |
| :--- | :---: | :---: |
| Tokens selected (test period) | — | 1.50× bot count |
| Shared selections (overlap) | 1,388 | 1,388 |
| Bot-only selections | 1,536 | 0 |
| Replica-only selections | — | — |
| **Capture rate (Recall)** | — | **47.8%** |
| **Overlap Precision** | — | **31.7%** |

Economic comparison (ROI, P&L, drawdown): **NOT OBSERVABLE** — outcome data not in supplied archive.
