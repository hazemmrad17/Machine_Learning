"""
FastAPI Application for Breast Cancer Detection
Provides REST API endpoints for model predictions.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
import sys
import os

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.model_inference import ModelInference, EXPECTED_FEATURES
from src.multi_model_inference import MultiModelInference, EXPECTED_FEATURES as MULTI_FEATURES
import yaml

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize FastAPI app
app = FastAPI(
    title="Breast Cancer Detection API",
    description="API for predicting malignant vs benign breast tumors with multiple algorithms",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize multi-model inference (supports SVM, MLP, L1-NN, L2-NN)
scaler_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['scaler_file'])

try:
    multi_inference = MultiModelInference(
        scaler_path=scaler_path,
        feature_names=MULTI_FEATURES
    )
    multi_inference.load_scaler()
    available_models = multi_inference.get_available_models()
    print(f"Multi-model inference initialized! Available models: {available_models}")
except Exception as e:
    print(f"Warning: Could not initialize multi-model inference: {e}")
    print("Please train models first using: python scripts/train_all_models.py")
    multi_inference = None
    available_models = []

# Keep backward compatibility with old single model
try:
    model_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['model_file'])
    inference = ModelInference(
        model_path=model_path,
        scaler_path=scaler_path,
        feature_names=EXPECTED_FEATURES
    )
    inference.load_model()
    inference.load_scaler()
    print("Legacy single model loaded for backward compatibility")
except Exception as e:
    print(f"Warning: Could not load legacy model: {e}")
    inference = None


# Pydantic models for request/response
class FeatureInput(BaseModel):
    """Single feature input model."""
    radius_mean: float = Field(..., description="Mean radius")
    texture_mean: float = Field(..., description="Mean texture")
    perimeter_mean: float = Field(..., description="Mean perimeter")
    area_mean: float = Field(..., description="Mean area")
    smoothness_mean: float = Field(..., description="Mean smoothness")
    compactness_mean: float = Field(..., description="Mean compactness")
    concavity_mean: float = Field(..., description="Mean concavity")
    concave_points_mean: float = Field(..., description="Mean concave points")
    symmetry_mean: float = Field(..., description="Mean symmetry")
    fractal_dimension_mean: float = Field(..., description="Mean fractal dimension")
    radius_se: float = Field(..., description="Radius standard error")
    texture_se: float = Field(..., description="Texture standard error")
    perimeter_se: float = Field(..., description="Perimeter standard error")
    area_se: float = Field(..., description="Area standard error")
    smoothness_se: float = Field(..., description="Smoothness standard error")
    compactness_se: float = Field(..., description="Compactness standard error")
    concavity_se: float = Field(..., description="Concavity standard error")
    concave_points_se: float = Field(..., description="Concave points standard error")
    symmetry_se: float = Field(..., description="Symmetry standard error")
    fractal_dimension_se: float = Field(..., description="Fractal dimension standard error")
    radius_worst: float = Field(..., description="Worst radius")
    texture_worst: float = Field(..., description="Worst texture")
    perimeter_worst: float = Field(..., description="Worst perimeter")
    area_worst: float = Field(..., description="Worst area")
    smoothness_worst: float = Field(..., description="Worst smoothness")
    compactness_worst: float = Field(..., description="Worst compactness")
    concavity_worst: float = Field(..., description="Worst concavity")
    concave_points_worst: float = Field(..., description="Worst concave points")
    symmetry_worst: float = Field(..., description="Worst symmetry")
    fractal_dimension_worst: float = Field(..., description="Worst fractal dimension")


class PredictionResponse(BaseModel):
    """Prediction response model."""
    prediction: int = Field(..., description="Prediction: 0=Benign, 1=Malignant")
    prediction_label: str = Field(..., description="Prediction label")
    probability_malignant: float = Field(..., description="Probability of malignant")
    probability_benign: float = Field(..., description="Probability of benign")
    confidence: float = Field(..., description="Confidence score")


# API Endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Breast Cancer Detection API",
        "version": "2.0.0",
        "status": "running",
        "available_models": available_models,
        "endpoints": {
            "/predict": "POST - Make a prediction (supports model_type parameter)",
            "/predict/compare": "POST - Compare predictions from all models",
            "/models": "GET - List available models and their metrics",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    models_loaded = multi_inference is not None and len(available_models) > 0
    return {
        "status": "healthy" if models_loaded else "models_not_loaded",
        "models_loaded": models_loaded,
        "available_models": available_models
    }

@app.get("/models")
async def list_models():
    """List all available models and their performance metrics."""
    if multi_inference is None:
        raise HTTPException(
            status_code=503,
            detail="Multi-model inference not initialized"
        )
    
    models_info = {}
    for model_type in available_models:
        metrics = multi_inference.get_model_metrics(model_type)
        models_info[model_type] = {
            "name": model_type.upper(),
            "description": {
                "mlp": "Multi-Layer Perceptron Neural Network",
                "svm": "Support Vector Machine (RBF kernel)",
                "l1_nn": "K-Nearest Neighbors with Manhattan distance (L1)",
                "l2_nn": "K-Nearest Neighbors with Euclidean distance (L2)",
                "logistic_regression": "Logistic Regression (binary classification)",
                "softmax_regression": "Softmax Regression (multinomial logistic regression)"
            }.get(model_type, "Unknown model"),
            "metrics": metrics
        }
    
    return {
        "available_models": available_models,
        "models": models_info
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: FeatureInput, model_type: str = "mlp"):
    """
    Make a prediction on breast cancer features.
    
    Args:
        features: FeatureInput model with all 30 features
        model_type: Model to use - one of 'mlp', 'svm', 'l1_nn', 'l2_nn', 'logistic_regression', 'softmax_regression' (default: 'mlp')
        
    Returns:
        PredictionResponse with prediction and probabilities
    """
    if multi_inference is None:
        raise HTTPException(
            status_code=503,
            detail="Models not loaded. Please train models first using: python scripts/train_all_models.py"
        )
    
    if model_type not in available_models:
        raise HTTPException(
            status_code=400,
            detail=f"Model type '{model_type}' not available. Available models: {available_models}"
        )
    
    try:
        # Convert Pydantic model to dictionary
        feature_dict = features.dict()
        
        # Make prediction with specified model
        result = multi_inference.predict(feature_dict, model_type=model_type)
        
        # Return response (excluding model_metrics from response model)
        response = {
            'prediction': result['prediction'],
            'prediction_label': result['prediction_label'],
            'probability_malignant': result['probability_malignant'],
            'probability_benign': result['probability_benign'],
            'confidence': result['confidence']
        }
        
        return PredictionResponse(**response)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )

@app.post("/predict/compare")
async def compare_models(features: FeatureInput):
    """
    Compare predictions from all available models.
    
    Args:
        features: FeatureInput model with all 30 features
        
    Returns:
        Dictionary with predictions from all models
    """
    if multi_inference is None:
        raise HTTPException(
            status_code=503,
            detail="Models not loaded. Please train models first."
        )
    
    try:
        # Convert Pydantic model to dictionary
        feature_dict = features.dict()
        
        # Get comparisons from all models
        comparison = multi_inference.compare_models(feature_dict)
        
        return comparison
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Comparison error: {str(e)}"
        )


@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(features_list: List[FeatureInput], model_type: str = "mlp"):
    """
    Make predictions on a batch of inputs.
    
    Args:
        features_list: List of FeatureInput models
        model_type: Model to use - one of 'mlp', 'svm', 'l1_nn', 'l2_nn', 'logistic_regression', 'softmax_regression' (default: 'mlp')
        
    Returns:
        List of PredictionResponse objects
    """
    if multi_inference is None:
        raise HTTPException(
            status_code=503,
            detail="Models not loaded. Please train models first."
        )
    
    if model_type not in available_models:
        raise HTTPException(
            status_code=400,
            detail=f"Model type '{model_type}' not available. Available models: {available_models}"
        )
    
    try:
        # Convert to list of dictionaries
        feature_dicts = [f.dict() for f in features_list]
        
        # Make batch predictions
        results = multi_inference.predict_batch(feature_dicts, model_type=model_type)
        
        # Format responses
        responses = []
        for r in results:
            response = {
                'prediction': r['prediction'],
                'prediction_label': r['prediction_label'],
                'probability_malignant': r['probability_malignant'],
                'probability_benign': r['probability_benign'],
                'confidence': r['confidence']
            }
            responses.append(PredictionResponse(**response))
        
        return responses
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Batch prediction error: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    
    api_config = config.get('api', {})
    uvicorn.run(
        "app:app",
        host=api_config.get('host', 'localhost'),
        port=api_config.get('port', 8000),
        reload=api_config.get('debug', False)
    )

