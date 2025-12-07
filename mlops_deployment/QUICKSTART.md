# 🚀 Quick Start Guide

## ✅ Step 1: Setup Virtual Environment

**Windows PowerShell:**
```powershell
.\setup_venv.ps1
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
chmod +x setup_venv.sh
./setup_venv.sh
source venv/bin/activate
```

## ✅ Step 2: Train the Model (if not already done)

```powershell
python scripts/train.py
```

This will:
- Load and preprocess the data
- Train the MLP model
- Save model to `models/mlp_model.pkl`
- Save scaler to `models/scaler.pkl`

## ✅ Step 3: Launch the System

### Option A: Run Everything Together (Recommended)

```powershell
python scripts/run_all.py
```

This starts both:
- 🌐 **Web UI** at http://localhost:8501
- 🔌 **API** at http://localhost:8000

### Option B: Run Separately (2 terminals)

**Terminal 1 - API:**
```powershell
python scripts/run_api.py
```

**Terminal 2 - Web UI:**
```powershell
python scripts/run_web_ui.py
```

## 🎯 Step 4: Use the Web Interface

1. Open your browser: **http://localhost:8501**
2. You'll see a beautiful Streamlit interface
3. **Manual Input Tab**: Enter 30 features one by one
4. **CSV Upload Tab**: Upload CSV for batch predictions
5. Click "Make Prediction"
6. View results with probabilities!

## 📊 Web UI Features

- ✅ **Manual Input**: Enter features individually
- ✅ **CSV Upload**: Batch predictions from CSV
- ✅ **Example Data**: Load sample data with one click
- ✅ **Real-time Predictions**: Instant results
- ✅ **Visual Results**: Color-coded predictions (Green=Benign, Red=Malignant)
- ✅ **Probability Display**: See confidence scores

## 🔧 Troubleshooting

### If packages don't install:

```powershell
# Activate venv first
.\venv\Scripts\Activate.ps1

# Install with pre-built wheels (no compilation)
pip install scikit-learn pandas numpy fastapi "uvicorn[standard]" pydantic streamlit requests pyyaml python-dotenv joblib --only-binary :all:
```

### If API is not connecting:

- Make sure API is running on port 8000
- Check the API status in the Web UI sidebar
- Try: `python scripts/run_api.py` in a separate terminal

### If Web UI doesn't start:

- Make sure port 8501 is not in use
- Try: `streamlit run web_ui/app.py --server.port 8502`

### If you get "ModuleNotFoundError":

```powershell
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 📝 Notes

- The Web UI requires the API to be running
- Model must be trained before using the Web UI
- All dependencies are in `requirements.txt`
- Virtual environment is in `venv/` folder

## 🎉 You're Ready!

Enjoy your MLOps workflow! The system is now ready for:
- ✅ Model training
- ✅ API inference
- ✅ Web UI predictions
- ✅ Batch processing
