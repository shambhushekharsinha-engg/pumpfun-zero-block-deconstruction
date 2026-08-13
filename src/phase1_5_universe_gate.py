import polars as pl

def run_universe_gate():
    print("Loading datasets...")
    # Load positive target labels (15,927)
    df_positives = pl.read_parquet("data/raw/bought_deploy_txs_index.parquet")
    positive_txs = df_positives['tx_hash'].to_list()
    positive_tokens = df_positives['token_address'].to_list()
    
    # Load universe activities (~4.9M)
    df_activity = pl.read_parquet("data/raw/bought_deployers_activity.parquet")
    
    # Filter only launches (411,137)
    df_launches = df_activity.filter(pl.col("event_type") == "launch")
    
    total_positives_provided = len(positive_txs)
    total_launches = df_launches.height
    
    print("\n=========================================")
    print("PHASE 1.5 - UNIVERSE DEFINITION GATE")
    print("=========================================")
    print(f"Total provided positive labels: {total_positives_provided:,}")
    print(f"Total launch events in activity: {total_launches:,}")
    
    # A. Mapping Positives
    # Identify which launches match our positive tx_hash list
    df_launches = df_launches.with_columns(
        pl.col("tx_hash").is_in(positive_txs).alias("is_positive")
    )
    
    positives_in_universe = df_launches.filter(pl.col("is_positive")).height
    negatives_in_universe = df_launches.filter(~pl.col("is_positive")).height
    
    print("\n--- A & B. Mapping Exactness ---")
    print(f"Positives found in universe: {positives_in_universe:,}")
    print(f"Negatives in universe: {negatives_in_universe:,}")
    
    # Check for duplicates
    dup_positives = df_launches.filter(pl.col("is_positive")).group_by("tx_hash").count().filter(pl.col("count") > 1).height
    print(f"Duplicate positive mappings: {dup_positives}")
    
    if positives_in_universe != total_positives_provided:
        print(f"WARNING: {total_positives_provided - positives_in_universe} positive tx_hashes are missing from the launch activity!")
        missing_txs = set(positive_txs) - set(df_launches.filter(pl.col("is_positive"))['tx_hash'].to_list())
        print(f"Sample of missing tx_hashes: {list(missing_txs)[:3]}")
        
    # C. Temporal Coverage
    print("\n--- C. Temporal Coverage ---")
    pos_min = df_launches.filter(pl.col("is_positive"))['timestamp'].min()
    pos_max = df_launches.filter(pl.col("is_positive"))['timestamp'].max()
    neg_min = df_launches.filter(~pl.col("is_positive"))['timestamp'].min()
    neg_max = df_launches.filter(~pl.col("is_positive"))['timestamp'].max()
    all_min = df_launches['timestamp'].min()
    all_max = df_launches['timestamp'].max()
    
    import datetime
    def ts_to_str(ts):
        return datetime.datetime.fromtimestamp(ts, tz=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    print(f"Overall Launches:   {ts_to_str(all_min)} to {ts_to_str(all_max)}")
    print(f"Positive Launches:  {ts_to_str(pos_min)} to {ts_to_str(pos_max)}")
    print(f"Negative Launches:  {ts_to_str(neg_min)} to {ts_to_str(neg_max)}")
    
    # D. Deployer Overlap
    print("\n--- D. Deployer Overlap ---")
    total_deployers = df_launches['wallet'].n_unique()
    pos_deployers = df_launches.filter(pl.col("is_positive"))['wallet'].n_unique()
    neg_deployers = df_launches.filter(~pl.col("is_positive"))['wallet'].n_unique()
    
    print(f"Total unique deployers: {total_deployers:,}")
    print(f"Deployers with at least 1 positive: {pos_deployers:,}")
    print(f"Deployers with at least 1 negative: {neg_deployers:,}")
    
    # Average deployments per deployer
    deployer_stats = df_launches.group_by("wallet").agg([
        pl.count("tx_hash").alias("total_launches"),
        pl.col("is_positive").sum().alias("positive_launches"),
        (~pl.col("is_positive")).sum().alias("negative_launches")
    ])
    
    print(f"\nAverage launches per deployer: {deployer_stats['total_launches'].mean():.2f}")
    print(f"Average positive per deployer: {deployer_stats['positive_launches'].mean():.2f}")
    print(f"Average negative per deployer: {deployer_stats['negative_launches'].mean():.2f}")
    
    print(f"\nMax launches by a single deployer: {deployer_stats['total_launches'].max():,}")

if __name__ == "__main__":
    run_universe_gate()
