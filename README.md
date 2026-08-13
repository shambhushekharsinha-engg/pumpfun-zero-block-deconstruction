<div align="center">
  <img src="https://pumpfun-zero-block-deconstruction.vercel.app/og-image.png" alt="Zero-Block Deconstruction Dashboard" width="1000" />
  
  <br/><br/>
  
  <h1>Zero-Block Deconstruction</h1>
  <p><strong>A Full-Stack Inference Engine Reconstructing Solana Sniper Behavior</strong></p>

  <a href="https://pumpfun-zero-block-deconstruction.vercel.app/"><img src="https://img.shields.io/badge/Live%20Demo-Vercel-000000?style=for-the-badge&logo=vercel" alt="Live Demo on Vercel"></a>
  <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction"><img src="https://img.shields.io/badge/Code-GitHub-181717?style=for-the-badge&logo=github" alt="Source Code"></a>
  <a href="https://nextjs.org/"><img src="https://img.shields.io/badge/Frontend-Next.js%2014-black?style=for-the-badge&logo=next.js" alt="Next.js"></a>
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Backend-Python%20AST-blue?style=for-the-badge&logo=python" alt="Python"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>

  <br/><br/>
</div>

## 🏆 Hackathon Project Overview

**Zero-Block Deconstruction** is a fully serverless, real-time machine learning dashboard that reverse-engineers the decision policy of a highly successful Solana sniper bot using *only* point-in-time on-chain evidence. 

In the hyper-competitive landscape of Solana MEV (Maximal Extractable Value) and token sniping, proprietary algorithmic bots dominate the zero-block (0 latency) transaction space. This project proves that we can mathematically deconstruct and replicate an elite sniper bot's exact decision-making process without any access to its private source code. 

We transformed 4.9 million raw blockchain events into a singular, highly generalized behavioral fingerprint—and built an ultra-premium, interactive platform to explore the resulting model.

---

## ⚡ Core Features & Engineering Breakthroughs

