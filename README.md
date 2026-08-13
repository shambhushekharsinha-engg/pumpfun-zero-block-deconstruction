<div align="center">
  <img src="https://pumpfun-zero-block-deconstruction.vercel.app/og-image.png" alt="Zero-Block Deconstruction Dashboard" width="800" />
  
  <br/><br/>
  
  <h1>Zero-Block Deconstruction</h1>
  <p><strong>A Full-Stack Inference Engine Reconstructing Solana Sniper Behavior</strong></p>

  <a href="https://pumpfun-zero-block-deconstruction.vercel.app/"><img src="https://img.shields.io/badge/Live%20Demo-Vercel-000000?style=for-the-badge&logo=vercel" alt="Live Demo on Vercel"></a>
  <a href="https://github.com/shambhushekharsinha-engg/pumpfun-zero-block-deconstruction"><img src="https://img.shields.io/badge/Code-GitHub-181717?style=for-the-badge&logo=github" alt="Source Code"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge" alt="License"></a>

  <br/><br/>
</div>

## 🏆 Hackathon Project Overview

**Zero-Block Deconstruction** is a fully serverless, real-time machine learning dashboard that reverse-engineers the decision policy of a highly successful Solana sniper bot using *only* point-in-time on-chain evidence. 

We transformed 4.9 million raw blockchain events into a singular, highly generalized behavioral fingerprint—and built an ultra-premium, interactive platform to explore the resulting model.

---

## ⚡ Key Features

- **Real-Time Inference Engine**: A custom Next.js `PolicyExplorer` that debounces user input and queries the Python API instantly, providing dynamic feedback on *why* a token would be selected.
- **Dependency-Free Python AST**: The heavy LightGBM machine learning model was compiled down to a pure Python Abstract Syntax Tree (AST), allowing it to run flawlessly on Vercel Serverless Functions with **zero** dependencies (instant cold starts).
- **Leakage Firewall**: Strict chronological isolation boundary guarantees that absolutely no future lookahead data poisoned the model. 
- **Premium UX/UI**: Buttery-smooth `framer-motion` stagger animations, `lucide-react` iconography, and glassmorphism layouts ensure a top-tier visual experience for hackathon judges.

---

## 📊 Scientific Metrics

Because positive prevalence is only ~4.7%, precision-recall evaluation is far more informative than accuracy.

| Metric | Random Baseline | Unseen Deployers (Generalization) |
|---|---|---|
| **PR-AUC** | 0.047 | **0.396** (+8.4x over baseline) |
| **Precision** | N/A | **31.7%** |
| **Target Capture** | N/A | **47.8%** |

The behavioral signal remained predictive on a strictly unseen-deployer cohort, proving the model discovers a generalized rule rather than memorizing identities.

---

## 🖥️ Tech Stack

- **Frontend**: Next.js 14 App Router, React, Tailwind CSS v4, Framer Motion
- **Backend / Edge**: Vercel Serverless Functions, Python `http.server`
- **Machine Learning**: LightGBM (training), `m2cgen` (model-to-code compilation), SHAP (Interpretability)

---

## 📂 Repository Structure

```text
.
├── dashboard/              # The Full-Stack Next.js Application
│   ├── src/app/            # UI Routes, Layouts, and Premium Pages
│   ├── src/components/     # Interactive PolicyExplorer, Navigation, and Framer Motion wrappers
│   └── api/                # Pure Python Dependency-Free Serverless API
├── submission/             # Original Kaggle ML pipeline, notebooks, and models
├── DATA_DICTIONARY.md      # Schema documentation
└── README.md               # You are here
```

## 🚀 Live Demo & Reproduction

Experience the real-time inference engine and the complete scientific narrative at our live deployment:
**👉 [https://pumpfun-zero-block-deconstruction.vercel.app/](https://pumpfun-zero-block-deconstruction.vercel.app/)**

For absolute scientific reproducibility, view our [Reproduction Contract](submission/REPRODUCTION_CONTRACT.md).
