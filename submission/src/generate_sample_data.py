import os
import sys
from pathlib import Path
import numpy as np
import polars as pl

# Project Root Setup
PROJECT_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "extracted"

def generate_synthetic_dataset(
    n_deployments: int = 50_000, 
    bot_buy_ratio: float = 0.0032  # ~0.32% realistic target bot rate
):
    """
    Generates realistic synthetic parquet datasets for testing feature pipelines 
    and backtests locally without loading the 40GB live dataset.
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    np.random.seed(42)

    print(f"[-->] Generating synthetic dataset ({n_deployments:,} deployments)...")

    # 1. Generate Timestamps and Base Keys
    start_slot = 300_000_000
    slots = start_slot + np.sort(np.random.choice(100_000, size=n_deployments, replace=True))
    
    # Generate datetime series
    created_ats = pl.datetime_range(
        start=pl.datetime(2026, 1, 1),
        end=pl.datetime(2026, 2, 1),
        interval="1m",
        eager=True
    ).sample(n_deployments, with_replacement=True)

    token_addresses = [f"Token_{i:06d}_PumpFun" for i in range(n_deployments)]
    deployers = [f"Deployer_{np.random.randint(1, 1000):04d}" for _ in range(n_deployments)]

    # Feature Signals (Dev Buy, Socials, Wallet Age)
    dev_buy_sol = np.random.exponential(scale=0.8, size=n_deployments)
    has_socials = np.random.choice([0, 1], size=n_deployments, p=[0.55, 0.45])
    is_jito_bundle = np.random.choice([0, 1], size=n_deployments, p=[0.70, 0.30])
    deployer_wallet_age_days = np.random.exponential(scale=30.0, size=n_deployments)

    # 2. Deployments DataFrame
    df_deployments = pl.DataFrame({
        "token_address": token_addresses,
        "deployer_address": deployers,
        "slot": slots,
        "created_at": created_ats,
        "dev_buy_sol": dev_buy_sol,
        "has_socials": has_socials,
        "is_jito_bundle": is_jito_bundle,
        "deployer_wallet_age_days": deployer_wallet_age_days,
        "ticker": [f"TICK_{i % 500}" for i in range(n_deployments)],
        "name": [f"Token Name {i}" for i in range(n_deployments)],
    })

    # 3. Simulate Target Bot Logic (Deterministic Probability)
    score = (
        2.0 * ((dev_buy_sol >= 0.4) & (dev_buy_sol <= 3.5)).astype(int) +
        2.5 * has_socials +
        1.5 * is_jito_bundle +
        1.0 * (deployer_wallet_age_days >= 7.0).astype(int) -
        3.5
    )
    probs = 1 / (1 + np.exp(-score))
    
    threshold = np.percentile(probs, (1 - bot_buy_ratio) * 100)
    bought_mask = probs >= threshold
    bought_indices = np.where(bought_mask)[0]

    print(f"[+] Simulated Bot Purchases: {len(bought_indices):,} tokens ({len(bought_indices)/n_deployments*100:.2f}%)")

    # 4. Target Bot Trades Parquet
    bot_trades = []
    for idx_np in bought_indices:
        idx = int(idx_np)  # Cast np.int64 to standard Python int for Polars indexing
        token = token_addresses[idx]
        slot = slots[idx]
        ts = created_ats[idx]
        buy_amount = float(np.random.normal(loc=0.15, scale=0.02)) # Fixed entry sizing ~0.15 SOL
        
        bot_trades.append({
            "token_address": token,
            "trader_address": "5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr",
            "slot": slot, # Zero-block entry
            "timestamp": ts,
            "tx_type": "buy",
            "sol_amount": max(0.05, buy_amount),
            "position_in_block": 1 if is_jito_bundle[idx] else 2
        })

        # Add simulated sell exit (partial / full)
        roi = float(np.random.choice([1.8, -0.9, 0.4, 3.5], p=[0.20, 0.60, 0.10, 0.10]))
        bot_trades.append({
            "token_address": token,
            "trader_address": "5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr",
            "slot": slot + np.random.randint(10, 200),
            "timestamp": ts,
            "tx_type": "sell",
            "sol_amount": max(0.01, buy_amount * (1 + roi)),
            "position_in_block": 5
        })

    df_bot_trades = pl.DataFrame(bot_trades)

    # 5. Bonding Curve Trades Parquet (For Backtest Outcome Evaluation)
    all_trades = []
    for i in range(min(5000, n_deployments)):
        token = token_addresses[i]
        slot = slots[i]
        ts = created_ats[i]
        for step in range(3):
            all_trades.append({
                "token_address": token,
                "slot": slot + step * 2,
                "timestamp": ts,
                "sol_amount": float(np.random.exponential(scale=0.2)),
                "tx_type": "buy" if step < 2 else "sell"
            })
    df_all_trades = pl.DataFrame(all_trades)

    # 6. Save Parquet Files
    deployments_path = OUTPUT_DIR / "deployments.parquet"
    bot_trades_path = OUTPUT_DIR / "target_bot_trades.parquet"
    all_trades_path = OUTPUT_DIR / "pumpfun_trades.parquet"

    df_deployments.write_parquet(deployments_path)
    df_bot_trades.write_parquet(bot_trades_path)
    df_all_trades.write_parquet(all_trades_path)

    print(f"\n[✓] Synthetic Dataset Successfully Created in: {OUTPUT_DIR}")
    print(f"    • deployments.parquet: {deployments_path.stat().st_size / (1024**2):.2f} MB")
    print(f"    • target_bot_trades.parquet: {bot_trades_path.stat().st_size / (1024**2):.2f} MB")
    print(f"    • pumpfun_trades.parquet: {all_trades_path.stat().st_size / (1024**2):.2f} MB")

if __name__ == "__main__":
    generate_synthetic_dataset()