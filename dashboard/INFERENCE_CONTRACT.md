# Inference Contract

## Input
Exactly five features:
- `past_launches`
- `past_buys`
- `past_sells`
- `past_burns`
- `deployer_age_seconds`

## Output
- `probability`: Float [0.0, 1.0]
- `top_5_percent`: Boolean (True if probability >= frozen threshold)
- `model_version`: "v1.0.0-final"
- `policy_version`: "top_5_percent"

## Guarantees
- ✓ No training
- ✓ No feature engineering
- ✓ No threshold tuning
- ✓ No competition data
- ✓ No economic prediction
- ✓ No live market information
- ✓ Frozen v1.0.0 model
