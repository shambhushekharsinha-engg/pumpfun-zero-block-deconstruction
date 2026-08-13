<div align="center">
  <img src="https://pumpfun-zero-block-deconstruction.vercel.app/og-image.png" alt="Zero-Block Deconstruction Dashboard Banner" width="1000" style="border-radius: 12px; box-shadow: 0 0 20px rgba(59,130,246,0.3);" />
  
  <br/><br/>
  
  <h1 style="font-size: 3em; margin-bottom: 0;">Zero-Block Deconstruction</h1>
  <p style="font-size: 1.2em; font-weight: 300; color: #888;"><strong>A Full-Stack Inference Engine Reconstructing Elite Solana Sniper Behavior</strong></p>

  <!-- Navigation Badges -->
  <a href="https://pumpfun-zero-block-deconstruction.vercel.app/"><img src="https://img.shields.io/badge/Live%20Demo-Vercel-000000?style=for-the-badge&logo=vercel" alt="Live Demo on Vercel"></a>
  <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction"><img src="https://img.shields.io/badge/Source%20Code-GitHub-181717?style=for-the-badge&logo=github" alt="Source Code"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-02569B?style=for-the-badge&logo=opensourceinitiative" alt="License"></a>

  <br/><br/>

  <!-- Tech Stack Badges -->
  <img src="https://img.shields.io/badge/Next.js%2014-black?style=flat-square&logo=next.js" alt="Next.js">
  <img src="https://img.shields.io/badge/React%2019-20232A?style=flat-square&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/Tailwind%20CSS%20v4-38B2AC?style=flat-square&logo=tailwind-css&logoColor=white" alt="Tailwind CSS">
  <img src="https://img.shields.io/badge/Framer%20Motion-0055FF?style=flat-square&logo=framer&logoColor=white" alt="Framer Motion">
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=flat-square&logo=typescript&logoColor=white" alt="TypeScript">
  <img src="https://img.shields.io/badge/Python%203.12-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/LightGBM-ff69b4?style=flat-square&logo=jupyter&logoColor=white" alt="LightGBM">
  <img src="https://img.shields.io/badge/Pandas-150458?style=flat-square&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Scikit_Learn-F7931E?style=flat-square&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Vercel%20Edge-000000?style=flat-square&logo=vercel&logoColor=white" alt="Vercel">

  <br/><br/>
</div>

---

## 🏆 Hackathon Executive Summary

**Zero-Block Deconstruction** is an ambitious, full-stack machine learning artifact that successfully reverse-engineers the proprietary decision-making policy of an elite Solana MEV (Maximal Extractable Value) sniper bot. 

In the hyper-competitive landscape of decentralized finance, proprietary algorithmic bots dominate the zero-block (0 latency) transaction space. By transforming over **4.9 million raw on-chain events** into a singular, highly generalized behavioral fingerprint, we proved that it is possible to mathematically deconstruct and replicate a black-box trading algorithm without any access to its source code.

We then took this rigorous data science pipeline and wrapped it in a **world-class, serverless Next.js dashboard**. The resulting platform features a real-time, interactive Inference Engine that allows users to dynamically simulate the bot's decisions directly in the browser—powered by a dependency-free Python Abstract Syntax Tree running at the edge.

---

## 🌌 The Problem Domain: Zero-Block Sniping on Solana

To understand the magnitude of this project, one must understand the environment the target bot operates in.

### 1. The Pump.fun Ecosystem
Solana's token launch ecosystems see thousands of micro-cap tokens deployed daily. The vast majority of these are noise, rug-pulls, or abandoned projects. Identifying the <1% of tokens that will succeed requires analyzing millions of data points across multiple RPC nodes.

