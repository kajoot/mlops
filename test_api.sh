#!/bin/bash
# Test script for API

echo "======================================"
echo "Testing Iris Classification API"
echo "======================================"

# Check if API is running
echo -e "\n1. Health Check..."
curl -s http://localhost:8000/health | python -m json.tool

# Test prediction - Setosa
echo -e "\n\n2. Prediction Test - Setosa (should predict: setosa)..."
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.1,
    "sepal_width": 3.5,
    "petal_length": 1.4,
    "petal_width": 0.2
  }' | python -m json.tool

# Test prediction - Versicolor
echo -e "\n\n3. Prediction Test - Versicolor (should predict: versicolor)..."
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 5.9,
    "sepal_width": 3.0,
    "petal_length": 4.2,
    "petal_width": 1.5
  }' | python -m json.tool

# Test prediction - Virginica
echo -e "\n\n4. Prediction Test - Virginica (should predict: virginica)..."
curl -s -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "sepal_length": 6.3,
    "sepal_width": 3.3,
    "petal_length": 6.0,
    "petal_width": 2.5
  }' | python -m json.tool

echo -e "\n\n======================================"
echo "Tests completed!"
echo "======================================"
