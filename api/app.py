# api/app.py
"""
FastAPI service for Heart Disease Classification.
Loads the trained model and exposes a /predict endpoint.
"""

from pathlib import Path
from typing import Any, Dict, List, Optional

import joblib
import numpy as np
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Import shared pipeline components so unpickling works
from classification_pipeline import (
    build_preprocessing,
    make_estimator_for_name,
    FEATURE_NAMES,
)

# Import database utilities
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from db_utils import get_database_info

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
MODEL_PATH = Path("/app/api/models/global_best_model_optuna.pkl")

app = FastAPI(
    title="Heart Disease Classification API",
    description="FastAPI service for predicting heart disease presence",
    version="1.0.0",
)


# -----------------------------------------------------------------------------
# Load model at startup
# -----------------------------------------------------------------------------
def load_model(path: Path):
    """Load the trained model from disk."""
    if not path.exists():
        raise FileNotFoundError(f"Model file not found: {path}")

    print(f"Loading model from: {path}")
    m = joblib.load(path)
    print("✓ Model loaded successfully!")
    print(f"  Model type: {type(m).__name__}")
    if hasattr(m, "named_steps"):
        print(f"  Pipeline steps: {list(m.named_steps.keys())}")
    return m


try:
    model = load_model(MODEL_PATH)
except Exception as e:
    print(f"✗ ERROR: Failed to load model from {MODEL_PATH}")
    print(f"  Error: {e}")
    raise RuntimeError(f"Failed to load model: {e}")


# -----------------------------------------------------------------------------
# Request / Response Schemas
# -----------------------------------------------------------------------------
class PatientFeatures(BaseModel):
    """Features for a single patient."""
    age: int = Field(..., ge=1, le=120, description="Age in years")
    sex: int = Field(..., ge=0, le=1, description="Sex (0=female, 1=male)")
    cp: int = Field(..., ge=0, le=3, description="Chest pain type (0-3)")
    trestbps: int = Field(..., ge=50, le=250, description="Resting blood pressure (mm Hg)")
    chol: int = Field(..., ge=100, le=600, description="Serum cholesterol (mg/dl)")
    fbs: int = Field(..., ge=0, le=1, description="Fasting blood sugar > 120 mg/dl")
    restecg: int = Field(..., ge=0, le=2, description="Resting ECG results (0-2)")
    thalach: int = Field(..., ge=50, le=250, description="Maximum heart rate achieved")
    exang: int = Field(..., ge=0, le=1, description="Exercise induced angina")
    oldpeak: float = Field(..., ge=0.0, le=10.0, description="ST depression")
    slope: int = Field(..., ge=0, le=2, description="Slope of peak exercise ST segment")
    ca: int = Field(..., ge=0, le=4, description="Number of major vessels (0-4)")
    thal: int = Field(..., ge=0, le=3, description="Thalassemia (0-3)")

    class Config:
        schema_extra = {
            "example": {
                "age": 63,
                "sex": 1,
                "cp": 3,
                "trestbps": 145,
                "chol": 233,
                "fbs": 1,
                "restecg": 0,
                "thalach": 150,
                "exang": 0,
                "oldpeak": 2.3,
                "slope": 0,
                "ca": 0,
                "thal": 1
            }
        }


class PredictRequest(BaseModel):
    """Prediction request with list of patient instances."""
    instances: List[Dict[str, Any]]

    class Config:
        schema_extra = {
            "example": {
                "instances": [
                    {
                        "age": 63, "sex": 1, "cp": 3, "trestbps": 145, "chol": 233,
                        "fbs": 1, "restecg": 0, "thalach": 150, "exang": 0,
                        "oldpeak": 2.3, "slope": 0, "ca": 0, "thal": 1
                    }
                ]
            }
        }


class PredictionResult(BaseModel):
    """Result for a single prediction."""
    prediction: int = Field(..., description="0 = No heart disease, 1 = Heart disease")
    probability: List[float] = Field(..., description="[prob_no_disease, prob_disease]")
    diagnosis: str = Field(..., description="Human-readable diagnosis")


class PredictResponse(BaseModel):
    """Response with predictions for all instances."""
    predictions: List[PredictionResult]
    count: int

    class Config:
        schema_extra = {
            "example": {
                "predictions": [
                    {
                        "prediction": 1,
                        "probability": [0.25, 0.75],
                        "diagnosis": "Heart Disease Detected"
                    }
                ],
                "count": 1,
            }
        }


# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "name": "Heart Disease Classification API",
        "version": "1.0.0",
        "description": "Predicts presence of heart disease based on patient features",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "docs": "/docs",
        },
    }


@app.get("/health")
def health() -> Dict[str, str]:
    db_info = get_database_info()
    return {
        "status": "healthy",
        "model_loaded": str(model is not None),
        "model_path": str(MODEL_PATH),
        "database_type": db_info.get("type", "Unknown"),
        "database_location": db_info.get("location", "Unknown"),
    }


@app.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    """
    Predict heart disease for one or more patients.
    
    Returns prediction (0/1), probability, and diagnosis string.
    """
    if not request.instances:
        raise HTTPException(
            status_code=400,
            detail="No instances provided. Please provide at least one instance.",
        )

    try:
        X = pd.DataFrame(request.instances)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid input format. Could not convert to DataFrame: {e}",
        )

    # Check required columns
    required_columns = FEATURE_NAMES
    missing = set(required_columns) - set(X.columns)
    if missing:
        raise HTTPException(
            status_code=400,
            detail=f"Missing required columns: {sorted(missing)}",
        )

    # Reorder columns to match training order
    X = X[required_columns]

    try:
        # Get predictions
        preds = model.predict(X)
        
        # Get probabilities if available
        if hasattr(model, "predict_proba"):
            probas = model.predict_proba(X)
        else:
            # Fallback for models without predict_proba
            probas = np.zeros((len(preds), 2))
            for i, p in enumerate(preds):
                probas[i] = [1 - p, p]
                
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model prediction failed: {e}",
        )

    # Build response
    results = []
    for i in range(len(preds)):
        pred = int(preds[i])
        proba = probas[i].tolist()
        diagnosis = "Heart Disease Detected" if pred == 1 else "No Heart Disease"
        
        results.append(PredictionResult(
            prediction=pred,
            probability=proba,
            diagnosis=diagnosis
        ))

    return PredictResponse(predictions=results, count=len(results))


@app.post("/predict/single")
def predict_single(patient: PatientFeatures) -> PredictionResult:
    """
    Predict heart disease for a single patient with validated input.
    """
    # Convert to dict and create DataFrame
    features = patient.dict()
    X = pd.DataFrame([features])
    X = X[FEATURE_NAMES]

    try:
        pred = int(model.predict(X)[0])
        
        if hasattr(model, "predict_proba"):
            proba = model.predict_proba(X)[0].tolist()
        else:
            proba = [1 - pred, pred]
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model prediction failed: {e}",
        )

    diagnosis = "Heart Disease Detected" if pred == 1 else "No Heart Disease"
    
    return PredictionResult(
        prediction=pred,
        probability=proba,
        diagnosis=diagnosis
    )


@app.on_event("startup")
async def startup_event():
    print("\n" + "=" * 80)
    print("Heart Disease Classification API - Starting Up")
    print("=" * 80)
    print(f"Model path: {MODEL_PATH}")
    print(f"Model loaded: {model is not None}")
    print(f"Features: {FEATURE_NAMES}")
    print("API is ready to accept requests!")
    print("=" * 80 + "\n")