### 1. Real-Time Debounced Inference Engine
The web dashboard features an interactive **Behavioral Simulator** (Policy Explorer). As you adjust hypothetical on-chain metrics (like a deployer's past token launches and wallet age), the React frontend automatically debounces your input (150ms) and queries the edge API. 

The inference engine responds in real-time, instantly adjusting the Replica Probability score and dynamically generating textual explanations of *why* the model made its decision.

### 2. Dependency-Free Python AST (Abstract Syntax Tree)
Deploying heavy machine learning models (like LightGBM or XGBoost) to Serverless environments (like Vercel Edge Functions) usually fails due to massive library sizes and native C++ compilation errors. 

**Our Solution:** We transpiled the entire LightGBM gradient-boosted tree ensemble into a **pure Python Abstract Syntax Tree (`predict.py`)** using `m2cgen`. 
- **Zero external dependencies** (No pandas, numpy, scikit-learn, or lightgbm required on the server).
- **Instant Cold Starts**: The API utilizes Python's native `http.server.BaseHTTPRequestHandler`, allowing the model to boot and score vectors in less than 20 milliseconds on Vercel's Edge network.

### 3. Absolute Zero-Leakage Firewall
In quantitative finance, look-ahead bias (data leakage) invalidates models. We implemented a strict chronological isolation boundary. All features passed into the Vercel API are aggregated strictly at $t_{decision}$ using data from $t < t_{decision}$. If an on-chain event occurred even one millisecond after the sniper bot made its buy transaction, it is rigorously excluded from the feature space.

### 4. Premium Next.js 14 Presentation Layer
Hackathon projects often neglect UX. We built a visually stunning, deeply interactive artifact using:
- **Next.js App Router & Tailwind CSS v4** for extreme performance and fluid mobile responsiveness.
- **Framer Motion** for buttery-smooth staggered entry animations and tabular-number score transitions.
- **Lucide-React** for crisp, scalable iconography.
- **Glassmorphism Design System** featuring ambient background glows, semi-transparent frosted navbars, and bespoke glowing badges for classification outputs.

---

## 🔬 Scientific Discovery: The Target's Behavioral Fingerprint

The target bot (`5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr`) is an elite competitor:
- **Speed**: Captures zero-block entries on 100% of its trades.
- **Sizing**: Highly rigid entry sizing (Mean: 0.1499 SOL, Median: 0.1498 SOL).
- **Profitability**: 38.55% Hit Rate with a 2.10x Profit Factor.

By feeding our clean, zero-leakage feature space into SHAP (SHapley Additive exPlanations), we successfully extracted the bot's dominant **Decision Policy**:
1. **Low Prior Launch History**: The bot heavily targets pristine developers. Extreme serial deployers are aggressively filtered out.
2. **Established Wallet Age**: Fresh wallets (0 days old) introduce severe noise. The bot waits for wallets that have aged non-trivially on-chain to confirm authenticity.
3. **Jito Bundle & Socials Interaction**: The bot exhibits a high affinity for tokens launched via Jito MEV bundles that explicitly include social links.

---

## 📊 Model Evaluation & Metrics

Because the baseline positive prevalence of the target bot firing is only **~4.7%**, standard accuracy is a useless metric. We evaluated the model using Precision-Recall Area Under Curve (PR-AUC) on a strictly chronological 75/25 train-test split.

| Metric | Random Baseline | Frozen Model Performance | Unseen Deployers (Generalization) |
|---|---|---|---|
| **PR-AUC** | 0.047 | **0.286** | **0.396** (+8.4x over baseline) |
| **Precision** | N/A | **31.7%** | N/A |
| **Target Capture (Recall)** | N/A | **47.8%** | N/A |
| **Selection Ratio** | N/A | **1.50×** | N/A |

Crucially, the behavioral signal remained highly predictive on a strictly unseen-deployer cohort, proving that our Next.js Inference Engine has discovered a generalized rule rather than just memorizing specific wallet identities.

---

## 🏗️ Technical Architecture & Directory Structure

The repository is divided into two major macro-environments: The Full-Stack Application and the Data Science Pipeline.

```text
.
├── dashboard/                  # 🌐 THE FULL-STACK NEXT.JS APPLICATION
│   ├── src/app/                # UI Routes, Custom Layouts, and Sub-pages
│   ├── src/components/         # Interactive PolicyExplorer & Framer Motion wrappers
│   ├── api/                    # ⚙️ Serverless Edge Python API 
│   │   ├── predict.py          # The AST-transpiled LightGBM model
│   │   └── requirements.txt    # Explicitly empty to force 0-dependency builds
│   ├── tailwind.config.ts      # Tailwind v4 configuration
│   └── package.json            # React/Next.js dependencies
│
├── submission/                 # 🧠 THE DATA SCIENCE & ML PIPELINE
│   ├── notebook/               # Original Kaggle Jupyter Notebooks
│   ├── src/                    # Modularized causal feature engine
│   ├── tests/                  # Strict reproducibility and leakage tests
│   ├── REPRODUCTION_CONTRACT.md# Strict rules of scientific engagement
│   └── Kaggle_Writeup.md       # Comprehensive statistical deep-dive
│
├── DATA_DICTIONARY.md          # On-chain schema documentation
└── README.md                   # You are here
```

---

## 🚀 Getting Started & Local Development

Want to run the interactive Next.js dashboard and Python API on your own machine?

### 1. Clone the Repository
```bash
git clone https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction.git
cd pumpfun-zero-block-deconstruction/dashboard
```

### 2. Install Node Dependencies
We use modern npm and Turbopack for lightning-fast frontend compilation.
```bash
npm install
```

### 3. Run the Development Server
This will simultaneously launch the Next.js frontend on port 3000, and the Python API routing backend!
```bash
npm run dev
```

Visit `http://localhost:3000` in your browser. As you adjust the sliders in the Policy Explorer, you will see the Next.js client seamlessly POSTing to your local Python API.

---

## ⚖️ Scientific Integrity & License

This pipeline adheres to a strict scientific reproduction contract. We explicitly distinguish absence of evidence from negative evidence, and no execution P&L was fabricated using synthetic assumptions. 

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

<div align="center">
  <br/>
  <i>Built for the frontier of decentralized finance and machine learning.</i>
</div>
