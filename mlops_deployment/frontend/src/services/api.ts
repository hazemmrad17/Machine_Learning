const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface FeatureInput {
  radius_mean: number;
  texture_mean: number;
  perimeter_mean: number;
  area_mean: number;
  smoothness_mean: number;
  compactness_mean: number;
  concavity_mean: number;
  concave_points_mean: number;
  symmetry_mean: number;
  fractal_dimension_mean: number;
  radius_se: number;
  texture_se: number;
  perimeter_se: number;
  area_se: number;
  smoothness_se: number;
  compactness_se: number;
  concavity_se: number;
  concave_points_se: number;
  symmetry_se: number;
  fractal_dimension_se: number;
  radius_worst: number;
  texture_worst: number;
  perimeter_worst: number;
  area_worst: number;
  smoothness_worst: number;
  compactness_worst: number;
  concavity_worst: number;
  concave_points_worst: number;
  symmetry_worst: number;
  fractal_dimension_worst: number;
}

export interface PredictionResponse {
  prediction: number;
  prediction_label: string;
  probability_malignant: number;
  probability_benign: number;
  confidence: number;
  model_type?: string;
  model_metrics?: {
    accuracy: number;
    roc_auc: number;
    recall: number;
    precision: number;
    f1_score: number;
  };
}

export interface ModelInfo {
  name: string;
  description: string;
  metrics: {
    accuracy: number;
    roc_auc: number;
    recall: number;
    precision: number;
    f1_score: number;
  };
}

export interface ModelComparison {
  comparisons: Record<string, PredictionResponse>;
  available_models: string[];
}

export type ModelType = 'mlp' | 'svm' | 'l1_nn' | 'l2_nn' | 'logistic_regression' | 'softmax_regression';

export const api = {
  async healthCheck(): Promise<{ status: string; models_loaded: boolean; available_models: string[] }> {
    const response = await fetch(`${API_URL}/health`);
    if (!response.ok) {
      throw new Error('Health check failed');
    }
    return response.json();
  },

  async listModels(): Promise<{ available_models: string[]; models: Record<string, ModelInfo> }> {
    const response = await fetch(`${API_URL}/models`);
    if (!response.ok) {
      throw new Error('Failed to fetch models');
    }
    return response.json();
  },

  async predict(features: FeatureInput, modelType: ModelType = 'mlp'): Promise<PredictionResponse> {
    const response = await fetch(`${API_URL}/predict?model_type=${modelType}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Prediction failed' }));
      throw new Error(error.detail || 'Prediction failed');
    }

    const result = await response.json();
    return { ...result, model_type: modelType };
  },

  async compareModels(features: FeatureInput): Promise<ModelComparison> {
    const response = await fetch(`${API_URL}/predict/compare`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Comparison failed' }));
      throw new Error(error.detail || 'Comparison failed');
    }

    return response.json();
  },

  async predictBatch(features: FeatureInput[], modelType: ModelType = 'mlp'): Promise<PredictionResponse[]> {
    const response = await fetch(`${API_URL}/predict/batch?model_type=${modelType}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(features),
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: 'Batch prediction failed' }));
      throw new Error(error.detail || 'Batch prediction failed');
    }

    return response.json();
  },
};
