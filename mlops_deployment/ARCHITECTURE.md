# Architecture Overview

## System Design

```
┌─────────────────┐
│   Client/User   │
└────────┬────────┘
         │ HTTP/REST
         ▼
┌─────────────────┐
│   FastAPI App   │  ← api/app.py
│   (Port 8000)   │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Model Inference │  ← src/model_inference.py
│   (Prediction)  │
└────────┬────────┘
         │
         ├─────────────────┐
         ▼                 ▼
┌──────────────┐   ┌──────────────┐
│   MLP Model  │   │   Scaler     │
│  (model.pkl) │   │ (scaler.pkl) │
└──────────────┘   └──────────────┘
```

## Components

### 1. **Data Preprocessing** (`src/data_preprocessing.py`)
- Loads and cleans data
- Handles feature scaling
- Splits data into train/test sets
- Saves/loads scaler for production use

### 2. **Model Training** (`src/model_training.py`)
- Creates and trains MLP model
- Evaluates model performance
- Saves trained model and metrics

### 3. **Model Inference** (`src/model_inference.py`)
- Loads trained model and scaler
- Preprocesses input features
- Makes predictions
- Returns formatted results

### 4. **API Layer** (`api/app.py`)
- FastAPI REST API
- Endpoints:
  - `GET /` - API information
  - `GET /health` - Health check
  - `POST /predict` - Single prediction
  - `POST /predict/batch` - Batch predictions
- Automatic API documentation (Swagger/ReDoc)

### 5. **Training Script** (`scripts/train.py`)
- Orchestrates the training pipeline
- Loads configuration
- Runs preprocessing and training
- Saves artifacts

## Data Flow

### Training Phase
```
data.csv → Preprocessing → Train/Test Split → Model Training → model.pkl + scaler.pkl
```

### Inference Phase
```
Input Features → Scaling → Model Prediction → Formatted Response
```

## Model Information

- **Type:** Multi-Layer Perceptron (MLP)
- **Architecture:** 3 hidden layers (500, 500, 500 neurons)
- **Input:** 30 features (mean, se, worst for 10 base measurements)
- **Output:** Binary classification (0=Benign, 1=Malignant)
- **Performance:** ~97% accuracy, ~98% ROC-AUC

## Deployment Options

1. **Local Development:** Run `python scripts/run_api.py`
2. **Docker:** Build and run container
3. **Cloud:** Deploy to AWS/GCP/Azure using Docker
4. **Serverless:** Convert to serverless function (AWS Lambda, etc.)

## Security Considerations

- Input validation via Pydantic models
- Error handling and logging
- CORS configuration for web clients
- Rate limiting (can be added)
- Authentication/Authorization (can be added)

