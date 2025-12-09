import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PredictionResponse } from '@/services/api';
import { CheckCircle2, XCircle, TrendingUp, Download } from 'lucide-react';
import { exportUtils } from '@/utils/exportUtils';

interface PredictionResultsProps {
  result: PredictionResponse;
  features?: Record<string, number>;
}

export function PredictionResults({ result, features }: PredictionResultsProps) {
  const isMalignant = result.prediction === 1;

  return (
    <Card className="w-full max-w-2xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-2xl font-bold flex items-center gap-2">
          {isMalignant ? (
            <>
              <XCircle className="h-6 w-6 text-destructive" />
              <span className="text-destructive">Malignant Detected</span>
            </>
          ) : (
            <>
              <CheckCircle2 className="h-6 w-6 text-green-600" />
              <span className="text-green-600">Benign</span>
            </>
          )}
          </CardTitle>
          <Button
            onClick={() => exportUtils.exportToPDF(result, features)}
            variant="outline"
            size="sm"
          >
            <Download className="h-4 w-4 mr-2" />
            Export PDF
          </Button>
        </div>
        <CardDescription>
          Model: {result.model_type?.toUpperCase() || 'MLP'}
          {result.model_metrics && (
            <span className="ml-2 text-xs">
              (Model Accuracy: {(result.model_metrics.accuracy * 100).toFixed(1)}%)
            </span>
          )}
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-2 gap-4">
          <div className="p-4 rounded-lg bg-green-50 border border-green-200">
            <div className="text-sm text-green-700 font-medium mb-1">Benign Probability</div>
            <div className="text-2xl font-bold text-green-800">
              {(result.probability_benign * 100).toFixed(2)}%
            </div>
          </div>
          <div className="p-4 rounded-lg bg-red-50 border border-red-200">
            <div className="text-sm text-red-700 font-medium mb-1">Malignant Probability</div>
            <div className="text-2xl font-bold text-red-800">
              {(result.probability_malignant * 100).toFixed(2)}%
            </div>
          </div>
        </div>

        <div className="mt-6 p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-start gap-2">
            <TrendingUp className="h-5 w-5 text-blue-600 mt-0.5" />
            <div>
              <div className="font-semibold text-blue-900 mb-1">Interpretation</div>
              <p className="text-sm text-blue-800">
                {isMalignant
                  ? 'The model predicts this sample is likely malignant. Please consult with a healthcare professional for further evaluation.'
                  : 'The model predicts this sample is likely benign. However, this is a prediction tool and should not replace professional medical diagnosis.'}
              </p>
            </div>
          </div>
        </div>


        <div className="text-xs text-gray-500 mt-4">
          <strong>Medical Disclaimer:</strong> This is a machine learning prediction tool and should not be used as a substitute for professional medical diagnosis, advice, or treatment.
        </div>
      </CardContent>
    </Card>
  );
}

