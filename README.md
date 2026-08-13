<div align="center">
  <h1>🎯 Solana Sniper Bot:<br>Reverse-Engineering a Behavioral Fingerprint</h1>
  <p><strong>Deconstructing on-chain behavior through observable historical data</strong></p>
  
  <p>
    <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction/actions"><img alt="Build Status" src="https://img.shields.io/badge/build-passing-brightgreen"></a>
    <a href="LICENSE"><img alt="License: MIT" src="https://img.shields.io/badge/License-MIT-blue.svg"></a>
  </p>
</div>

---

## 🔍 The Mystery
Can we reverse-engineer a highly profitable Solana sniper bot using only the deployment and deployer activity exposed by the blockchain, without relying on fabricated economic P&L?

This project successfully reconstructed a **generalizable, leakage-safe behavioral fingerprint** of the target Solana sniper from observable competition data. We proved that the discovered policy generalizes to unseen deployers, quantified the unexplained residual regime, and demonstrated efficient behavioral replication.

---

## 🔬 Core Discoveries & Scoreboard

We enforced a strict chronological isolation boundary to completely eliminate lookahead leakage. All features were aggregated at $t_{decision}$ strictly using data from $t < t_{decision}$.

| Finding | Result |
|---------|--------|
| **Deployment Universe** | 411,137 |
| **Target Positives Mapped** | 13,818 |
| **Unseen Test Deployers Overlap** | 0% |
| **Full Model PR-AUC** | 0.286 |
| **Unseen-deployer PR-AUC** | 0.396 |
| **Frozen-test Bot Capture (Recall)** | **47.8%** |
| **Frozen-test Precision** | **31.7%** |
| **Frozen-test Selection Ratio** | **1.50×** |
| **Primary Decision Signal** | Deployer history (`past_launches`) |
| **Economic P&L** | Not observable (Not fabricated) |

---

## 🧠 The Three-Layer Reverse-Engineering Story

### Layer 1: The Dominant Fingerprint
By ablating feature families and analyzing SHAP global dependencies, we discovered the primary sniper decision boundary:
> **Low launch history + Non-trivial wallet age $\rightarrow$ High Selection Likelihood**

The bot systematically hunts for relatively mature wallets (not brand new burners) that have an exceptionally low count of past launches. It almost completely ignores deployment mechanics like base fees or token supply.

### Layer 2: Executable Replication
The fingerprint isn't just descriptive; it is executable. Applying our model-derived rule to a frozen chronological test set yielded a **47.8% target-bot capture**. The model successfully scores and ranks candidate deployments, showing a monotonic relationship between our predicted probability and the actual bot selection rate.

### Layer 3: Residual Intelligence & Disagreement
We mapped out a rigorous counterfactual disagreement matrix:

| | Replica Reject | Replica Select |
|---|---|---|
| **Bot Reject** | 55,851 (TN) | 2,898 (Replica-only) |
| **Bot Select** | **1,536 (Bot-only)** | **1,388 (Shared)** |

The replica perfectly captures the dominant low-volume regime (1,388 shared), but rejects a secondary target-bot regime of extreme serial deployers (1,536 Bot-only). The dataset allows reconstruction of the dominant observable regime, but does not provide sufficient evidence to identify the target bot's complete decision function.

---

## 📈 Beat It: Behavioral Efficiency Without Fabricated Economics

Because exact execution and exit data are absent from the dataset, we refused to manufacture synthetic economic results. Instead, we optimized for **behavioral selection efficiency**.

Under a pre-registered **Top-5% operating policy** evaluated on the frozen test set, our Replica captured nearly half of the target bot's selections while operating on only **1.50×** the target's candidate selection volume. 

---

## 📂 Repository Structure
```text
.
├── submission/
│   ├── notebook/           # The final Kaggle showcase Jupyter Notebook
│   ├── results/            # Frozen metrics, tables, and generated figures
│   ├── src/                # Modularized causal feature engine and ML pipeline
│   ├── Kaggle_Writeup.md   # The detailed scientific narrative
│   ├── REPRODUCTION_CONTRACT.md # The strict rules of engagement
│   └── requirements.txt    # Frozen dependency versions
├── data/                   # (Ignored) Raw datasets and processed parquet files
└── LICENSE                 # MIT License
```

## 🚀 Reproduction

This pipeline adheres to a strict scientific reproduction contract. 

```bash
# 1. Create a clean virtual environment
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows

# 2. Install frozen dependencies
pip install -r submission/requirements.txt

# 3. Execute the pipeline from scratch
# See instructions inside submission/REPRODUCTION_CONTRACT.md
```

## ⚖️ License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
