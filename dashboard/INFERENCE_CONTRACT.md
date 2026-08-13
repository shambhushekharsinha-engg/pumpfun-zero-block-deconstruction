# Inference Contract

## Input
Exactly five point-in-time causal-in-time features, in this order:
1. `past_launches`
2. `past_buys`
3. `past_sells`
4. `past_burns`
5. `deployer_age_seconds`

## Output
- `probability`: Float [0.0, 1.0]
- `top_5_percent`: Boolean (True if probability >= frozen threshold)
- `model_version`: "v1.1.0-final"
- `policy_version`: "top_5_percent"

## Guarantees
- ✓ No training
- ✓ No feature engineering
- ✓ No threshold tuning
- ✓ No competition data
- ✓ No economic prediction
- ✓ No live market information
- ✓ Frozen v1.1.0-final inference artifact (AST-transpiled LightGBM via m2cgen)

## Provenance
`v1.0.0-final` is the historical scientific checkpoint tag. `v1.1.0-final` is
the canonical final submission package, incorporating the dashboard presentation
layer, upgraded CI, and this inference contract. The frozen model scorer
(`predict.py`) and threshold (`0.793`) are identical between both checkpoints.

## Verification
The production AST scorer reproduces the frozen golden inference vectors
with <1e-6 numerical error and 100% classification agreement at the
validation-selected threshold of 0.793.

See: `dashboard/tests/inference_equivalence/test_scorer.py`
