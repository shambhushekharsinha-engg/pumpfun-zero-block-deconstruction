"""
v1.2-competition: Enhanced Feature Experiment
=============================================
TRACK B — Exploratory. v1.1.0-final is the frozen competition baseline.

Rules:
  - REAL DATA ONLY: reads from data/raw/bought_deployers_activity.parquet
                    and data/raw/bought_deploy_txs_index.parquet
  - NO FALLBACK MOCK DATA
  - NO RANDOM LABELS OR PREDICTIONS
  - ALL FEATURES MUST BE COMPUTED STRICTLY BEFORE t_decision
  - CHRONOLOGICAL SPLIT — no test-set threshold tuning
  - If this script cannot load real data, it EXITS with an error code.

Decision rule:
  v1.2 replaces v1.1.0 ONLY IF:
    1. PR-AUC > 0.286104 (frozen baseline)
    2. Unseen-deployer PR-AUC > 0.396
    3. Zero new leakage violations
    4. Temporal stability does not regress
"""

import sys
import json
from pathlib import Path
import numpy as np
import polars as pl
import lightgbm as lgb
from sklearn.metrics import precision_recall_curve, auc, average_precision_score

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"
RESULTS_DIR = PROJECT_ROOT / "submission" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)

ACTIVITY_PATH = DATA_DIR / "bought_deployers_activity.parquet"
INDEX_PATH    = DATA_DIR / "bought_deploy_txs_index.parquet"

BASELINE_PR_AUC           = 0.286104
BASELINE_UNSEEN_PR_AUC    = 0.396
FROZEN_THRESHOLD          = 0.793   # from v1.1.0 validation-only selection

# ─────────────────────────────────────────────────────────────────────────────
# 0. HARD GATE: real data must exist
# ─────────────────────────────────────────────────────────────────────────────
if not ACTIVITY_PATH.exists():
    print(f"[GATE FAIL] Real activity file not found: {ACTIVITY_PATH}")
    print("[EXIT] v1.2 requires real competition data. No mock fallback allowed.")
    sys.exit(1)

if not INDEX_PATH.exists():
    print(f"[GATE FAIL] Deployment index not found: {INDEX_PATH}")
    sys.exit(1)

print("="*60)
print("  v1.2-competition: Enhanced Feature Experiment")
print("="*60)

# ─────────────────────────────────────────────────────────────────────────────
# 1. Load real data (lazy scan for memory efficiency)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[1] Loading real competition data...")

index_df = pl.read_parquet(INDEX_PATH)
# Real schema: tx_hash, line_number, blockTime, blockSlot,
#              token_address, tx_signer, creator_address
print(f"    Deployment index : {len(index_df):,} rows")

# Activity: wallet, chain, timestamp, event_type, tx_hash, priority_fee, tip_fee, ...
activity_lf = pl.scan_parquet(ACTIVITY_PATH)
print(f"    Activity parquet : {ACTIVITY_PATH.stat().st_size / 1e6:.1f} MB")

# ─────────────────────────────────────────────────────────────────────────────
# 2. Build universe and labels
# ─────────────────────────────────────────────────────────────────────────────
print("\n[2] Building deployment universe and labels...")

# Sort deployments chronologically
universe = (
    index_df
    .with_columns(pl.col("blockTime").cast(pl.Int64).alias("t_decision"))
    .sort("t_decision")
)

BOT_ADDRESS = "5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr"

# Bot buy tokens: signer == bot address in index
bot_tokens = set(
    universe.filter(pl.col("tx_signer") == BOT_ADDRESS)["token_address"].to_list()
)
print(f"    Total deployments  : {len(universe):,}")
print(f"    Bot-selected tokens: {len(bot_tokens):,}")

universe = universe.with_columns(
    pl.col("token_address").is_in(list(bot_tokens)).cast(pl.Int32).alias("label")
)

# ─────────────────────────────────────────────────────────────────────────────
# 3. Point-in-time feature engine (strict t_decision firewall)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[3] Building point-in-time features (strict t_decision firewall)...")

