# Reproduction Contract

This project adheres to a strict scientific reproduction contract to guarantee that the results presented are legitimate, leakage-free, and empirically sound.

## The Reproduction Pipeline

```text
INPUT
  ↓
data/raw/
  ↓
Universe construction
  ↓
Causal feature generation
  ↓
Leakage validation
  ↓
Chronological split
  ↓
Model training
  ↓
Validation threshold selection
  ↓
Frozen test evaluation
  ↓
Figures / tables
```

## Immutable Rules of Engagement

The following actions are **NEVER ALLOWED** within this project's pipeline:

1. **Modifying raw data:** The contents of `data/raw/` are immutable and treated as frozen cryptographic evidence.
2. **Using future events:** Features must only be aggregated from data where $t_{event} < t_{decision}$.
3. **Tuning on Test:** The chronological test set is evaluated exactly once. It is never used for threshold selection, model selection, or feature engineering.
4. **Treating unknown targets as negatives:** The 2,109 target-bot selections that could not be mapped to the universe are treated as `UNKNOWN` and withheld, never silently converted to negatives.
5. **Fabricating P&L:** Economic outcomes (entry/exit prices, slippage, latency) are unobservable in the dataset and are never fabricated or synthetically modeled.
6. **Changing the Pre-Registered Policy:** The Top-5% operating policy was selected on the validation set and locked prior to final test evaluation. It is never retroactively adjusted to improve the test score.

## Reproduction Guarantee
Any execution of Phase 8 (Fresh Runtime Verification) against the frozen raw dataset will yield the exact analytical conclusions, behavioral fingerprints, and performance metrics (within floating-point determinism) as presented in the final submission.
