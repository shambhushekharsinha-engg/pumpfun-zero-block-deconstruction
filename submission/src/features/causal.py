import polars as pl
from pathlib import Path

def build_features():
    print("Loading datasets...")
    df_positives = pl.read_parquet("data/raw/bought_deploy_txs_index.parquet")
    positive_txs = set(df_positives['tx_hash'].to_list())
    
    df_activity = pl.read_parquet("data/raw/bought_deployers_activity.parquet")
    
    print("Grouping by exact timestamp to ensure strict < t_decision filtering...")
    # Group by wallet and timestamp to combine simultaneous events
    df_grouped = df_activity.group_by(["wallet", "timestamp"]).agg([
        (pl.col("event_type") == "launch").sum().alias("launches_at_ts"),
        (pl.col("event_type") == "buy").sum().alias("buys_at_ts"),
        (pl.col("event_type") == "sell").sum().alias("sells_at_ts"),
        (pl.col("event_type") == "burn").sum().alias("burns_at_ts"),
    ]).sort(["wallet", "timestamp"])
    
    print("Calculating strictly historical features...")
    # By shifting 1 row in a dataset where every row is a unique timestamp per wallet,
    # we mathematically guarantee that we are summing events where event_ts < current_ts.
    df_features = df_grouped.with_columns([
        pl.col("launches_at_ts").shift(1).fill_null(0).cum_sum().over("wallet").alias("past_launches"),
        pl.col("buys_at_ts").shift(1).fill_null(0).cum_sum().over("wallet").alias("past_buys"),
        pl.col("sells_at_ts").shift(1).fill_null(0).cum_sum().over("wallet").alias("past_sells"),
        pl.col("burns_at_ts").shift(1).fill_null(0).cum_sum().over("wallet").alias("past_burns"),
        pl.col("timestamp").min().over("wallet").alias("first_seen_timestamp")
    ])
    
    df_features = df_features.with_columns([
        (pl.col("timestamp") - pl.col("first_seen_timestamp")).alias("deployer_age_seconds")
    ])
    
    print("Joining safe features back to launch events...")
    # We only want to assign these features to the actual launch events (decisions)
    df_launches = df_activity.filter(pl.col("event_type") == "launch")
    
    # We join on wallet and timestamp. 
    # Because df_features is built per (wallet, timestamp), this gives the exact historical state at t_decision.
    df_launches = df_launches.join(df_features, on=["wallet", "timestamp"], how="left")
    
    print("Assigning labels...")
    df_launches = df_launches.with_columns(
        pl.col("tx_hash").is_in(positive_txs).alias("is_positive")
    )
    
    df_launches = df_launches.with_columns(
        pl.col("is_positive").cast(pl.Int32).alias("label")
    )
    
    # Select final columns for modeling
    model_features = [
        "tx_hash", "wallet", "token_address", "timestamp", 
        "past_launches", "past_buys", "past_sells", "past_burns", 
        "deployer_age_seconds", "label"
    ]
    df_final = df_launches.select(model_features)
    
    out_dir = Path("data/processed")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "features_v1.parquet"
    
    print(f"Saving leakage-safe features to {out_path}...")
    df_final.write_parquet(out_path)
    print("Phase 3 Feature Engine Prep Complete.")

if __name__ == "__main__":
    build_features()