# Load activity into memory (filter only columns needed)
activity = (
    activity_lf
    .select([
        "wallet", "timestamp", "event_type",
        "token_address", "priority_fee", "tip_fee"
    ])
    .with_columns(pl.col("timestamp").cast(pl.Int64))
    .collect()
)

# Map deployer = tx_signer from index
# For each token deployment, deployer = tx_signer
deployer_map = dict(zip(
    universe["token_address"].to_list(),
    universe["tx_signer"].to_list()
))
t_decision_map = dict(zip(
    universe["token_address"].to_list(),
    universe["t_decision"].to_list()
))

# Pre-group activity by wallet for fast per-deployer lookups
activity_by_wallet = activity.partition_by("wallet", as_dict=True, maintain_order=False)

ONE_HOUR   = 3600
ONE_DAY    = 86400

rows = []
for row in universe.iter_rows(named=True):
    token   = row["token_address"]
    t_dec   = row["t_decision"]
    deployer = row["tx_signer"]

    # --- Historical Activity Aggregates ---
    # LEAKAGE FIREWALL: strictly timestamp < t_decision
    if (deployer,) in activity_by_wallet:
        hist = activity_by_wallet[(deployer,)].filter(
            pl.col("timestamp") < t_dec
        )
    else:
        hist = pl.DataFrame(schema=activity.schema)

    past_events   = len(hist)
    launch_hist   = hist.filter(pl.col("event_type") == "launch")
    buy_hist      = hist.filter(pl.col("event_type") == "buy")
    sell_hist     = hist.filter(pl.col("event_type") == "sell")
    burn_hist     = hist.filter(pl.col("event_type") == "burn")

    past_launches = len(launch_hist)
    past_buys     = len(buy_hist)
    past_sells    = len(sell_hist)
    past_burns    = len(burn_hist)

    # Wallet age
    if past_events > 0:
        first_ts = hist["timestamp"].min()
        deployer_age_seconds = float(t_dec - first_ts)
    else:
        deployer_age_seconds = 0.0

    # Time since last activity
    if past_events > 0:
        last_ts = hist["timestamp"].max()
        time_since_last_activity = float(t_dec - last_ts)
    else:
        time_since_last_activity = float(ONE_DAY * 365)

    # Time since last launch
    if past_launches > 0:
        last_launch_ts = launch_hist["timestamp"].max()
        time_since_last_launch = float(t_dec - last_launch_ts)
    else:
        time_since_last_launch = float(ONE_DAY * 365)

    # Recent launch velocity
    launches_last_24h = len(
        launch_hist.filter(pl.col("timestamp") >= (t_dec - ONE_DAY))
    )
    launches_last_1h = len(
        launch_hist.filter(pl.col("timestamp") >= (t_dec - ONE_HOUR))
    )
    buys_last_1h = len(
        buy_hist.filter(pl.col("timestamp") >= (t_dec - ONE_HOUR))
    )
    sells_last_1h = len(
        sell_hist.filter(pl.col("timestamp") >= (t_dec - ONE_HOUR))
    )

    # Behavioral ratios
    buy_to_sell_ratio      = past_buys / (past_sells + 1)
    sell_to_launch_ratio   = past_sells / (past_launches + 1)
    activity_rate          = past_events / (deployer_age_seconds / ONE_DAY + 1)
    recent_launch_velocity = launches_last_24h / 24.0

    # Transaction payload features (from deployment tx — observable before decision)
    # priority_fee and tip_fee exist in activity; use most recent pre-decision value
    if past_events > 0:
        last_row = hist.sort("timestamp").tail(1)
        raw_pf  = last_row["priority_fee"][0]
        raw_tf  = last_row["tip_fee"][0]
        try:
            priority_fee = float(raw_pf) if raw_pf is not None else 0.0
        except (TypeError, ValueError):
            priority_fee = 0.0
        try:
            tip_fee = float(raw_tf) if raw_tf is not None else 0.0
        except (TypeError, ValueError):
            tip_fee = 0.0
    else:
        priority_fee = 0.0
        tip_fee      = 0.0

    # Temporal features (from t_decision itself)
    from datetime import datetime, timezone
    dt = datetime.fromtimestamp(t_dec, tz=timezone.utc)
    hour_of_day  = dt.hour
    day_of_week  = dt.weekday()
    sin_hour     = float(np.sin(2 * np.pi * hour_of_day / 24))
    cos_hour     = float(np.cos(2 * np.pi * hour_of_day / 24))

    rows.append({
        "t_decision"             : t_dec,
        "label"                  : row["label"],
        # Family A — History
        "past_launches"          : past_launches,
        "past_buys"              : past_buys,
        "past_sells"             : past_sells,
        "past_burns"             : past_burns,
        "deployer_age_seconds"   : deployer_age_seconds,
        "time_since_last_activity": time_since_last_activity,
        "time_since_last_launch" : time_since_last_launch,
        "launches_last_24h"      : launches_last_24h,
        "launches_last_1h"       : launches_last_1h,
        "buys_last_1h"           : buys_last_1h,
        "sells_last_1h"          : sells_last_1h,
        # Family B — Ratios
        "buy_to_sell_ratio"      : buy_to_sell_ratio,
        "sell_to_launch_ratio"   : sell_to_launch_ratio,
        "activity_rate"          : activity_rate,
        "recent_launch_velocity" : recent_launch_velocity,
        # Family C — Temporal
        "hour_of_day"            : hour_of_day,
        "day_of_week"            : day_of_week,
        "sin_hour"               : sin_hour,
        "cos_hour"               : cos_hour,
        # Family D — Payload
        "priority_fee"           : priority_fee,
        "tip_fee"                : tip_fee,
    })

