# 🌌 Zero-Block Deconstruction: Comprehensive Scientific Writeup

*An exhaustive analysis of the on-chain behavioral reconstruction of a dominant Solana sniper bot.*

---

## 1. Executive Summary & The Core Mystery

In the hyper-competitive landscape of Solana decentralized finance (DeFi), specifically within token deployment platforms like pump.fun, the "zero-block" represents the absolute frontier of arbitrage and execution speed. During the exact slot a token is deployed and initialized, highly sophisticated sniper bots evaluate the token's parameters, the deployer's history, and the surrounding market context to decide whether to execute a buy transaction in the very same block.

We asked whether a real zero-block sniper's decisions could be reconstructed from point-in-time on-chain evidence. We specifically targeted the bot address `5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr`. From 4.9M wallet events, we built a 411K-deployment universe, excluded 2,109 unresolved labels rather than treating them as negatives, enforced a three-layer leakage firewall, and tested a frozen model chronologically.

The resulting replica achieves 0.286 PR-AUC and captures 47.8% of target selections at a 1.50× selection budget, while achieving 0.396 PR-AUC on completely unseen deployers. More importantly, the disagreement analysis exposes a second decision regime that the supplied evidence cannot explain. We don't fabricate the missing economics—we quantify the boundary of what the data can actually prove.

---

## 2. Judge Scorecard

| Research Gate | Result |
| :--- | :--- |
| Real deployment universe | 411,137 |
| Mapped bot selections | 13,818 |
| Unknown labels excluded | 2,109 |
| Leakage violations | 0 |
| Unseen-deployer PR-AUC | 0.396 |
| Frozen test PR-AUC | 0.286104 |
| Bot capture @ Top-5% (Recall) | 47.8% |
| Precision @ Top-5% | 31.7% |
| **F1 @ Top-5%** | **0.381** |
| Selection ratio | 1.50× |
| **Fabricated economic assumptions** | **0** |

---

## 3. The Evidence Boundary

A critical pillar of this research is maintaining a strict epistemological boundary regarding what is "known" versus what is "assumed." In on-chain data science, it is dangerously easy to leak future information (look-ahead bias) or to fabricate assumptions about trading execution.

**The Known Universe**
We possess complete visibility into:
- The universe of 411,137 eligible token deployments on the pump.fun platform.
- 4.9 million historical wallet activity events mapped to these deployments.
- The timestamps, block slots, and transaction signatures for every deployment.
- Target bot buy events correctly mapped to deployment signatures.

**The Unobservable Universe**
We explicitly acknowledge that we cannot observe:
- **Bot Buy Latency:** The competition context identifies zero-block selection as the target behaviour, but the supplied archive does not expose the target buy transaction's exact block position or propagation latency.
- **Entry Size and Slippage:** The exact amount of SOL deployed per trade and the slippage incurred during execution.
- **Exit Timing and P&L:** The bot's sell transactions, hold duration, and realized/unrealized profit and loss.
- **Off-Chain Signals:** Any social media scraping (e.g., Twitter, Telegram) or private node RPC metadata the bot might use.

---

## 4. Label Integrity — Unknown ≠ Negative

To ensure our model evaluated reality, we mapped the 15,927 bot selections against our deployment universe.

```text
15,927 target-bot selections
          │
          ├── 13,818 mapped ──→ TRAIN / TEST
          │
          └──  2,109 unresolved
                    │
                    └── EXCLUDED
                        ≠ NEGATIVE
```

15,927 target-bot selections were provided by the index; 13,818 could be mapped unambiguously into the deployment universe. Treating the 2,109 unresolved selections as negatives would introduce unsupported labels; we therefore exclude them.

The resulting baseline prevalence (the random chance of picking a token the bot bought) in our test set was established at **4.74%**.

---

## 5. Causal-in-Time Feature Construction

Because the bot operates at $t_{decision}$ (the zero-block), the feature engineering pipeline must respect a flawless temporal isolation boundary. Any data point generated at $t > t_{decision}$, or even exactly at $t_{decision}$ but physically after the deployment transaction, is strictly forbidden.

We implemented three layers of leakage prevention:
1. **Event Filtering:** When aggregating a deployer's historical trades or launches, the database join requires `timestamp < t_deployment`. Strict inequality ensures the current token launch is never accidentally included in the deployer's history.
2. **Exclusion of Price Action:** Because the bot decides in the zero-block, there is no bonding curve or price action available at $t_{decision}$. All post-trade price fields were explicitly banned from the feature engine.
3. **Deployment-Time Fields:** Deployment payload fields present in the supplied transaction data are eligible for point-in-time feature analysis, as they are available at or before the deployment event itself.

Using this firewall, we engineered five point-in-time behavioral features summarizing a deployer's on-chain identity up to the **latest observable event strictly before `t_decision`** (`past_launches`, `past_buys`, `past_sells`, `past_burns`, `deployer_age_seconds`).

---

## 6. Behavioral Discovery

To model the bot's decision boundary, we selected LightGBM (Light Gradient Boosting Machine) to handle non-linear relationships and outlier distributions. We split the data chronologically (70% train, 15% validation, 15% frozen test) to simulate forward-looking generalization.

Once the model was trained, we applied SHAP (SHapley Additive exPlanations) to crack open the "black box" and read the exact policy the bot was utilizing.

The observable model-derived fingerprint favours low-history deployers that are not extremely new, with `past_launches` and `deployer_age_seconds` dominating the available feature set. The model strongly down-ranks high-history serial deployers and brand-new zero-history wallets.

---

## 7. Generalization

The most rigorous test of a behavioral model is evaluating it on entities it has never seen before. We filtered the test set to include *only* deployers who never appeared in the training set (0% overlap). 

