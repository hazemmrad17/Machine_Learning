"""
Streamlit Web UI for Breast Cancer Detection
Provides an interactive interface for model predictions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import sys
import os
import requests
import json
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Optional imports with fallbacks
try:
    from streamlit_extras.colored_header import colored_header
except ImportError:
    def colored_header(label, description="", color_name="blue-70"):
        st.markdown(f"### {label}")
        if description:
            st.caption(description)

try:
    from streamlit_extras.metric_cards import style_metric_cards
except ImportError:
    def style_metric_cards(*args, **kwargs):
        pass  # No-op if not available

# Import utilities
try:
    from .utils import calculate_risk_score, generate_pdf_report, load_model_for_shap
except ImportError:
    # Fallback if utils not available
    def calculate_risk_score(features, prediction):
        return {'score': 50, 'level': 'Moderate', 'color': '#ffc107', 'breakdown': {}, 'confidence_contribution': 0}
    def generate_pdf_report(*args, **kwargs):
        return None
    def load_model_for_shap():
        return None, None

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Page configuration
st.set_page_config(
    page_title="Breast Cancer Detection",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with animations
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #1f77b4, #ff7f0e, #2ca02c);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        animation: fadeInDown 0.8s ease-out;
    }
    
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateX(-20px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.05);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }
    
    .prediction-box {
        padding: 2rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        animation: slideIn 0.5s ease-out;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .prediction-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 12px rgba(0, 0, 0, 0.15);
    }
    
    .benign {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%);
        border: 3px solid #28a745;
        animation: pulse 2s infinite;
        color: #155724 !important;
    }
    
    .benign h2 {
        color: #155724 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3) !important;
        font-weight: bold !important;
    }
    
    .malignant {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%);
        border: 3px solid #dc3545;
        animation: pulse 2s infinite;
        color: #721c24 !important;
    }
    
    .malignant h2 {
        color: #dc3545 !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.5) !important;
        font-weight: bold !important;
    }
    
    
    .metric-card {
        background: linear-gradient(135deg, #f0f2f6 0%, #e9ecef 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        animation: fadeInDown 0.6s ease-out;
    }
    
    .metric-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
    }
    
    .loading-spinner {
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        animation: spin 1s linear infinite;
        margin: 20px auto;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .success-badge {
        background: linear-gradient(135deg, #28a745 0%, #20c997 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        animation: slideIn 0.5s ease-out;
    }
    
    .warning-badge {
        background: linear-gradient(135deg, #dc3545 0%, #c82333 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        display: inline-block;
        animation: slideIn 0.5s ease-out;
    }
    
    .feature-card {
        background: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #3498db;
        transition: all 0.3s ease;
    }
    
    .feature-card:hover {
        border-left-width: 6px;
        transform: translateX(5px);
    }
    
    .stButton>button {
        border-radius: 10px;
        transition: all 0.3s ease;
        font-weight: 600;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    
    .progress-bar-container {
        background: #e9ecef;
        border-radius: 10px;
        overflow: hidden;
        height: 30px;
        position: relative;
        margin: 1rem 0;
    }
    
    .progress-bar-fill {
        height: 100%;
        border-radius: 10px;
        transition: width 1s ease-out;
        display: flex;
        align-items: center;
        justify-content: center;
        color: white;
        font-weight: bold;
    }
    
    .progress-benign {
        background: linear-gradient(90deg, #28a745, #20c997);
    }
    
    .progress-malignant {
        background: linear-gradient(90deg, #dc3545, #c82333);
    }
    
    .confetti {
        position: fixed;
        width: 10px;
        height: 10px;
        background: #f0f;
        position: absolute;
        animation: confetti-fall 3s linear infinite;
    }
    
    @keyframes confetti-fall {
        to {
            transform: translateY(100vh) rotate(360deg);
        }
    }
</style>
""", unsafe_allow_html=True)

# API Configuration
API_URL = os.getenv("API_URL", "http://localhost:8000")

