import jsPDF from 'jspdf';
import * as XLSX from 'xlsx';
import { PredictionResponse } from '@/services/api';

const formatDate = (date: Date): string => {
  return date.toISOString().replace('T', '_').split('.')[0];
};

export const exportUtils = {
  exportToPDF(prediction: PredictionResponse, features?: Record<string, number>) {
    const doc = new jsPDF();
    
    // Title
    doc.setFontSize(18);
    doc.text('Breast Cancer Detection Report', 20, 20);
    
    // Date
    doc.setFontSize(10);
    doc.text(`Generated: ${new Date().toLocaleString()}`, 20, 30);
    
    let yPos = 40;
    
    // Prediction Result
    doc.setFontSize(14);
    doc.text('Prediction Result', 20, yPos);
    yPos += 10;
    
    doc.setFontSize(12);
    doc.text(`Model: ${prediction.model_type?.toUpperCase() || 'MLP'}`, 20, yPos);
    yPos += 7;
    doc.text(`Prediction: ${prediction.prediction_label}`, 20, yPos);
    yPos += 7;
    doc.text(`Confidence: ${(prediction.confidence * 100).toFixed(2)}%`, 20, yPos);
    yPos += 10;
    
    // Probabilities
    doc.setFontSize(14);
    doc.text('Probabilities', 20, yPos);
    yPos += 10;
    
    doc.setFontSize(12);
    doc.text(`Benign: ${(prediction.probability_benign * 100).toFixed(2)}%`, 20, yPos);
    yPos += 7;
    doc.text(`Malignant: ${(prediction.probability_malignant * 100).toFixed(2)}%`, 20, yPos);
    yPos += 10;
    
    // Model Metrics
    if (prediction.model_metrics) {
      doc.setFontSize(14);
      doc.text('Model Performance', 20, yPos);
      yPos += 10;
      
      doc.setFontSize(12);
      doc.text(`Accuracy: ${(prediction.model_metrics.accuracy * 100).toFixed(2)}%`, 20, yPos);
      yPos += 7;
      doc.text(`ROC-AUC: ${prediction.model_metrics.roc_auc.toFixed(4)}`, 20, yPos);
      yPos += 7;
      doc.text(`Recall: ${(prediction.model_metrics.recall * 100).toFixed(2)}%`, 20, yPos);
      yPos += 7;
      doc.text(`Precision: ${(prediction.model_metrics.precision * 100).toFixed(2)}%`, 20, yPos);
      yPos += 7;
      doc.text(`F1-Score: ${prediction.model_metrics.f1_score.toFixed(4)}`, 20, yPos);
      yPos += 10;
    }
    
    // Features (if provided)
    if (features) {
      doc.setFontSize(14);
      doc.text('Input Features', 20, yPos);
      yPos += 10;
      
      doc.setFontSize(10);
      const featureEntries = Object.entries(features).slice(0, 15); // First 15 features
      featureEntries.forEach(([key, value]) => {
        if (yPos > 270) {
          doc.addPage();
          yPos = 20;
        }
        doc.text(`${key}: ${value.toFixed(4)}`, 20, yPos);
        yPos += 6;
      });
    }
    
    // Disclaimer
    yPos = 270;
    doc.setFontSize(8);
    doc.text('This is a machine learning prediction tool and should not be used', 20, yPos);
    doc.text('as a substitute for professional medical diagnosis.', 20, yPos + 5);
    
    doc.save(`prediction_${formatDate(new Date())}.pdf`);
  },

  exportBatchToExcel(results: PredictionResponse[], filename?: string) {
    const data = results.map((result, index) => ({
      'Sample': index + 1,
      'Model': result.model_type?.toUpperCase() || 'MLP',
      'Prediction': result.prediction,
      'Label': result.prediction_label,
      'Benign Probability (%)': (result.probability_benign * 100).toFixed(2),
      'Malignant Probability (%)': (result.probability_malignant * 100).toFixed(2),
      'Confidence (%)': (result.confidence * 100).toFixed(2),
      'Model Accuracy': result.model_metrics ? (result.model_metrics.accuracy * 100).toFixed(2) + '%' : 'N/A',
      'ROC-AUC': result.model_metrics ? result.model_metrics.roc_auc.toFixed(4) : 'N/A'
    }));

    const ws = XLSX.utils.json_to_sheet(data);
    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, 'Predictions');
    
    const defaultFilename = filename || `batch_predictions_${new Date().toISOString().split('T')[0]}.xlsx`;
    XLSX.writeFile(wb, defaultFilename);
  }
};

