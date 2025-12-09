"""
Training Script for All Models
Trains SVM, MLP, L1-NN (KNN), L2-NN (KNN), Logistic Regression, and Softmax Regression models.
"""

import sys
import os
import yaml
import joblib
import json
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_preprocessing import preprocess_pipeline
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score, roc_auc_score, recall_score,
    precision_score, f1_score, confusion_matrix
)

def train_svm(X_train, X_test, y_train, y_test):
    """Train SVM model."""
    print("\n--- Training SVM ---")
    model = SVC(
        C=5.0,
        kernel='rbf',
        probability=True,
        max_iter=3000,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'recall': float(recall_score(y_test, y_pred, pos_label=1)),
        'precision': float(precision_score(y_test, y_pred, pos_label=1)),
        'f1_score': float(f1_score(y_test, y_pred, pos_label=1)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  F1-Score: {metrics['f1_score']:.4f}")
    
    return model, metrics

def train_mlp(X_train, X_test, y_train, y_test):
    """Train MLP model."""
    print("\n--- Training MLP ---")
    model = MLPClassifier(
        hidden_layer_sizes=(500, 500, 500),
        learning_rate_init=0.01,
        alpha=0.01,
        max_iter=3000,
        early_stopping=False,
        random_state=42,
        verbose=1,
        validation_fraction=0.1
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'recall': float(recall_score(y_test, y_pred, pos_label=1)),
        'precision': float(precision_score(y_test, y_pred, pos_label=1)),
        'f1_score': float(f1_score(y_test, y_pred, pos_label=1)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  F1-Score: {metrics['f1_score']:.4f}")
    
    return model, metrics

def train_l1_nn(X_train, X_test, y_train, y_test):
    """Train L1-NN (KNN with Manhattan distance) model."""
    print("\n--- Training L1-NN (KNN Manhattan) ---")
    model = KNeighborsClassifier(n_neighbors=5, p=1)  # p=1 for Manhattan distance
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'recall': float(recall_score(y_test, y_pred, pos_label=1)),
        'precision': float(precision_score(y_test, y_pred, pos_label=1)),
        'f1_score': float(f1_score(y_test, y_pred, pos_label=1)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  F1-Score: {metrics['f1_score']:.4f}")
    
    return model, metrics

def train_l2_nn(X_train, X_test, y_train, y_test):
    """Train L2-NN (KNN with Euclidean distance) model."""
    print("\n--- Training L2-NN (KNN Euclidean) ---")
    model = KNeighborsClassifier(n_neighbors=5, p=2)  # p=2 for Euclidean distance
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'recall': float(recall_score(y_test, y_pred, pos_label=1)),
        'precision': float(precision_score(y_test, y_pred, pos_label=1)),
        'f1_score': float(f1_score(y_test, y_pred, pos_label=1)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  F1-Score: {metrics['f1_score']:.4f}")
    
    return model, metrics

def train_logistic_regression(X_train, X_test, y_train, y_test):
    """Train Logistic Regression model."""
    print("\n--- Training Logistic Regression ---")
    model = LogisticRegression(
        max_iter=3000,
        random_state=42,
        solver='liblinear'
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'recall': float(recall_score(y_test, y_pred, pos_label=1)),
        'precision': float(precision_score(y_test, y_pred, pos_label=1)),
        'f1_score': float(f1_score(y_test, y_pred, pos_label=1)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  F1-Score: {metrics['f1_score']:.4f}")
    
    return model, metrics

def train_softmax_regression(X_train, X_test, y_train, y_test):
    """Train Softmax Regression (multinomial logistic regression) model."""
    print("\n--- Training Softmax Regression ---")
    model = LogisticRegression(
        multi_class='multinomial',
        solver='lbfgs',
        max_iter=3000,
        random_state=42
    )
    model.fit(X_train, y_train)
    
    # Evaluate
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test)[:, 1]  # Probability of class 1 (malignant)
    
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
        'recall': float(recall_score(y_test, y_pred, pos_label=1)),
        'precision': float(precision_score(y_test, y_pred, pos_label=1)),
        'f1_score': float(f1_score(y_test, y_pred, pos_label=1)),
        'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
    }
    
    print(f"  Accuracy: {metrics['accuracy']:.4f}")
    print(f"  ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"  Recall: {metrics['recall']:.4f}")
    print(f"  Precision: {metrics['precision']:.4f}")
    print(f"  F1-Score: {metrics['f1_score']:.4f}")
    
    return model, metrics

def main():
    """Main training function."""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("="*60)
    print("Breast Cancer Detection - Multi-Model Training")
    print("="*60)
    
    # Get data path - resolve relative to config file location
    config_data_path = config['data']['data_path']
    script_dir = os.path.dirname(os.path.abspath(__file__))
    mlops_dir = os.path.dirname(script_dir)
    
    # Try multiple possible locations
    possible_paths = [
        config_data_path,  # Original path from config
        os.path.join(mlops_dir, config_data_path),  # Relative to mlops_deployment
        os.path.join(mlops_dir, '..','data.csv'),  # Parent of mlops_deployment
        os.path.normpath(os.path.join(mlops_dir, '..', 'data.csv')),  # Normalized
    ]
    
    data_path = None
    for path in possible_paths:
        if os.path.exists(path):
            data_path = os.path.abspath(path)
            print(f"Found data file at: {data_path}")
            break
    
    if data_path is None:
        print(f"Error: Data file not found!")
        print(f"Tried the following paths:")
        for path in possible_paths:
            print(f"  - {os.path.abspath(path)}")
        print("\nPlease ensure data.csv exists in the project root directory")
        return
    
    # Preprocess data
    print("\n[1/6] Preprocessing data...")
    X_train, X_test, y_train, y_test, preprocessor = preprocess_pipeline(
        data_path, 
        config
    )
    
    # Save scaler
    scaler_path = config['paths']['scaler_file']
    preprocessor.save_scaler(scaler_path)
    print(f"Scaler saved to {scaler_path}")
    
    print(f"\nTraining samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    
    # Models directory
    models_dir = Path(config['paths']['model_dir'])
    models_dir.mkdir(exist_ok=True)
    
    # Train all models
    all_metrics = {}
    
    # Train SVM
    print("\n[2/6] Training SVM...")
    svm_model, svm_metrics = train_svm(X_train, X_test, y_train, y_test)
    joblib.dump(svm_model, models_dir / "svm_model.pkl")
    all_metrics['svm'] = svm_metrics
    print(f"  ✓ SVM model saved")
    
    # Train MLP
    print("\n[3/6] Training MLP...")
    mlp_model, mlp_metrics = train_mlp(X_train, X_test, y_train, y_test)
    joblib.dump(mlp_model, models_dir / "mlp_model.pkl")
    all_metrics['mlp'] = mlp_metrics
    print(f"  ✓ MLP model saved")
    
    # Train L1-NN
    print("\n[4/6] Training L1-NN...")
    l1_model, l1_metrics = train_l1_nn(X_train, X_test, y_train, y_test)
    joblib.dump(l1_model, models_dir / "l1_nn_model.pkl")
    all_metrics['l1_nn'] = l1_metrics
    print(f"  ✓ L1-NN model saved")
    
    # Train L2-NN
    print("\n[5/6] Training L2-NN...")
    l2_model, l2_metrics = train_l2_nn(X_train, X_test, y_train, y_test)
    joblib.dump(l2_model, models_dir / "l2_nn_model.pkl")
    all_metrics['l2_nn'] = l2_metrics
    print(f"  ✓ L2-NN model saved")
    
    # Train Logistic Regression
    print("\n[6/6] Training Logistic Regression...")
    lr_model, lr_metrics = train_logistic_regression(X_train, X_test, y_train, y_test)
    joblib.dump(lr_model, models_dir / "logistic_regression_model.pkl")
    all_metrics['logistic_regression'] = lr_metrics
    print(f"  ✓ Logistic Regression model saved")
    
    # Train Softmax Regression
    print("\n[6/6] Training Softmax Regression...")
    sm_model, sm_metrics = train_softmax_regression(X_train, X_test, y_train, y_test)
    joblib.dump(sm_model, models_dir / "softmax_regression_model.pkl")
    all_metrics['softmax_regression'] = sm_metrics
    print(f"  ✓ Softmax Regression model saved")
    
    # Save comparison metrics
    comparison_path = models_dir / "model_comparison.json"
    with open(comparison_path, 'w') as f:
        json.dump(all_metrics, f, indent=2)
    print(f"\n✓ Model comparison saved to {comparison_path}")
    
    # Print summary
    print("\n" + "="*60)
    print("Training Summary")
    print("="*60)
    print(f"{'Model':<12} {'Accuracy':<10} {'ROC-AUC':<10} {'Recall':<10} {'F1':<10}")
    print("-"*60)
    for model_name, metrics in all_metrics.items():
        print(f"{model_name:<12} {metrics['accuracy']:<10.4f} {metrics['roc_auc']:<10.4f} "
              f"{metrics['recall']:<10.4f} {metrics['f1_score']:<10.4f}")
    
    print("\n✓ All models trained and saved!")
    print("✓ Ready for deployment!")

if __name__ == "__main__":
    main()