# Expected features (30 features)
FEATURES = [
    'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
    'smoothness_mean', 'compactness_mean', 'concavity_mean',
    'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
    'radius_se', 'texture_se', 'perimeter_se', 'area_se',
    'smoothness_se', 'compactness_se', 'concavity_se',
    'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
    'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
    'smoothness_worst', 'compactness_worst', 'concavity_worst',
    'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

def check_api_health():
    """Check if API is running."""
    try:
        response = requests.get(f"{API_URL}/health", timeout=2)
        return response.status_code == 200
    except:
        return False

def make_prediction(features):
    """Make prediction via API."""
    try:
        response = requests.post(
            f"{API_URL}/predict",
            json=features,
            timeout=5
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"API Error: {response.status_code}"}
    except requests.exceptions.ConnectionError:
        return {"error": "Cannot connect to API. Make sure the API is running on port 8000."}
    except Exception as e:
        return {"error": str(e)}

def main():
    """Main application."""
    # Header with animation
    st.markdown("""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 class="main-header">🏥 Breast Cancer Detection System</h1>
        <p style="font-size: 1.2rem; color: #b0b0b0; animation: fadeInDown 1s ease-out 0.2s both;">
            AI-Powered Medical Diagnosis Assistant
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Dark theme styles (default)
    st.markdown("""
    <style>
    /* Dark Theme Styles (Default) */
    .stApp {
        background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 50%, #0f0f0f 100%);
        color: #e0e0e0;
    }
    
    .main .block-container {
        background: rgba(20, 20, 20, 0.95);
        border-radius: 15px;
        padding: 2rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Text colors */
    h1, h2, h3, h4, h5, h6, p, label, div {
        color: #e0e0e0 !important;
    }
    
    /* Input fields */
    .stNumberInput > div > div > input,
    .stTextInput > div > div > input,
    .stSelectbox > div > div > select,
    .stTextArea > div > div > textarea {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
        border: 2px solid #444 !important;
        border-radius: 6px !important;
    }
    
    .stNumberInput > div > div > input:focus,
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > select:focus {
        border-color: #1f77b4 !important;
        box-shadow: 0 0 0 3px rgba(31, 119, 180, 0.2) !important;
    }
    
    /* Input labels */
    .stNumberInput label,
    .stTextInput label,
    .stSelectbox label {
        color: #e0e0e0 !important;
        font-weight: 600 !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #1f77b4 !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        box-shadow: 0 2px 4px rgba(31, 119, 180, 0.3) !important;
    }
    
    .stButton > button:hover {
        background-color: #1565a0 !important;
        box-shadow: 0 4px 8px rgba(31, 119, 180, 0.4) !important;
        transform: translateY(-2px) !important;
    }
    
    button[kind="primary"] {
        background-color: #1f77b4 !important;
        color: #ffffff !important;
    }
    
    button[kind="secondary"] {
        background-color: #6c757d !important;
        color: #ffffff !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a1a 0%, #0f0f0f 100%);
    }
    
    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label {
        color: #e0e0e0 !important;
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        color: #e0e0e0 !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b0b0b0 !important;
    }
    
    /* Dataframes */
    .dataframe {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background-color: #1a1a1a;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #b0b0b0;
    }
    
    .stTabs [aria-selected="true"] {
        color: #1f77b4 !important;
        border-bottom: 3px solid #1f77b4 !important;
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        color: #e0e0e0 !important;
    }
    
    /* Code blocks */
    .stCodeBlock {
        background-color: #2a2a2a !important;
        border: 1px solid #444 !important;
    }
    
    /* Selectbox dropdown */
    [data-baseweb="select"] {
        background-color: #2a2a2a !important;
        color: #e0e0e0 !important;
    }
    
    /* File uploader */
    .stFileUploader label {
        color: #e0e0e0 !important;
    }
    
    /* Toggle switch */
    .stCheckbox label,
    .stToggle label {
        color: #e0e0e0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Sidebar with enhanced UI
    with st.sidebar:
        colored_header(
            label="⚙️ Configuration",
            description="System Settings",
            color_name="blue-70"
        )
        
        # API Status with better styling
        api_status = check_api_health()
        if api_status:
            st.success("✅ **API Connected**", icon="🟢")
        else:
            st.error("❌ **API Not Connected**", icon="🔴")
            with st.expander("How to start API"):
                st.code("python scripts/run_api.py", language="bash")
        
        st.divider()
        
        st.divider()
        
        # API URL Configuration
        with st.expander("🔗 API Settings"):
            api_url_input = st.text_input("API URL", value=API_URL, label_visibility="collapsed")
            if api_url_input != API_URL:
                st.info(f"Using: {api_url_input}")
        
        st.divider()
        
        # Load example data buttons with better UI
        colored_header(
            label="📋 Example Data",
            description="Load sample cases",
            color_name="green-70"
        )
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("✅ Benign", use_container_width=True, type="secondary"):
                example_path = os.path.join(os.path.dirname(__file__), 'examples', 'benign_example.json')
                if os.path.exists(example_path):
                    with open(example_path, 'r') as f:
                        example_data = json.load(f)
                    st.session_state.loaded_example = example_data
                    st.session_state.example_type = "Benign"
                    st.success("✅ Loaded!", icon="✅")
                    st.rerun()
                else:
                    st.error("File not found")
        
        with col2:
            if st.button("⚠️ Malignant", use_container_width=True, type="secondary"):
                example_path = os.path.join(os.path.dirname(__file__), 'examples', 'malignant_example.json')
                if os.path.exists(example_path):
                    with open(example_path, 'r') as f:
                        example_data = json.load(f)
                    st.session_state.loaded_example = example_data
                    st.session_state.example_type = "Malignant"
                    st.success("⚠️ Loaded!", icon="⚠️")
                    st.rerun()
                else:
                    st.error("File not found")
        
        # Clear loaded example
        if 'loaded_example' in st.session_state:
            if st.button("🗑️ Clear", use_container_width=True):
                del st.session_state.loaded_example
                if 'example_type' in st.session_state:
                    del st.session_state.example_type
                st.rerun()
        
        st.divider()
        
        # Quick Stats
        if 'prediction_history' in st.session_state and len(st.session_state.prediction_history) > 0:
            colored_header(
                label="📊 Quick Stats",
                description="Session Statistics",
                color_name="orange-70"
            )
            total = len(st.session_state.prediction_history)
            malignant_count = sum(1 for p in st.session_state.prediction_history if p.get('prediction') == 'Malignant')
            benign_count = total - malignant_count
            st.metric("Total Predictions", total)
            st.metric("Benign", benign_count, delta=f"{benign_count/total*100:.1f}%")
            st.metric("Malignant", malignant_count, delta=f"{malignant_count/total*100:.1f}%")
        
        # Initialize prediction history
        if 'prediction_history' not in st.session_state:
            st.session_state.prediction_history = []
    
    # Main content
    if not api_status:
        st.error("⚠️ **API Server Not Running**")
        st.info("""
        To start the API server, run:
        ```bash
        python scripts/run_api.py
        ```
        Or in a separate terminal:
        ```bash
        cd mlops_deployment
        python -m uvicorn api.app:app --host localhost --port 8000
        ```
        """)
        return
    
    # Create tabs directly (no option menu)
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🔬 Manual Input", 
        "📊 CSV Upload", 
        "📈 Prediction History",
        "📄 Export Reports",
        "ℹ️ About"
    ])
    
    with tab1:
        st.header("Enter Patient Data")
        st.markdown("Enter the 30 features from breast cancer measurements.")
        
        # Check if example data is loaded
        default_values = {}
        if 'loaded_example' in st.session_state:
            default_values = st.session_state.loaded_example
            st.info(f"📋 **{st.session_state.get('example_type', 'Example')} example loaded** - Values below are from a real dataset")
        else:
            # Default values (malignant example)
            default_values = {
                'radius_mean': 17.99, 'texture_mean': 10.38, 'perimeter_mean': 122.8, 'area_mean': 1001.0,
                'smoothness_mean': 0.1184, 'compactness_mean': 0.2776, 'concavity_mean': 0.3001,
                'concave_points_mean': 0.1471, 'symmetry_mean': 0.2419, 'fractal_dimension_mean': 0.07871,
                'radius_se': 1.095, 'texture_se': 0.9053, 'perimeter_se': 8.589, 'area_se': 153.4,
                'smoothness_se': 0.006399, 'compactness_se': 0.04904, 'concavity_se': 0.05373,
                'concave_points_se': 0.01587, 'symmetry_se': 0.03003, 'fractal_dimension_se': 0.006193,
                'radius_worst': 25.38, 'texture_worst': 17.33, 'perimeter_worst': 184.6, 'area_worst': 2019.0,
                'smoothness_worst': 0.1622, 'compactness_worst': 0.6656, 'concavity_worst': 0.7119,
                'concave_points_worst': 0.2654, 'symmetry_worst': 0.4601, 'fractal_dimension_worst': 0.1189
            }
        
        # Create form with feature inputs
        col1, col2, col3 = st.columns(3)
        
        features_dict = {}
        
        with col1:
            st.subheader("Mean Values")
            features_dict['radius_mean'] = st.number_input("Radius Mean", value=default_values.get('radius_mean', 17.99), format="%.4f")
            features_dict['texture_mean'] = st.number_input("Texture Mean", value=default_values.get('texture_mean', 10.38), format="%.4f")
            features_dict['perimeter_mean'] = st.number_input("Perimeter Mean", value=default_values.get('perimeter_mean', 122.8), format="%.4f")
            features_dict['area_mean'] = st.number_input("Area Mean", value=default_values.get('area_mean', 1001.0), format="%.2f")
            features_dict['smoothness_mean'] = st.number_input("Smoothness Mean", value=default_values.get('smoothness_mean', 0.1184), format="%.6f")
            features_dict['compactness_mean'] = st.number_input("Compactness Mean", value=default_values.get('compactness_mean', 0.2776), format="%.6f")
            features_dict['concavity_mean'] = st.number_input("Concavity Mean", value=default_values.get('concavity_mean', 0.3001), format="%.6f")
            features_dict['concave_points_mean'] = st.number_input("Concave Points Mean", value=default_values.get('concave_points_mean', 0.1471), format="%.6f")
            features_dict['symmetry_mean'] = st.number_input("Symmetry Mean", value=default_values.get('symmetry_mean', 0.2419), format="%.6f")
            features_dict['fractal_dimension_mean'] = st.number_input("Fractal Dimension Mean", value=default_values.get('fractal_dimension_mean', 0.07871), format="%.6f")
        
        with col2:
            st.subheader("Standard Error")
            features_dict['radius_se'] = st.number_input("Radius SE", value=default_values.get('radius_se', 1.095), format="%.4f")
            features_dict['texture_se'] = st.number_input("Texture SE", value=default_values.get('texture_se', 0.9053), format="%.4f")
            features_dict['perimeter_se'] = st.number_input("Perimeter SE", value=default_values.get('perimeter_se', 8.589), format="%.4f")
            features_dict['area_se'] = st.number_input("Area SE", value=default_values.get('area_se', 153.4), format="%.2f")
            features_dict['smoothness_se'] = st.number_input("Smoothness SE", value=default_values.get('smoothness_se', 0.006399), format="%.6f")
            features_dict['compactness_se'] = st.number_input("Compactness SE", value=default_values.get('compactness_se', 0.04904), format="%.6f")
            features_dict['concavity_se'] = st.number_input("Concavity SE", value=default_values.get('concavity_se', 0.05373), format="%.6f")
            features_dict['concave_points_se'] = st.number_input("Concave Points SE", value=default_values.get('concave_points_se', 0.01587), format="%.6f")
            features_dict['symmetry_se'] = st.number_input("Symmetry SE", value=default_values.get('symmetry_se', 0.03003), format="%.6f")
            features_dict['fractal_dimension_se'] = st.number_input("Fractal Dimension SE", value=default_values.get('fractal_dimension_se', 0.006193), format="%.6f")
        
        with col3:
            st.subheader("Worst Values")
            features_dict['radius_worst'] = st.number_input("Radius Worst", value=default_values.get('radius_worst', 25.38), format="%.4f")
            features_dict['texture_worst'] = st.number_input("Texture Worst", value=default_values.get('texture_worst', 17.33), format="%.4f")
            features_dict['perimeter_worst'] = st.number_input("Perimeter Worst", value=default_values.get('perimeter_worst', 184.6), format="%.2f")
            features_dict['area_worst'] = st.number_input("Area Worst", value=default_values.get('area_worst', 2019.0), format="%.2f")
            features_dict['smoothness_worst'] = st.number_input("Smoothness Worst", value=default_values.get('smoothness_worst', 0.1622), format="%.6f")
            features_dict['compactness_worst'] = st.number_input("Compactness Worst", value=default_values.get('compactness_worst', 0.6656), format="%.6f")
            features_dict['concavity_worst'] = st.number_input("Concavity Worst", value=default_values.get('concavity_worst', 0.7119), format="%.6f")
            features_dict['concave_points_worst'] = st.number_input("Concave Points Worst", value=default_values.get('concave_points_worst', 0.2654), format="%.6f")
            features_dict['symmetry_worst'] = st.number_input("Symmetry Worst", value=default_values.get('symmetry_worst', 0.4601), format="%.6f")
            features_dict['fractal_dimension_worst'] = st.number_input("Fractal Dimension Worst", value=default_values.get('fractal_dimension_worst', 0.1189), format="%.6f")
        
        # Predict button with enhanced styling
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            predict_button = st.button("🔍 Make Prediction", type="primary", use_container_width=True)
        
        # Make prediction with loading animation
        if predict_button:
            # Custom loading message
            loading_placeholder = st.empty()
            with loading_placeholder.container():
                st.markdown("""
                <div style="text-align: center; padding: 2rem;">
                    <div class="loading-spinner"></div>
                    <h3 style="color: #1f77b4; margin-top: 1rem;">Analyzing patient data...</h3>
                    <p style="color: #666;">Please wait while our AI model processes the information</p>
                </div>
                """, unsafe_allow_html=True)
            
            result = make_prediction(features_dict)
            loading_placeholder.empty()
            
            if "error" in result:
                st.error(f"❌ Error: {result['error']}")
            else:
                # Display results
                st.divider()
                st.header("📊 Prediction Results")
                
                # Prediction box with enhanced styling
                is_malignant = result['prediction'] == 1
                box_class = "malignant" if is_malignant else "benign"
                icon = "⚠️" if is_malignant else "✅"
                color = "#ff4444" if is_malignant else "#28a745"  # Brighter red for better visibility
                emoji = "🔴" if is_malignant else "🟢"
                
                # Prediction box
                st.markdown(f"""
                <div class="prediction-box {box_class}">
                    <div style="text-align: center;">
                        <h1 style="color: {color}; margin: 0; font-size: 3rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{emoji}</h1>
                        <h2 style="text-align: center; color: {color}; margin-top: 0.5rem; font-weight: bold; text-shadow: 2px 2px 4px rgba(0,0,0,0.5); font-size: 2rem;">
                            {icon} {result['prediction_label']}
                        </h2>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Add explanation about 100% probability (separate markdown for proper rendering)
                if result['confidence'] >= 0.99:
                    st.info("""
                    **ℹ️ About High Confidence:**
                    
                    A confidence level of 100% means the model is very certain based on the input features. 
                    This is normal for well-trained models when features strongly indicate one class. 
                    However, always consult with medical professionals for final diagnosis.
                    """)
                
                # Confetti effect for benign predictions (using CSS animation)
                if not is_malignant:
                    st.markdown("""
                    <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; pointer-events: none; z-index: 9999;">
                        <div style="animation: confetti-fall 3s ease-out infinite; background: #28a745; width: 10px; height: 10px; position: absolute; left: 10%;"></div>
                        <div style="animation: confetti-fall 3s ease-out 0.5s infinite; background: #20c997; width: 10px; height: 10px; position: absolute; left: 30%;"></div>
                        <div style="animation: confetti-fall 3s ease-out 1s infinite; background: #28a745; width: 10px; height: 10px; position: absolute; left: 50%;"></div>
                        <div style="animation: confetti-fall 3s ease-out 1.5s infinite; background: #20c997; width: 10px; height: 10px; position: absolute; left: 70%;"></div>
                        <div style="animation: confetti-fall 3s ease-out 2s infinite; background: #28a745; width: 10px; height: 10px; position: absolute; left: 90%;"></div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Metrics
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric(
                        "Probability (Malignant)",
                        f"{result['probability_malignant']:.2%}",
                        delta=None
                    )
                
                with col2:
                    st.metric(
                        "Probability (Benign)",
                        f"{result['probability_benign']:.2%}",
                        delta=None
                    )
                
                with col3:
                    st.metric(
                        "Confidence",
                        f"{result['confidence']:.2%}",
                        delta=None
                    )
                
                with col4:
                    st.metric(
                        "Prediction",
                        result['prediction_label'],
                        delta=None
                    )
                
                # Enhanced progress bars with animations
                st.subheader("📊 Probability Distribution")
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**⚠️ Malignant:** {result['probability_malignant']:.2%}")
                    st.markdown(f"""
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill progress-malignant" style="width: {result['probability_malignant']*100}%;">
                            {result['probability_malignant']:.1%}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"**✅ Benign:** {result['probability_benign']:.2%}")
                    st.markdown(f"""
                    <div class="progress-bar-container">
                        <div class="progress-bar-fill progress-benign" style="width: {result['probability_benign']*100}%;">
                            {result['probability_benign']:.1%}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Interactive probability chart with Plotly
                fig = go.Figure()
                
                categories = ['Benign', 'Malignant']
                probabilities = [result['probability_benign'], result['probability_malignant']]
                colors = ['#28a745', '#dc3545']
                
                fig.add_trace(go.Bar(
                    x=categories,
                    y=probabilities,
                    marker_color=colors,
                    text=[f'{p:.2%}' for p in probabilities],
                    textposition='auto',
                    hovertemplate='<b>%{x}</b><br>Probability: %{y:.2%}<extra></extra>',
                    name='Probability'
                ))
                
                fig.update_layout(
                    title='📊 Prediction Probabilities (Interactive)',
                    xaxis_title='Diagnosis',
                    yaxis_title='Probability',
                    yaxis=dict(range=[0, 1]),
                    height=400,
                    template='plotly_white',
                    showlegend=False,
                    font=dict(family="Poppins", size=12)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Gauge chart for confidence
                fig_gauge = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = result['confidence'] * 100,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Confidence Level"},
                    delta = {'reference': 50},
                    gauge = {
                        'axis': {'range': [None, 100]},
                        'bar': {'color': "#1f77b4"},
                        'steps': [
                            {'range': [0, 50], 'color': "lightgray"},
                            {'range': [50, 80], 'color': "gray"},
                            {'range': [80, 100], 'color': "darkgray"}
                        ],
                        'threshold': {
                            'line': {'color': "red", 'width': 4},
                            'thickness': 0.75,
                            'value': 90
                        }
                    }
                ))
                
                fig_gauge.update_layout(height=300, font=dict(family="Poppins"))
                st.plotly_chart(fig_gauge, use_container_width=True)
                
                # Feature importance visualization (top features) - Interactive
                st.subheader("📊 Feature Analysis")
                feature_values = pd.Series(features_dict)
                
                # Top 10 features by absolute value
                top_features = feature_values.abs().nlargest(10).sort_values(ascending=True)
                
                fig = go.Figure(go.Bar(
                    x=top_features.values,
                    y=top_features.index,
                    orientation='h',
                    marker=dict(
                        color=top_features.values,
                        colorscale='Viridis',
                        showscale=True,
                        colorbar=dict(title="Magnitude")
                    ),
                    text=[f'{v:.4f}' for v in top_features.values],
                    textposition='auto',
                    hovertemplate='<b>%{y}</b><br>Value: %{x:.4f}<extra></extra>'
                ))
                
                fig.update_layout(
                    title='Top 10 Features by Magnitude (Interactive)',
                    xaxis_title='Feature Value',
                    yaxis_title='Feature',
                    height=500,
                    template='plotly_white',
                    font=dict(family="Poppins", size=11)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Comparison with reference values (normal ranges)
                st.subheader("🔍 Comparison with Normal Ranges")
                
                # Reference values (approximate normal ranges from dataset)
                reference_ranges = {
                    'radius_mean': (10.0, 15.0),
                    'texture_mean': (15.0, 20.0),
                    'perimeter_mean': (80.0, 120.0),
                    'area_mean': (500.0, 900.0),
                    'smoothness_mean': (0.08, 0.12),
                    'compactness_mean': (0.05, 0.15),
                    'concavity_mean': (0.02, 0.10),
                    'concave_points_mean': (0.01, 0.05),
                }
                
                # Select a few key features for comparison
                key_features = ['radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean']
                
                comparison_data = []
                for feat in key_features:
                    if feat in features_dict and feat in reference_ranges:
                        val = features_dict[feat]
                        low, high = reference_ranges[feat]
                        status = "Normal" if low <= val <= high else ("High" if val > high else "Low")
                        comparison_data.append({
                            'Feature': feat.replace('_', ' ').title(),
                            'Value': val,
                            'Normal Low': low,
                            'Normal High': high,
                            'Status': status
                        })
                
                if comparison_data:
                    comp_df = pd.DataFrame(comparison_data)
                    
                    fig = go.Figure()
                    
                    for idx, row in comp_df.iterrows():
                        color = '#28a745' if row['Status'] == 'Normal' else '#dc3545'
                        fig.add_trace(go.Scatter(
                            x=[row['Normal Low'], row['Normal High']],
                            y=[row['Feature'], row['Feature']],
                            mode='lines',
                            line=dict(color='lightblue', width=8),
                            name='Normal Range',
                            showlegend=(idx == 0),
                            hovertemplate='Normal Range: %{x[0]:.2f} - %{x[1]:.2f}<extra></extra>'
                        ))
                        fig.add_trace(go.Scatter(
                            x=[row['Value']],
                            y=[row['Feature']],
                            mode='markers',
                            marker=dict(size=15, color=color, symbol='diamond'),
                            name=row['Status'],
                            hovertemplate=f'<b>{row["Feature"]}</b><br>Value: %{{x:.2f}}<br>Status: {row["Status"]}<extra></extra>'
                        ))
                    
                    fig.update_layout(
                        title='Feature Values vs Normal Ranges',
                        xaxis_title='Value',
                        yaxis_title='Feature',
                        height=300,
                        template='plotly_white',
                        font=dict(family="Poppins", size=11),
                        hovermode='closest'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Status summary
                    normal_count = sum(1 for d in comparison_data if d['Status'] == 'Normal')
                    st.info(f"📈 **Status:** {normal_count}/{len(comparison_data)} features within normal range")
                
                # Calculate Risk Score
                st.subheader("🎯 Personalized Risk Assessment")
                risk_score = calculate_risk_score(features_dict, result)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Risk Score", f"{risk_score['score']:.1f}/100")
                with col2:
                    # Enhanced risk level display with better visibility
                    risk_text_color = "#ffffff" if risk_score['score'] > 50 else "#000000"
                    st.markdown(f"""
                    <div style="padding: 1.5rem; background: {risk_score['color']}; border-radius: 10px; text-align: center; box-shadow: 0 4px 6px rgba(0,0,0,0.3);">
                        <h3 style="color: {risk_text_color}; margin: 0; font-weight: bold; font-size: 1.5rem; text-shadow: 2px 2px 4px rgba(0,0,0,0.5);">{risk_score['level']} Risk</h3>
                    </div>
                    """, unsafe_allow_html=True)
                with col3:
                    # Risk gauge
                    fig_risk = go.Figure(go.Indicator(
                        mode = "gauge+number",
                        value = risk_score['score'],
                        domain = {'x': [0, 1], 'y': [0, 1]},
                        title = {'text': "Risk Level"},
                        gauge = {
                            'axis': {'range': [None, 100]},
                            'bar': {'color': risk_score['color']},
                            'steps': [
                                {'range': [0, 30], 'color': "#28a745"},
                                {'range': [30, 60], 'color': "#ffc107"},
                                {'range': [60, 80], 'color': "#fd7e14"},
                                {'range': [80, 100], 'color': "#dc3545"}
                            ],
                            'threshold': {
                                'line': {'color': "red", 'width': 4},
                                'thickness': 0.75,
                                'value': risk_score['score']
                            }
                        }
                    ))
                    fig_risk.update_layout(height=250)
                    st.plotly_chart(fig_risk, use_container_width=True)
                
                # Risk breakdown
                with st.expander("📊 Risk Score Breakdown"):
                    risk_df = pd.DataFrame([
                        {
                            'Feature': feat.replace('_', ' ').title(),
                            'Value': info['value'],
                            'Contribution': f"{info['contribution']:.2f}%"
                        }
                        for feat, info in risk_score['breakdown'].items()
                    ])
                    st.dataframe(risk_df, use_container_width=True, hide_index=True)
                    st.info(f"Confidence Contribution: {risk_score['confidence_contribution']:.2f}%")
                
                # Save to history with full details
                prediction_record = {
                    'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'prediction': result['prediction_label'],
                    'probability_malignant': result['probability_malignant'],
                    'probability_benign': result['probability_benign'],
                    'confidence': result['confidence'],
                    'risk_score': risk_score['score'],
                    'risk_level': risk_score['level'],
                    'features': features_dict.copy()
                }
                st.session_state.prediction_history.append(prediction_record)
                
                # Store current result for export
                st.session_state.last_prediction = {
                    'result': result,
                    'features': features_dict,
                    'risk_score': risk_score,
                    'timestamp': prediction_record['timestamp']
                }
                
                # Show recent history
                if len(st.session_state.prediction_history) > 1:
                    st.subheader("📜 Recent Predictions")
                    recent_history = st.session_state.prediction_history[-5:]
                    history_df = pd.DataFrame([
                        {
                            'Time': h['timestamp'],
                            'Prediction': h['prediction'],
                            'Confidence': f"{h['confidence']:.2%}",
                            'Risk Score': f"{h.get('risk_score', 0):.1f}"
                        }
                        for h in recent_history
                    ])
                    st.dataframe(history_df, use_container_width=True, hide_index=True)
    
    with tab2:
        st.header("Upload CSV File")
        st.markdown("Upload a CSV file with patient data for batch predictions.")
        
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
        
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.success(f"✅ File loaded: {len(df)} rows")
                
                # Display preview
                st.subheader("Data Preview")
                st.dataframe(df.head())
                
                # Check if all features are present
                missing_features = [f for f in FEATURES if f not in df.columns]
                if missing_features:
                    st.error(f"❌ Missing features: {', '.join(missing_features)}")
                else:
                    st.success("✅ All required features present")
                    
                    if st.button("🔍 Predict All", type="primary"):
                        with st.spinner("Processing predictions..."):
                            results = []
                            for idx, row in df.iterrows():
                                features = row[FEATURES].to_dict()
                                result = make_prediction(features)
                                if "error" not in result:
                                    result['row_index'] = idx
                                    results.append(result)
                            
                            if results:
                                # Create results DataFrame
                                results_df = pd.DataFrame(results)
                                st.subheader("📊 Batch Prediction Results")
                                st.dataframe(results_df)
                                
                                # Download results
                                csv = results_df.to_csv(index=False)
                                st.download_button(
                                    label="📥 Download Results",
                                    data=csv,
                                    file_name="predictions.csv",
                                    mime="text/csv"
                                )
                                
                                # Summary statistics
                                st.subheader("Summary Statistics")
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Total Predictions", len(results))
                                with col2:
                                    malignant_count = sum(1 for r in results if r['prediction'] == 1)
                                    st.metric("Malignant Cases", malignant_count)
                                with col3:
                                    benign_count = sum(1 for r in results if r['prediction'] == 0)
                                    st.metric("Benign Cases", benign_count)
            
            except Exception as e:
                st.error(f"❌ Error processing file: {str(e)}")
    
    with tab3:
        st.header("📈 Prediction History")
        st.markdown("View and compare your prediction history")
        
        if 'prediction_history' in st.session_state and len(st.session_state.prediction_history) > 0:
            history = st.session_state.prediction_history
            
            # Summary statistics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Predictions", len(history))
            with col2:
                malignant_count = sum(1 for h in history if h.get('prediction') == 'Malignant')
                st.metric("Malignant Cases", malignant_count)
            with col3:
                benign_count = sum(1 for h in history if h.get('prediction') == 'Benign')
                st.metric("Benign Cases", benign_count)
            with col4:
                avg_confidence = np.mean([h.get('confidence', 0) for h in history])
                st.metric("Avg Confidence", f"{avg_confidence:.2%}")
            
            st.divider()
            
            # Full history table
            history_df = pd.DataFrame([
                {
                    'Timestamp': h['timestamp'],
                    'Prediction': h['prediction'],
                    'Malignant Prob': f"{h['probability_malignant']:.2%}",
                    'Benign Prob': f"{h['probability_benign']:.2%}",
                    'Confidence': f"{h['confidence']:.2%}",
                    'Risk Score': f"{h.get('risk_score', 0):.1f}",
                    'Risk Level': h.get('risk_level', 'N/A')
                }
                for h in history
            ])
            
            st.dataframe(history_df, use_container_width=True, hide_index=True)
            
            # Trend visualization
            if len(history) > 1:
                st.subheader("📊 Trends Over Time")
                
                timestamps = [h['timestamp'] for h in history]
                confidences = [h['confidence'] for h in history]
                risk_scores = [h.get('risk_score', 0) for h in history]
                
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=confidences,
                        name="Confidence",
                        line=dict(color='#1f77b4', width=3),
                        mode='lines+markers'
                    ),
                    secondary_y=False,
                )
                
                fig.add_trace(
                    go.Scatter(
                        x=timestamps,
                        y=risk_scores,
                        name="Risk Score",
                        line=dict(color='#dc3545', width=3),
                        mode='lines+markers'
                    ),
                    secondary_y=True,
                )
                
                fig.update_xaxes(title_text="Time")
                fig.update_yaxes(title_text="Confidence", secondary_y=False)
                fig.update_yaxes(title_text="Risk Score", secondary_y=True)
                fig.update_layout(
                    title="Confidence and Risk Score Trends",
                    height=400,
                    template='plotly_white'
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            # Comparison with previous prediction
            if len(history) > 1:
                st.subheader("🔄 Compare with Previous")
                current = history[-1]
                previous = history[-2]
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Previous Prediction**")
                    st.write(f"Time: {previous['timestamp']}")
                    st.write(f"Prediction: {previous['prediction']}")
                    st.write(f"Confidence: {previous['confidence']:.2%}")
                    st.write(f"Risk Score: {previous.get('risk_score', 0):.1f}")
                
                with col2:
                    st.markdown("**Current Prediction**")
                    st.write(f"Time: {current['timestamp']}")
                    st.write(f"Prediction: {current['prediction']}")
                    st.write(f"Confidence: {current['confidence']:.2%}")
                    st.write(f"Risk Score: {current.get('risk_score', 0):.1f}")
                
                # Calculate differences
                conf_diff = current['confidence'] - previous['confidence']
                risk_diff = current.get('risk_score', 0) - previous.get('risk_score', 0)
                
                st.info(f"📊 **Changes:** Confidence {conf_diff:+.2%}, Risk Score {risk_diff:+.1f}")
            
            # Clear history button
            if st.button("🗑️ Clear History", type="secondary"):
                st.session_state.prediction_history = []
                st.rerun()
        else:
            st.info("No prediction history yet. Make some predictions to see them here!")
    
    with tab4:
        st.header("📄 Export Reports")
        st.markdown("Generate and download detailed reports")
        
        if 'last_prediction' in st.session_state:
            last_pred = st.session_state.last_prediction
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("📋 Report Options")
                patient_id = st.text_input("Patient ID (Optional)", placeholder="Enter patient ID")
                include_features = st.checkbox("Include Feature Values", value=True)
                include_risk = st.checkbox("Include Risk Analysis", value=True)
                include_charts = st.checkbox("Include Charts", value=False)
            
            with col2:
                st.subheader("📊 Report Preview")
                st.write(f"**Prediction:** {last_pred['result']['prediction_label']}")
                st.write(f"**Confidence:** {last_pred['result']['confidence']:.2%}")
                st.write(f"**Risk Score:** {last_pred['risk_score']['score']:.1f} ({last_pred['risk_score']['level']})")
                st.write(f"**Date:** {last_pred['timestamp']}")
            
            # Generate PDF
            if st.button("📥 Generate PDF Report", type="primary", use_container_width=True):
                try:
                    pdf_bytes = generate_pdf_report(
                        last_pred['result'],
                        last_pred['features'],
                        last_pred['risk_score'],
                        patient_id if patient_id else None
                    )
                    
                    if pdf_bytes:
                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_bytes,
                            file_name=f"breast_cancer_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                            mime="application/pdf",
                            use_container_width=True
                        )
                        st.success("✅ PDF report generated successfully!")
                    else:
                        st.error("❌ Error generating PDF")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
            
            # Export to CSV
            st.divider()
            st.subheader("📊 Export Data")
            
            if st.button("📥 Export to CSV", use_container_width=True):
                export_data = {
                    'timestamp': [last_pred['timestamp']],
                    'prediction': [last_pred['result']['prediction_label']],
                    'probability_malignant': [last_pred['result']['probability_malignant']],
                    'probability_benign': [last_pred['result']['probability_benign']],
                    'confidence': [last_pred['result']['confidence']],
                    'risk_score': [last_pred['risk_score']['score']],
                    'risk_level': [last_pred['risk_score']['level']]
                }
                
                if include_features:
                    export_data.update({k: [v] for k, v in last_pred['features'].items()})
                
                export_df = pd.DataFrame(export_data)
                csv = export_df.to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"prediction_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        else:
            st.info("Make a prediction first to generate reports!")
    
    with tab5:
        st.header("About This System")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### 🏥 Breast Cancer Detection System
            
            This web application provides an interactive interface for predicting breast cancer 
            diagnosis based on cell nucleus measurements.
            
            #### 📊 Model Information
            - **Model Type:** Multi-Layer Perceptron (MLP)
            - **Architecture:** 3 hidden layers (500, 500, 500 neurons)
            - **Input Features:** 30 features (mean, standard error, worst values)
            - **Performance:** ~97% accuracy, ~98% ROC-AUC
            
            #### 🔬 Features
            The model uses 30 features derived from 10 base measurements:
            - Radius
            - Texture
            - Perimeter
            - Area
            - Smoothness
            - Compactness
            - Concavity
            - Concave Points
            - Symmetry
            - Fractal Dimension
            
            Each measurement has 3 statistical aggregations:
            - **Mean:** Average value
            - **Standard Error (SE):** Measurement variability
            - **Worst:** Largest (most extreme) value
            """)
        
        with col2:
            st.markdown("""
            #### 🎯 How to Use
            
            1. **Load Examples:** Use sidebar buttons to load real examples from both classes
            2. **Manual Input:** Enter patient measurements in the form
            3. **CSV Upload:** Upload batch files for multiple predictions
            4. **View Results:** See probabilities, visualizations, and history
            
            #### 📈 Features Added
            
            - ✅ Real examples from both classes (Benign & Malignant)
            - ✅ Probability visualization charts
            - ✅ Feature analysis graphs
            - ✅ Prediction history tracking
            - ✅ Batch processing support
            - ✅ Interactive visualizations
            
            #### ⚠️ Disclaimer
            This system is for educational and research purposes only. 
            It should not be used as a substitute for professional medical diagnosis.
            
            #### 🛠️ Technical Stack
            - **Backend API:** FastAPI
            - **Web UI:** Streamlit
            - **ML Framework:** scikit-learn
            - **Model:** MLPClassifier
            - **Visualization:** Matplotlib, Seaborn
            """)
        
        # Model metrics display
        st.divider()
        st.subheader("📊 Model Performance Metrics")
        
        metrics_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r') as f:
                metrics = json.load(f)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Accuracy", f"{metrics.get('accuracy', 0):.2%}")
            with col2:
                st.metric("ROC-AUC", f"{metrics.get('roc_auc', 0):.2%}")
            with col3:
                st.metric("Precision", f"{metrics.get('precision', 0):.2%}")
            with col4:
                st.metric("Recall", f"{metrics.get('recall', 0):.2%}")

if __name__ == "__main__":
    main()

