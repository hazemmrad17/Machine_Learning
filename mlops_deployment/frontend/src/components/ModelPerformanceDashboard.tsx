import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { api, ModelInfo } from '@/services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';
import { TrendingUp, Activity } from 'lucide-react';

export function ModelPerformanceDashboard() {
  const [models, setModels] = useState<Record<string, ModelInfo>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadModels();
  }, []);

  const loadModels = async () => {
    try {
      const data = await api.listModels();
      setModels(data.models);
    } catch (error) {
      console.error('Failed to load models:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="text-center py-8">Loading model performance data...</div>;
  }

  const modelArray = Object.entries(models).map(([key, value]) => ({
    name: key.toUpperCase(),
    accuracy: (value.metrics.accuracy * 100).toFixed(1),
    rocAuc: (value.metrics.roc_auc * 100).toFixed(1),
    recall: (value.metrics.recall * 100).toFixed(1),
    precision: (value.metrics.precision * 100).toFixed(1),
    f1: (value.metrics.f1_score * 100).toFixed(1),
    ...value.metrics
  }));

  return (
    <div className="space-y-6">
      <Card className="bg-white/90 backdrop-blur-sm">
        <CardHeader>
          <CardTitle className="text-2xl font-bold flex items-center gap-2">
            <Activity className="h-6 w-6" />
            Model Performance Dashboard
          </CardTitle>
          <CardDescription>
            Compare performance metrics across all trained models
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-6">
          {/* Accuracy Comparison */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Accuracy Comparison</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelArray}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[90, 100]} />
                <Tooltip formatter={(value: number) => `${value.toFixed(2)}%`} />
                <Legend />
                <Bar dataKey="accuracy" fill="#1e9df1" name="Accuracy (%)" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* ROC-AUC Comparison */}
          <div>
            <h3 className="text-lg font-semibold mb-4">ROC-AUC Score Comparison</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={modelArray}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0.9, 1.0]} />
                <Tooltip formatter={(value: number) => value.toFixed(4)} />
                <Legend />
                <Bar dataKey="rocAuc" fill="#00b87a" name="ROC-AUC" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          {/* All Metrics Line Chart */}
          <div>
            <h3 className="text-lg font-semibold mb-4">All Metrics Comparison</h3>
            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={modelArray}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis domain={[0.85, 1.0]} />
                <Tooltip formatter={(value: number) => value.toFixed(3)} />
                <Legend />
                <Line type="monotone" dataKey="accuracy" stroke="#1e9df1" name="Accuracy" />
                <Line type="monotone" dataKey="roc_auc" stroke="#00b87a" name="ROC-AUC" />
                <Line type="monotone" dataKey="recall" stroke="#f7b928" name="Recall" />
                <Line type="monotone" dataKey="precision" stroke="#e0245e" name="Precision" />
                <Line type="monotone" dataKey="f1_score" stroke="#17bf63" name="F1-Score" />
              </LineChart>
            </ResponsiveContainer>
          </div>

          {/* Metrics Table */}
          <div>
            <h3 className="text-lg font-semibold mb-4">Detailed Metrics</h3>
            <div className="overflow-x-auto">
              <table className="w-full border-collapse">
                <thead>
                  <tr className="border-b">
                    <th className="text-left p-2">Model</th>
                    <th className="text-right p-2">Accuracy</th>
                    <th className="text-right p-2">ROC-AUC</th>
                    <th className="text-right p-2">Recall</th>
                    <th className="text-right p-2">Precision</th>
                    <th className="text-right p-2">F1-Score</th>
                  </tr>
                </thead>
                <tbody>
                  {modelArray.map((model) => (
                    <tr key={model.name} className="border-b hover:bg-slate-50">
                      <td className="p-2 font-medium">{model.name}</td>
                      <td className="text-right p-2">{(model.accuracy * 100).toFixed(2)}%</td>
                      <td className="text-right p-2">{model.roc_auc.toFixed(4)}</td>
                      <td className="text-right p-2">{(model.recall * 100).toFixed(2)}%</td>
                      <td className="text-right p-2">{(model.precision * 100).toFixed(2)}%</td>
                      <td className="text-right p-2">{model.f1_score.toFixed(4)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