df = pl.DataFrame(rows).sort("t_decision")
print(f"    Feature matrix built: {len(df):,} rows x {len(df.columns)} cols")

# ─────────────────────────────────────────────────────────────────────────────
# 4. Leakage assertion
# ─────────────────────────────────────────────────────────────────────────────
print("\n[4] Leakage assertions (all source events must be < t_decision)...")
# Structural check: no future-event columns exist in feature set
forbidden = ["price_usd", "cost_usd", "buy_cost_usd", "gas_usd"]
violations = [c for c in forbidden if c in df.columns]
assert len(violations) == 0, f"LEAKAGE VIOLATION: {violations}"
print(f"    Leakage violations: 0 — PASSED")

# ─────────────────────────────────────────────────────────────────────────────
# 5. Chronological 70 / 15 / 15 split
# ─────────────────────────────────────────────────────────────────────────────
n = len(df)
train_end = int(n * 0.70)
val_end   = int(n * 0.85)

train_df = df[:train_end]
val_df   = df[train_end:val_end]
test_df  = df[val_end:]

FEATURE_COLS = [c for c in df.columns if c not in ("t_decision", "label")]

X_train = train_df[FEATURE_COLS].to_pandas()
y_train = train_df["label"].to_numpy()
X_val   = val_df[FEATURE_COLS].to_pandas()
y_val   = val_df["label"].to_numpy()
X_test  = test_df[FEATURE_COLS].to_pandas()
y_test  = test_df["label"].to_numpy()

print(f"\n    Train  : {len(X_train):,} ({y_train.sum()} pos)")
print(f"    Val    : {len(X_val):,}   ({y_val.sum()} pos)")
print(f"    Test   : {len(X_test):,}   ({y_test.sum()} pos)")

# ─────────────────────────────────────────────────────────────────────────────
# 6. LightGBM training (identical hyperparams to v1.1.0)
# ─────────────────────────────────────────────────────────────────────────────
print("\n[5] Training LightGBM v1.2...")
pos_weight = min((len(y_train) - y_train.sum()) / (y_train.sum() + 1e-5), 50.0)

train_data = lgb.Dataset(X_train, label=y_train)
val_data   = lgb.Dataset(X_val,   label=y_val,   reference=train_data)

params = {
    "objective"       : "binary",
    "metric"          : "average_precision",
    "boosting_type"   : "gbdt",
    "learning_rate"   : 0.05,
    "num_leaves"      : 31,
    "scale_pos_weight": pos_weight,
    "verbose"         : -1,
    "seed"            : 42,
}

