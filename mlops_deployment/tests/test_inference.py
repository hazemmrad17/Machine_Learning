"""
Unit tests for model inference.
"""

import pytest
import numpy as np
from src.model_inference import ModelInference, EXPECTED_FEATURES


def test_feature_names():
    """Test that we have 30 features."""
    assert len(EXPECTED_FEATURES) == 30


def test_prepare_features():
    """Test feature preparation."""
    # Create dummy model inference (won't load actual model)
    inference = ModelInference(
        model_path="dummy.pkl",
        scaler_path="dummy.pkl",
        feature_names=EXPECTED_FEATURES
    )
    
    # Create sample data
    sample_data = {feature: 1.0 for feature in EXPECTED_FEATURES}
    
    # Prepare features
    features = inference.prepare_features(sample_data)
    
    assert features.shape == (1, 30)
    assert np.all(features == 1.0)


if __name__ == "__main__":
    pytest.main([__file__])

