import polars as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import shap
from pathlib import Path
from sklearn.tree import DecisionTreeClassifier, export_text
from lightgbm import LGBMClassifier
from sklearn.metrics import precision_recall_curve, auc, precision_score, recall_score, f1_score
import warnings
warnings.filterwarnings('ignore')

def compute_metrics(y_true, y_probs, threshold=None):
    if len(y_true) == 0:
        return np.nan, np.nan, np.nan, np.nan
    precision_v, recall_v, thresholds_v = precision_recall_curve(y_true, y_probs)
    pr_auc = auc(recall_v, precision_v)
    
    if threshold is None:
        f1_scores = 2 * (precision_v * recall_v) / (precision_v + recall_v + 1e-10)
        best_idx = np.argmax(f1_scores)
        best_thresh = thresholds_v[best_idx] if best_idx < len(thresholds_v) else 0.5
        threshold = best_thresh
        
    y_preds = (y_probs >= threshold).astype(int)
    prec = precision_score(y_true, y_preds, zero_division=0)
    rec = recall_score(y_true, y_preds, zero_division=0)
    f1 = f1_score(y_true, y_preds, zero_division=0)
    return pr_auc, prec, rec, f1, threshold

def run_phase4_5():
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
    
    # 1. Base Model
    print("\nTraining Base LightGBM Model...")
    clf = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
    clf.fit(X_train, y_train)
    
    val_probs = clf.predict_proba(X_val)[:, 1]
    _, _, _, _, best_thresh = compute_metrics(y_val, val_probs)
    
    test_probs = clf.predict_proba(X_test)[:, 1]
    pr_auc, prec, rec, f1, _ = compute_metrics(y_test, test_probs, best_thresh)
    print(f"Base Test PR-AUC: {pr_auc:.4f}, F1: {f1:.4f}")
    
    # 2. SHAP Analysis
    print("\nRunning SHAP Analysis...")
    # Sample background for shap if needed, but TreeExplainer handles all
    explainer = shap.TreeExplainer(clf)
    # Only use a sample of test for shap to save time/memory, or use all
    X_test_sample = X_test.sample(min(10000, len(X_test)), random_state=42)
    shap_values = explainer.shap_values(X_test_sample)
    # For LightGBM binary classification, shap_values is a list of [class_0, class_1] or just class_1 depending on version
    if isinstance(shap_values, list):
        shap_values_cls1 = shap_values[1]
    else:
        shap_values_cls1 = shap_values
        
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values_cls1, X_test_sample, show=False)
    plt.savefig(out_dir / "shap_beeswarm.png", bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(10, 6))
    shap.summary_plot(shap_values_cls1, X_test_sample, plot_type="bar", show=False)
    plt.savefig(out_dir / "shap_global_importance.png", bbox_inches='tight')
    plt.close()
    
    # Dependence plots for top features
    top_feats = ["deployer_age_seconds", "past_launches", "past_sells"]
    for feat in top_feats:
        plt.figure(figsize=(8, 5))
        shap.dependence_plot(feat, shap_values_cls1, X_test_sample, show=False, interaction_index=None)
        plt.savefig(out_dir / f"shap_dependence_{feat}.png", bbox_inches='tight')
        plt.close()

    # 3. Feature Ablation
    print("\nRunning Feature-Family Ablation...")
    ablation_results = []
    history_features = ["past_launches", "past_buys", "past_sells", "past_burns", "deployer_age_seconds"]
    
    ablation_results.append({
        "Ablated_Feature": "None (Full Model)",
        "PR_AUC": pr_auc,
        "F1": f1
    })
    
    for feat in history_features:
        ablated_features = [f for f in features if f != feat]
        clf_abl = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
        clf_abl.fit(X_train[ablated_features], y_train)
        
        val_p = clf_abl.predict_proba(X_val[ablated_features])[:, 1]
        _, _, _, _, thresh_abl = compute_metrics(y_val, val_p)
        
        test_p = clf_abl.predict_proba(X_test[ablated_features])[:, 1]
        pr_auc_abl, _, _, f1_abl, _ = compute_metrics(y_test, test_p, thresh_abl)
        
        ablation_results.append({
            "Ablated_Feature": f"Removed {feat}",
            "PR_AUC": pr_auc_abl,
            "F1": f1_abl
        })
        print(f"  Removed {feat}: PR-AUC={pr_auc_abl:.4f}, F1={f1_abl:.4f}")
        
    pd.DataFrame(ablation_results).to_csv(out_dir / "feature_ablation.csv", index=False)
    
    # 4. Decision Tree Rule Reconstruction
    print("\nExtracting Decision Tree Rules...")
    dt = DecisionTreeClassifier(max_depth=3, random_state=42, class_weight='balanced')
    dt.fit(X_train, y_train)
    rules = export_text(dt, feature_names=features)
    
    with open(out_dir / "rule_reconstruction.txt", "w") as f:
        f.write("Model-derived behavioral rules (Not the actual bot source code):\n")
        f.write("Class 1 = Bot selected, Class 0 = Not selected\n\n")
        f.write(rules)
        
    # 5. Seen vs Unseen Deployer Test
    print("\nRunning Seen vs Unseen Deployer Test...")
    train_deployers = set(w_train.tolist())
    
    # Create mask for seen vs unseen in test set
    is_seen = w_test.isin(train_deployers)
    
    X_test_seen = X_test[is_seen]
    y_test_seen = y_test[is_seen]
    probs_seen = test_probs[is_seen]
    
    X_test_unseen = X_test[~is_seen]
    y_test_unseen = y_test[~is_seen]
    probs_unseen = test_probs[~is_seen]
    
    pr_auc_seen, prec_seen, rec_seen, f1_seen, _ = compute_metrics(y_test_seen, probs_seen, best_thresh)
    pr_auc_unseen, prec_unseen, rec_unseen, f1_unseen, _ = compute_metrics(y_test_unseen, probs_unseen, best_thresh)
    
    seen_unseen_res = [
        {"Cohort": "Seen Deployers", "Count": len(X_test_seen), "PR_AUC": pr_auc_seen, "Precision": prec_seen, "Recall": rec_seen, "F1": f1_seen},
        {"Cohort": "Unseen Deployers", "Count": len(X_test_unseen), "PR_AUC": pr_auc_unseen, "Precision": prec_unseen, "Recall": rec_unseen, "F1": f1_unseen}
    ]
    
    df_seen_unseen = pd.DataFrame(seen_unseen_res)
    df_seen_unseen.to_csv(out_dir / "seen_vs_unseen.csv", index=False)
    
    print("\n--- SEEN VS UNSEEN RESULTS ---")
    print(df_seen_unseen.to_string(index=False))
    
    print("\nPhase 4.5 Execution Complete.")

if __name__ == "__main__":
    run_phase4_5()
