import React, { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Select } from '@/components/ui/select';
import { api, FeatureInput, PredictionResponse, ModelType, ModelInfo } from '@/services/api';
import { Loader2, AlertCircle, Info, GitCompare } from 'lucide-react';
import { ModelComparison } from './ModelComparison';
import { FeatureImportance } from './FeatureImportance';
import { predictionHistory } from '@/utils/predictionHistory';

interface PredictionFormProps {
  onPrediction: (result: PredictionResponse, features?: Record<string, number>) => void;
}

const FEATURE_GROUPS = [
  {
    title: 'Mean Features',
    features: [
      'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
      'smoothness_mean', 'compactness_mean', 'concavity_mean',
      'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean'
    ]
  },
  {
    title: 'Standard Error Features',
    features: [
      'radius_se', 'texture_se', 'perimeter_se', 'area_se',
      'smoothness_se', 'compactness_se', 'concavity_se',
      'concave_points_se', 'symmetry_se', 'fractal_dimension_se'
    ]
  },
  {
    title: 'Worst Features',
    features: [
      'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
      'smoothness_worst', 'compactness_worst', 'concavity_worst',
      'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
    ]
  }
];

const BENIGN_EXAMPLE: FeatureInput = {
  radius_mean: 13.54,
  texture_mean: 14.36,
  perimeter_mean: 87.46,
  area_mean: 566.3,
  smoothness_mean: 0.09779,
  compactness_mean: 0.08129,
  concavity_mean: 0.06664,
  concave_points_mean: 0.04781,
  symmetry_mean: 0.1885,
  fractal_dimension_mean: 0.05766,
  radius_se: 0.2699,
  texture_se: 0.7886,
  perimeter_se: 2.058,
  area_se: 23.56,
  smoothness_se: 0.008462,
  compactness_se: 0.0146,
  concavity_se: 0.02387,
  concave_points_se: 0.01315,
  symmetry_se: 0.0198,
  fractal_dimension_se: 0.0023,
  radius_worst: 15.11,
  texture_worst: 19.26,
  perimeter_worst: 99.7,
  area_worst: 711.2,
  smoothness_worst: 0.144,
  compactness_worst: 0.1773,
  concavity_worst: 0.239,
  concave_points_worst: 0.1288,
  symmetry_worst: 0.2977,
  fractal_dimension_worst: 0.07259
};

const MALIGNANT_EXAMPLE: FeatureInput = {
  radius_mean: 17.99,
  texture_mean: 10.38,
  perimeter_mean: 122.8,
  area_mean: 1001.0,
  smoothness_mean: 0.1184,
  compactness_mean: 0.2776,
  concavity_mean: 0.3001,
  concave_points_mean: 0.1471,
  symmetry_mean: 0.2419,
  fractal_dimension_mean: 0.07871,
  radius_se: 1.095,
  texture_se: 0.9053,
  perimeter_se: 8.589,
  area_se: 153.4,
  smoothness_se: 0.006399,
  compactness_se: 0.04904,
  concavity_se: 0.05373,
  concave_points_se: 0.01587,
  symmetry_se: 0.03003,
  fractal_dimension_se: 0.006193,
  radius_worst: 25.38,
  texture_worst: 17.33,
  perimeter_worst: 184.6,
  area_worst: 2019.0,
  smoothness_worst: 0.1622,
  compactness_worst: 0.6656,
  concavity_worst: 0.7119,
  concave_points_worst: 0.2654,
  symmetry_worst: 0.4601,
  fractal_dimension_worst: 0.1189
};


