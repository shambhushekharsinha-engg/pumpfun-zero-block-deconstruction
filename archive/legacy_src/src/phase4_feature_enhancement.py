import polars as pl
from pathlib import Path

def enhance_features():
    print("Loading features_v1...")
    df_features = pl.read_parquet("data/processed/features_v1.parquet")
    
    print("Loading raw activity for deployment-level features...")
    df_activity = pl.read_parquet("data/raw/bought_deployers_activity.parquet")
    
    # Filter only to launches
    df_launches_raw = df_activity.filter(pl.col("event_type") == "launch")
    
    # Select deployment-only features
    deploy_feats = df_launches_raw.select([
        "tx_hash",
        "priority_fee",
        "tip_fee",
        "gas_native",
        "token_total_supply"
    ])
    
    # Handle missing/null values if any (assume 0 for fees)
    deploy_feats = deploy_feats.with_columns([
        pl.col("priority_fee").fill_null(0),
        pl.col("tip_fee").fill_null(0),
        pl.col("gas_native").fill_null(0),
        pl.col("token_total_supply").fill_null(1_000_000_000) # Common default
    ])
    
    print("Merging deployment features...")
    df_full = df_features.join(deploy_feats, on="tx_hash", how="left")
    
    out_path = Path("data/processed/features_v2_full.parquet")
    print(f"Saving fully enhanced features to {out_path}...")
    df_full.write_parquet(out_path)
    print("Feature enhancement complete.")

if __name__ == "__main__":
    enhance_features()
