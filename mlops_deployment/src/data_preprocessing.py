"""
Data Preprocessing Module
Handles data loading, cleaning, and preprocessing for the breast cancer detection model.
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os


class DataPreprocessor:
    """Handles data preprocessing pipeline."""
    
    def __init__(self, config=None):
        """
        Initialize the preprocessor.
        
        Args:
            config: Configuration dictionary with preprocessing settings
        """
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.config = config or {}
        self.feature_names = None
        
    def load_data(self, data_path):
        """
        Load data from CSV file.
        
        Args:
            data_path: Path to the CSV file
            
        Returns:
            DataFrame with loaded data
        """
        df = pd.read_csv(data_path)
        print(f"Data loaded: {df.shape[0]} samples, {df.shape[1]} features")
        return df
    
    def clean_data(self, df):
        """
        Clean the dataset by removing unnecessary columns.
        
        Args:
            df: Input DataFrame
            
        Returns:
            Cleaned DataFrame
        """
        # Drop unnecessary columns
        drop_cols = self.config.get('drop_columns', ['id', 'Unnamed: 32'])
        df = df.drop(columns=drop_cols, errors='ignore')
        
        # Check for missing values
        missing = df.isnull().sum().sum()
        if missing > 0:
            print(f"Warning: {missing} missing values found")
        
        return df
    
    def encode_labels(self, y):
        """
        Encode categorical labels to numerical values.
        
        Args:
            y: Series with categorical labels (M/B)
            
        Returns:
            Encoded labels (0/1)
        """
        y_encoded = self.label_encoder.fit_transform(y)
        return y_encoded
    
    def prepare_features(self, df):
        """
        Prepare features and target variable.
        
        Args:
            df: DataFrame with diagnosis column
            
        Returns:
            X: Features DataFrame
            y: Target Series
        """
        # Separate features and target
        X = df.drop('diagnosis', axis=1)
        y = df['diagnosis']
        
        # Store feature names for later use
        self.feature_names = X.columns.tolist()
        
        # Encode labels
        y_encoded = self.encode_labels(y)
        
        return X, y_encoded
    
    def split_data(self, X, y, test_size=0.3, random_state=42, stratify=None):
        """
        Split data into train and test sets.
        
        Args:
            X: Features
            y: Target
            test_size: Proportion of test set
            random_state: Random seed
            stratify: Whether to stratify by target
            
        Returns:
            X_train, X_test, y_train, y_test
        """
        return train_test_split(
            X, y, 
            test_size=test_size, 
            random_state=random_state, 
            stratify=y if stratify else None
        )
    
    def fit_scaler(self, X_train):
        """
        Fit the scaler on training data.
        
        Args:
            X_train: Training features
        """
        self.scaler.fit(X_train)
        print("Scaler fitted on training data")
    
    def transform_features(self, X):
        """
        Transform features using fitted scaler.
        
        Args:
            X: Features to transform
            
        Returns:
            Scaled features
        """
        return self.scaler.transform(X)
    
    def fit_transform_features(self, X_train):
        """
        Fit scaler and transform training data.
        
        Args:
            X_train: Training features
            
        Returns:
            Scaled training features
        """
        return self.scaler.fit_transform(X_train)
    
    def save_scaler(self, filepath):
        """
        Save the fitted scaler to disk.
        
        Args:
            filepath: Path to save the scaler
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        joblib.dump(self.scaler, filepath)
        print(f"Scaler saved to {filepath}")
    
    def load_scaler(self, filepath):
        """
        Load a fitted scaler from disk.
        
        Args:
            filepath: Path to the saved scaler
        """
        self.scaler = joblib.load(filepath)
        print(f"Scaler loaded from {filepath}")
    
    def get_feature_names(self):
        """Get the list of feature names."""
        return self.feature_names


def preprocess_pipeline(data_path, config):
    """
    Complete preprocessing pipeline.
    
    Args:
        data_path: Path to the data CSV file
        config: Configuration dictionary
        
    Returns:
        X_train_scaled, X_test_scaled, y_train, y_test, preprocessor
    """
    preprocessor = DataPreprocessor(config)
    
    # Load data
    df = preprocessor.load_data(data_path)
    
    # Clean data
    df = preprocessor.clean_data(df)
    
    # Prepare features
    X, y = preprocessor.prepare_features(df)
    
    # Split data
    X_train, X_test, y_train, y_test = preprocessor.split_data(
        X, y,
        test_size=config.get('test_size', 0.3),
        random_state=config.get('random_state', 42),
        stratify=True
    )
    
    # Scale features
    X_train_scaled = preprocessor.fit_transform_features(X_train)
    X_test_scaled = preprocessor.transform_features(X_test)
    
    return X_train_scaled, X_test_scaled, y_train, y_test, preprocessor

