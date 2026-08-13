import polars as pl
import pandas as pd
import numpy as np
from pathlib import Path
from sklearn.model_selection import train_test_split
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import precision_recall_curve, auc, precision_score, recall_score, f1_score
from lightgbm import LGBMClassifier
import warnings
warnings.filterwarnings('ignore')

def evaluate_model(clf, X_train, y_train, X_val, y_val, X_test, y_test, name, exp_name):
    # Train
    clf.fit(X_train, y_train)
    
    # Val Probas
    val_probs = clf.predict_proba(X_val)[:, 1]
    
    # Calculate PR-AUC on Validation
    precision_v, recall_v, thresholds_v = precision_recall_curve(y_val, val_probs)
    pr_auc_val = auc(recall_v, precision_v)
    
    # Choose best threshold on Validation (maximizing F1)
    f1_scores = 2 * (precision_v * recall_v) / (precision_v + recall_v + 1e-10)
    best_idx = np.argmax(f1_scores)
    best_thresh = thresholds_v[best_idx] if best_idx < len(thresholds_v) else 0.5
    
    # Apply locked threshold to TEST
    test_probs = clf.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= best_thresh).astype(int)
    
    # Test PR-AUC
    precision_t, recall_t, _ = precision_recall_curve(y_test, test_probs)
    pr_auc_test = auc(recall_t, precision_t)
    
    prec_test = precision_score(y_test, test_preds, zero_division=0)
    rec_test = recall_score(y_test, test_preds, zero_division=0)
    f1_test = f1_score(y_test, test_preds, zero_division=0)
    
    # Bot Capture Rate is literally just Recall for class 1
    bot_capture = rec_test
    
    return {
        "Experiment": exp_name,
        "Model": name,
        "Val_PR_AUC": pr_auc_val,
        "Test_PR_AUC": pr_auc_test,
        "Test_Precision": prec_test,
        "Test_Recall (Bot Capture)": bot_capture,
        "Test_F1": f1_test,
        "Threshold_Locked": best_thresh
    }

def run_phase4():
    print("Loading features...")
    df = pl.read_parquet("data/processed/features_v2_full.parquet").sort("timestamp")
    
    # Define feature sets
    history_feats = ["past_launches", "past_buys", "past_sells", "past_burns", "deployer_age_seconds"]
    deploy_feats = ["priority_fee", "tip_fee", "gas_native", "token_total_supply"]
    full_feats = history_feats + deploy_feats
    
    # Fill NAs
    df = df.fill_null(0)
    
    total_len = df.height
    train_end = int(total_len * 0.7)
    val_end = int(total_len * 0.85)
    
    print("Chronological split: 70% Train, 15% Val, 15% Test")
    df_train = df.head(train_end)
    df_val = df.slice(train_end, val_end - train_end)
    df_test = df.tail(total_len - val_end)
    
    # Convert to pandas for sklearn
    df_train_pd = df_train.to_pandas()
    df_val_pd = df_val.to_pandas()
    df_test_pd = df_test.to_pandas()
    
    y_train = df_train_pd['label']
    y_val = df_val_pd['label']
    y_test = df_test_pd['label']
    
    experiments = {
        "A: Full Model": full_feats,
        "B: Deployment-Only": deploy_feats,
        "C: History-Only": history_feats
    }
    
    models = {
        "1. Dummy Baseline": DummyClassifier(strategy="prior"),
        "2. Logistic Regression": LogisticRegression(max_iter=1000, random_state=42, class_weight='balanced'),
        "3. Decision Tree": DecisionTreeClassifier(max_depth=5, random_state=42, class_weight='balanced'),
        "4. LightGBM": LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
    }
    
    results = []
    
    for exp_name, features in experiments.items():
        print(f"\nRunning {exp_name}...")
        X_train = df_train_pd[features].astype(float)
        X_val = df_val_pd[features].astype(float)
        X_test = df_test_pd[features].astype(float)
        
        for model_name, model in models.items():
            print(f"  Training {model_name}...")
            res = evaluate_model(model, X_train, y_train, X_val, y_val, X_test, y_test, model_name, exp_name)
            results.append(res)
            
    res_df = pd.DataFrame(results)
    
    # Save results
    out_dir = Path("results")
    out_dir.mkdir(exist_ok=True)
    res_df.to_csv(out_dir / "model_comparison.csv", index=False)
    
    print("\n--- PHASE 4 RESULTS SUMMARY ---")
    print(res_df.to_string(index=False))

if __name__ == "__main__":
    run_phase4()
