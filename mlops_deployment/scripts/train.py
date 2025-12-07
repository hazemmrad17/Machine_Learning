"""
Training Script
Trains the MLP model and saves it for deployment.
"""

import sys
import os
import yaml

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.data_preprocessing import preprocess_pipeline
from src.model_training import train_model_pipeline

def main():
    """Main training function."""
    # Load configuration
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    print("="*60)
    print("Breast Cancer Detection - Model Training")
    print("="*60)
    
    # Get data path
    data_path = config['data']['data_path']
    if not os.path.exists(data_path):
        print(f"Error: Data file not found at {data_path}")
        print("Please ensure data.csv is in the parent directory")
        return
    
    # Preprocess data
    print("\n[1/3] Preprocessing data...")
    X_train, X_test, y_train, y_test, preprocessor = preprocess_pipeline(
        data_path, 
        config
    )
    
    # Save scaler
    scaler_path = config['paths']['scaler_file']
    preprocessor.save_scaler(scaler_path)
    
    print(f"\n[2/3] Training model...")
    print(f"Training samples: {X_train.shape[0]}")
    print(f"Test samples: {X_test.shape[0]}")
    
    # Train model
    trainer, metrics = train_model_pipeline(
        X_train, X_test, y_train, y_test, config
    )
    
    print("\n[3/3] Training completed!")
    print("\n=== Final Metrics ===")
    print(f"Accuracy: {metrics['accuracy']:.4f}")
    print(f"ROC-AUC: {metrics['roc_auc']:.4f}")
    print(f"Recall: {metrics['recall']:.4f}")
    print(f"Precision: {metrics['precision']:.4f}")
    print(f"F1-Score: {metrics['f1_score']:.4f}")
    
    print(f"\nModel saved to: {config['paths']['model_file']}")
    print(f"Scaler saved to: {config['paths']['scaler_file']}")
    print("\n✓ Ready for deployment!")

if __name__ == "__main__":
    main()

