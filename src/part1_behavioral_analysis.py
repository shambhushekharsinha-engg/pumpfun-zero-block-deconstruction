import os
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import polars as pl
import seaborn as sns

# -----------------------------------------------------------------------------
# Path Setup
# -----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
EXTRACTED_DIR = PROJECT_ROOT / "data" / "raw" / "extracted"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Set clean aesthetic for Kaggle media gallery charts
plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.size"] = 10


def run_behavioral_analysis():
    print("============================================================")
    print("  PART 1: TARGET BOT BEHAVIORAL ANALYSIS (5brv...LyAr)")
    print("============================================================\n")

    # 1. Load Parquet Data via Polars LazyFrames
    deployments_lf = pl.scan_parquet(EXTRACTED_DIR / "deployments.parquet")
    bot_trades_lf = pl.scan_parquet(EXTRACTED_DIR / "target_bot_trades.parquet")

    # Join bot trades with deployment records to analyze latency and zero-block entry
    df_joined = (
        bot_trades_lf.filter(pl.col("tx_type") == "buy")
        .join(deployments_lf, on="token_address", how="inner", suffix="_deploy")
        .collect()
    )

    total_bought = len(df_joined)
    print(f"[+] Total Tokens Bought Analyzed: {total_bought:,}")

    # -------------------------------------------------------------------------
    # A. ENTRY SIZE METRICS
    # -------------------------------------------------------------------------
    buy_sizes = df_joined["sol_amount"]
    mean_entry = buy_sizes.mean()
    median_entry = buy_sizes.median()
    std_entry = buy_sizes.std()
    min_entry = buy_sizes.min()
    max_entry = buy_sizes.max()

    print("\n--- ENTRY SIZE STATISTICS (SOL) ---")
    print(f"  • Mean Entry Size   : {mean_entry:.4f} SOL")
    print(f"  • Median Entry Size : {median_entry:.4f} SOL")
    print(f"  • Std Dispersion    : {std_entry:.4f} SOL")
    print(f"  • Min / Max Sizing  : {min_entry:.4f} / {max_entry:.4f} SOL")

    # -------------------------------------------------------------------------
    # B. LATENCY & ZERO-BLOCK ANALYSIS
    # -------------------------------------------------------------------------
    df_latency = df_joined.with_columns(
        slot_delta=(pl.col("slot") - pl.col("slot_deploy")),
    )

    zero_block_buys = df_latency.filter(pl.col("slot_delta") == 0)
    zero_block_share = (len(zero_block_buys) / total_bought) * 100

    print("\n--- LATENCY & ZERO-BLOCK SHARE ---")
    print(f"  • Zero-Block Entries (slot_delta == 0) : {len(zero_block_buys):,} ({zero_block_share:.2f}%)")
    print(f"  • Mean Slot Latency                     : {df_latency['slot_delta'].mean():.2f} slots")

    # -------------------------------------------------------------------------
    # C. P&L & WIN/LOSS PERFORMANCE
    # -------------------------------------------------------------------------
    df_all_bot = bot_trades_lf.collect()
    
    # Calculate per-token P&L by summing buy and sell SOL amounts
    df_pnl = (
        df_all_bot.group_by("token_address")
        .agg(
            total_spent=pl.col("sol_amount").filter(pl.col("tx_type") == "buy").sum(),
            total_received=pl.col("sol_amount").filter(pl.col("tx_type") == "sell").sum(),
            tx_count=pl.len(),
        )
        .with_columns(
            net_pnl=pl.col("total_received") - pl.col("total_spent"),
            roi=(pl.col("total_received") - pl.col("total_spent")) / (pl.col("total_spent") + 1e-6)
        )
    )

    wins = df_pnl.filter(pl.col("net_pnl") > 0)
    losses = df_pnl.filter(pl.col("net_pnl") <= 0)

    hit_rate = (len(wins) / len(df_pnl)) * 100 if len(df_pnl) > 0 else 0.0
    avg_win = wins["net_pnl"].mean() if len(wins) > 0 else 0.0
    avg_loss = losses["net_pnl"].mean() if len(losses) > 0 else 0.0
    total_pnl = df_pnl["net_pnl"].sum()

    print("\n--- P&L & PERFORMANCE SUMMARY ---")
    print(f"  • Overall Hit Rate      : {hit_rate:.2f}%")
    print(f"  • Total Net P&L         : {total_pnl:.2f} SOL")
    print(f"  • Average Win           : +{avg_win:.4f} SOL")
    print(f"  • Average Loss          : {avg_loss:.4f} SOL")
    print(f"  • Profit Factor (Win/Loss): {abs(avg_win / avg_loss):.2f}x" if avg_loss != 0 else "N/A")

    # -------------------------------------------------------------------------
    # D. GENERATE KAGGLE MEDIA GALLERY CHARTS
    # -------------------------------------------------------------------------
    print("\n[-->] Generating Media Gallery plots...")

    # Plot 1: Entry Sizing & Latency Distribution
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    sns.histplot(buy_sizes.to_numpy(), ax=axes[0], kde=True, color="#2b5c8f", bins=30)
    axes[0].axvline(mean_entry, color="red", linestyle="--", label=f"Mean: {mean_entry:.2f} SOL")
    axes[0].axvline(median_entry, color="green", linestyle="-.", label=f"Median: {median_entry:.2f} SOL")
    axes[0].set_title("Target Bot Entry Size Distribution (SOL)")
    axes[0].set_xlabel("Entry Size (SOL)")
    axes[0].set_ylabel("Trade Count")
    axes[0].legend()

    # Latency Bar
    sns.countplot(x=df_latency["slot_delta"].to_numpy(), ax=axes[1], palette="crest")
    axes[1].set_title("Entry Latency Relative to Token Deployment (Slots)")
    axes[1].set_xlabel("Slot Delta (0 = Zero Block)")
    axes[1].set_ylabel("Buy Count")

    plt.tight_layout()
    chart1_path = FIGURES_DIR / "part1_entry_sizing_latency.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"  [✓] Saved: {chart1_path.relative_to(PROJECT_ROOT)}")

    # Plot 2: Per-Trade ROI Distribution
    plt.figure(figsize=(9, 5))
    rois = df_pnl["roi"].to_numpy() * 100
    sns.histplot(rois, bins=40, kde=True, color="#107c41")
    plt.axvline(0, color="black", linewidth=1.2, linestyle="--")
    plt.title(f"Target Bot Trade ROI Distribution (Hit Rate: {hit_rate:.1f}%)")
    plt.xlabel("Return on Investment (ROI %)")
    plt.ylabel("Frequency")
    
    chart2_path = FIGURES_DIR / "part1_pnl_distribution.png"
    plt.tight_layout()
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"  [✓] Saved: {chart2_path.relative_to(PROJECT_ROOT)}")

    print("\n[✓] Part 1 Behavioral Analysis Execution Complete!")


if __name__ == "__main__":
    run_behavioral_analysis()