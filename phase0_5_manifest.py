import os
import json
import hashlib
import polars as pl
from pathlib import Path

DATA_DIR = Path("c:/pumpfun-zero-block-deconstruction/data/raw")
FILES = [
    DATA_DIR / "bought_deploy_txs_index.parquet",
    DATA_DIR / "bought_deployers_activity.parquet",
    DATA_DIR / "bought_deploy_txs.jsonl" / "deploy_txs.jsonl"
]

def get_checksum(filepath):
    sha256_hash = hashlib.sha256()
    with open(filepath, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def analyze_file(filepath):
    print(f"Analyzing {filepath.name}...")
    size = os.path.getsize(filepath)
    checksum = get_checksum(filepath)
    
    if filepath.name.endswith(".parquet"):
        try:
            df = pl.read_parquet(filepath)
            row_count = df.height
            columns = df.columns
            dtypes = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
            
            # Try to find a timestamp column
            ts_cols = [c for c in columns if 'time' in c.lower() or 'ts' in c.lower() or 'date' in c.lower()]
            min_ts, max_ts = None, None
            if ts_cols:
                ts_col = ts_cols[0]
                try:
                    min_ts = str(df[ts_col].min())
                    max_ts = str(df[ts_col].max())
                except:
                    pass
            
            return {
                "file": filepath.name,
                "size_bytes": size,
                "row_count": row_count,
                "columns": columns,
                "dtypes": dtypes,
                "min_timestamp": min_ts,
                "max_timestamp": max_ts,
                "checksum": checksum
            }
        except Exception as e:
            return {"file": filepath.name, "error": str(e)}
            
    elif filepath.name.endswith(".jsonl"):
        try:
            df = pl.read_ndjson(filepath, n_rows=500000) # Read up to 500k rows, or use scan
            row_count = df.height
            columns = df.columns
            dtypes = {col: str(dtype) for col, dtype in zip(df.columns, df.dtypes)}
            
            # Try to find a timestamp column
            ts_cols = [c for c in columns if 'time' in c.lower() or 'ts' in c.lower() or 'date' in c.lower()]
            min_ts, max_ts = None, None
            if ts_cols:
                ts_col = ts_cols[0]
                try:
                    min_ts = str(df[ts_col].min())
                    max_ts = str(df[ts_col].max())
                except:
                    pass
            
            return {
                "file": filepath.name,
                "size_bytes": size,
                "row_count": row_count,
                "columns": columns,
                "dtypes": dtypes,
                "min_timestamp": min_ts,
                "max_timestamp": max_ts,
                "checksum": checksum
            }
        except Exception as e:
            # Fallback for large JSONL
            rows = 0
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    rows += 1
            return {
                "file": filepath.name,
                "size_bytes": size,
                "row_count": rows,
                "columns": "unknown",
                "checksum": checksum
            }

def main():
    manifest = {}
    for f in FILES:
        if f.exists():
            manifest[f.name] = analyze_file(f)
        else:
            print(f"Not found: {f}")
            
    out_path = Path("c:/pumpfun-zero-block-deconstruction/data/manifests")
    out_path.mkdir(parents=True, exist_ok=True)
    manifest_file = out_path / "data_manifest.json"
    
    with open(manifest_file, "w") as f:
        json.dump(manifest, f, indent=4)
        
    print(f"Data manifest saved to {manifest_file}")
    
if __name__ == "__main__":
    main()
