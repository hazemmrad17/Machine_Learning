"""
Model Training Module
Handles model training, evaluation, and saving.
"""

import joblib
import os
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, roc_auc_score, recall_score, 
    precision_score, f1_score, confusion_matrix
)
import json


class ModelTrainer:
    """Handles model training and evaluation."""
    
    def __init__(self, config=None):
        """
        Initialize the model trainer.
        
        Args:
            config: Configuration dictionary with model settings
        """
        self.config = config or {}
        self.model = None
        self.history = {}
        
    def create_model(self):
        """Create MLP model based on configuration."""
        model_config = self.config.get('model', {})
        
        self.model = MLPClassifier(
            hidden_layer_sizes=tuple(model_config.get('architecture', [500, 500, 500])),
            learning_rate_init=model_config.get('learning_rate', 0.01),
            alpha=model_config.get('alpha', 0.01),
            max_iter=model_config.get('max_iter', 3000),
            early_stopping=False,
            random_state=model_config.get('random_state', 42),
            verbose=1,
            validation_fraction=0.1
        )
        
        print("MLP model created with architecture:", model_config.get('architecture', [500, 500, 500]))
        return self.model
    
    def train(self, X_train, y_train):
        """
        Train the model.
        
        Args:
            X_train: Training features
            y_train: Training labels
        """
        if self.model is None:
            self.create_model()
        
        print("Training model...")
        self.model.fit(X_train, y_train)
        print("Training completed!")
        
        return self.model
    
    def evaluate(self, X_test, y_test):
        """
        Evaluate the model on test data.
        
        Args:
            X_test: Test features
            y_test: Test labels
            
        Returns:
            Dictionary with evaluation metrics
        """
        if self.model is None:
            raise ValueError("Model not trained yet. Call train() first.")
        
        # Predictions
        y_pred = self.model.predict(X_test)
        y_pred_proba = self.model.predict_proba(X_test)[:, 1]
        
        # Calculate metrics
        metrics = {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'roc_auc': float(roc_auc_score(y_test, y_pred_proba)),
            'recall': float(recall_score(y_test, y_pred, pos_label=1)),
            'precision': float(precision_score(y_test, y_pred, pos_label=1)),
            'f1_score': float(f1_score(y_test, y_pred, pos_label=1))
        }
        
        # Confusion matrix
        cm = confusion_matrix(y_test, y_pred)
        metrics['confusion_matrix'] = cm.tolist()
        
        print("\n=== Model Evaluation ===")
        print(f"Accuracy: {metrics['accuracy']:.4f}")
        print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
        print(f"Recall: {metrics['recall']:.4f}")
        print(f"Precision: {metrics['precision']:.4f}")
        print(f"F1-Score: {metrics['f1_score']:.4f}")
        
        return metrics
    
    def save_model(self, filepath):
        """
        Save the trained model to disk.
        
        Args:
            filepath: Path to save the model
        """
        if self.model is None:
            raise ValueError("No model to save. Train the model first.")
        
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath):
        """
        Load a trained model from disk.
        
        Args:
            filepath: Path to the saved model
        """
        self.model = joblib.load(filepath)
        print(f"Model loaded from {filepath}")
        return self.model
    
    def save_metrics(self, metrics, filepath):
        """
        Save evaluation metrics to JSON file.
        
        Args:
            metrics: Dictionary with metrics
            filepath: Path to save metrics
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(metrics, f, indent=2)
        print(f"Metrics saved to {filepath}")


def train_model_pipeline(X_train, X_test, y_train, y_test, config):
    """
    Complete training pipeline.
    
    Args:
        X_train: Training features
        X_test: Test features
        y_train: Training labels
        y_test: Test labels
        config: Configuration dictionary
        
    Returns:
        trainer: ModelTrainer instance
        metrics: Evaluation metrics
    """
    trainer = ModelTrainer(config)
    
    # Train model
    trainer.train(X_train, y_train)
    
    # Evaluate model
    metrics = trainer.evaluate(X_test, y_test)
    
    # Save model
    model_path = config['paths']['model_file']
    trainer.save_model(model_path)
    
    # Save metrics
    metrics_path = os.path.join(config['paths']['model_dir'], 'metrics.json')
    trainer.save_metrics(metrics, metrics_path)
    
    return trainer, metrics

