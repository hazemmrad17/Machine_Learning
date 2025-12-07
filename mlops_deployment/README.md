# Breast Cancer Detection - MLOps Deployment

This is the production-ready MLOps deployment of the Breast Cancer Detection project.

## Project Structure

```
mlops_deployment/
├── src/                    # Source code modules
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── model_training.py
│   └── model_inference.py
├── api/                    # API endpoints
│   ├── __init__.py
│   └── app.py             # FastAPI application
├── scripts/                # Training and utility scripts
│   ├── train.py           # Model training script
│   └── evaluate.py        # Model evaluation script
├── models/                 # Saved models (gitignored)
├── data/                   # Data files
├── tests/                  # Unit tests
├── config.yaml            # Configuration file
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker container definition
└── README.md             # This file
```

## Setup

### 1. Create Virtual Environment

**Windows (PowerShell):**
```powershell
.\setup_venv.ps1
```

**Linux/Mac:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
```

**Manual setup:**
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR
.\venv\Scripts\Activate.ps1  # Windows PowerShell
pip install -r requirements.txt
```

### 2. Train the Model

```bash
python scripts/train.py
```

### 3. Run the System

**Option A: Web UI (Recommended)**
```bash
python scripts/run_web_ui.py
```
Then open http://localhost:8501 in your browser

**Option B: API Only**
```bash
python scripts/run_api.py
```
API will be available at http://localhost:8000

**Option C: Both (2 terminals)**
- Terminal 1: `python scripts/run_api.py`
- Terminal 2: `python scripts/run_web_ui.py`

## API Usage

The API provides a REST endpoint for predictions:

```bash
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{
       "radius_mean": 17.99,
       "texture_mean": 10.38,
       ...
     }'
```

## Model Information

- **Model Type:** Multi-Layer Perceptron (MLP)
- **Architecture:** (500, 500, 500) hidden layers
- **Performance:** ~97% accuracy, ~98% ROC-AUC
- **Input Features:** 30 features from breast cancer measurements

