import json
import os
from pathlib import Path
from typing import Any, Dict

import requests
import streamlit as st

# -----------------------------------------------------------------------------
# Page Configuration - MUST be first Streamlit command
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered"
)

# -----------------------------------------------------------------------------
# Config
# -----------------------------------------------------------------------------
SCHEMA_PATH = Path("/app/data/data_schema.json")
API_BASE_URL = os.getenv("API_URL", "http://localhost:8000")
PREDICT_ENDPOINT = f"{API_BASE_URL}/predict/single"

# -----------------------------------------------------------------------------
# Load schema from JSON file
# -----------------------------------------------------------------------------
@st.cache_resource
def load_schema(path: Path) -> Dict[str, Any]:
    if not path.exists():
        # Return default schema if file not found
        return {
            "numerical": {
                "age": {"min": 29, "max": 77, "mean": 54.4, "median": 55.0},
                "trestbps": {"min": 94, "max": 200, "mean": 131.6, "median": 130.0},
                "chol": {"min": 126, "max": 564, "mean": 246.3, "median": 240.0},
                "thalach": {"min": 71, "max": 202, "mean": 149.6, "median": 153.0},
                "oldpeak": {"min": 0.0, "max": 6.2, "mean": 1.04, "median": 0.8}
            },
            "categorical": {}
        }
    with open(path, "r") as f:
        return json.load(f)


schema = load_schema(SCHEMA_PATH)
numerical_features = schema.get("numerical", {})
categorical_features = schema.get("categorical", {})

