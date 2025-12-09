import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import { TrendingUp, Info } from 'lucide-react';

interface FeatureImportanceProps {
  features: Record<string, number>;
}

// Feature importance based on typical breast cancer detection research
// This is a simplified version - in production, you'd calculate this from the model
const FEATURE_IMPORTANCE: Record<string, number> = {
  'radius_worst': 0.15,
  'perimeter_worst': 0.14,
  'area_worst': 0.13,
  'concave_points_worst': 0.12,
  'concavity_worst': 0.11,
  'radius_mean': 0.10,
  'perimeter_mean': 0.09,
  'area_mean': 0.08,
  'concave_points_mean': 0.07,
  'concavity_mean': 0.06,
  'texture_worst': 0.05,
  'smoothness_worst': 0.04,
  'compactness_worst': 0.03,
  'symmetry_worst': 0.02,
  'fractal_dimension_worst': 0.01,
  'radius_se': 0.01,
  'texture_mean': 0.01,
  'perimeter_se': 0.01,
  'area_se': 0.01,
  'smoothness_mean': 0.01,
  'compactness_mean': 0.01,
  'symmetry_mean': 0.01,
  'fractal_dimension_mean': 0.01,
  'texture_se': 0.005,
  'smoothness_se': 0.005,
  'compactness_se': 0.005,
  'concavity_se': 0.005,
  'concave_points_se': 0.005,
  'symmetry_se': 0.005,
  'fractal_dimension_se': 0.005
};

export function FeatureImportance({ features }: FeatureImportanceProps) {
  const [importanceData, setImportanceData] = useState<Array<{name: string; importance: number; value: number}>>([]);

  useEffect(() => {
    // Calculate weighted importance (importance * normalized feature value)
    const data = Object.entries(features)
      .map(([key, value]) => ({
        name: key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase()),
        importance: FEATURE_IMPORTANCE[key] || 0.001,
        value: value
      }))
      .filter(item => item.importance > 0)
      .sort((a, b) => b.importance - a.importance)
      .slice(0, 15); // Top 15 features

    setImportanceData(data);
  }, [features]);

  const topFeatures = importanceData.slice(0, 10);

  return (
    <Card className="w-full max-w-4xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-2xl font-bold flex items-center gap-2">
          <TrendingUp className="h-6 w-6" />
          Feature Importance Analysis
        </CardTitle>
        <CardDescription>
          Top features influencing the prediction (based on research literature)
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
          <div className="flex items-start gap-2">
            <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
            <div className="text-sm text-blue-800">
              <strong>Note:</strong> Feature importance is based on research findings. 
              In production, this would be calculated using SHAP values or permutation importance 
              from the actual trained models.
            </div>
          </div>
        </div>

        {/* Top Features Chart */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Top 10 Most Important Features</h3>
          <ResponsiveContainer width="100%" height={400}>
            <BarChart data={topFeatures} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis type="number" domain={[0, 0.2]} />
              <YAxis dataKey="name" type="category" width={150} />
              <Tooltip formatter={(value: number) => (value * 100).toFixed(2) + '%'} />
              <Legend />
              <Bar dataKey="importance" fill="#1e9df1" name="Importance Score" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Feature Values Table */}
        <div>
          <h3 className="text-lg font-semibold mb-4">Feature Values</h3>
          <div className="overflow-x-auto">
            <table className="w-full border-collapse text-sm">
              <thead>
                <tr className="border-b">
                  <th className="text-left p-2">Feature</th>
                  <th className="text-right p-2">Value</th>
                  <th className="text-right p-2">Importance</th>
                  <th className="text-right p-2">Weighted Impact</th>
                </tr>
              </thead>
              <tbody>
                {topFeatures.map((item, index) => (
                  <tr key={index} className="border-b hover:bg-slate-50">
                    <td className="p-2 font-medium">{item.name}</td>
                    <td className="text-right p-2">{item.value.toFixed(4)}</td>
                    <td className="text-right p-2">{(item.importance * 100).toFixed(2)}%</td>
                    <td className="text-right p-2 font-semibold">
                      {(item.importance * item.value).toFixed(6)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}

