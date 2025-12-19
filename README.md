# Heart Disease Classification Project

EAS 503 Final Project - Heart Disease Prediction using Machine Learning

## Project Overview

This project implements a complete ML pipeline for heart disease classification that fully meets all final project requirements:

### ✅ Requirements Compliance
- **Classification Problem**: Heart disease prediction (binary classification)
- **Kaggle Dataset**: Downloaded using `kagglehub` (johnsmith88/heart-disease-dataset)
- **Normalized Database**: 3NF PostgreSQL schema on Render with proper foreign keys
- **16 Experiments**: 4 algorithms × 4 conditions (PCA/no-PCA, Optuna/no-Optuna)
- **F1-Score Tracking**: All 16 experiments tracked with F1-scores
- **Dagshub Integration**: MLflow experiment tracking and visualization
- **FastAPI Backend**: RESTful API for model inference
- **Streamlit Frontend**: Interactive web UI for predictions
- **Docker Deployment**: Complete containerized deployment setup

## Dataset

**Heart Disease Dataset** from Kaggle (johnsmith88/heart-disease-dataset)
- **Source**: Downloaded automatically using `kagglehub.dataset_download()`
- **Size**: 1,025 patients
- **Features**: 13 clinical features (age, sex, chest pain, blood pressure, etc.)
- **Target**: Binary classification (0 = No heart disease, 1 = Heart disease)
- **Balance**: ~54% disease cases, ~46% healthy cases

## 16 Experiments Matrix

| Algorithm | No PCA, No Tuning | No PCA + Optuna | PCA, No Tuning | PCA + Optuna |
|-----------|-------------------|-----------------|----------------|--------------|
| Logistic Regression | ✓ | ✓ | ✓ | ✓ |
| Random Forest | ✓ | ✓ | ✓ | ✓ |
| SVM | ✓ | ✓ | ✓ | ✓ |
| XGBoost | ✓ | ✓ | ✓ | ✓ |

## Project Structure

```
.
├── api/
│   ├── app.py                    # FastAPI application
│   ├── classification_pipeline.py # ML pipeline components
│   ├── Dockerfile
│   └── requirements.txt
├── data/
│   ├── heart.csv                 # Raw dataset
│   ├── heart_disease.db          # SQLite database (3NF)
│   └── data_schema.json          # Feature schema for Streamlit
├── models/
│   ├── global_best_model.pkl     # Best model without Optuna
│   ├── global_best_model_optuna.pkl # Best model with Optuna
│   └── *.pkl                     # All 16 trained models
├── notebooks/
│   ├── 01_create_database.ipynb  # Database setup
│   ├── 02_train_model_without_optuna.ipynb  # 8 experiments
│   ├── 03_train_models_with_optuna.ipynb    # 8 experiments
│   └── .env                      # Dagshub credentials (create this)
├── streamlit/
│   ├── app.py                    # Streamlit UI
│   ├── Dockerfile
│   └── requirements.txt
├── classification_pipeline.py    # Shared ML components
├── docker-compose.yml
└── README.md
```

## Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO
```

### 2. Set Up Environment

```bash
# Install dependencies
pip install -r requirements.txt
```

### 3. Set Up Render PostgreSQL Database

1. Create a PostgreSQL database on [Render](https://render.com)
2. Get your database URL from Render dashboard
3. Create `.env` file in project root:

```
DATABASE_URL=postgresql://username:password@host:port/database
MLFLOW_TRACKING_URI=https://dagshub.com/YOUR_USERNAME/YOUR_REPO.mlflow
MLFLOW_TRACKING_USERNAME=YOUR_USERNAME
MLFLOW_TRACKING_PASSWORD=YOUR_TOKEN
```

### 4. Set Up Dagshub (for Experiment Tracking)

1. Create a [Dagshub](https://dagshub.com) account
2. Create a new repository
3. Get your token from: Dagshub → Profile → Settings → Tokens

### 5. Initialize Database

```bash
# Run the database setup script
python setup_render_db.py

# Or run the notebook
jupyter notebook notebooks/01_create_database.ipynb
```

### 6. Run ML Experiments

```bash
# Run 8 experiments without Optuna
jupyter notebook notebooks/02_train_models_without_optuna.ipynb

# Run 8 experiments with Optuna hyperparameter tuning
jupyter notebook notebooks/03_train_models_with_optuna.ipynb

# Or run directly
python run_optuna_experiments.py
```

### 4. Run Locally with Docker

```bash
docker-compose up -d

# Access:
# - Streamlit UI: http://localhost:8501
# - API Docs: http://localhost:8000/docs
```

### 5. Deploy to DigitalOcean

```bash
# Create a Droplet (Ubuntu 22.04, 2GB RAM minimum)

# SSH into the droplet
ssh root@YOUR_DROPLET_IP

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Install Docker Compose
apt install docker-compose -y

# Clone your repository
git clone https://github.com/YOUR_USERNAME/YOUR_REPO.git
cd YOUR_REPO

# Start the application
docker-compose up -d

# Access:
# - Streamlit UI: http://YOUR_DROPLET_IP:8501
# - API: http://YOUR_DROPLET_IP:8000
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API info |
| `/health` | GET | Health check |
| `/predict` | POST | Batch predictions |
| `/predict/single` | POST | Single patient prediction |
| `/docs` | GET | Interactive API docs |

### Example API Request

```bash
curl -X POST "http://localhost:8000/predict/single" \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Grading Checklist

- [x] Classification problem (not regression)
- [x] Normalized database (3NF SQLite)
- [x] 16 experiments (4 algorithms × 4 conditions)
- [x] F1-scores tracked for all experiments
- [x] Dagshub integration for experiment logging
- [x] FastAPI backend for inference
- [x] Streamlit frontend
- [x] Docker + docker-compose deployment
- [x] All models saved

## Technologies Used

- **ML**: scikit-learn, XGBoost, Optuna
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **Database**: SQLite
- **Tracking**: MLflow, Dagshub
- **Deployment**: Docker, Docker Compose

## Author

EAS 503 - Programming and Database Fundamentals for Data Science
University at Buffalo

## Disclaimer

This is a machine learning model for educational purposes only. It should not be used as a substitute for professional medical advice.