# -----------------------------------------------------------------------------
# Custom CSS
# -----------------------------------------------------------------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #e63946;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #457b9d;
        text-align: center;
        margin-bottom: 2rem;
    }
    .result-positive {
        background-color: #f8d7da;
        border: 2px solid #f5c6cb;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
    .result-negative {
        background-color: #d4edda;
        border: 2px solid #c3e6cb;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Header
# -----------------------------------------------------------------------------
st.markdown('<p class="main-header">❤️ Heart Disease Prediction</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enter patient information to predict heart disease risk</p>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------
# Input Form
# -----------------------------------------------------------------------------
st.header("📋 Patient Information")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Demographics")
    
    age_stats = numerical_features.get("age", {"min": 29, "max": 77, "median": 55})
    age = st.slider(
        "Age (years)",
        min_value=int(age_stats.get("min", 29)),
        max_value=int(age_stats.get("max", 77)),
        value=int(age_stats.get("median", 55)),
        help="Patient's age in years"
    )
    
    sex = st.selectbox(
        "Sex",
        options=[0, 1],
        format_func=lambda x: "Female" if x == 0 else "Male",
        help="Patient's biological sex"
    )
    
    st.subheader("Chest Pain")
    cp = st.selectbox(
        "Chest Pain Type",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "Typical Angina",
            1: "Atypical Angina", 
            2: "Non-anginal Pain",
            3: "Asymptomatic"
        }[x],
        help="Type of chest pain experienced"
    )

with col2:
    st.subheader("Vital Signs")
    
    bp_stats = numerical_features.get("trestbps", {"min": 94, "max": 200, "median": 130})
    trestbps = st.slider(
        "Resting Blood Pressure (mm Hg)",
        min_value=int(bp_stats.get("min", 94)),
        max_value=int(bp_stats.get("max", 200)),
        value=int(bp_stats.get("median", 130)),
        help="Resting blood pressure on admission"
    )
    
    chol_stats = numerical_features.get("chol", {"min": 126, "max": 564, "median": 240})
    chol = st.slider(
        "Serum Cholesterol (mg/dl)",
        min_value=int(chol_stats.get("min", 126)),
        max_value=int(chol_stats.get("max", 564)),
        value=int(chol_stats.get("median", 240)),
        help="Serum cholesterol level"
    )
    
    fbs = st.selectbox(
        "Fasting Blood Sugar > 120 mg/dl",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes",
        help="Whether fasting blood sugar exceeds 120 mg/dl"
    )

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("ECG & Heart Rate")
    
    restecg = st.selectbox(
        "Resting ECG Results",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "Normal",
            1: "ST-T Wave Abnormality",
            2: "Left Ventricular Hypertrophy"
        }[x],
        help="Resting electrocardiographic results"
    )
    
    thalach_stats = numerical_features.get("thalach", {"min": 71, "max": 202, "median": 153})
    thalach = st.slider(
        "Maximum Heart Rate",
        min_value=int(thalach_stats.get("min", 71)),
        max_value=int(thalach_stats.get("max", 202)),
        value=int(thalach_stats.get("median", 153)),
        help="Maximum heart rate achieved during exercise"
    )
    
    exang = st.selectbox(
        "Exercise Induced Angina",
        options=[0, 1],
        format_func=lambda x: "No" if x == 0 else "Yes",
        help="Whether exercise induced angina"
    )

with col4:
    st.subheader("Exercise Test Results")
    
    oldpeak_stats = numerical_features.get("oldpeak", {"min": 0.0, "max": 6.2, "median": 0.8})
    oldpeak = st.slider(
        "ST Depression (oldpeak)",
        min_value=float(oldpeak_stats.get("min", 0.0)),
        max_value=float(oldpeak_stats.get("max", 6.2)),
        value=float(oldpeak_stats.get("median", 0.8)),
        step=0.1,
        help="ST depression induced by exercise relative to rest"
    )
    
    slope = st.selectbox(
        "Slope of Peak Exercise ST",
        options=[0, 1, 2],
        format_func=lambda x: {
            0: "Upsloping",
            1: "Flat",
            2: "Downsloping"
        }[x],
        help="Slope of the peak exercise ST segment"
    )
    
    ca = st.selectbox(
        "Major Vessels Colored by Fluoroscopy",
        options=[0, 1, 2, 3, 4],
        help="Number of major vessels colored (0-4)"
    )
    
    thal = st.selectbox(
        "Thalassemia",
        options=[0, 1, 2, 3],
        format_func=lambda x: {
            0: "Normal",
            1: "Fixed Defect",
            2: "Reversible Defect",
            3: "Unknown"
        }[x],
        help="Thalassemia type"
    )

st.markdown("---")

# -----------------------------------------------------------------------------
# Prediction Button
# -----------------------------------------------------------------------------
if st.button("🔮 Predict Heart Disease Risk", type="primary", use_container_width=True):
    # Prepare payload
    payload = {
        "age": age,
        "sex": sex,
        "cp": cp,
        "trestbps": trestbps,
        "chol": chol,
        "fbs": fbs,
        "restecg": restecg,
        "thalach": thalach,
        "exang": exang,
        "oldpeak": oldpeak,
        "slope": slope,
        "ca": ca,
        "thal": thal
    }
    
    with st.spinner("Analyzing patient data..."):
        try:
            resp = requests.post(PREDICT_ENDPOINT, json=payload, timeout=30)
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Connection error: {e}")
            st.info(f"Make sure the API is running at {API_BASE_URL}")
        else:
            if resp.status_code != 200:
                st.error(f"❌ API error: HTTP {resp.status_code}")
                st.code(resp.text)
            else:
                data = resp.json()
                prediction = data.get("prediction", 0)
                probability = data.get("probability", [0.5, 0.5])
                diagnosis = data.get("diagnosis", "Unknown")
                
                st.markdown("---")
                st.header("📊 Prediction Result")
                
                if prediction == 1:
                    st.markdown(
                        '<div class="result-positive">'
                        '<h2 style="color: #721c24;">⚠️ Heart Disease Risk Detected</h2>'
                        f'<p style="font-size: 1.2rem;">Probability: {probability[1]*100:.1f}%</p>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    st.warning("**Recommendation:** Please consult a cardiologist for further evaluation.")
                else:
                    st.markdown(
                        '<div class="result-negative">'
                        '<h2 style="color: #155724;">✅ No Heart Disease Detected</h2>'
                        f'<p style="font-size: 1.2rem;">Probability of disease: {probability[1]*100:.1f}%</p>'
                        '</div>',
                        unsafe_allow_html=True
                    )
                    st.success("**Result:** Based on the input features, no immediate heart disease risk is detected.")
                
                # Show probability chart
                st.subheader("Probability Distribution")
                col_a, col_b = st.columns(2)
                with col_a:
                    st.metric("No Disease", f"{probability[0]*100:.1f}%")
                with col_b:
                    st.metric("Heart Disease", f"{probability[1]*100:.1f}%")
                
                # Show input summary
                with st.expander("📋 View Input Summary"):
                    st.json(payload)

# -----------------------------------------------------------------------------
# Footer
# -----------------------------------------------------------------------------
st.markdown("---")
st.caption(
    f"🔧 API Endpoint: `{API_BASE_URL}`\n\n"
    "⚠️ **Disclaimer:** This is a machine learning model for educational purposes only. "
    "It should not be used as a substitute for professional medical advice, diagnosis, or treatment."
)
