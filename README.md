# Breast Cancer Detection - Machine Learning Project

A comprehensive machine learning project for breast cancer detection using the Wisconsin Diagnostic Dataset, featuring both research notebooks and a production-ready MLOps deployment with modern React frontend.

## Project Structure

```
Breast Cancer Detection/
├── Project_Machine_Learning_Paper.ipynb          # Main research notebook
├── Project_Machine_Learning_Paper_Explicatif.ipynb  # Detailed explanatory notebook
├── modular_ml_pipeline/                          # Production MLOps deployment
│   ├── api/                                      # FastAPI REST API
│   │   └── app.py                                # Main API server
│   ├── frontend/                                 # React + Vite frontend
│   │   ├── src/                                  # React source code
│   │   │   ├── pages/                           # Page components
│   │   │   ├── components/                     # Reusable components
│   │   │   └── services/                        # API services
│   │   └── package.json                         # Frontend dependencies
│   ├── src/                                      # ML modules
│   │   ├── models/                              # Model implementations
│   │   ├── preprocessing/                       # Data preprocessing
│   │   └── training/                            # Training scripts
│   ├── models/                                  # Trained models (gitignored)
│   ├── data/                                    # Dataset files
│   └── main.py                                  # Main training script
├── requirements.txt                             # Python dependencies
└── README.md                                    # This file

```

## Quick Start

### Prerequisites

- Python 3.8+
- Node.js 18+ and npm
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/hazemmrad17/Machine_Learning.git
cd Machine_Learning
```

### 2. Backend Setup (FastAPI)

```bash
# Install Python dependencies
pip install -r requirements.txt

# Train models (optional - models are already trained)
cd modular_ml_pipeline
python main.py

# Start the API server
cd api
uvicorn app:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 3. Frontend Setup (React)

```bash
# Navigate to frontend directory
cd modular_ml_pipeline/frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000` (or the port shown in terminal)

### 4. Access the Application

- **Frontend UI**: Open `http://localhost:3000` in your browser
- **API Documentation**: Open `http://localhost:8000/docs` for Swagger UI
- **API Health Check**: `http://localhost:8000/health`

## Features

### Machine Learning Models

- **Linear Regression** - Baseline logistic regression model
- **Softmax Regression** - Multi-class classification
- **Multi-Layer Perceptron (MLP)** - Deep neural network
- **Support Vector Machine (SVM)** - Kernel-based classifier
- **K-Nearest Neighbors (KNN)** - L1 and L2 distance variants
- **GRU-SVM Hybrid** - Recurrent neural network with SVM

### Frontend Features

- **Modern UI** - Beautiful neural network shader background with GSAP animations
- **Real-time Predictions** - Interactive prediction interface
- **Model Comparison** - Compare multiple models side-by-side
- **Hyperparameter Tuning** - Adjust model parameters and retrain
- **Visualizations** - Model performance metrics and charts
- **Model Visualization** - See models in action with real-time predictions

### API Endpoints

- `GET /health` - Health check
- `GET /models` - List available models
- `POST /predict` - Make predictions
- `POST /retrain` - Retrain models with custom hyperparameters
- `GET /models/{model_name}/info` - Get model information

## Model Performance

Based on the Wisconsin Diagnostic Dataset:

- **Best Model**: Multi-Layer Perceptron (MLP)
- **Accuracy**: ~97%
- **ROC-AUC**: ~98%
- **Precision**: ~96%
- **Recall**: ~98%

## Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Scikit-learn** - Machine learning library
- **NumPy & Pandas** - Data processing
- **Pickle** - Model serialization

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Three.js** - 3D graphics and shaders
- **GSAP** - Animations
- **React Query** - Data fetching
- **Framer Motion** - UI animations
- **Recharts** - Data visualization

## Documentation

- `modular_ml_pipeline/README.md` - MLOps deployment guide
- `modular_ml_pipeline/FRONTEND_README.md` - Frontend development guide
- `modular_ml_pipeline/api/README.md` - API documentation

## Research Paper

This project replicates and extends the methodology from:
**"On Breast Cancer Detection: An Application of Machine Learning Algorithms on the Wisconsin Diagnostic Dataset"**

The notebooks include:
- Comprehensive data analysis
- Feature engineering
- Model training and evaluation
- Hyperparameter optimization
- Results visualization

## Usage Examples

### Making a Prediction via API

```python
import requests

data = {
    "features": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189],
    "model": "mlp"
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

### Retraining a Model

```python
import requests

retrain_data = {
    "model": "mlp",
    "hyperparameters": {
        "hidden_layer_sizes": [100, 50],
        "learning_rate": 0.001,
        "max_iter": 1000
    }
}

response = requests.post("http://localhost:8000/retrain", json=retrain_data)
print(response.json())
```

## Development

### Running Tests

```bash
# Backend tests
cd modular_ml_pipeline
pytest tests/

# Frontend tests
cd frontend
npm test
```

### Building for Production

```bash
# Build frontend
cd modular_ml_pipeline/frontend
npm run build

# The built files will be in the `dist/` directory
```

## License

Educational use only. This project is for learning and research purposes.

## Disclaimer

This system is for **educational and research purposes only**. It should **not** be used as a substitute for professional medical diagnosis. Always consult qualified healthcare professionals for medical decisions.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Contact

For questions or issues, please open an issue on GitHub.

## Acknowledgments

- Wisconsin Diagnostic Breast Cancer Dataset
- Scikit-learn team for excellent ML tools
- React and Three.js communities for amazing libraries

---

**Made with love for Machine Learning Education**

