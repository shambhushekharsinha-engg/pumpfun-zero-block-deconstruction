from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import lightgbm as lgb
import numpy as np
import json
import os
from pathlib import Path

app = FastAPI(title="Zero-Block Deconstruction Inference API")

# Load model and threshold at startup
MODEL_DIR = Path(__file__).resolve().parent.parent / "model"
SCORER_PATH = MODEL_DIR / "frozen-scorer.txt"
THRESHOLD_PATH = MODEL_DIR / "threshold.json"

try:
    bst = lgb.Booster(model_file=str(SCORER_PATH))
    with open(THRESHOLD_PATH, "r") as f:
        threshold_data = json.load(f)
        FROZEN_THRESHOLD = threshold_data["threshold"]
except Exception as e:
    bst = None
    FROZEN_THRESHOLD = 0.5
    print(f"Error loading model: {e}")

class FeatureVector(BaseModel):
    past_launches: float
    past_buys: float
    past_sells: float
    past_burns: float
    deployer_age_seconds: float

@app.post("/api/predict")
async def predict(features: FeatureVector):
    if bst is None:
        raise HTTPException(status_code=500, detail="Frozen model not loaded.")
        
    X_input = np.array([[
        features.past_launches,
        features.past_buys,
        features.past_sells,
        features.past_burns,
        features.deployer_age_seconds
    ]])
    
    # Run inference
    prob = float(bst.predict(X_input)[0])
    
    return {
        "probability": prob,
        "top_5_percent": prob >= FROZEN_THRESHOLD,
        "model_version": "v1.0.0-final",
        "policy_version": "top_5_percent"
    }
