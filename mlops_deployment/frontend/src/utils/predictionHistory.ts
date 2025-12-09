import { PredictionResponse } from '@/services/api';

export interface PredictionHistoryItem extends PredictionResponse {
  id: string;
  timestamp: number;
  features?: Record<string, number>;
}

const STORAGE_KEY = 'breast_cancer_predictions';

export const predictionHistory = {
  save(prediction: PredictionResponse, features?: Record<string, number>): void {
    const history = this.getAll();
    const item: PredictionHistoryItem = {
      ...prediction,
      id: Date.now().toString() + Math.random().toString(36).substr(2, 9),
      timestamp: Date.now(),
      features
    };
    history.unshift(item);
    // Keep only last 100 predictions
    const limited = history.slice(0, 100);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(limited));
  },

  getAll(): PredictionHistoryItem[] {
    try {
      const data = localStorage.getItem(STORAGE_KEY);
      return data ? JSON.parse(data) : [];
    } catch {
      return [];
    }
  },

  getByModel(modelType: string): PredictionHistoryItem[] {
    return this.getAll().filter(item => item.model_type === modelType);
  },

  getByDateRange(startDate: Date, endDate: Date): PredictionHistoryItem[] {
    return this.getAll().filter(item => {
      const itemDate = new Date(item.timestamp);
      return itemDate >= startDate && itemDate <= endDate;
    });
  },

  getByPrediction(prediction: number): PredictionHistoryItem[] {
    return this.getAll().filter(item => item.prediction === prediction);
  },

  delete(id: string): void {
    const history = this.getAll().filter(item => item.id !== id);
    localStorage.setItem(STORAGE_KEY, JSON.stringify(history));
  },

  clear(): void {
    localStorage.removeItem(STORAGE_KEY);
  },

  getStats() {
    const all = this.getAll();
    return {
      total: all.length,
      benign: all.filter(p => p.prediction === 0).length,
      malignant: all.filter(p => p.prediction === 1).length,
      byModel: all.reduce((acc, p) => {
        const model = p.model_type || 'unknown';
        acc[model] = (acc[model] || 0) + 1;
        return acc;
      }, {} as Record<string, number>)
    };
  }
};

