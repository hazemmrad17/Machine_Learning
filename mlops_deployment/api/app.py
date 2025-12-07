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
import yaml

# Load configuration
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

# Initialize FastAPI app
app = FastAPI(
    title="Breast Cancer Detection API",
    description="API for predicting malignant vs benign breast tumors",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize model inference
model_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['model_file'])
scaler_path = os.path.join(os.path.dirname(__file__), '..', config['paths']['scaler_file'])

try:
    inference = ModelInference(
        model_path=model_path,
        scaler_path=scaler_path,
        feature_names=EXPECTED_FEATURES
    )
    inference.load_model()
    inference.load_scaler()
    print("Model and scaler loaded successfully!")
except Exception as e:
    print(f"Warning: Could not load model: {e}")
    print("Please train the model first using: python scripts/train.py")
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
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "/predict": "POST - Make a prediction",
            "/health": "GET - Health check",
            "/docs": "GET - API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    model_loaded = inference is not None and inference.model is not None
    return {
        "status": "healthy" if model_loaded else "model_not_loaded",
        "model_loaded": model_loaded
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(features: FeatureInput):
    """
    Make a prediction on breast cancer features.
    
    Args:
        features: FeatureInput model with all 30 features
        
    Returns:
        PredictionResponse with prediction and probabilities
    """
    if inference is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    try:
        # Convert Pydantic model to dictionary
        feature_dict = features.dict()
        
        # Make prediction
        result = inference.predict(feature_dict)
        
        return PredictionResponse(**result)
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction error: {str(e)}"
        )


@app.post("/predict/batch", response_model=List[PredictionResponse])
async def predict_batch(features_list: List[FeatureInput]):
    """
    Make predictions on a batch of inputs.
    
    Args:
        features_list: List of FeatureInput models
        
    Returns:
        List of PredictionResponse objects
    """
    if inference is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Please train the model first."
        )
    
    try:
        # Convert to list of dictionaries
        feature_dicts = [f.dict() for f in features_list]
        
        # Make batch predictions
        results = inference.predict_batch(feature_dicts)
        
        return [PredictionResponse(**r) for r in results]
    
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
        host=api_config.get('host', '0.0.0.0'),
        port=api_config.get('port', 8000),
        reload=api_config.get('debug', False)
    )

