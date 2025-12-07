"""
Model Inference Module
Handles model loading and prediction for production use.
"""

import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Optional


class ModelInference:
    """Handles model inference for predictions."""
    
    def __init__(self, model_path: str, scaler_path: str, feature_names: Optional[List[str]] = None):
        """
        Initialize the inference class.
        
        Args:
            model_path: Path to the saved model
            scaler_path: Path to the saved scaler
            feature_names: List of feature names (optional)
        """
        self.model = None
        self.scaler = None
        self.feature_names = feature_names
        self.model_path = model_path
        self.scaler_path = scaler_path
        
    def load_model(self):
        """Load the trained model from disk."""
        if self.model is None:
            self.model = joblib.load(self.model_path)
            print(f"Model loaded from {self.model_path}")
        return self.model
    
    def load_scaler(self):
        """Load the scaler from disk."""
        if self.scaler is None:
            self.scaler = joblib.load(self.scaler_path)
            print(f"Scaler loaded from {self.scaler_path}")
        return self.scaler
    
    def prepare_features(self, data: Dict) -> np.ndarray:
        """
        Prepare features from input dictionary.
        
        Args:
            data: Dictionary with feature names as keys
            
        Returns:
            Numpy array of features
        """
        if self.feature_names is None:
            # Use keys from input data as feature names
            self.feature_names = list(data.keys())
        
        # Create feature array in correct order
        features = np.array([data.get(feature, 0.0) for feature in self.feature_names])
        features = features.reshape(1, -1)
        
        return features
    
    def scale_features(self, features: np.ndarray) -> np.ndarray:
        """
        Scale features using the fitted scaler.
        
        Args:
            features: Raw features array
            
        Returns:
            Scaled features array
        """
        if self.scaler is None:
            self.load_scaler()
        
        return self.scaler.transform(features)
    
    def predict(self, data: Dict) -> Dict:
        """
        Make prediction on input data.
        
        Args:
            data: Dictionary with feature values
            
        Returns:
            Dictionary with prediction results
        """
        if self.model is None:
            self.load_model()
        
        # Prepare features
        features = self.prepare_features(data)
        
        # Scale features
        features_scaled = self.scale_features(features)
        
        # Make prediction
        prediction = self.model.predict(features_scaled)[0]
        probability = self.model.predict_proba(features_scaled)[0]
        
        # Format results
        result = {
            'prediction': int(prediction),
            'prediction_label': 'Malignant' if prediction == 1 else 'Benign',
            'probability_malignant': float(probability[1]),
            'probability_benign': float(probability[0]),
            'confidence': float(max(probability))
        }
        
        return result
    
    def predict_batch(self, data_list: List[Dict]) -> List[Dict]:
        """
        Make predictions on a batch of inputs.
        
        Args:
            data_list: List of dictionaries with feature values
            
        Returns:
            List of prediction results
        """
        results = []
        for data in data_list:
            result = self.predict(data)
            results.append(result)
        
        return results


# Expected feature names (30 features from the dataset)
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

