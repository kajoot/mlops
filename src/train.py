"""
Baseline model training with MLflow tracking
Implements Logistic Regression and SVM classifiers for Iris dataset
"""
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import numpy as np
import os
import joblib
from data_loader import prepare_data


def train_logistic_regression(X_train, y_train, random_state=42, C=1.0, max_iter=1000):
    """Train Logistic Regression model."""
    model = LogisticRegression(
        random_state=random_state,
        C=C,
        max_iter=max_iter,
        multi_class='multinomial',
        solver='lbfgs'
    )
    model.fit(X_train, y_train)
    return model


def train_svm(X_train, y_train, random_state=42, C=1.0, kernel='rbf', gamma='scale'):
    """Train SVM model."""
    model = SVC(
        random_state=random_state,
        C=C,
        kernel=kernel,
        gamma=gamma
    )
    model.fit(X_train, y_train)
    return model


def evaluate_model(model, X_test, y_test):
    """Evaluate model and return metrics."""
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted')
    
    metrics = {
        'accuracy': accuracy,
        'f1_score': f1
    }
    
    return metrics, y_pred


def train_and_log_model(model_type='logistic_regression', params=None, experiment_name='iris-classification'):
    """
    Train model and log to MLflow.
    
    Args:
        model_type: 'logistic_regression' or 'svm'
        params: Dictionary of model parameters
        experiment_name: MLflow experiment name
    """
    if params is None:
        params = {}
    
    # Set MLflow tracking URI
    mlflow.set_tracking_uri("http://localhost:5000")
    mlflow.set_experiment(experiment_name)
    
    # Load data
    X_train, X_test, y_train, y_test, target_names = prepare_data()
    
    with mlflow.start_run(run_name=f"{model_type}_baseline"):
        # Log parameters
        mlflow.log_param("model_type", model_type)
        mlflow.log_param("test_size", 0.2)
        mlflow.log_param("random_state", 42)
        
        for key, value in params.items():
            mlflow.log_param(key, value)
        
        # Train model
        if model_type == 'logistic_regression':
            model = train_logistic_regression(X_train, y_train, **params)
        elif model_type == 'svm':
            model = train_svm(X_train, y_train, **params)
        else:
            raise ValueError(f"Unknown model type: {model_type}")
        
        # Evaluate model
        metrics, y_pred = evaluate_model(model, X_test, y_test)
        
        # Log metrics
        for metric_name, metric_value in metrics.items():
            mlflow.log_metric(metric_name, metric_value)
        
        # Log classification report
        report = classification_report(y_test, y_pred, target_names=target_names)
        mlflow.log_text(report, "classification_report.txt")
        
        # Log confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        mlflow.log_dict({
            "confusion_matrix": cm.tolist(),
            "labels": target_names.tolist()
        }, "confusion_matrix.json")
        
        # Log model
        mlflow.sklearn.log_model(model, "model")
        
        # Save model locally
        os.makedirs("models", exist_ok=True)
        model_path = f"models/{model_type}_baseline.joblib"
        joblib.dump(model, model_path)
        mlflow.log_artifact(model_path)
        
        print(f"\n{'='*50}")
        print(f"Model: {model_type}")
        print(f"{'='*50}")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"F1 Score: {metrics['f1_score']:.4f}")
        print(f"\nClassification Report:")
        print(report)
        print(f"\nModel saved to: {model_path}")
        print(f"MLflow run ID: {mlflow.active_run().info.run_id}")
        
    return model, metrics


if __name__ == "__main__":
    print("Training Logistic Regression baseline...")
    train_and_log_model(
        model_type='logistic_regression',
        params={'C': 1.0, 'max_iter': 1000, 'random_state': 42}
    )
    
    print("\n" + "="*70 + "\n")
    
    print("Training SVM baseline...")
    train_and_log_model(
        model_type='svm',
        params={'C': 1.0, 'kernel': 'rbf', 'gamma': 'scale', 'random_state': 42}
    )
