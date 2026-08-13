import polars as pl
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import precision_recall_curve, auc, precision_score, recall_score, f1_score
from lightgbm import LGBMClassifier
import warnings
warnings.filterwarnings('ignore')

def run_stability():
    print("Loading features...")
    df = pl.read_parquet("data/processed/features_v2_full.parquet").sort("timestamp")
    df = df.fill_null(0)
    df_pd = df.to_pandas()
    
    features = [
        "past_launches", "past_buys", "past_sells", "past_burns", "deployer_age_seconds",
        "priority_fee", "tip_fee", "gas_native", "token_total_supply"
    ]
    X = df_pd[features].astype(float)
    y = df_pd['label']
    
    tscv = TimeSeriesSplit(n_splits=3)
    
    results = []
    feature_importances = []
    
    fold = 1
    for train_index, test_index in tscv.split(X):
        # We further split test into val and test to simulate 70/15/15 if we want,
        # but for stability, simple train/test is enough.
        X_train, X_test = X.iloc[train_index], X.iloc[test_index]
        y_train, y_test = y.iloc[train_index], y.iloc[test_index]
        
        clf = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
        clf.fit(X_train, y_train)
        
        test_probs = clf.predict_proba(X_test)[:, 1]
        precision_t, recall_t, thresholds_t = precision_recall_curve(y_test, test_probs)
        pr_auc = auc(recall_t, precision_t)
        
        # Max F1 threshold on test (for diagnostic stability purpose)
        f1_scores = 2 * (precision_t * recall_t) / (precision_t + recall_t + 1e-10)
        best_idx = np.argmax(f1_scores)
        best_thresh = thresholds_t[best_idx] if best_idx < len(thresholds_t) else 0.5
        
        test_preds = (test_probs >= best_thresh).astype(int)
        prec = precision_score(y_test, test_preds, zero_division=0)
        rec = recall_score(y_test, test_preds, zero_division=0)
        f1 = f1_score(y_test, test_preds, zero_division=0)
        
        results.append({
            "Fold": fold,
            "PR-AUC": pr_auc,
            "Precision": prec,
            "Recall": rec,
            "F1": f1
        })
        
        # Feature importance
        imp = clf.feature_importances_
        for f_name, f_imp in zip(features, imp):
            feature_importances.append({
                "Fold": fold,
                "Feature": f_name,
                "Importance": f_imp
            })
            
        fold += 1
        
    res_df = pd.DataFrame(results)
    fi_df = pd.DataFrame(feature_importances)
    
    out_dir = Path("results")
    res_df.to_csv(out_dir / "temporal_folds.csv", index=False)
    
    # Calculate feature stability (ranking per fold)
    fi_df['Rank'] = fi_df.groupby('Fold')['Importance'].rank(ascending=False)
    fi_pivot = fi_df.pivot(index='Feature', columns='Fold', values='Rank')
    fi_pivot.to_csv(out_dir / "feature_stability.csv")
    
    print("\n--- TEMPORAL FOLDS ---")
    print(res_df.to_string(index=False))
    print("\n--- FEATURE STABILITY (RANK) ---")
    print(fi_pivot)

if __name__ == "__main__":
    run_stability()
