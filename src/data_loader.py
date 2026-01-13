"""
Data loader for UCI Iris dataset
"""
import pandas as pd
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
import os


def load_iris_data():
    """Load the Iris dataset from scikit-learn."""
    iris = load_iris()
    X = pd.DataFrame(iris.data, columns=iris.feature_names)
    y = pd.Series(iris.target, name='target')
    
    return X, y, iris.target_names


def prepare_data(test_size=0.2, random_state=42):
    """
    Load and split the Iris dataset.
    
    Args:
        test_size: Proportion of dataset to include in test split
        random_state: Random seed for reproducibility
    
    Returns:
        X_train, X_test, y_train, y_test
    """
    X, y, target_names = load_iris_data()
    
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    return X_train, X_test, y_train, y_test, target_names


def save_data(X_train, X_test, y_train, y_test, output_dir='data'):
    """Save processed data to CSV files."""
    os.makedirs(output_dir, exist_ok=True)
    
    # Combine features and target
    train_df = X_train.copy()
    train_df['target'] = y_train.values
    
    test_df = X_test.copy()
    test_df['target'] = y_test.values
    
    train_df.to_csv(f'{output_dir}/train.csv', index=False)
    test_df.to_csv(f'{output_dir}/test.csv', index=False)
    
    print(f"Data saved to {output_dir}/")
    print(f"Train set: {len(train_df)} samples")
    print(f"Test set: {len(test_df)} samples")


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, target_names = prepare_data()
    save_data(X_train, X_test, y_train, y_test)
    print(f"\nTarget classes: {target_names}")
