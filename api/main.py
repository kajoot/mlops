"""
FastAPI Inference API for Iris Classification
Student MLOps Project 2025-26
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np
from typing import List
import os

# Initialize FastAPI app
app = FastAPI(
    title="Iris Classification API",
    description="ML model serving for Iris species classification",
    version="1.0.0"
)

# Global variables for model
model = None
model_version = "1.0"
model_type = "logistic_regression"


class IrisFeatures(BaseModel):
    """Input features for iris prediction."""
    sepal_length: float = Field(..., description="Sepal length in cm", ge=0)
    sepal_width: float = Field(..., description="Sepal width in cm", ge=0)
    petal_length: float = Field(..., description="Petal length in cm", ge=0)
    petal_width: float = Field(..., description="Petal width in cm", ge=0)
    
    class Config:
        json_schema_extra = {
            "example": {
                "sepal_length": 5.1,
                "sepal_width": 3.5,
                "petal_length": 1.4,
                "petal_width": 0.2
            }
        }


class PredictionResponse(BaseModel):
    """Prediction response."""
    prediction: str
    prediction_id: int
    confidence: float
    model_version: str
    model_type: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_loaded: bool
    model_version: str
    model_type: str


def load_model(model_path: str = "models/logistic_regression_baseline.joblib"):
    """Load the trained model."""
    global model, model_type
    
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    model = joblib.load(model_path)
    model_type = model_path.split('/')[-1].split('_')[0]
    print(f"Model loaded successfully from {model_path}")
    return model


@app.on_event("startup")
async def startup_event():
    """Load model on startup."""
    try:
        load_model()
    except Exception as e:
        print(f"Warning: Could not load model on startup: {e}")


@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Iris Classification API",
        "version": model_version,
        "endpoints": {
            "/health": "Health check",
            "/predict": "Make predictions",
            "/docs": "API documentation"
        }
    }


@app.get("/health", response_model=HealthResponse)
async def health():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy" if model is not None else "unhealthy",
        model_loaded=model is not None,
        model_version=model_version,
        model_type=model_type
    )


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: IrisFeatures):
    """Make a prediction."""
    if model is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    try:
        # Prepare input
        X = np.array([[
            features.sepal_length,
            features.sepal_width,
            features.petal_length,
            features.petal_width
        ]])
        
        # Make prediction
        prediction_id = model.predict(X)[0]
        
        # Get class names
        class_names = ['setosa', 'versicolor', 'virginica']
        prediction_name = class_names[prediction_id]
        
        # Calculate confidence (for models that support predict_proba)
        try:
            probas = model.predict_proba(X)[0]
            confidence = float(probas[prediction_id])
        except AttributeError:
            # SVM without probability=True
            confidence = 1.0
        
        return PredictionResponse(
            prediction=prediction_name,
            prediction_id=int(prediction_id),
            confidence=confidence,
            model_version=model_version,
            model_type=model_type
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")


@app.post("/reload")
async def reload_model(model_path: str = "models/logistic_regression_baseline.joblib"):
    """Reload the model from disk."""
    try:
        load_model(model_path)
        return {
            "message": "Model reloaded successfully",
            "model_type": model_type,
            "model_version": model_version
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reload model: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
