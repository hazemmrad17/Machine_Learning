"""
Utility functions for the Web UI
"""
import joblib
import numpy as np
import pandas as pd
from typing import Dict, List, Optional
import os
from datetime import datetime

def load_model_for_shap():
    """Load model and scaler for SHAP analysis."""
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'mlp_model.pkl')
        scaler_path = os.path.join(os.path.dirname(__file__), '..', 'models', 'scaler.pkl')
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            model = joblib.load(model_path)
            scaler = joblib.load(scaler_path)
            return model, scaler
        return None, None
    except Exception as e:
        print(f"Error loading model: {e}")
        return None, None

def calculate_risk_score(features: Dict, prediction: Dict) -> Dict:
    """
    Calculate personalized risk score based on features and prediction.
    
    Args:
        features: Dictionary of feature values
        prediction: Prediction results dictionary
        
    Returns:
        Dictionary with risk score and breakdown
    """
    # Risk factors (higher values = higher risk)
    risk_factors = {
        'radius_mean': (10, 20, 0.15),
        'perimeter_mean': (80, 130, 0.15),
        'area_mean': (400, 1200, 0.15),
        'concavity_mean': (0.05, 0.3, 0.2),
        'concave_points_mean': (0.02, 0.15, 0.2),
        'compactness_mean': (0.05, 0.3, 0.15),
    }
    
    risk_score = 0
    risk_breakdown = {}
    
    for feature, (low, high, weight) in risk_factors.items():
        if feature in features:
            value = features[feature]
            # Normalize to 0-1 scale
            if value < low:
                normalized = 0
            elif value > high:
                normalized = 1
            else:
                normalized = (value - low) / (high - low)
            
            feature_risk = normalized * weight * 100
            risk_score += feature_risk
            risk_breakdown[feature] = {
                'value': value,
                'normalized': normalized,
                'contribution': feature_risk
            }
    
    # Add prediction confidence to risk score
    confidence_risk = prediction.get('probability_malignant', 0) * 100 * 0.3
    risk_score += confidence_risk
    
    # Normalize to 0-100 scale
    risk_score = min(100, max(0, risk_score))
    
    # Risk level interpretation
    if risk_score < 30:
        risk_level = "Low"
        risk_color = "#28a745"
    elif risk_score < 60:
        risk_level = "Moderate"
        risk_color = "#ffc107"
    elif risk_score < 80:
        risk_level = "High"
        risk_color = "#fd7e14"
    else:
        risk_level = "Very High"
        risk_color = "#dc3545"
    
    return {
        'score': round(risk_score, 2),
        'level': risk_level,
        'color': risk_color,
        'breakdown': risk_breakdown,
        'confidence_contribution': confidence_risk
    }

def generate_pdf_report(prediction: Dict, features: Dict, risk_score: Dict, 
                        patient_id: Optional[str] = None) -> bytes:
    """
    Generate PDF report of prediction results.
    
    Args:
        prediction: Prediction results
        features: Input features
        risk_score: Risk score dictionary
        patient_id: Optional patient ID
        
    Returns:
        PDF bytes
    """
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.lib import colors
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
        from reportlab.lib.units import inch
        from io import BytesIO
        
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        story = []
        styles = getSampleStyleSheet()
        
        # Title
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1f77b4'),
            spaceAfter=30,
            alignment=1  # Center
        )
        story.append(Paragraph("Breast Cancer Detection Report", title_style))
        story.append(Spacer(1, 0.2*inch))
        
        # Patient info
        if patient_id:
            story.append(Paragraph(f"<b>Patient ID:</b> {patient_id}", styles['Normal']))
            story.append(Spacer(1, 0.1*inch))
        
        story.append(Paragraph(f"<b>Date:</b> {prediction.get('timestamp', 'N/A')}", styles['Normal']))
        story.append(Spacer(1, 0.3*inch))
        
        # Prediction result
        is_malignant = prediction['prediction'] == 1
        result_text = f"<b>Prediction:</b> {prediction['prediction_label']}"
        result_color = colors.HexColor('#dc3545') if is_malignant else colors.HexColor('#28a745')
        
        result_style = ParagraphStyle(
            'Result',
            parent=styles['Heading2'],
            fontSize=18,
            textColor=result_color,
            spaceAfter=20
        )
        story.append(Paragraph(result_text, result_style))
        
        # Metrics table
        data = [
            ['Metric', 'Value'],
            ['Probability (Malignant)', f"{prediction['probability_malignant']:.2%}"],
            ['Probability (Benign)', f"{prediction['probability_benign']:.2%}"],
            ['Confidence', f"{prediction['confidence']:.2%}"],
            ['Risk Score', f"{risk_score['score']:.1f} ({risk_score['level']})"],
        ]
        
        table = Table(data, colWidths=[3*inch, 2*inch])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        story.append(table)
        story.append(Spacer(1, 0.3*inch))
        
        # Disclaimer
        disclaimer_style = ParagraphStyle(
            'Disclaimer',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey,
            fontStyle='Italic'
        )
        story.append(Paragraph(
            "<b>Disclaimer:</b> This report is for educational and research purposes only. "
            "It should not be used as a substitute for professional medical diagnosis. "
            "Always consult with qualified healthcare professionals.",
            disclaimer_style
        ))
        
        doc.build(story)
        buffer.seek(0)
        return buffer.getvalue()
    except Exception as e:
        print(f"Error generating PDF: {e}")
        return None

