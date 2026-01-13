# Quick Start Guide

## 🚀 Running the Complete Project

### Option 1: Run Everything with Docker (Recommended)

```bash
# 1. Start MLflow and API
docker-compose up -d

# 2. Wait for services to start (check logs)
docker-compose logs -f

# 3. Access services:
# - MLflow UI: http://localhost:5000
# - API v1: http://localhost:8000
# - API Docs: http://localhost:8000/docs
```

### Option 2: Run Locally (Development)

```bash
# 1. Start MLflow server (Terminal 1)
make mlflow

# 2. Train baseline models (Terminal 2)
make train

# 3. Run API (Terminal 3)
make api-local

# 4. Test API (Terminal 4)
make test-api
```

## 📋 Step-by-Step Workflow

### 1. Data Preparation
```bash
# Generate/load data
python src/data_loader.py

# Track with DVC
dvc add data/train.csv data/test.csv
git add data/*.dvc
git commit -m "Track dataset with DVC"
dvc push
```

### 2. Baseline Training
```bash
# Train both baselines (logs to MLflow)
python src/train.py

# View results in MLflow UI
# http://localhost:5000
```

### 3. Hyperparameter Optimization
```bash
# Optimize Logistic Regression (10 trials)
python src/optimize.py --model logistic_regression --n-trials 10

# Optimize SVM (10 trials)
python src/optimize.py --model svm --n-trials 10

# Compare in MLflow UI
```

### 4. ZenML Pipeline
```bash
# Initialize ZenML
zenml init

# Run pipeline
python pipelines/training_pipeline.py

# View ZenML dashboard
zenml up
# Visit: http://localhost:8237
```

### 5. Deploy with Docker

#### Start Services
```bash
docker-compose up -d
```

#### Test API v1 (Logistic Regression)
```bash
# Health check
curl http://localhost:8000/health

# Prediction
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"sepal_length": 5.1, "sepal_width": 3.5, "petal_length": 1.4, "petal_width": 0.2}'
```

#### Deploy v2 (SVM)
```bash
# Start v2 API
docker-compose --profile v2 up -d api-v2

# Test v2 on port 8001
curl http://localhost:8001/health
```

#### Rollback to v1
```bash
# Stop v2
docker-compose stop api-v2

# v1 still running on port 8000
```

## 🔄 Common Commands

### Training
```bash
make train              # Train baseline models
make optimize-lr        # Optimize Logistic Regression
make optimize-svm       # Optimize SVM
```

### Services
```bash
make mlflow            # Start MLflow server
make api-local         # Run API locally
make test-api          # Test API endpoints
```

### Docker
```bash
make docker-up         # Start all services
make docker-down       # Stop all services
make docker-logs       # View logs
```

### ZenML
```bash
make zenml-pipeline    # Run training pipeline
make zenml-dashboard   # Open ZenML UI
```

### Data
```bash
make data             # Generate dataset
make dvc-push         # Push data to DVC remote
make dvc-pull         # Pull data from DVC remote
```

## 📊 Expected Results

### Baseline Models
- Logistic Regression: ~97% accuracy
- SVM (RBF kernel): ~97% accuracy

### After Optuna Optimization
- Both models: 97-98% accuracy
- Best parameters logged in MLflow

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Check what's using the port
lsof -i :8000  # or :5000

# Kill the process
kill -9 <PID>

# Or use different ports in docker-compose.yml
```

### MLflow Connection Issues
```bash
# Make sure MLflow server is running
ps aux | grep mlflow

# Start if not running
mlflow server --host 0.0.0.0 --port 5000
```

### Docker Issues
```bash
# Rebuild images
docker-compose build --no-cache

# Remove containers and volumes
docker-compose down -v

# Start fresh
docker-compose up -d
```

### DVC Issues
```bash
# Check DVC status
dvc status

# Reinstall DVC cache
dvc fetch
dvc checkout
```

## ✅ Verification Checklist

- [ ] MLflow UI accessible at http://localhost:5000
- [ ] At least 2 experiments logged in MLflow
- [ ] API responds at http://localhost:8000/health
- [ ] API documentation at http://localhost:8000/docs
- [ ] Successful predictions for all 3 iris species
- [ ] Models saved in `models/` directory
- [ ] DVC tracked files (*.dvc) in data/
- [ ] Git commits with proper messages

## 🎯 Demo Scenario

```bash
# 1. Start services
docker-compose up -d

# 2. Train and compare models
python src/train.py

# 3. View experiments in MLflow
# Open: http://localhost:5000

# 4. Optimize best model
python src/optimize.py --model logistic_regression --n-trials 10

# 5. Test API
./test_api.sh

# 6. Deploy v2 and rollback
docker-compose --profile v2 up -d api-v2
# Test both versions
docker-compose stop api-v2
# Back to v1
```

## 📞 Need Help?

Check the main [README.md](README.md) for detailed documentation.