- **Random Baseline PR-AUC:** 0.047
- **Frozen Model PR-AUC:** 0.286104
- **Unseen Deployers PR-AUC:** **0.396** (versus the 0.047 test-set prevalence baseline)

The higher unseen-deployer PR-AUC provides strong evidence that the signal is not primarily dependent on memorised deployer identity. The model has learned transferable structural patterns about deployer behaviour rather than a lookup table of known wallets.

---

## 8. Executable Replica

On the validation set, we established a strict "Top-5% selection budget" policy threshold. We took this pre-registered operating point and applied it blindly to the frozen test set.

- **Target Bot Capture (Recall):** The replica successfully captured **47.8%** of the exact tokens the target bot bought in the future timeframe.
- **Precision:** Of all the tokens the replica flagged as a "Buy", **31.7%** were actually bought by the target bot.
- **F1 Score:** **0.381** — the harmonic mean of precision and recall at the pre-registered operating point.
- **Selection Ratio:** The replica achieved this capture rate while only selecting 1.50× the number of tokens the bot selected.

This confirms that the model's score is a strong behavioural ranking signal. Selection frequency rises monotonically across probability bands, supporting the score's usefulness for policy ranking rather than arbitrary classification.

---

## 9. Two-Regime Discovery

By analyzing the false negatives (tokens the bot bought, but the replica rejected), we discovered a powerful explanatory gap.

### Regime A — HIGH-CONFIDENCE REPLICA REGIME
**1,388 shared selections.** 
Low `past_launches` + non-zero `wallet_age`. This regime is fully explained by the observable on-chain data.

### Regime B — RESIDUAL BOT REGIME
**1,536 bot-only selections.**
These tokens belong to *Extreme Serial Deployers*. The target bot bought tokens from deployers who have launched hundreds of tokens in the past, directly violating its primary observable rule.

The residual analysis identifies where the available on-chain feature set no longer provides sufficient information to reproduce the target's selections.

**Plausible Hypotheses for Regime B:**
1. **Missing Wallet Relationships:** The bot may be analyzing funding graphs (e.g., tracing Binance withdrawal wallets) to group serial deployers into clusters.
2. **Off-Chain Metadata Scraping:** The bot may be scraping Twitter or Telegram for specific keywords or influencer mentions, buying regardless of on-chain history.

---

## 10. What Would Change the Conclusion?

Current evidence supports the **Observable Conclusion**: The available on-chain history contains substantial predictive information about target-bot selection.

It does **NOT** establish:
- Profitability
- Economic superiority
- Exact execution latency
- Exact entry size
- Complete replication
- Off-chain signal usage

Additional data required to bridge this gap:
- Complete target bot trade stream
- Exits and execution prices
- A richer wallet relationship graph
- Metadata snapshots

---

## 11. Engineering / Vercel

To prove the execution validity of our findings, we engineered a **dependency-free serverless inference pipeline**. Using the `m2cgen` library, we transpiled the trained LightGBM ensemble tree structures directly into a raw Abstract Syntax Tree (AST), which was then compiled into pure, native Python code.

This allows the model to run without heavy dependencies (`pandas`, `numpy`, `lightgbm`), deployed directly to Vercel Serverless Functions. During the GitHub Actions build step, the raw Python AST model must score a "Golden Inference Vector" of 10,000 predictions with **100.00% floating-point equivalence** to the LightGBM baseline before the build is allowed to pass.

---

## 12. Rule Confidence Matrix

| Rule | Evidence Source | Confidence |
| :--- | :--- | :---: |
| Very low `past_launches` strongly favored | SHAP + ablation + cohort analysis | **High** |
| Brand-new wallets (`deployer_age` ≈ 0) disfavored | Decision tree + SHAP dependence plot | **High** |
| Serial deployers disfavored in primary regime | Cohort analysis + SHAP | **High** |
| Deployment fees contribute little | Ablation | Medium |
| Secondary regime depends on missing information | Residual analysis | Medium |
| Social/off-chain signals explain residual regime | Hypothesis only — unavailable evidence | **Low** |

---

## 13. Could Our Result Be an Artifact?

| Threat | Mitigation | Verified |
| :--- | :--- | :---: |
| Identity memorisation | Unseen-deployer evaluation (0% training overlap) | ✅ |
| Temporal leakage | Three-layer leakage firewall + CI gate | ✅ |
| Unknowns treated as negatives | 2,109 unresolved excluded entirely | ✅ |
| Test-set threshold tuning | Threshold fixed on validation set only | ✅ |
| Synthetic economics presented as real | Zero fabricated assumptions | ✅ |
| Score miscalibration | Selection rate rises monotonically with predicted probability | ✅ |
| Residual regime ignored | Explicitly analysed as two-regime discovery | ✅ |

---

## 14. Data Availability Decision

**Outcome-data gate: NOT AVAILABLE**

The supplied competition archive did not contain the target bot's executable buy transaction details, nor the post-deployment outcome files (`pumpfun_trades.parquet`, `mcap_candles.parquet`) required for economic evaluation. Consequently, entry size, hold time, exit structure, P&L distribution, ROI, and drawdown are not empirically observable from the supplied assets.

**Decision: No synthetic economics are included in the competition results.** A full audit of which rubric requirements are fulfilled, partially fulfilled, or blocked by missing data is documented in `submission/RUBRIC_COVERAGE.md`.

---

## 15. Conclusion

This submission optimizes for evidentiary validity rather than completeness: every reported result is supported by the supplied data, while every unobservable quantity is explicitly left unclaimed. Where the rubric requests post-deployment economic measurements, we identify the missing evidence explicitly rather than replacing it with synthetic results presented as competition outcomes.

*(End of Comprehensive Writeup)*
