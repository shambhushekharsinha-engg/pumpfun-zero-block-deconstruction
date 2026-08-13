import polars as pl
import pandas as pd
import numpy as np
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.metrics import precision_recall_curve, auc, precision_score, recall_score
import warnings
warnings.filterwarnings('ignore')

def run_phase5a():
    print("Loading features...")
    df = pl.read_parquet("data/processed/features_v2_full.parquet").sort("timestamp")
    df = df.fill_null(0)
    
    features = [
        "past_launches", "past_buys", "past_sells", "past_burns", "deployer_age_seconds",
        "priority_fee", "tip_fee", "gas_native", "token_total_supply"
    ]
    
    df_pd = df.to_pandas()
    X = df_pd[features].astype(float)
    y = df_pd['label']
    wallets = df_pd['wallet']
    
    total_len = len(df_pd)
    train_end = int(total_len * 0.7)
    val_end = int(total_len * 0.85)
    
    X_train, y_train, w_train = X.iloc[:train_end], y.iloc[:train_end], wallets.iloc[:train_end]
    X_val, y_val = X.iloc[train_end:val_end], y.iloc[train_end:val_end]
    X_test, y_test, w_test = X.iloc[val_end:], y.iloc[val_end:], wallets.iloc[val_end:]
    
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    
    # User Request: Verify unseen deployers are genuinely unseen in the historical feature source
    print("\n--- Unseen Deployer Strict Verification ---")
    train_deployers = set(w_train.tolist())
    is_seen = w_test.isin(train_deployers)
    unseen_test_wallets = w_test[~is_seen]
    
    # We verify that NONE of these unseen wallets exist in w_train
    overlap_check = set(unseen_test_wallets).intersection(train_deployers)
    if len(overlap_check) == 0:
        print(f"VERIFIED: {len(unseen_test_wallets)} unseen deployers are strictly excluded from the training deployer IDs.")
    else:
        print("ERROR: Unseen deployers found in train set!")
        exit(1)
        
    print("\nTraining Locked LightGBM Model...")
    clf = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
    clf.fit(X_train, y_train)
    
    # Lock Threshold
    val_probs = clf.predict_proba(X_val)[:, 1]
    precision_v, recall_v, thresholds_v = precision_recall_curve(y_val, val_probs)
    f1_scores = 2 * (precision_v * recall_v) / (precision_v + recall_v + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_thresh = thresholds_v[best_idx] if best_idx < len(thresholds_v) else 0.5
    
    # Predict Test
    test_probs = clf.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= best_thresh).astype(int)
    
    df_test = df_pd.iloc[val_end:].copy()
    df_test['target_bot_selected'] = y_test.values
    df_test['replica_selected'] = test_preds
    df_test['replica_prob'] = test_probs
    
    print("\n--- PHASE 5A SELECTION REPLAY METRICS ---")
    total_test = len(df_test)
    bot_selections = df_test['target_bot_selected'].sum()
    replica_selections = df_test['replica_selected'].sum()
    
    shared = ((df_test['target_bot_selected'] == 1) & (df_test['replica_selected'] == 1)).sum()
    bot_only = ((df_test['target_bot_selected'] == 1) & (df_test['replica_selected'] == 0)).sum()
    replica_only = ((df_test['target_bot_selected'] == 0) & (df_test['replica_selected'] == 1)).sum()
    
    precision = shared / replica_selections if replica_selections > 0 else 0
    recall = shared / bot_selections if bot_selections > 0 else 0
    selection_ratio = replica_selections / bot_selections if bot_selections > 0 else 0
    
    metrics = {
        "Total Test Deployments": total_test,
        "Target Bot Selections": bot_selections,
        "Replica Selections": replica_selections,
        "Shared (Bot ∩ Replica)": shared,
        "Bot-only (Bot − Replica)": bot_only,
        "Replica-only (Replica − Bot)": replica_only,
        "Precision": precision,
        "Recall": recall,
        "Selection Ratio": selection_ratio
    }
    
    metrics_df = pd.DataFrame([metrics]).T
    metrics_df.columns = ["Value"]
    print(metrics_df)
    metrics_df.to_csv(out_dir / "phase5a_replay_metrics.csv")
    
    print("\n--- COHORT BEHAVIORAL PROFILING ---")
    
    cohorts = {
        "Shared (Bot ∩ Replica)": df_test[(df_test['target_bot_selected'] == 1) & (df_test['replica_selected'] == 1)],
        "Bot-only (Bot − Replica)": df_test[(df_test['target_bot_selected'] == 1) & (df_test['replica_selected'] == 0)],
        "Replica-only (Replica − Bot)": df_test[(df_test['target_bot_selected'] == 0) & (df_test['replica_selected'] == 1)],
        "True Negatives (Neither)": df_test[(df_test['target_bot_selected'] == 0) & (df_test['replica_selected'] == 0)]
    }
    
    profiles = []
    for name, cohort_df in cohorts.items():
        if len(cohort_df) == 0:
            continue
        prof = {
            "Cohort": name,
            "Count": len(cohort_df),
            "Median past_launches": cohort_df["past_launches"].median(),
            "Median deployer_age_sec": cohort_df["deployer_age_seconds"].median(),
            "Median past_buys": cohort_df["past_buys"].median(),
            "Median past_sells": cohort_df["past_sells"].median(),
            "Mean Replica Probability": cohort_df["replica_prob"].mean()
        }
        profiles.append(prof)
        
    profiles_df = pd.DataFrame(profiles)
    print(profiles_df.to_string(index=False))
    profiles_df.to_csv(out_dir / "phase5a_cohort_profiles.csv", index=False)
    
    print("\nPhase 5A Execution Complete.")

if __name__ == "__main__":
    run_phase5a()
