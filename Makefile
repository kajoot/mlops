# Training Scripts
train:
	python src/train.py

optimize-lr:
	python src/optimize.py --model logistic_regression --n-trials 10

optimize-svm:
	python src/optimize.py --model svm --n-trials 10

# Data
data:
	python src/data_loader.py

# DVC
dvc-push:
	dvc push

dvc-pull:
	dvc pull

# MLflow
mlflow:
	mlflow server --backend-store-uri file://$(PWD)/mlruns \
		--default-artifact-root file://$(PWD)/mlartifacts \
		--host 0.0.0.0 --port 5000

# ZenML
zenml-pipeline:
	python pipelines/training_pipeline.py

zenml-dashboard:
	zenml up

# Docker
docker-build-train:
	docker build -t iris-train:latest -f Dockerfile.train .

docker-build-api:
	docker build -t iris-api:latest -f Dockerfile.api .

docker-up:
	docker-compose up -d

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

# API
api-local:
	cd api && uvicorn main:app --reload --port 8000

test-api:
	./test_api.sh

# Clean
clean:
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf .coverage

# Help
help:
	@echo "Available commands:"
	@echo "  make data              - Generate dataset"
	@echo "  make train             - Train baseline models"
	@echo "  make optimize-lr       - Optimize Logistic Regression"
	@echo "  make optimize-svm      - Optimize SVM"
	@echo "  make mlflow            - Start MLflow server"
	@echo "  make zenml-pipeline    - Run ZenML pipeline"
	@echo "  make zenml-dashboard   - Open ZenML dashboard"
	@echo "  make docker-up         - Start Docker services"
	@echo "  make docker-down       - Stop Docker services"
	@echo "  make api-local         - Run API locally"
	@echo "  make test-api          - Test API endpoints"
	@echo "  make clean             - Clean Python cache"

.PHONY: train optimize-lr optimize-svm data dvc-push dvc-pull mlflow zenml-pipeline zenml-dashboard docker-build-train docker-build-api docker-up docker-down docker-logs api-local test-api clean help
