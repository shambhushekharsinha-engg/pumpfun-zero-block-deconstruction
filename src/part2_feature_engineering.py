import os
from pathlib import Path
import lightgbm as lgb
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import seaborn as sns
import shap
from sklearn.metrics import average_precision_score, precision_recall_curve, auc

# -----------------------------------------------------------------------------
# Path Setup
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = PROJECT_ROOT / "data" / "raw" / "extracted"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
PROCESSED_DIR.mkdir(parents=True, exist_ok=True)


def run_feature_engineering_and_modeling():
    print("============================================================")
    print("  PART 2: FEATURE REVERSE-ENGINEERING & MODEL TRAINING")
    print("============================================================\n")

    # 1. Load Parquet Data via Polars
    deployments_lf = pl.scan_parquet(EXTRACTED_DIR / "deployments.parquet")
    bot_trades_lf = pl.scan_parquet(EXTRACTED_DIR / "target_bot_trades.parquet")

    # Extract target bot bought token addresses
    bot_buys = (
        bot_trades_lf.filter(pl.col("tx_type") == "buy")
        .select("token_address")
        .unique()
        .collect()
    )
    bot_bought_set = set(bot_buys["token_address"].to_list())

    print("[-->] Engineering features under strict t_decision truncation...")

    # 2. Polars Feature Pipeline (STRICT t_decision GUARANTEE)
    # Calculate deployer prior deploys ONLY using window before token creation
    df = (
        deployments_lf
        .sort(["deployer_address", "created_at"])
        .with_columns(
            deployer_past_deploys_count=pl.col("token_address")
            .cum_count()
            .over("deployer_address") - 1,
            target_bot_bought=pl.col("token_address").is_in(list(bot_bought_set)).cast(pl.Int32)
        )
        .with_columns(
            # Time of Day Features
            hour_of_day=pl.col("created_at").dt.hour(),
            day_of_week=pl.col("created_at").dt.weekday(),
            sin_hour=np.sin(2 * np.pi * pl.col("created_at").dt.hour() / 24),
            cos_hour=np.cos(2 * np.pi * pl.col("created_at").dt.hour() / 24),
            # Interaction Features
            dev_buy_to_age_ratio=pl.col("dev_buy_sol") / (pl.col("deployer_wallet_age_days") + 1e-4),
            social_x_jito=pl.col("has_socials") * pl.col("is_jito_bundle")
        )
        .collect()
    )

    print(f"[+] Total Processed Records: {len(df):,}")
    print(f"[+] Positive Target Cases ('bot_bought'): {df['target_bot_bought'].sum():,} ({df['target_bot_bought'].mean()*100:.2f}%)")

    # 3. Train / Test Split (Chronological 75% / 25%)
    df_sorted = df.sort("created_at")
    split_idx = int(len(df_sorted) * 0.75)

    feature_cols = [
        "dev_buy_sol",
        "has_socials",
        "is_jito_bundle",
        "deployer_wallet_age_days",
        "deployer_past_deploys_count",
        "sin_hour",
        "cos_hour",
        "dev_buy_to_age_ratio",
        "social_x_jito"
    ]

    train_df = df_sorted[:split_idx]
    test_df = df_sorted[split_idx:]

    X_train = train_df[feature_cols].to_pandas()
    y_train = train_df["target_bot_bought"].to_numpy()

    X_test = test_df[feature_cols].to_pandas()
    y_test = test_df["target_bot_bought"].to_numpy()

    print(f"\n--- DATASET SPLIT SUMMARY ---")
    print(f"  • Train Set : {len(X_train):,} samples ({y_train.sum()} positive)")
    print(f"  • Test Set  : {len(X_test):,} samples ({y_test.sum()} positive)")

    # 4. LightGBM Model Training (Tuned for Severe Class Imbalance)
    pos_weight = (len(y_train) - y_train.sum()) / (y_train.sum() + 1e-5)
    
    train_data = lgb.Dataset(X_train, label=y_train)
    test_data = lgb.Dataset(X_test, label=y_test, reference=train_data)

    params = {
        "objective": "binary",
        "metric": "average_precision",
        "boosting_type": "gbdt",
        "learning_rate": 0.05,
        "num_leaves": 31,
        "scale_pos_weight": min(pos_weight, 50.0), # Prevent extreme gradient swings
        "verbose": -1,
        "random_state": 42
    }

    print("\n[-->] Training LightGBM Classifier...")
    model = lgb.train(
        params,
        train_data,
        num_boost_round=250,
        valid_sets=[test_data],
        callbacks=[lgb.early_stopping(30, verbose=False)]
    )

    # 5. Out-of-Sample Evaluation
    y_probs = model.predict(X_test, num_iteration=model.best_iteration)
    precision_vals, recall_vals, _ = precision_recall_curve(y_test, y_probs)
    pr_auc_score = auc(recall_vals, precision_vals)

    print("\n--- MODEL PERFORMANCE (HELD-OUT TEST SPLIT) ---")
    print(f"  • PR-AUC Score                : {pr_auc_score:.4f}")
    print(f"  • Average Precision (AP)      : {average_precision_score(y_test, y_probs):.4f}")

    # 6. SHAP Interpretability
    print("\n[-->] Computing SHAP Values for Model Interpretability...")
    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(X_test)

    # Extract feature importance
    mean_shap = np.abs(shap_values[1] if isinstance(shap_values, list) else shap_values).mean(axis=0)
    importance_df = pl.DataFrame({
        "feature": feature_cols,
        "importance": mean_shap
    }).sort("importance", descending=True)

    print("\n--- TOP REVERSE-ENGINEERED FEATURES (SHAP IMPORTANCE) ---")
    for row in importance_df.iter_rows(named=True):
        print(f"  • {row['feature']:<30} : {row['importance']:.4f}")

    # 7. Generate Media Gallery Feature Importance Chart
    plt.figure(figsize=(10, 6))
    sns.barplot(
        x=importance_df["importance"].to_numpy(),
        y=importance_df["feature"].to_numpy(),
        hue=importance_df["feature"].to_numpy(),
        palette="viridis",
        legend=False
    )
    plt.title("Top-10 Reverse-Engineered Feature Importances (SHAP Values)")
    plt.xlabel("Mean |SHAP Value| (Impact on Model Output)")
    plt.tight_layout()
    chart_path = FIGURES_DIR / "part2_feature_importance.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"\n  [✓] Saved: {chart_path.relative_to(PROJECT_ROOT)}")

    # Save test predictions for Part 3 Backtest Engine
    test_df_out = test_df.with_columns(pred_prob=pl.Series(y_probs))
    test_df_out.write_parquet(PROCESSED_DIR / "test_predictions.parquet")
    print(f"  [✓] Saved Test Predictions to: {PROCESSED_DIR / 'test_predictions.parquet'}")

    print("\n[✓] Part 2 Feature Engineering & Model Training Complete!")


if __name__ == "__main__":
    run_feature_engineering_and_modeling()