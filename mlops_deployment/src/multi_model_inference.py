"""
Multi-Model Inference Module
Supports multiple algorithms: SVM, MLP, L1-NN (KNN), L2-NN (KNN), Logistic Regression, Softmax Regression
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from pathlib import Path


class MultiModelInference:
    """Handles inference for multiple model types."""
    
    MODELS_DIR = Path(__file__).parent.parent / "models"
    
    def __init__(self, scaler_path: str, feature_names: Optional[List[str]] = None):
        """
        Initialize the multi-model inference class.
        
        Args:
            scaler_path: Path to the saved scaler
            feature_names: List of feature names (optional)
        """
        self.scaler = None
        self.feature_names = feature_names
        self.scaler_path = scaler_path
        self.models = {}  # Cache loaded models
        self.model_metrics = {}  # Store model performance metrics
        
    def load_scaler(self):
        """Load the scaler from disk."""
        if self.scaler is None:
            self.scaler = joblib.load(self.scaler_path)
            print(f"Scaler loaded from {self.scaler_path}")
        return self.scaler
    
    def load_model(self, model_type: str):
        """
        Load a specific model type.
        
        Args:
            model_type: One of 'mlp', 'svm', 'l1_nn', 'l2_nn', 'logistic_regression', 'softmax_regression'
            
        Returns:
            Loaded model
        """
        if model_type in self.models:
            return self.models[model_type]
        
        model_path = self.MODELS_DIR / f"{model_type}_model.pkl"
        
        if not model_path.exists():
            raise FileNotFoundError(
                f"Model {model_type} not found at {model_path}. "
                f"Please train the model first using: python scripts/train_all_models.py"
            )
        
        model = joblib.load(model_path)
        self.models[model_type] = model
        print(f"Model {model_type} loaded from {model_path}")
        return model
    
    def get_available_models(self) -> List[str]:
        """Get list of available model types."""
        available = []
        for model_type in ['mlp', 'svm', 'l1_nn', 'l2_nn', 'logistic_regression', 'softmax_regression']:
            model_path = self.MODELS_DIR / f"{model_type}_model.pkl"
            if model_path.exists():
                available.append(model_type)
        return available
    
    def get_model_metrics(self, model_type: str) -> Dict:
        """Get performance metrics for a model."""
        if model_type in self.model_metrics:
            return self.model_metrics[model_type]
        
        # Try to load from results files or model_comparison.json
        results_path = Path(__file__).parent.parent.parent / "results" / f"{model_type}_results.json"
        comparison_path = self.MODELS_DIR / "model_comparison.json"
        
        # First try model_comparison.json (from training script)
        if comparison_path.exists():
            import json
            with open(comparison_path, 'r') as f:
                comparison_data = json.load(f)
                if model_type in comparison_data:
                    metrics = comparison_data[model_type]
                    self.model_metrics[model_type] = metrics
                    return metrics
        
        # Fallback to results files
        if results_path.exists():
            import json
            with open(results_path, 'r') as f:
                data = json.load(f)
                # Normalize the structure
                if 'test_set' in data:
                    metrics = data['test_set']
                elif 'Test_Accuracy' in data:
                    metrics = {
                        'accuracy': data.get('Test_Accuracy', 0),
                        'roc_auc': data.get('Test_ROC_AUC', 0),
                        'recall': data.get('Test_Recall', 0),
                        'precision': data.get('Test_Precision', 0),
                        'f1_score': data.get('Test_F1', 0)
                    }
                else:
                    metrics = data
                
                self.model_metrics[model_type] = metrics
                return metrics
        
        # Default metrics if not found
        return {
            'accuracy': 0.0,
            'roc_auc': 0.0,
            'recall': 0.0,
            'precision': 0.0,
            'f1_score': 0.0
        }
    
    def prepare_features(self, data: Dict) -> np.ndarray:
        """Prepare features from input dictionary."""
        if self.feature_names is None:
            self.feature_names = list(data.keys())
        
        features = np.array([data.get(feature, 0.0) for feature in self.feature_names])
        features = features.reshape(1, -1)
        return features
    
    def scale_features(self, features: np.ndarray) -> np.ndarray:
        """Scale features using the fitted scaler."""
        if self.scaler is None:
            self.load_scaler()
        # Convert to DataFrame if we have feature names to avoid warnings
        if self.feature_names and len(self.feature_names) == features.shape[1]:
            features_df = pd.DataFrame(features, columns=self.feature_names)
            scaled = self.scaler.transform(features_df)
            return scaled
        else:
            return self.scaler.transform(features)
    
    def predict(self, data: Dict, model_type: str = 'mlp') -> Dict:
        """
        Make prediction using specified model.
        
        Args:
            data: Dictionary with feature values
            model_type: One of 'mlp', 'svm', 'l1_nn', 'l2_nn'
            
        Returns:
            Dictionary with prediction results including model info
        """
        # Load model
        model = self.load_model(model_type)
        
        # Prepare and scale features
        features = self.prepare_features(data)
        features_scaled = self.scale_features(features)
        
        # Make prediction
        prediction = model.predict(features_scaled)[0]
        
        # Get probabilities (if available)
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(features_scaled)[0]
            prob_malignant = float(probability[1])
            prob_benign = float(probability[0])
            confidence = float(max(probability))
        else:
            # For models without probability (shouldn't happen with our models)
            prob_malignant = 1.0 if prediction == 1 else 0.0
            prob_benign = 1.0 if prediction == 0 else 0.0
            confidence = 1.0
        
        # Get model metrics
        metrics = self.get_model_metrics(model_type)
        
        # Format results
        result = {
            'prediction': int(prediction),
            'prediction_label': 'Malignant' if prediction == 1 else 'Benign',
            'probability_malignant': prob_malignant,
            'probability_benign': prob_benign,
            'confidence': confidence,
            'model_type': model_type,
            'model_metrics': metrics
        }
        
        return result
    
    def predict_batch(self, data_list: List[Dict], model_type: str = 'mlp') -> List[Dict]:
        """Make predictions on a batch of inputs."""
        results = []
        for data in data_list:
            result = self.predict(data, model_type)
            results.append(result)
        return results
    
    def compare_models(self, data: Dict) -> Dict:
        """
        Compare predictions from all available models.
        
        Args:
            data: Dictionary with feature values
            
        Returns:
            Dictionary with predictions from all models
        """
        available_models = self.get_available_models()
        comparisons = {}
        
        for model_type in available_models:
            try:
                result = self.predict(data, model_type)
                comparisons[model_type] = result
            except Exception as e:
                comparisons[model_type] = {
                    'error': str(e)
                }
        
        return {
            'comparisons': comparisons,
            'available_models': available_models
        }


# Expected feature names
EXPECTED_FEATURES = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
    'smoothness_mean', 'compactness_mean', 'concavity_mean',
    'concave points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se',
    'concave points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
    'smoothness_worst', 'compactness_worst', 'concavity_worst',
    'concave points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

