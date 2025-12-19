# classification_pipeline.py
"""
Shared ML pipeline components for the Heart Disease Classification project.

This module holds all custom transformers and helper functions that are used
both in training and in inference (FastAPI app), so that joblib pickles
refer to a stable module path: `classification_pipeline.<name>`.
"""

import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.preprocessing import StandardScaler

# Classification models
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier


# =============================================================================
# Building blocks for preprocessing
# =============================================================================

# Standard numerical pipeline
num_pipeline = make_pipeline(
    SimpleImputer(strategy="median"),
    StandardScaler(),
)


def build_preprocessing():
    """
    Return the ColumnTransformer preprocessing for heart disease classification.
    
    Features:
    - Numerical: age, trestbps, chol, thalach, oldpeak
    - Categorical (treated as numerical): sex, cp, fbs, restecg, exang, slope, ca, thal
    
    All features are scaled using StandardScaler after imputation.
    """
    # All features in the heart disease dataset
    all_features = [
        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
        'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
    ]
    
    preprocessing = ColumnTransformer(
        [
            ("num", num_pipeline, all_features),
        ],
        remainder='drop',  # Drop any extra columns like patient_id
    )
    return preprocessing


# =============================================================================
# Estimator factory for classification models
# =============================================================================

def make_estimator_for_name(name: str):
    """
    Given a model name, return an unconfigured classifier instance.
    
    Supported models:
    - logistic: LogisticRegression
    - randomforest: RandomForestClassifier
    - svm: SVC with probability=True
    - xgboost: XGBClassifier
    """
    if name == "logistic":
        return LogisticRegression(
            random_state=42,
            max_iter=1000,
            solver='lbfgs',
        )
    elif name == "randomforest":
        return RandomForestClassifier(
            random_state=42,
            n_estimators=100,
            max_depth=10,
            n_jobs=-1,
        )
    elif name == "svm":
        return SVC(
            random_state=42,
            kernel='rbf',
            probability=True,  # Enable predict_proba
        )
    elif name == "xgboost":
        return XGBClassifier(
            objective="binary:logistic",
            random_state=42,
            n_estimators=100,
            learning_rate=0.1,
            max_depth=6,
            use_label_encoder=False,
            eval_metric='logloss',
            n_jobs=-1,
        )
    else:
        raise ValueError(f"Unknown model name: {name}. Supported: logistic, randomforest, svm, xgboost")


# =============================================================================
# Feature names for the heart disease dataset
# =============================================================================

FEATURE_NAMES = [
    'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 
    'restecg', 'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
]

TARGET_NAME = 'target'

# Feature descriptions for documentation
FEATURE_DESCRIPTIONS = {
    'age': 'Age in years',
    'sex': 'Sex (0=female, 1=male)',
    'cp': 'Chest pain type (0-3)',
    'trestbps': 'Resting blood pressure (mm Hg)',
    'chol': 'Serum cholesterol (mg/dl)',
    'fbs': 'Fasting blood sugar > 120 mg/dl (0=false, 1=true)',
    'restecg': 'Resting ECG results (0-2)',
    'thalach': 'Maximum heart rate achieved',
    'exang': 'Exercise induced angina (0=no, 1=yes)',
    'oldpeak': 'ST depression induced by exercise',
    'slope': 'Slope of peak exercise ST segment (0-2)',
    'ca': 'Number of major vessels colored by fluoroscopy (0-4)',
    'thal': 'Thalassemia (0-3)',
}


# =============================================================================
# Utility functions
# =============================================================================

def get_model_names():
    """Return list of supported model names."""
    return ["logistic", "randomforest", "svm", "xgboost"]


def create_full_pipeline(model_name: str, use_pca: bool = False, pca_components: float = 0.95):
    """
    Create a complete pipeline with preprocessing and model.
    
    Args:
        model_name: Name of the model (logistic, randomforest, svm, xgboost)
        use_pca: Whether to include PCA in the pipeline
        pca_components: Number of components or variance ratio for PCA
    
    Returns:
        sklearn Pipeline
    """
    preprocessing = build_preprocessing()
    estimator = make_estimator_for_name(model_name)
    
    if use_pca:
        return make_pipeline(
            preprocessing,
            PCA(n_components=pca_components),
            estimator
        )
    else:
        return make_pipeline(
            preprocessing,
            estimator
        )



