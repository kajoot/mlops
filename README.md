# Iris Classification MLOps Project

## 📋 Project Overview

This project implements a complete MLOps workflow for UCI Iris dataset classification using **Logistic Regression** and **SVM** as baseline models. The project demonstrates industry-standard ML operations practices including:

- ✅ Code versioning with Git
- ✅ Data versioning with DVC
- ✅ Experiment tracking with MLflow
- ✅ Pipeline orchestration with ZenML
- ✅ Hyperparameter optimization with Optuna
- ✅ Containerization with Docker
- ✅ API serving with FastAPI
- ✅ CI/CD with GitLab CI

## 🏗️ Project Structure

```
mlops/
├── .dvc/                      # DVC configuration
├── .gitlab-ci.yml             # GitLab CI/CD pipeline
├── api/                       # FastAPI inference service
│   └── main.py
├── data/                      # Dataset (DVC tracked)
│   ├── train.csv.dvc
│   └── test.csv.dvc
├── docker-compose.yml         # Docker Compose configuration
├── Dockerfile.api             # Dockerfile for API serving
├── Dockerfile.train           # Dockerfile for training
├── models/                    # Trained models
├── pipelines/                 # ZenML pipelines
│   └── training_pipeline.py
├── requirements.txt           # Python dependencies
└── src/                       # Source code
    ├── data_loader.py         # Data loading utilities
    ├── optimize.py            # Optuna optimization
    └── train.py               # Training scripts with MLflow
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.12+
- Docker & Docker Compose
- Git
- Virtual environment

### 2. Setup Environment

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
```

### 3. Data Versioning with DVC

```bash
# Initialize DVC (already done)
dvc init

# Setup DVC remote
dvc remote add -d local ./dvc_remote

# Pull data from remote
dvc pull

# Generate data if not exists
python src/data_loader.py
```

### 4. Train Baseline Models

#### Start MLflow Server

```bash
# Start MLflow tracking server
mlflow server --backend-store-uri file:///$(pwd)/mlruns \
              --default-artifact-root file:///$(pwd)/mlartifacts \
              --host 0.0.0.0 --port 5000
```

Visit MLflow UI at: http://localhost:5000

#### Train Models with MLflow Tracking

```bash
# Train both baseline models
python src/train.py

# Results:
# - Logistic Regression: ~97% accuracy
# - SVM: ~97% accuracy
# - Models saved to models/
# - Experiments logged to MLflow
```

### 5. Hyperparameter Optimization with Optuna

```bash
# Optimize Logistic Regression
python src/optimize.py --model logistic_regression --n-trials 10

# Optimize SVM
python src/optimize.py --model svm --n-trials 10

# Results logged to MLflow experiment 'iris-classification-optimized'
```

### 6. Run ZenML Pipeline

```bash
# Initialize ZenML
zenml init

# Run training pipeline
python pipelines/training_pipeline.py

# View ZenML dashboard
zenml up
```

Visit ZenML Dashboard at: http://localhost:8237

### 7. Deploy with Docker Compose

```bash
# Start all services (MLflow + API v1)
docker-compose up -d

# Check services
docker-compose ps

# View logs
docker-compose logs -f api-v1

# Services:
# - MLflow UI: http://localhost:5000
# - API v1: http://localhost:8000
# - API v2: http://localhost:8001 (when enabled)
```

### 8. Test Inference API

```bash
# Health check
curl http://localhost:8000/health

# Make prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }'

# Expected response:
# {
#   "prediction": "setosa",
#   "prediction_id": 0,
#   "confidence": 0.99,
#   "model_version": "1.0",
#   "model_type": "logistic"
# }

# Visit API documentation
# http://localhost:8000/docs
```

## 🔄 Version Update and Rollback Demo

### Deploy Version 2 (SVM Model)

```bash
# Start v2 API
docker-compose --profile v2 up -d api-v2

# Test v2 API
curl http://localhost:8001/health

# Make prediction with v2
curl -X POST http://localhost:8001/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.9,
    "sepal_width": 3.0,
    "petal_length": 5.1,
    "petal_width": 1.8
  }'
```

