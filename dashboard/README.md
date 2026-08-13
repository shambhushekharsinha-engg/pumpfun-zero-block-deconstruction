# Zero-Block Deconstruction — Dashboard

The interactive research presentation layer for the Zero-Block Deconstruction project.

## Purpose

This Next.js application serves as the **research artifact dashboard** for the Kaggle competition submission. It allows judges and reviewers to:

- Explore the dominant behavioral fingerprint identified by the model
- Simulate the frozen replica's decisions using a real-time inference engine
- Understand the scientific methodology, evidence boundaries, and reproducibility contract

## Architecture

```
dashboard/
├── src/app/                # Next.js App Router pages
│   ├── page.tsx            # Homepage: Policy Explorer + Evidence Summary
│   ├── methodology/        # Leakage firewall & point-in-time construction
│   ├── fingerprint/        # SHAP-derived behavioral fingerprint
│   ├── interpretability/   # PR-AUC, class imbalance, model evaluation
│   └── reproduction/       # Scientific reproduction contract
├── src/components/
│   ├── PolicyExplorer.tsx  # Real-time debounced inference simulator
│   ├── Navigation.tsx      # Responsive frosted-glass header
│   ├── FadeIn.tsx          # Framer Motion stagger wrappers
│   └── EvidenceBadge.tsx   # Observable/unobservable evidence markers
├── api/
│   └── predict.py          # Dependency-free AST-transpiled LightGBM scorer
├── model/
│   ├── feature_schema.json # Frozen feature order (5 causal-in-time features)
│   ├── threshold.json      # Validation-selected operating threshold (0.793)
│   └── golden_predictions.json  # Golden inference set for CI verification
└── tests/
    └── inference_equivalence/
        └── test_scorer.py  # Golden inference + feature order verification
```

## Frozen Inference Contract

The dashboard's `/api/predict` endpoint enforces a strict contract:

| Property | Value |
|---|---|
| **Model** | LightGBM (transpiled to pure Python AST via m2cgen) |
| **Input Features** | 5 causal-in-time features (see `model/feature_schema.json`) |
| **Threshold** | 0.793 (selected on validation set only) |
| **Dependencies** | Zero (no pandas, numpy, scikit-learn, or lightgbm) |
| **No Training** | Model is frozen. No learning occurs at inference time. |
| **No Economic Prediction** | Realized P&L is not observable from the dataset. |
| **Version** | v1.1.0-final |

## Local Development

```bash
# Install dependencies
npm install

# Start development server (Next.js + Python API routing)
npm run dev

# Visit http://localhost:3000
```

## Running Tests

```bash
# Dashboard golden inference test (requires Python + numpy)
pytest tests/ -v

# Production build verification
npm run build
```

## Scientific Limitations

This dashboard is a **research presentation tool**, not a live trading system.

- The model is frozen. Adjust sliders to explore existing learned behavior.
- All observable signals are point-in-time on-chain features only.
- The simulator does not predict economic outcomes (P&L, entry size, exit timing).
- The classification threshold (0.793) was selected on the validation set before the test set was ever examined.
