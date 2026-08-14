# Experiment Status — Zero-Block Deconstruction

## Track A — v1.1.0-final

```
STATUS: FROZEN / ACTIVE COMPETITION SUBMISSION
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
STATUS: EXECUTED — ARCHITECTURE MISMATCH — NOT PROMOTED
```

**Executed:** Yes — ran against the real 657MB competition archive.

**Finding:** `bought_deploy_txs_index.parquet` contains only the bot's 15,927 selections, not the full 411,137-deployment universe. After filtering out the bot's own deployer address, the test set had 0 positives, making evaluation impossible from that starting point alone.

**Root cause:** The full deployment universe must be reconstructed from `activity.filter(event_type == "launch")` — precisely the architecture used by v1.1.0. v1.2 requires this universe reconstruction step as a prerequisite.

**Decision:** v1.1.0 RETAINED. This is not a model quality finding — it is a data pipeline dependency that requires additional engineering before v1.2 can be fairly evaluated.

**Promotion gate result:**

| Gate | Requirement | Status |
| :--- | :--- | :---: |
| 1. PR-AUC > 0.286104 | — | ❌ Not evaluable |
| 2. Unseen-deployer PR-AUC > 0.396 | — | ❌ Not evaluable |
| 3. Recall ≥ 47.8% | — | ❌ Not evaluable |
| 4. Precision ≥ 31.7% | — | ❌ Not evaluable |
| 5. Calibration monotonic | — | ❌ Not evaluable |
| 6. Leakage = 0 | **0 violations confirmed** | ✅ |
| 7. No mock data | **Real data loaded** | ✅ |
| 8. No random labels | **Confirmed** | ✅ |

**Next step (if time permits):** Reconstruct the full 411,137-token universe from `activity.filter(event_type == "launch")`, join bot selections as labels (matching `bought_deploy_txs_index.token_address`), then re-run v1.2.

---

## Version Firewall

```
v1.1.0-final (SUBMISSION)          v1.2-competition (LAB)
        │                                   │
   NEVER TOUCH                    Requires universe reconstruction
        │                         before evaluation is possible
   Kaggle writeup                           │
   RUBRIC_COVERAGE                   NOT PROMOTED
   FINAL_RESULTS                           │
        │                              archived
        ▼
   Submit this ← kaggle_submission.zip
```

**No v1.2 result appears in the Kaggle writeup, manifest, or submission zip.**
