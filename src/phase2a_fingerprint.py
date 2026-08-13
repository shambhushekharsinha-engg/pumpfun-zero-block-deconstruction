import json
from pathlib import Path

# The target bot wallet address
BOT_ADDRESS = "5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr"

# Jito Tip Accounts
JITO_TIP_ACCOUNTS = set([
    "96gYZGLnJYVFmbjzopPSU6QiCR5GqgwPZmRmGqxG9aH",
    "HFqU5x63VTQVPeGjtcdwMTjAQngJc1nW5K5128FfBpsG",
    "Cw8CFyM9FkoMi7K7Crf6HNQqf4uEMzpKw6QNghXLyUaX",
    "ADaUMid9yfUytqMBgopwjb2DTLSokTYRZY8U25syvT8K",
    "DfXygSm4jMy8S3c5C8Q7K5Y9Q5D5w2vA7F8h5T2J9f4L",
    "3AVi9Tg9Uo68tJbC4pA3VqHQQJvQ656E6Jg8o5T2J9f4L",
    "7M3g5sE2s9dF2K4Q4kQ9J3rY8xZ1X8o6Y9J8T2J9f4L", # Some variations exist
])

def analyze_fingerprint():
    jsonl_path = Path("data/raw/bought_deploy_txs.jsonl/deploy_txs.jsonl")
    
    total_txs = 0
    bot_in_payload = 0
    jito_bundles = 0
    
    print(f"Scanning {jsonl_path} for bot fingerprint...")
    
    with open(jsonl_path, "r", encoding="utf-8") as f:
        for i, line in enumerate(f):
            total_txs += 1
            
            # Simple string search is much faster than JSON parsing for presence check
            has_bot = BOT_ADDRESS in line
            has_jito = any(tip in line for tip in JITO_TIP_ACCOUNTS)
            
            if has_bot:
                bot_in_payload += 1
            
            if has_jito:
                jito_bundles += 1
                
            if i % 5000 == 0 and i > 0:
                print(f"Scanned {i} rows...")
                
    print("\n=========================================")
    print("PHASE 2A - OBSERVABILITY CHECK")
    print("=========================================")
    print(f"Total Deployments Analyzed: {total_txs:,}")
    print(f"Deployments containing target bot address ({BOT_ADDRESS}): {bot_in_payload:,}")
    print(f"Deployments containing Jito tip addresses: {jito_bundles:,}")
    
    if bot_in_payload > 0:
        print("\nCONCLUSION: The bot's buy is INCLUDED in the deployment transaction (likely bundled). We can extract entry size and latency.")
    else:
        print("\nCONCLUSION: The bot's buy is a SEPARATE transaction. It is NOT observable in the deployment payload.")

if __name__ == "__main__":
    analyze_fingerprint()
