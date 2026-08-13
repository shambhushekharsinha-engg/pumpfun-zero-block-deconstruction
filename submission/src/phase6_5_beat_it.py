import polars as pl
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from lightgbm import LGBMClassifier
from sklearn.metrics import precision_recall_curve, auc
import warnings
warnings.filterwarnings('ignore')

def run_phase6_5():
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
    
    print("\n--- 6.5A: Validation Operating-Point Optimization ---")
    clf = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
    clf.fit(X_train, y_train)
    
    val_probs = clf.predict_proba(X_val)[:, 1]
    
    val_df = pd.DataFrame({'prob': val_probs, 'target': y_val.values})
    val_df = val_df.sort_values('prob', ascending=False)
    
    total_val_targets = val_df['target'].sum()
    total_val = len(val_df)
    
    top_k_pcts = [0.01, 0.02, 0.05, 0.10, 0.15, 0.20]
    frontier_results = []
    
    chosen_threshold = 0.5
    chosen_k = 0.05
    
    for k in top_k_pcts:
        k_count = int(total_val * k)
        top_k_df = val_df.iloc[:k_count]
        captured = top_k_df['target'].sum()
        
        recall = captured / total_val_targets
        precision = captured / k_count
        selection_ratio = k_count / total_val_targets
        thresh = val_df.iloc[k_count-1]['prob']
        
        if k == chosen_k:
            chosen_threshold = thresh
            
        frontier_results.append({
            "Top K%": f"{int(k*100)}%",
            "Threshold": thresh,
            "Replica Size": k_count,
            "Target Size": total_val_targets,
            "Selection Ratio": selection_ratio,
            "Precision": precision,
            "Recall (Capture)": recall
        })
        
    frontier_df = pd.DataFrame(frontier_results)
    frontier_df.to_csv(out_dir / "validation_fidelity_frontier.csv", index=False)
    print(frontier_df.to_string(index=False))
    
    # Selection Efficiency Curve
    plt.figure(figsize=(8, 6))
    plt.plot(frontier_df['Selection Ratio'], frontier_df['Recall (Capture)'], marker='o')
    plt.axline((0, 0), slope=1, color='red', linestyle='--', label='Random Guessing')
    plt.title('Selection Efficiency Curve (Validation)')
    plt.xlabel('Selection Ratio (Replica Size / Target Size)')
    plt.ylabel('Bot Capture (Recall)')
    plt.legend()
    plt.grid(True)
    plt.savefig(out_dir / "selection_efficiency_curve.png")
    
    print("\n--- 6.5B: Secondary Regime Investigation (Validation) ---")
    # Identify Bot-only and True Negative in validation
    # For this investigation, we use the standard max-F1 threshold so we know the typical rejection boundary
    prec_v, rec_v, th_v = precision_recall_curve(y_val, val_probs)
    f1_v = 2 * (prec_v * rec_v) / (prec_v + rec_v + 1e-10)
    best_th_f1 = th_v[np.argmax(f1_v)]
    val_preds = (val_probs >= best_th_f1).astype(int)
    
    val_investigate_df = X_val.copy()
    val_investigate_df['target'] = y_val.values
    val_investigate_df['pred'] = val_preds
    
    bot_only_val = val_investigate_df[(val_investigate_df['target'] == 1) & (val_investigate_df['pred'] == 0)]
    tn_val = val_investigate_df[(val_investigate_df['target'] == 0) & (val_investigate_df['pred'] == 0)]
    
    print(f"Bot-only (Val): {len(bot_only_val)}, True Negatives (Val): {len(tn_val)}")
    
    if len(bot_only_val) > 0 and len(tn_val) > 0:
        # Train secondary discriminator
        X_sec = pd.concat([bot_only_val[features], tn_val[features]])
        y_sec = np.array([1]*len(bot_only_val) + [0]*len(tn_val))
        
        clf_sec = LGBMClassifier(random_state=42, class_weight='balanced', verbose=-1)
        clf_sec.fit(X_sec, y_sec)
        
        sec_imp = pd.DataFrame({
            'Feature': features,
            'Importance': clf_sec.feature_importances_
        }).sort_values('Importance', ascending=False)
        
        print("\nDiscriminator Feature Importances (Bot-only vs TN):")
        print(sec_imp.to_string(index=False))
        sec_imp.to_csv(out_dir / "secondary_regime_importance.csv", index=False)
        
        # Test PR-AUC of the discriminator on the training set (just to see if ANY signal exists)
        sec_probs = clf_sec.predict_proba(X_sec)[:, 1]
        p_sec, r_sec, _ = precision_recall_curve(y_sec, sec_probs)
        sec_pr_auc = auc(r_sec, p_sec)
        print(f"Discriminator PR-AUC (Train-on-self): {sec_pr_auc:.4f}")
        if sec_pr_auc < 0.2:
            print("Conclusion: The available features CANNOT explain the secondary regime. It relies on unobservable data.")
        else:
            print("Conclusion: Some signal exists in the available features to separate Bot-only from True Negatives.")
    else:
        print("Not enough samples for secondary regime analysis.")
        
    print("\n--- 6.5C: Final Frozen Test Evaluation ---")
    print(f"Applying pre-registered Top {int(chosen_k*100)}% policy (Threshold = {chosen_threshold:.6f}) to Test set...")
    
    test_probs = clf.predict_proba(X_test)[:, 1]
    test_preds = (test_probs >= chosen_threshold).astype(int)
    
    total_test = len(test_probs)
    target_selections = y_test.sum()
    replica_selections = test_preds.sum()
    shared = ((y_test.values == 1) & (test_preds == 1)).sum()
    
    test_precision = shared / replica_selections if replica_selections > 0 else 0
    test_recall = shared / target_selections if target_selections > 0 else 0
    test_sel_ratio = replica_selections / target_selections if target_selections > 0 else 0
    
    test_metrics = {
        "Policy": f"Top {int(chosen_k*100)}%",
        "Target Bot Selections": target_selections,
        "Replica Selections": replica_selections,
        "Selection Ratio": test_sel_ratio,
        "Target Bot Capture (Recall)": test_recall,
        "Precision": test_precision,
    }
    
    test_metrics_df = pd.DataFrame([test_metrics])
    print(test_metrics_df.to_string(index=False))
    test_metrics_df.to_csv(out_dir / "final_test_beat_it.csv", index=False)
    
    print("\nPhase 6.5 Execution Complete.")

if __name__ == "__main__":
    run_phase6_5()