export function PredictionForm({ onPrediction }: PredictionFormProps) {
  const [features, setFeatures] = useState<FeatureInput>({} as FeatureInput);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<ModelType>('mlp');
  const [availableModels, setAvailableModels] = useState<string[]>(['mlp']);
  const [modelInfo, setModelInfo] = useState<Record<string, ModelInfo>>({});
  const [showComparison, setShowComparison] = useState(false);

  useEffect(() => {
    // Load available models on mount
    api.listModels().then((data: { available_models: string[]; models: Record<string, ModelInfo> }) => {
      setAvailableModels(data.available_models);
      setModelInfo(data.models);
      if (data.available_models.length > 0 && !data.available_models.includes(selectedModel)) {
        setSelectedModel(data.available_models[0] as ModelType);
      }
    }).catch(() => {
      // If API fails, use default
      console.warn('Could not load model list');
    });
  }, []);

  const handleInputChange = (key: keyof FeatureInput, value: string) => {
    setFeatures(prev => ({
      ...prev,
      [key]: parseFloat(value) || 0
    }));
    setError(null);
  };

  const loadExample = (example: FeatureInput) => {
    setFeatures(example);
    setError(null);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const result = await api.predict(features, selectedModel);
      // Save to history
      predictionHistory.save(result, features as unknown as Record<string, number>);
      onPrediction(result, features as unknown as Record<string, number>);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to make prediction');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-4xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-2xl font-bold">Breast Cancer Detection</CardTitle>
        <CardDescription>
          Enter the 30 features from the Wisconsin Diagnostic Breast Cancer dataset
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-6">
          {/* Model Selection */}
          <div className="space-y-2">
            <Label htmlFor="model-select">Select Algorithm</Label>
            <div className="flex gap-2">
              <Select
                id="model-select"
                value={selectedModel}
                onChange={(e) => setSelectedModel(e.target.value as ModelType)}
                className="flex-1"
              >
                {availableModels.map((model) => (
                  <option key={model} value={model}>
                    {model.toUpperCase()} {modelInfo[model]?.metrics && 
                      `(Acc: ${(modelInfo[model].metrics.accuracy * 100).toFixed(1)}%)`}
                  </option>
                ))}
              </Select>
            </div>
            {modelInfo[selectedModel] && (
              <div className="flex items-start gap-2 p-3 bg-blue-50 border border-blue-200 rounded-md text-sm">
                <Info className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                <div>
                  <div className="font-semibold text-blue-900 mb-1">
                    {modelInfo[selectedModel].description}
                  </div>
                  <div className="text-blue-800 space-y-1">
                    <div>Accuracy: {(modelInfo[selectedModel].metrics.accuracy * 100).toFixed(2)}%</div>
                    <div>ROC-AUC: {modelInfo[selectedModel].metrics.roc_auc.toFixed(4)}</div>
                    <div className="text-xs text-blue-600 mt-1">
                      Note: Confidence score is the maximum probability, not a true confidence measure.
                      High confidence (e.g., 95%+) means the model is very certain, but doesn't guarantee accuracy.
                    </div>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="flex gap-2 mb-4">
            <Button
              type="button"
              variant="outline"
              onClick={() => loadExample(BENIGN_EXAMPLE)}
              className="flex-1"
            >
              Load Benign Example
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => loadExample(MALIGNANT_EXAMPLE)}
              className="flex-1"
            >
              Load Malignant Example
            </Button>
          </div>

          {error && (
            <div className="flex items-center gap-2 p-3 bg-destructive/10 text-destructive rounded-md">
              <AlertCircle className="h-4 w-4" />
              <span className="text-sm">{error}</span>
            </div>
          )}

          <div className="space-y-6 max-h-[60vh] overflow-y-auto pr-2">
            {FEATURE_GROUPS.map((group) => (
              <div key={group.title} className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-700">{group.title}</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
                  {group.features.map((feature) => (
                    <div key={feature} className="space-y-2">
                      <Label htmlFor={feature} className="text-xs">
                        {feature.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}
                      </Label>
                      <Input
                        id={feature}
                        type="number"
                        step="any"
                        value={features[feature as keyof FeatureInput] || ''}
                        onChange={(e) => handleInputChange(feature as keyof FeatureInput, e.target.value)}
                        required
                        className="h-9"
                      />
                    </div>
                  ))}
                </div>
              </div>
            ))}
          </div>

          <div className="flex gap-2">
            <Button
              type="submit"
              disabled={loading}
              className="flex-1"
              size="lg"
            >
              {loading ? (
                <>
                  <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                  Predicting...
                </>
              ) : (
                'Make Prediction'
              )}
            </Button>
            <Button
              type="button"
              variant="outline"
              onClick={() => setShowComparison(true)}
              disabled={loading}
              size="lg"
            >
              <GitCompare className="mr-2 h-4 w-4" />
              Compare All
            </Button>
          </div>
        </form>

        {showComparison && (
          <div className="mt-6">
            <ModelComparison
              features={features}
              onClose={() => setShowComparison(false)}
            />
          </div>
        )}

        {/* Feature Importance */}
        {Object.keys(features).length > 0 && (
          <div className="mt-6">
            <FeatureImportance features={features as unknown as Record<string, number>} />
          </div>
        )}
      </CardContent>
    </Card>
  );
}

