# Experiment Status — Zero-Block Deconstruction

## Track A — v1.1.0-final

```
STATUS: FROZEN / COMPETITION SUBMISSION CANDIDATE
```

| Metric | Value |
| :--- | :---: |
| PR-AUC (frozen test) | **0.286104** |
| PR-AUC (unseen deployers) | **0.396** |
| Recall @ Top-5% | **47.8%** |
| Precision @ Top-5% | **31.7%** |
| Selection ratio | **1.50×** |
| Leakage violations | **0** |
| Fabricated economic assumptions | **0** |

**DO NOT MODIFY.** This is the active Kaggle submission.
Model, threshold (0.793), feature set, and test metrics are all frozen.

---

## Track B — v1.2-competition

```
STATUS: EXPERIMENTAL / NOT PROMOTED
```

**Reason:** No executed real-data result has yet demonstrated improvement over the frozen v1.1.0 baseline.

The script `submission/src/v12_enhanced_feature_engine.py` is real-schema-valid and requires the full competition archive. It will not produce output without real data and contains no mock fallbacks.

**Promotion gate (all conditions must hold to replace v1.1.0):**

| Gate | Requirement | Status |
| :--- | :--- | :---: |
| 1. PR-AUC | > 0.286104 | ⏳ Pending |
| 2. Unseen-deployer PR-AUC | > 0.396 | ⏳ Pending |
| 3. Recall | ≥ 47.8% OR justified tradeoff documented | ⏳ Pending |
| 4. Precision | ≥ 31.7% OR justified tradeoff documented | ⏳ Pending |
| 5. Calibration | Monotonic selection-rate bands | ⏳ Pending |
| 6. Temporal stability | No regression in chronological eval | ⏳ Pending |
| 7. Leakage violations | 0 | ⏳ Pending |
| 8. Feature provenance | All source events < t_decision asserted | ⏳ Pending |

Until all gates are verified with real-data output, **v1.1.0 remains the competition submission.**

---

## Version Firewall

```
v1.1.0-final (submission)          v1.2-competition (lab)
        │                                   │
   NEVER TOUCH                    Run against real archive
        │                                   │
   Kaggle writeup                  Compare all 8 gates
   RUBRIC_COVERAGE                          │
   FINAL_RESULTS                    PASS → candidate
        │                           FAIL → archive
        ▼                                   │
   Submit this                      archive/
```

**Any result from Track B MUST NOT appear in the Kaggle writeup, manifest, or submission zip unless all 8 promotion gates pass.**
