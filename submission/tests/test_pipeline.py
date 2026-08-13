import pytest
import json
from pathlib import Path

MANIFEST_PATH = Path("submission/results/experiment_manifest.json")

def load_manifest():
    with open(MANIFEST_PATH) as f:
        return json.load(f)

def test_manifest_exists():
    """The experiment manifest must be present and parseable."""
    assert MANIFEST_PATH.exists(), f"FAIL: {MANIFEST_PATH} not found"
    manifest = load_manifest()
    assert "experiment_version" in manifest
    assert manifest["experiment_version"] == "v1.1.0-final"

def test_temporal_integrity():
    """Split fractions must be valid and sum to 1.0."""
    manifest = load_manifest()
    split = manifest["split"]
    assert split["strategy"] == "chronological", "Split must be chronological"
    total = split["train"] + split["validation"] + split["test"]
    assert abs(total - 1.0) < 1e-6, f"Split fractions sum to {total}, expected 1.0"
    # Chronological ordering: train < validation < test (no exact timestamps, but fractions are correct)
    assert split["train"] > split["validation"] >= split["test"]

def test_unknown_label_handling():
    """Unknowns must be EXCLUDED, never converted to negatives."""
    manifest = load_manifest()
    ds = manifest["dataset"]
    # Exact accounting
    assert ds["mapped_positive_labels"] == 13818, "Mapped positives mismatch"
    assert ds["unknown_positive_labels"] == 2109, "Unknown count mismatch"
    assert ds["confirmed_negative_labels"] == 395210
    total_universe = ds["mapped_positive_labels"] + ds["unknown_positive_labels"] + ds["confirmed_negative_labels"]
    assert total_universe == 411137, f"Universe total mismatch: {total_universe}"
    # Unknowns must be excluded, not relabeled
    assert "EXCLUDED" in ds["unknown_treatment"].upper(), \
        "FAIL: Unknown labels must be EXCLUDED not treated as negatives"

def test_threshold_selection_source():
    """Threshold must be selected on validation ONLY — no test-set tuning."""
    manifest = load_manifest()
    policy = manifest["policy"]
    assert policy["threshold_source"] == "validation_set_only", \
        "FAIL: Threshold source must be validation_set_only"
    assert policy["test_tuning"] is False, "FAIL: test_tuning must be False"
    assert policy["threshold"] == 0.793

def test_feature_schema():
    """The canonical feature set must match the frozen five features."""
    manifest = load_manifest()
    expected_features = [
        "past_launches", "past_buys", "past_sells",
        "past_burns", "deployer_age_seconds"
    ]
    assert manifest["features"] == expected_features, \
        f"Feature schema mismatch: {manifest['features']}"

def test_no_economic_backtest():
    """Economic P&L backtest status must be NOT_OBSERVABLE."""
    manifest = load_manifest()
    econ = manifest["economic_backtest"]
    assert econ["status"] == "NOT_OBSERVABLE", \
        "FAIL: Economic backtest must be marked NOT_OBSERVABLE"

def test_leakage_adversary():
    """Adversarial: future features (exit_price, future_pl) must be rejected."""
    def check_no_future_features(feature_list):
        forbidden = {"exit_price", "future_pl", "realized_pnl", "holding_time",
                     "sell_timestamp", "profit", "loss"}
        violations = set(feature_list) & forbidden
        if violations:
            raise ValueError(f"FAIL: Future features detected: {violations}")
        return True
    
    # Should pass cleanly
    manifest = load_manifest()
    check_no_future_features(manifest["features"])
    
    # Adversarial injection should raise
    with pytest.raises(ValueError, match="Future features detected"):
        check_no_future_features(["past_launches", "deployer_age_seconds", "exit_price"])