### Rollback to Version 1

```bash
# Stop v2
docker-compose stop api-v2

# v1 is still running on port 8000
curl http://localhost:8000/health
```

## 🔍 MLflow Experiment Tracking

### View Experiments

```bash
# MLflow UI at http://localhost:5000

# Experiments:
# 1. iris-classification (baseline models)
# 2. iris-classification-optimized (Optuna results)

# Compare runs:
# - Parameters: C, kernel, max_iter, etc.
# - Metrics: accuracy, f1_score
# - Artifacts: models, classification reports, confusion matrices
```

### Access via Python

```python
import mlflow

mlflow.set_tracking_uri("http://localhost:5000")

# Get best run
experiment = mlflow.get_experiment_by_name("iris-classification")
runs = mlflow.search_runs(experiment.experiment_id)
best_run = runs.loc[runs['metrics.accuracy'].idxmax()]

print(f"Best model accuracy: {best_run['metrics.accuracy']}")
```

## 📊 Results

### Baseline Models

| Model | Accuracy | F1 Score |
|-------|----------|----------|
| Logistic Regression | 0.9667 | 0.9667 |
| SVM (RBF) | 0.9667 | 0.9667 |

### Optimized Models (After Optuna)

| Model | Best Accuracy | Improvement |
|-------|---------------|-------------|
| Logistic Regression | 0.9750+ | +0.83% |
| SVM | 0.9750+ | +0.83% |

## 🧪 GitLab CI/CD Pipeline

The `.gitlab-ci.yml` includes:

### Stages:
1. **Test**: Code quality checks, unit tests
2. **Build**: Docker image building, registry push
3. **Deploy**: Production deployment (manual trigger)

### Continuous Training (CT):
- Scheduled smoke tests
- Automated retraining triggers
- Model performance monitoring

### Setup in GitLab:

```bash
# 1. Push to GitLab
git remote add origin <your-gitlab-repo>
git push -u origin main

# 2. Configure CI/CD variables:
# - CI_REGISTRY_USER
# - CI_REGISTRY_PASSWORD

# 3. Setup schedule for CT:
# CI/CD > Schedules > New schedule
# Interval: Daily at 2 AM
# Target Branch: main
```

## 📈 DVC Data Versioning

### Track New Data

```bash
# Modify data
python src/data_loader.py

# Track changes
dvc add data/train.csv data/test.csv

# Commit changes
git add data/*.dvc data/.gitignore
git commit -m "Update dataset v2"

# Push data to remote
dvc push

# Push code to Git
git push
```

### Reproduce on Another Machine

```bash
# Clone repo
git clone <your-repo-url>
cd mlops

# Pull data
dvc pull

# Train model
python src/train.py
```

## 🛠️ Development

### Add New Model

1. Add training function in `src/train.py`
2. Add Optuna objective in `src/optimize.py`
3. Update ZenML pipeline in `pipelines/training_pipeline.py`
4. Log experiments to MLflow

### Add Tests

```bash
# Create tests/
mkdir tests
# Add test files
# test_data_loader.py
# test_model.py
# Run with pytest
pytest tests/
```

## 📚 Additional Resources

- [MLflow Documentation](https://mlflow.org/docs/latest/index.html)
- [DVC Documentation](https://dvc.org/doc)
- [ZenML Documentation](https://docs.zenml.io/)
- [Optuna Documentation](https://optuna.readthedocs.io/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)

## 🎯 Project Requirements Checklist

- [x] Git repository with proper structure
- [x] DVC for data versioning with remote
- [x] MLflow experiment tracking (baseline + variations)
- [x] ZenML pipeline orchestration
- [x] Optuna hyperparameter optimization
- [x] Docker containerization (train + serve)
- [x] Docker Compose for local deployment
- [x] FastAPI inference service
- [x] GitLab CI/CD pipeline
- [x] Version update (v1 → v2) demonstration
- [x] Rollback mechanism
- [x] Comprehensive documentation

## 👥 Author

MLOps Mini-Project - 2025-26

## 📝 License

This project is for educational purposes.
