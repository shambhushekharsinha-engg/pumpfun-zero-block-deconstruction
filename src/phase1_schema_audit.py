import polars as pl
import json
import sys

def analyze_parquet(filepath):
    print(f"\n============================================================")
    print(f"FILE: {filepath}")
    print(f"============================================================")
    try:
        df = pl.read_parquet(filepath)
        print(f"Total Rows: {df.height:,}")
        print("\n--- SCHEMA & NULLS ---")
        for col in df.columns:
            null_count = df[col].null_count()
            null_pct = (null_count / df.height) * 100
            n_unique = df[col].n_unique()
            print(f"  {col:<30} | {str(df.dtypes[df.columns.index(col)]):<15} | Nulls: {null_pct:5.2f}% ({null_count}) | Unique: {n_unique:,}")
            
            # Print min/max if numeric or time
            if df.dtypes[df.columns.index(col)] in [pl.Int64, pl.Float64, pl.Int32, pl.Float32]:
                print(f"      Min: {df[col].min()} | Max: {df[col].max()}")
                
        print("\n--- SAMPLE ROWS (3) ---")
        print(df.head(3))
    except Exception as e:
        print(f"Error: {e}")

def analyze_jsonl(filepath):
    print(f"\n============================================================")
    print(f"FILE: {filepath}")
    print(f"============================================================")
    try:
        df = pl.read_ndjson(filepath)
        print(f"Total Rows: {df.height:,}")
        print("\n--- SCHEMA & NULLS ---")
        for col in df.columns:
            null_count = df[col].null_count()
            null_pct = (null_count / df.height) * 100
            print(f"  {col:<30} | {str(df.dtypes[df.columns.index(col)]):<15} | Nulls: {null_pct:5.2f}% ({null_count})")
        print("\n--- SAMPLE ROW (1) ---")
        print(df.head(1))
    except Exception as e:
        print(f"Error reading as dataframe, reading first line manually...")
        with open(filepath, 'r') as f:
            line = f.readline()
            try:
                data = json.loads(line)
                for k, v in data.items():
                    print(f"  {k}: {type(v).__name__}")
                print(f"\nSample: {json.dumps(data, indent=2)[:500]}...")
            except:
                print("Failed to parse JSON")

if __name__ == "__main__":
    analyze_parquet("data/raw/bought_deploy_txs_index.parquet")
    analyze_jsonl("data/raw/bought_deploy_txs.jsonl/deploy_txs.jsonl")
    
    # Read just a subset of the 5M rows for faster schema analysis
    print(f"\n============================================================")
    print(f"FILE: data/raw/bought_deployers_activity.parquet (Scanning subset)")
    print(f"============================================================")
    df_activity = pl.read_parquet("data/raw/bought_deployers_activity.parquet")
    print(f"Total Rows: {df_activity.height:,}")
    print("\n--- EVENT TYPES DISTRIBUTION ---")
    print(df_activity['event_type'].value_counts())
    
    # Let's see some columns and nulls for a random sample of 1M rows
    sample_df = df_activity.sample(min(1000000, df_activity.height))
    print("\n--- SCHEMA & NULLS (Based on 1M sample) ---")
    for col in sample_df.columns:
        null_count = sample_df[col].null_count()
        null_pct = (null_count / sample_df.height) * 100
        n_unique = sample_df[col].n_unique()
        print(f"  {col:<30} | {str(sample_df.dtypes[sample_df.columns.index(col)]):<15} | Nulls: {null_pct:5.2f}% | Unique (approx): {n_unique:,}")
        
        if sample_df.dtypes[sample_df.columns.index(col)] in [pl.Int64, pl.Float64, pl.Int32, pl.Float32]:
            print(f"      Min: {sample_df[col].min()} | Max: {sample_df[col].max()}")

    print("\n--- SAMPLE ROWS (3) ---")
    print(sample_df.head(3))