### 2. The Zero-Block Holy Grail
The target bot (`5brv79eFZ2rGprXNvqgVJBkBptkkw8GJX1XydJyZLyAr`) is an elite competitor. Our analysis revealed:
- **Absolute Latency Domination**: The bot captures zero-block entries on **100% of its trades** (0 slots of latency between the token deployment and the bot's buy transaction).
- **Rigid Risk Management**: It utilizes a highly consistent entry size (Mean: 0.1499 SOL, Median: 0.1498 SOL).
- **Elite Profitability**: A 38.55% Hit Rate with a 2.10x Profit Factor, yielding 83.92 SOL in net P&L over the simulated period.

**The Challenge:** Could we build a model that predicts *exactly* which tokens this bot will snipe, using only the data available to the bot at the exact millisecond of deployment?

---

## 🛡️ Data Engineering & The Leakage Firewall

In quantitative finance and machine learning, **look-ahead bias (data leakage)** invalidates models. If our model knows a token succeeded *after* it launched, the prediction is meaningless. 

We implemented a strict, impenetrable chronological isolation boundary:
- **The $t_{decision}$ Barrier**: All features passed into the model are aggregated strictly at $t_{decision}$ (the exact block the token was launched). 
- **Causal Validation**: If an on-chain event (a transfer, a burn, a social link update) occurred even one millisecond *after* the sniper bot made its buy transaction, it was ruthlessly purged from the feature space.
- **Unseen Deployer Verification**: We tested the model on a chronologically held-out dataset of tokens launched by deployers the model had *never* seen before, ensuring it learned a generalized behavioral rule, not just memorized wallet addresses.

---

## 🧠 Machine Learning Architecture

### Handling Extreme Class Imbalance
The target bot is highly selective, firing on only **~4.7%** of all token launches. In this extreme class imbalance, standard accuracy is a useless metric (a model that guesses "No" 100% of the time would be 95.3% accurate). 

We utilized a **LightGBM gradient-boosted tree ensemble**, optimizing and evaluating entirely on **Precision-Recall Area Under Curve (PR-AUC)**.

### Model Evaluation & Scientific Metrics

| Metric | Random Baseline | Frozen Model Performance | Unseen Deployers (Generalization) |
|---|---|---|---|
| **PR-AUC** | 0.047 | **0.286** | **0.396** (+8.4x over baseline) |
| **Precision** | N/A | **31.7%** | N/A |
| **Target Capture (Recall)** | N/A | **47.8%** | N/A |
| **Selection Ratio** | N/A | **1.50×** | N/A |

### SHAP Interpretability: Unlocking the Black Box
By feeding our zero-leakage feature space into SHAP (SHapley Additive exPlanations), we extracted the bot's dominant **Decision Policy**. The bot looks for:
1. **Low Prior Launch History**: Pristine developers are favored. Extreme serial deployers are aggressively filtered out.
2. **Established Wallet Age**: Fresh wallets (0 days old) introduce severe noise. The bot waits for wallets that have aged non-trivially on-chain.
3. **Jito Bundle & Socials Interaction**: A massive affinity for tokens launched via Jito MEV bundles that explicitly include social links at launch.

---

## ⚡ Engineering Breakthrough: The AST Transpilation

Deploying heavy machine learning models (like LightGBM) to Serverless environments (like Vercel Edge Functions) is notoriously difficult. Native C++ compilation errors, 100MB+ library sizes, and 5-second cold starts ruin the user experience.

**Our Unorthodox Solution:**
Instead of fighting the cloud environment, we eliminated the dependencies entirely. 
1. We trained the LightGBM model in a local Jupyter environment.
2. We used `m2cgen` (Model-2-Code Generator) to transpile the entire gradient-boosted tree ensemble into a **pure Python Abstract Syntax Tree (AST)** (`predict.py`).
3. We deployed this raw Python file to Vercel Serverless Functions using Python's native standard library `http.server.BaseHTTPRequestHandler`.

**The Result:** 
- **0 Dependencies** (No pandas, numpy, scikit-learn, or lightgbm required on the server).
- **0MB Package Bloat** (We explicitly override Vercel's pip installer with an empty `requirements.txt`).
- **Sub-20ms Cold Starts**, allowing real-time inference directly from the frontend.

---

## 🎨 The Full-Stack Presentation Layer

To present these complex scientific findings, we built a bespoke, visually stunning Next.js application designed to provide a premium SaaS-level user experience.

### 1. Real-Time Debounced Inference Engine (Policy Explorer)
The web dashboard features an interactive **Behavioral Simulator**. As users adjust hypothetical on-chain metrics via custom range sliders, the React frontend automatically debounces the input (150ms) and queries the edge API. The UI responds in real-time, instantly adjusting the Replica Probability score and dynamically generating textual explanations of *why* the model made its decision.

### 2. Next.js 14 & Tailwind CSS v4
The entire frontend is built on the bleeding-edge Next.js App Router, leveraging Tailwind CSS v4 for lightning-fast styling, grid layouts, and extreme mobile responsiveness (fully handling tricky viewport scaling edge cases).

### 3. Glassmorphism & Framer Motion
- **Animations**: Buttery-smooth `framer-motion` staggered entry animations make the data feel alive.
- **Micro-Interactions**: Tabular-number score transitions prevent layout shifting during real-time inference.
- **Design Language**: A cohesive Glassmorphism design system featuring ambient background glows, semi-transparent frosted navbars, and bespoke glowing status badges.

---

## 📂 Comprehensive Directory Structure

The repository is divided into two distinct, modular environments:

```text
.
├── dashboard/                  # 🌐 THE FULL-STACK NEXT.JS APPLICATION
│   ├── src/
│   │   ├── app/                # Next.js App Router (UI Routes, Custom Layouts)
│   │   │   ├── fingerprint/    # Visualizes the SHAP decision policy
│   │   │   ├── interpretability/# Explains the PR-AUC and class imbalance
│   │   │   ├── methodology/    # Documents the Leakage Firewall
│   │   │   └── reproduction/   # Provides the strict scientific reproduction contract
│   │   └── components/         
│   │       ├── PolicyExplorer.tsx # The real-time interactive inference engine
│   │       ├── Navigation.tsx     # Responsive, mobile-friendly frosted header
│   │       └── FadeIn.tsx         # Reusable Framer Motion stagger wrappers
│   ├── api/                    # ⚙️ SERVERLESS EDGE PYTHON API 
│   │   ├── predict.py          # The AST-transpiled LightGBM model (Zero Dependencies)
│   │   └── requirements.txt    # Explicitly empty to force ultra-fast Vercel builds
│   ├── tailwind.config.ts      # Tailwind v4 configuration
│   └── package.json            # React/Next.js/Turbopack dependencies
│
├── submission/                 # 🧠 THE DATA SCIENCE & ML PIPELINE
│   ├── notebook/               # Original Kaggle Jupyter Notebooks containing the EDA
│   ├── src/                    # Modularized causal feature engine
│   ├── tests/                  # Strict reproducibility and leakage tests
│   ├── REPRODUCTION_CONTRACT.md# Strict rules of scientific engagement
│   └── Kaggle_Writeup.md       # Comprehensive statistical deep-dive
│
├── DATA_DICTIONARY.md          # On-chain schema documentation mapping the 4.9M events
└── README.md                   # You are here
```

---

## 🚀 Live Demo & Getting Started

Experience the real-time inference engine and the complete scientific narrative at our live production deployment:
### 👉 **[https://pumpfun-zero-block-deconstruction.vercel.app/](https://pumpfun-zero-block-deconstruction.vercel.app/)**

### Run the Full-Stack App Locally
To run the interactive Next.js dashboard and Python API on your own machine:

```bash
# 1. Clone the repository
git clone https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction.git
cd pumpfun-zero-block-deconstruction/dashboard

# 2. Install modern Node dependencies
npm install

# 3. Boot the Turbopack Development Server
# This launches the Next.js frontend (Port 3000) and the Python API routing backend simultaneously.
npm run dev
```

Visit `http://localhost:3000`. Adjust the sliders in the Policy Explorer, and watch the Next.js client seamlessly POST to your local Python API in real time.

---

## 🔬 Strict Scientific Reproduction Contract

We do not believe in black-box claims. This pipeline adheres to a strict scientific reproduction contract. We explicitly distinguish absence of evidence from negative evidence, and **no execution P&L was fabricated using synthetic assumptions.**

To completely reproduce the machine learning models from scratch using the raw data:

```bash
# 1. Create a clean virtual environment
python -m venv venv
source venv/bin/activate  # Or `venv\Scripts\activate` on Windows

# 2. Install frozen data science dependencies
pip install -r submission/requirements.txt

# 3. Execute the pipeline from scratch
# See detailed execution parameters inside submission/REPRODUCTION_CONTRACT.md
```

---

## 🛣️ Future Roadmap

While the behavioral reconstruction is highly successful, we plan to push the envelope further:
1. **Dynamic Kelly Sizing**: Instead of fixed 0.15 SOL entries, scaling the automated trade sizing logarithmically based on the LightGBM prediction confidence interval.
2. **Geolocated RPC Optimization**: To prevent the 1-2 slot delay penalties inherent in standard Solana infrastructure, deploying the AST-inference engine directly alongside a geolocated Jito validator.
3. **Advanced Graph Theory Features**: Including deep wallet funding graphs (analyzing the exact exchange withdrawal patterns that funded the deployer) computed strictly before $t_{decision}$.

---

## 👨‍💻 Developer Profile

<div align="left">
  <img src="https://img.shields.io/badge/Developer-Shambhu%20Shekhar%20Sinha-0A66C2?style=for-the-badge&logo=linkedin" alt="Shambhu Shekhar Sinha">
</div>

**Shambhu Shekhar Sinha**  
*Full-Stack Engineer & Data Scientist*

Shambhu is a specialized developer operating at the intersection of high-performance web architecture, machine learning, and decentralized finance. Passionate about bringing extreme rigorousness to data science, Shambhu specializes in breaking down complex, black-box algorithmic systems and surfacing those insights through incredibly polished, user-centric web interfaces.

By bridging the gap between heavy backend quantitative analysis and bleeding-edge frontend frameworks (like Next.js and Framer Motion), Shambhu builds applications that don't just process data—they tell a compelling, interactive story.

- **GitHub**: [shambhushekharsinha-engg](https://github.com/shambhushekharsinha-engg)
- **Focus Areas**: Machine Learning, React/Next.js, MEV Architectures, Serverless Edge Computing

---

## ⚖️ License
This project is open-source and licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

<div align="center">
  <br/>
  <i>Built with absolute precision for the frontier of decentralized finance and machine learning.</i>
</div>