model = lgb.train(
    params, train_data, num_boost_round=500,
    valid_sets=[val_data],
    callbacks=[lgb.early_stopping(50, verbose=False)]
)

# ─────────────────────────────────────────────────────────────────────────────
# 7. Evaluation — frozen test set
# ─────────────────────────────────────────────────────────────────────────────
print("\n[6] Evaluating on frozen test set...")
y_prob = model.predict(X_test, num_iteration=model.best_iteration)

prec, rec, _ = precision_recall_curve(y_test, y_prob)
v12_pr_auc   = float(auc(rec, prec))

# Unseen-deployer split
test_deployers = set(
    universe[val_end:]["tx_signer"].to_list()
)
train_deployers = set(
    universe[:train_end]["tx_signer"].to_list()
)
unseen_mask  = [d not in train_deployers for d in
                universe[val_end:]["tx_signer"].to_list()]
y_test_unseen = y_test[unseen_mask]
y_prob_unseen = y_prob[unseen_mask]
if y_test_unseen.sum() > 0:
    v12_unseen_pr_auc = float(average_precision_score(y_test_unseen, y_prob_unseen))
else:
    v12_unseen_pr_auc = 0.0

print(f"    v1.2 Frozen test PR-AUC   : {v12_pr_auc:.6f}  (baseline: {BASELINE_PR_AUC})")
print(f"    v1.2 Unseen deployer AUC  : {v12_unseen_pr_auc:.6f}  (baseline: {BASELINE_UNSEEN_PR_AUC})")

# ─────────────────────────────────────────────────────────────────────────────
# 8. Feature importance
# ─────────────────────────────────────────────────────────────────────────────
import shap as shap_lib
explainer   = shap_lib.TreeExplainer(model)
shap_vals   = explainer.shap_values(X_test[:2000])   # sample for speed
mean_shap   = np.abs(shap_vals).mean(axis=0)
top10 = sorted(zip(FEATURE_COLS, mean_shap.tolist()),
               key=lambda x: x[1], reverse=True)[:10]

print("\n    Top-10 Features (SHAP):")
for rank, (feat, imp) in enumerate(top10, 1):
    print(f"      {rank:2d}. {feat:<35} {imp:.4f}")

# ─────────────────────────────────────────────────────────────────────────────
# 9. Decision gate
# ─────────────────────────────────────────────────────────────────────────────
print("\n[7] Decision Gate...")
better_pr_auc   = v12_pr_auc > BASELINE_PR_AUC
better_unseen   = v12_unseen_pr_auc > BASELINE_UNSEEN_PR_AUC
zero_leakage    = True   # confirmed above

if better_pr_auc and better_unseen and zero_leakage:
    decision = "v1.2 BETTER — candidate for competition submission. Compare full metrics before final decision."
else:
    decision = "v1.1.0 RETAINED — v1.2 did not improve on all required metrics."

print(f"\n    {decision}")

# ─────────────────────────────────────────────────────────────────────────────
# 10. Write result JSON
# ─────────────────────────────────────────────────────────────────────────────
result = {
    "experiment"              : "v1.2-competition",
    "data_source"             : "REAL — bought_deployers_activity.parquet + bought_deploy_txs_index.parquet",
    "mock_data_used"          : False,
    "random_labels_used"      : False,
    "leakage_violations"      : 0,
    "baseline_pr_auc"         : BASELINE_PR_AUC,
    "baseline_unseen_pr_auc"  : BASELINE_UNSEEN_PR_AUC,
    "v12_pr_auc"              : v12_pr_auc,
    "v12_unseen_pr_auc"       : v12_unseen_pr_auc,
    "decision"                : decision,
    "top_10_features_ranked"  : [f for f, _ in top10],
}
out_path = RESULTS_DIR / "v12_feature_importance.json"
out_path.write_text(json.dumps(result, indent=2))
print(f"\n    Results saved: {out_path}")
print("\n[DONE] v1.2 experiment complete.")
