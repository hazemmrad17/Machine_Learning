import { useState } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { api, FeatureInput, ModelComparison as ModelComparisonType } from '@/services/api';
import { Loader2, AlertCircle, TrendingUp, CheckCircle2, XCircle } from 'lucide-react';

interface ModelComparisonProps {
  features: FeatureInput;
  onClose: () => void;
}

export function ModelComparison({ features, onClose }: ModelComparisonProps) {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [comparison, setComparison] = useState<ModelComparisonType | null>(null);

  const handleCompare = async () => {
    setLoading(true);
    setError(null);

    try {
      const result = await api.compareModels(features);
      // Validate the response structure
      if (!result || !result.comparisons || !result.available_models) {
        throw new Error('Invalid response format from API');
      }
      setComparison(result);
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : 'Failed to compare models';
      setError(errorMessage);
      console.error('Model comparison error:', err);
    } finally {
      setLoading(false);
    }
  };

  const getModelName = (modelType: string): string => {
    const names: Record<string, string> = {
      mlp: 'MLP (Neural Network)',
      svm: 'SVM (Support Vector Machine)',
      l1_nn: 'L1-NN (KNN Manhattan)',
      l2_nn: 'L2-NN (KNN Euclidean)',
      logistic_regression: 'Logistic Regression',
      softmax_regression: 'Softmax Regression'
    };
    return names[modelType] || modelType.toUpperCase();
  };

  return (
    <Card className="w-full max-w-6xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-2xl font-bold flex items-center gap-2">
          <TrendingUp className="h-6 w-6" />
          Model Comparison
        </CardTitle>
        <CardDescription>
          Compare predictions from all available algorithms
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="flex gap-2">
          <Button
            onClick={handleCompare}
            disabled={loading}
            className="flex-1"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Comparing...
              </>
            ) : (
              'Compare All Models'
            )}
          </Button>
          <Button
            onClick={onClose}
            variant="outline"
          >
            Close
          </Button>
        </div>

        {error && (
          <div className="flex items-center gap-2 p-3 bg-destructive/10 text-destructive rounded-md">
            <AlertCircle className="h-4 w-4" />
            <span className="text-sm">{error}</span>
          </div>
        )}

        {comparison && comparison.available_models && comparison.available_models.length > 0 && (
          <div className="space-y-4">
            <div className="grid md:grid-cols-2 gap-4">
              {comparison.available_models.map((modelType) => {
                const result = comparison.comparisons?.[modelType];
                if (!result) {
                  return (
                    <Card key={modelType} className="border-yellow-200">
                      <CardContent className="p-4">
                        <div className="font-semibold text-yellow-600">{getModelName(modelType)}</div>
                        <div className="text-sm text-yellow-500 mt-1">No result available</div>
                      </CardContent>
                    </Card>
                  );
                }
                
                if ('error' in result) {
                  return (
                    <Card key={modelType} className="border-red-200">
                      <CardContent className="p-4">
                        <div className="font-semibold text-red-600">{getModelName(modelType)}</div>
                        <div className="text-sm text-red-500 mt-1">Error: {String(result.error)}</div>
                      </CardContent>
                    </Card>
                  );
                }

                const isMalignant = result.prediction === 1;
                const confidence = result.confidence ? (result.confidence * 100).toFixed(1) : 'N/A';

                return (
                  <Card key={modelType} className={isMalignant ? "border-red-200" : "border-green-200"}>
                    <CardContent className="p-4">
                      <div className="flex items-center justify-between mb-3">
                        <div className="font-semibold text-lg">{getModelName(modelType)}</div>
                        {isMalignant ? (
                          <XCircle className="h-5 w-5 text-destructive" />
                        ) : (
                          <CheckCircle2 className="h-5 w-5 text-green-600" />
                        )}
                      </div>
                      
                      <div className="space-y-2 text-sm">
                        <div className="flex justify-between">
                          <span className="text-gray-600">Prediction:</span>
                          <span className={isMalignant ? "text-destructive font-semibold" : "text-green-600 font-semibold"}>
                            {result.prediction_label}
                          </span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Confidence:</span>
                          <span className="font-semibold">{confidence}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Benign Prob:</span>
                          <span>{result.probability_benign ? (result.probability_benign * 100).toFixed(2) : 'N/A'}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-gray-600">Malignant Prob:</span>
                          <span>{result.probability_malignant ? (result.probability_malignant * 100).toFixed(2) : 'N/A'}%</span>
                        </div>
                        {result.model_metrics && (
                          <div className="mt-3 pt-3 border-t border-gray-200">
                            <div className="text-xs text-gray-500 mb-1">Model Performance:</div>
                            <div className="grid grid-cols-2 gap-1 text-xs">
                              <div>Accuracy: {(result.model_metrics.accuracy * 100).toFixed(1)}%</div>
                              <div>ROC-AUC: {result.model_metrics.roc_auc.toFixed(3)}</div>
                              <div>Recall: {(result.model_metrics.recall * 100).toFixed(1)}%</div>
                              <div>F1: {result.model_metrics.f1_score.toFixed(3)}</div>
                            </div>
                          </div>
                        )}
                      </div>
                    </CardContent>
                  </Card>
                );
              })}
            </div>

            <div className="mt-4 p-4 bg-blue-50 border border-blue-200 rounded-lg">
              <div className="font-semibold text-blue-900 mb-2">Interpretation</div>
              <div className="text-sm text-blue-800">
                <p className="mb-2">
                  Different algorithms may give different predictions. This is normal - each algorithm 
                  has different strengths and makes decisions differently.
                </p>
                <p>
                  <strong>If all models agree:</strong> High confidence in the result.
                </p>
                <p>
                  <strong>If models disagree:</strong> The case may be borderline. Consider consulting 
                  multiple models or a medical professional.
                </p>
              </div>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

