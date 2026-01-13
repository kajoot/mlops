"""
ZenML Training Pipeline for Iris Classification
Implements end-to-end ML workflow with ZenML
"""

from zenml import pipeline, step
from zenml.config import DockerSettings
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score
import mlflow
import mlflow.sklearn
import joblib
import os
from typing import Tuple, Annotated


@step
def load_data() -> Tuple[
    Annotated[pd.DataFrame, "X_train"],
    Annotated[pd.DataFrame, "X_test"],
    Annotated[pd.Series, "y_train"],
    Annotated[pd.Series, "y_test"],
    Annotated[list, "target_names"]
]:
    """
    Load and prepare Iris dataset
    Returns train/test splits and target names
    """
    import sys
    import os
    # Add src directory to path
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
    from data_loader import prepare_data
    
    X_train, X_test, y_train, y_test, target_names = prepare_data()
    return X_train, X_test, y_train, y_test, target_names.tolist()


@step
def train_model(
    X_train: pd.DataFrame,
    y_train: pd.Series,
    model_type: str = 'logistic_regression',
    C: float = 1.0
) -> object:
    """Train machine learning model."""
    if model_type == 'logistic_regression':
        model = LogisticRegression(
            C=C,
            max_iter=1000,
            multi_class='multinomial',
            solver='lbfgs',
            random_state=42
        )
    elif model_type == 'svm':
        model = SVC(
            C=C,
            kernel='rbf',
            gamma='scale',
            random_state=42
        )
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    model.fit(X_train, y_train)
    return model


@step
def evaluate_model(
    model: object,
    X_test: pd.DataFrame,
    y_test: pd.Series,
    target_names: list
) -> dict:
    """Evaluate model and return metrics."""
    y_pred = model.predict(X_test)
    
    metrics = {
        'accuracy': accuracy_score(y_test, y_pred),
        'f1_score': f1_score(y_test, y_pred, average='weighted')
    }
    
    print(f"\nModel Evaluation Results:")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"F1 Score: {metrics['f1_score']:.4f}")
    
    return metrics


@step
def save_model(
    model: object,
    metrics: dict,
    model_type: str = 'logistic_regression'
) -> str:
    """Save model to disk."""
    os.makedirs("models", exist_ok=True)
    model_path = f"models/{model_type}_zenml.joblib"
    joblib.dump(model, model_path)
    
    print(f"\nModel saved to: {model_path}")
    return model_path


@pipeline
def iris_training_pipeline(
    model_type: str = 'logistic_regression',
    C: float = 1.0
):
    """
    Complete ML pipeline for Iris classification.
    
    Args:
        model_type: Type of model to train
        C: Regularization parameter
    """
    X_train, X_test, y_train, y_test, target_names = load_data()
    model = train_model(X_train, y_train, model_type=model_type, C=C)
    metrics = evaluate_model(model, X_test, y_test, target_names)
    model_path = save_model(model, metrics, model_type=model_type)


if __name__ == "__main__":
    # Run pipeline with different configurations
    print("Running ZenML Pipeline - Logistic Regression")
    print("="*60)
    iris_training_pipeline(model_type='logistic_regression', C=1.0)
    
    print("\n\nRunning ZenML Pipeline - SVM")
    print("="*60)
    iris_training_pipeline(model_type='svm', C=1.0)
