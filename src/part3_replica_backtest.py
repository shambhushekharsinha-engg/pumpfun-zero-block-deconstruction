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
DATA_DIR = PROJECT_ROOT / "data"
PROCESSED_DIR = DATA_DIR / "processed"
EXTRACTED_DIR = DATA_DIR / "raw" / "extracted"
FIGURES_DIR = PROJECT_ROOT / "outputs" / "figures"
FIGURES_DIR.mkdir(parents=True, exist_ok=True)

# Plotting aesthetics
plt.style.use("seaborn-v0_8-darkgrid" if "seaborn-v0_8-darkgrid" in plt.style.available else "default")


def run_replica_backtest():
    print("============================================================")
    print("  PART 3: REPLICA STRATEGY & BACKTEST ENGINE")
    print("============================================================\n")

    # 1. Load Processed Test Predictions and Trades
    test_preds_path = PROCESSED_DIR / "test_predictions.parquet"
    bot_trades_path = EXTRACTED_DIR / "target_bot_trades.parquet"

    if not test_preds_path.exists():
        raise FileNotFoundError("Missing test_predictions.parquet. Run part2_feature_engineering.py first.")

    df_test = pl.read_parquet(test_preds_path)
    df_bot_trades = pl.read_parquet(bot_trades_path)

    # Compute target bot ground-truth outcomes on test split
    bot_outcomes = (
        df_bot_trades.group_by("token_address")
        .agg(
            spent=pl.col("sol_amount").filter(pl.col("tx_type") == "buy").sum(),
            received=pl.col("sol_amount").filter(pl.col("tx_type") == "sell").sum(),
        )
        .with_columns(
            net_pnl=pl.col("received") - pl.col("spent"),
            roi=(pl.col("received") - pl.col("spent")) / (pl.col("spent") + 1e-6)
        )
    )

    # Join predictions with ground-truth trade outcomes
    df_eval = df_test.join(bot_outcomes, on="token_address", how="left").fill_null(0.0)

    # -------------------------------------------------------------------------
    # 2. REPLICA STRATEGY DEFINITION & ENTRY SCORING
    # -------------------------------------------------------------------------
    # Operating point threshold (e.g. Prob >= 0.70)
    SCORE_THRESHOLD = 0.70
    FIXED_ENTRY_SOL = 0.15 # Fixed sizing matching target bot

    df_eval = df_eval.with_columns(
        replica_signal=(pl.col("pred_prob") >= SCORE_THRESHOLD).cast(pl.Int32)
    )

    # -------------------------------------------------------------------------
    # 3. BACKTEST SIMULATION WITH SLOT-DELAY SENSITIVITY
    # -------------------------------------------------------------------------
    def simulate_strategy(df_data, slot_delay=0):
        """
        Simulates entry execution with slippage penalties for 1-2 slot delays.
        Solana zero-block price impact increases rapidly with delayed slots.
        """
        entries = df_data.filter(pl.col("replica_signal") == 1)
        if len(entries) == 0:
            return {"Delay": slot_delay, "Trades": 0, "ROI": 0.0, "Hit_Rate": 0.0, "P&L": 0.0, "Max_DD": 0.0}

        # Slippage penalty per slot delay (15% per delayed slot)
        slippage_factor = 1.0 + (0.15 * slot_delay)
        
        # Calculate adjusted ROI and net P&L
        base_rois = entries["roi"].to_numpy()
        adjusted_rois = ((1.0 + base_rois) / slippage_factor) - 1.0
        pnl_sol = adjusted_rois * FIXED_ENTRY_SOL

        cum_pnl = np.cumsum(pnl_sol)
        cum_max = np.maximum.accumulate(cum_pnl)
        drawdowns = cum_pnl - cum_max
        max_dd = drawdowns.min() if len(drawdowns) > 0 else 0.0

        hit_rate = (adjusted_rois > 0).mean() * 100
        total_pnl = pnl_sol.sum()
        avg_roi = adjusted_rois.mean() * 100

        return {
            "Slot Delay": f"{slot_delay} Slot(s)",
            "Trades": len(entries),
            "Hit Rate": f"{hit_rate:.2f}%",
            "Avg ROI": f"{avg_roi:.2f}%",
            "Total P&L": f"{total_pnl:.2f} SOL",
            "Max Drawdown": f"{max_dd:.2f} SOL",
            "pnl_series": cum_pnl
        }

    # Run simulations across 0, 1, and 2 slot delays
    res_delay_0 = simulate_strategy(df_eval, slot_delay=0)
    res_delay_1 = simulate_strategy(df_eval, slot_delay=1)
    res_delay_2 = simulate_strategy(df_eval, slot_delay=2)

    # -------------------------------------------------------------------------
    # 4. HEAD-TO-HEAD COMPARISON MATRIX VS TARGET BOT
    # -------------------------------------------------------------------------
    bot_entries = df_eval.filter(pl.col("target_bot_bought") == 1)
    replica_entries = df_eval.filter(pl.col("replica_signal") == 1)

    # Overlap Metrics (Precision / Recall of Replica vs Bot)
    overlap_count = df_eval.filter(
        (pl.col("target_bot_bought") == 1) & (pl.col("replica_signal") == 1)
    ).height

    replica_precision = (overlap_count / len(replica_entries) * 100) if len(replica_entries) > 0 else 0.0
    replica_recall = (overlap_count / len(bot_entries) * 100) if len(bot_entries) > 0 else 0.0

    print("--- REPLICA OVERLAP WITH TARGET BOT ---")
    print(f"  • Replica Total Entries  : {len(replica_entries):,}")
    print(f"  • Target Bot Entries     : {len(bot_entries):,}")
    print(f"  • Overlapping Entries    : {overlap_count:,}")
    print(f"  • Replica Precision      : {replica_precision:.2f}% (Share of Replica buys taken by Bot)")
    print(f"  • Replica Recall         : {replica_recall:.2f}% (Share of Bot buys captured by Replica)")

    print("\n--- SLOT DELAY SENSITIVITY BACKTEST RESULTS ---")
    bt_summary = pl.DataFrame([
        {k: v for k, v in res_delay_0.items() if k != "pnl_series"},
        {k: v for k, v in res_delay_1.items() if k != "pnl_series"},
        {k: v for k, v in res_delay_2.items() if k != "pnl_series"},
    ])
    print(bt_summary)

    # -------------------------------------------------------------------------
    # 5. EQUITY CURVE COMPARISON CHART
    # -------------------------------------------------------------------------
    plt.figure(figsize=(12, 6))
    if len(res_delay_0.get("pnl_series", [])) > 0:
        plt.plot(res_delay_0["pnl_series"], label="Replica Strategy (0 Slot Delay / Zero Block)", color="#107c41", linewidth=2)
        plt.plot(res_delay_1["pnl_series"], label="Replica Strategy (1 Slot Delay)", color="#d97706", linestyle="--")
        plt.plot(res_delay_2["pnl_series"], label="Replica Strategy (2 Slot Delay)", color="#dc2626", linestyle=":")

    plt.title("Backtest Cumulative P&L Equity Curve & Slot Delay Sensitivity")
    plt.xlabel("Trade Number")
    plt.ylabel("Cumulative Net P&L (SOL)")
    plt.legend()
    plt.tight_layout()

    chart_path = FIGURES_DIR / "part3_equity_curve.png"
    plt.savefig(chart_path, dpi=300)
    plt.close()
    print(f"\n  [✓] Saved Equity Curve Chart: {chart_path.relative_to(PROJECT_ROOT)}")

    print("\n[✓] Part 3 Replica Backtest Execution Complete!")


if __name__ == "__main__":
    run_replica_backtest()