"""
Student: MLOps Mini-Project 2025-26
Hyperparameter optimization using Optuna framework
"""
import optuna
import mlflow
import mlflow.sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.model_selection import cross_val_score
import numpy as np
from data_loader import prepare_data


def objective_logistic(trial, X_train, y_train):
    """
    Optuna objective function for Logistic Regression hyperparameter tuning.
    
    Args:
        trial: Optuna trial object
        X_train: Training features
        y_train: Training labels
        
    Returns:
        Mean cross-validation accuracy score
    """
    C = trial.suggest_float('C', 0.01, 10.0, log=True)
    max_iter = trial.suggest_int('max_iter', 500, 2000)
    
    model = LogisticRegression(
        C=C,
        max_iter=max_iter,
        multi_class='multinomial',
        solver='lbfgs',
        random_state=42
    )
    
    # Cross-validation score
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    return scores.mean()


def objective_svm(trial, X_train, y_train):
    """Optuna objective function for SVM."""
    C = trial.suggest_float('C', 0.01, 10.0, log=True)
    kernel = trial.suggest_categorical('kernel', ['rbf', 'linear', 'poly'])
    
    if kernel == 'poly':
        degree = trial.suggest_int('degree', 2, 5)
        model = SVC(C=C, kernel=kernel, degree=degree, random_state=42)
    elif kernel == 'rbf':
        gamma = trial.suggest_categorical('gamma', ['scale', 'auto'])
        model = SVC(C=C, kernel=kernel, gamma=gamma, random_state=42)
    else:
        model = SVC(C=C, kernel=kernel, random_state=42)
    
    # Cross-validation score
    scores = cross_val_score(model, X_train, y_train, cv=5, scoring='accuracy')
    return scores.mean()


def optimize_model(model_type='logistic_regression', n_trials=10):
    """
    Run Optuna optimization.
    
    Args:
        model_type: 'logistic_regression' or 'svm'
        n_trials: Number of Optuna trials
    """
    # Load data
    X_train, X_test, y_train, y_test, target_names = prepare_data()
    
    # Create Optuna study
    study = optuna.create_study(
        direction='maximize',
        study_name=f'{model_type}_optimization'
    )
    
    # Select objective function
    if model_type == 'logistic_regression':
        objective = lambda trial: objective_logistic(trial, X_train, y_train)
    elif model_type == 'svm':
        objective = lambda trial: objective_svm(trial, X_train, y_train)
    else:
        raise ValueError(f"Unknown model type: {model_type}")
    
    # Run optimization
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
    
    print(f"\n{'='*60}")
    print(f"Optuna Optimization Results - {model_type}")
    print(f"{'='*60}")
    print(f"Number of trials: {len(study.trials)}")
    print(f"Best trial: {study.best_trial.number}")
    print(f"Best value (accuracy): {study.best_value:.4f}")
    print(f"\nBest parameters:")
    for key, value in study.best_params.items():
        print(f"  {key}: {value}")
    
    return study


def train_best_model(study, model_type):
    """Train final model with best parameters from Optuna study."""
    from train import train_and_log_model
    
    best_params = study.best_params
    best_params['random_state'] = 42
    
    print(f"\n{'='*60}")
    print(f"Training final model with best parameters...")
    print(f"{'='*60}")
    
    model, metrics = train_and_log_model(
        model_type=model_type,
        params=best_params,
        experiment_name='iris-classification-optimized'
    )
    
    return model, metrics


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Optimize model hyperparameters with Optuna')
    parser.add_argument('--model', type=str, default='logistic_regression',
                        choices=['logistic_regression', 'svm'],
                        help='Model type to optimize')
    parser.add_argument('--n-trials', type=int, default=10,
                        help='Number of Optuna trials')
    
    args = parser.parse_args()
    
    # Run optimization
    study = optimize_model(model_type=args.model, n_trials=args.n_trials)
    
    # Train final model with best parameters
    train_best_model(study, model_type=args.model)
