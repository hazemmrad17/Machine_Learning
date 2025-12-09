import React, { useState, useRef, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { api, FeatureInput, PredictionResponse, ModelType } from '@/services/api';
import { Upload, FileText, Loader2, AlertCircle, CheckCircle2 } from 'lucide-react';
import { Select } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import Papa from 'papaparse';

interface CSVUploadProps {
  onBatchPredictions: (results: PredictionResponse[]) => void;
}

export function CSVUpload({ onBatchPredictions }: CSVUploadProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [selectedModel, setSelectedModel] = useState<ModelType>('mlp');
  const [availableModels, setAvailableModels] = useState<string[]>(['mlp']);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    api.listModels().then((data: { available_models: string[]; models: Record<string, any> }) => {
      setAvailableModels(data.available_models);
      if (data.available_models.length > 0 && !data.available_models.includes(selectedModel)) {
        setSelectedModel(data.available_models[0] as ModelType);
      }
    }).catch(() => {
      console.warn('Could not load model list');
    });
  }, []);

  const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    setLoading(true);
    setError(null);
    setSuccess(null);

    try {
        // Parse CSV file
      Papa.parse<Record<string, string>>(file, {
        header: true,
        complete: async (results: Papa.ParseResult<Record<string, string>>) => {
          try {
            // Expected feature names (30 features)
            const expectedFeatures = [
              'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean',
              'smoothness_mean', 'compactness_mean', 'concavity_mean',
              'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
              'radius_se', 'texture_se', 'perimeter_se', 'area_se',
              'smoothness_se', 'compactness_se', 'concavity_se',
              'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
              'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst',
              'smoothness_worst', 'compactness_worst', 'concavity_worst',
              'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
            ];

            // Validate and convert to FeatureInput format
            const features: FeatureInput[] = results.data
              .filter((row: Record<string, string>) => {
                // Check if row has at least some required fields
                return expectedFeatures.some(feat => feat in row && row[feat] !== '');
              })
              .map((row: Record<string, string>) => {
                const feature: Partial<FeatureInput> = {};
                // Only include expected features and convert to numbers
                expectedFeatures.forEach((key) => {
                  const value = parseFloat(row[key] || row[key.toLowerCase()] || '0');
                  (feature as any)[key] = isNaN(value) ? 0 : value;
                });
                return feature as FeatureInput;
              });

            if (features.length === 0) {
              throw new Error('No valid rows found in CSV file');
            }

            // Make batch prediction
            const predictions = await api.predictBatch(features, selectedModel);
            onBatchPredictions(predictions);
            setSuccess(`Successfully processed ${predictions.length} predictions using ${selectedModel.toUpperCase()}`);
          } catch (err) {
            setError(err instanceof Error ? err.message : 'Failed to process CSV file');
          } finally {
            setLoading(false);
          }
        },
        error: (error: Error & { code?: string }) => {
          setError(`CSV parsing error: ${error.message}`);
          setLoading(false);
        },
      });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to read file');
      setLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-2xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-2xl font-bold flex items-center gap-2">
          <FileText className="h-6 w-6" />
          Batch Prediction from CSV
        </CardTitle>
        <CardDescription>
          Upload a CSV file with 30 features per row for batch predictions
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="space-y-2">
          <Label htmlFor="csv-model-select">Select Algorithm</Label>
          <Select
            id="csv-model-select"
            value={selectedModel}
            onChange={(e) => setSelectedModel(e.target.value as ModelType)}
          >
            {availableModels.map((model) => (
              <option key={model} value={model}>
                {model.toUpperCase()}
              </option>
            ))}
          </Select>
        </div>

        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-gray-400 transition-colors">
          <input
            ref={fileInputRef}
            type="file"
            accept=".csv"
            onChange={handleFileUpload}
            className="hidden"
            disabled={loading}
          />
          <Upload className="h-12 w-12 mx-auto text-gray-400 mb-4" />
          <p className="text-sm text-gray-600 mb-2">
            Click to upload or drag and drop
          </p>
          <p className="text-xs text-gray-500 mb-4">
            CSV file with 30 feature columns
          </p>
          <Button
            onClick={() => fileInputRef.current?.click()}
            disabled={loading}
            variant="outline"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Processing...
              </>
            ) : (
              <>
                <Upload className="mr-2 h-4 w-4" />
                Select CSV File
              </>
            )}
          </Button>
        </div>

        {error && (
          <div className="flex items-center gap-2 p-3 bg-destructive/10 text-destructive rounded-md">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {success && (
          <div className="flex items-center gap-2 p-3 bg-green-50 text-green-700 rounded-md">
            <CheckCircle2 className="h-4 w-4" />
            <span className="text-sm">{success}</span>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

