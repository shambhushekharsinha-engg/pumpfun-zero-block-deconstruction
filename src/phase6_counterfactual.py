import polars as pl
import pandas as pd
import numpy as np
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.metrics import precision_recall_curve

def run_phase6():
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
    
    total_len = len(df_pd)
    train_end = int(total_len * 0.7)
    val_end = int(total_len * 0.85)
    
    X_train, y_train = X.iloc[:train_end], y.iloc[:train_end]
    X_val, y_val = X.iloc[train_end:val_end], y.iloc[train_end:val_end]
    X_test, y_test = X.iloc[val_end:], y.iloc[val_end:]
    
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    
    print("Training Locked LightGBM Model...")
    clf = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
    clf.fit(X_train, y_train)
    
    # Lock Threshold
    val_probs = clf.predict_proba(X_val)[:, 1]
    precision_v, recall_v, thresholds_v = precision_recall_curve(y_val, val_probs)
    f1_scores = 2 * (precision_v * recall_v) / (precision_v + recall_v + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_thresh = thresholds_v[best_idx] if best_idx < len(thresholds_v) else 0.5
    
    test_probs = clf.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= best_thresh).astype(int)
    
    df_test = df_pd.iloc[val_end:].copy()
    for f in features:
        df_test[f] = df_test[f].astype(float)
    df_test['target_bot_label'] = y_test.values
    df_test['replica_selection'] = test_preds
    df_test['replica_probability'] = test_probs
    
    # Assign Cohorts
    def assign_cohort(row):
        if row['target_bot_label'] == 1 and row['replica_selection'] == 1:
            return "Shared"
        elif row['target_bot_label'] == 1 and row['replica_selection'] == 0:
            return "Bot-only"
        elif row['target_bot_label'] == 0 and row['replica_selection'] == 1:
            return "Replica-only"
        else:
            return "True Negative"
            
    df_test['cohort'] = df_test.apply(assign_cohort, axis=1)
    
    # Save base counterfactual dataset
    print("Saving counterfactual_analysis.csv...")
    export_cols = ['tx_hash', 'wallet', 'cohort', 'target_bot_label', 'replica_selection', 'replica_probability'] + features
    df_test[export_cols].to_csv(out_dir / "counterfactual_analysis.csv", index=False)
    
    print("\n--- Cohort Distribution Analysis ---")
    dist_results = []
    cohorts = ["Shared", "Bot-only", "Replica-only", "True Negative"]
    
    for c in cohorts:
        cdf = df_test[df_test['cohort'] == c]
        for f in features + ['replica_probability']:
            dist_results.append({
                "Cohort": c,
                "Feature": f,
                "Mean": cdf[f].mean(),
                "P25": cdf[f].quantile(0.25),
                "Median": cdf[f].median(),
                "P75": cdf[f].quantile(0.75),
                "P90": cdf[f].quantile(0.90),
                "P95": cdf[f].quantile(0.95)
            })
            
    df_dist = pd.DataFrame(dist_results)
    df_dist.to_csv(out_dir / "cohort_comparison.csv", index=False)
    print("Saved cohort_comparison.csv")
    
    print("\n--- Probability Calibration Analysis ---")
    bins = np.arange(0.0, 1.1, 0.1)
    df_test['prob_bin'] = pd.cut(df_test['replica_probability'], bins=bins, include_lowest=True)
    
    calib = df_test.groupby('prob_bin', observed=False).agg(
        deployments=('target_bot_label', 'count'),
        bot_selections=('target_bot_label', 'sum')
    ).reset_index()
    
    calib['bot_selection_rate'] = (calib['bot_selections'] / calib['deployments']).fillna(0)
    calib.to_csv(out_dir / "probability_calibration.csv", index=False)
    print("Saved probability_calibration.csv")
    print("\nProbability Calibration:")
    print(calib.to_string())

if __name__ == "__main__":
    run_phase6()
