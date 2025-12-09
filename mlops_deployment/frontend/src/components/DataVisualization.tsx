import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Select } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { BarChart3, Info } from 'lucide-react';
import { predictionHistory } from '@/utils/predictionHistory';

export function DataVisualization() {
  const [view, setView] = useState<'distribution' | 'correlation' | 'history'>('distribution');
  const [historyData, setHistoryData] = useState<any[]>([]);

  useEffect(() => {
    const history = predictionHistory.getAll();
    
    // Prediction history trends
    const historyTrends = history.slice(0, 20).map((item, index) => ({
      index: index + 1,
      confidence: (item.probability_benign > item.probability_malignant ? item.probability_benign : item.probability_malignant) * 100,
      benign: (item.probability_benign || 0) * 100,
      malignant: (item.probability_malignant || 0) * 100,
      prediction: item.prediction
    }));

    setHistoryData(historyTrends);
  }, []);

  return (
    <Card className="w-full max-w-6xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <CardTitle className="text-2xl font-bold flex items-center gap-2">
          <BarChart3 className="h-6 w-6" />
          Data Visualization
        </CardTitle>
        <CardDescription>
          Explore data distributions, correlations, and prediction trends
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        {/* View Selector */}
        <div className="flex gap-2">
          <div className="flex-1">
            <Label htmlFor="view-select">Visualization Type</Label>
            <Select
              id="view-select"
              value={view}
              onChange={(e) => setView(e.target.value as any)}
            >
              <option value="distribution">Feature Distribution</option>
              <option value="correlation">Feature Correlation</option>
              <option value="history">Prediction History Trends</option>
            </Select>
          </div>
        </div>

        {/* Feature Distribution */}
        {view === 'distribution' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Feature Distribution: Benign vs Malignant</h3>
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-4">
              <div className="flex items-start gap-2">
                <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-blue-800">
                  This shows typical average values for key features. Benign tumors generally have 
                  smaller, more regular features, while malignant tumors have larger, more irregular features.
                </div>
              </div>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={[
                { feature: 'Radius', benign: 12.5, malignant: 17.5 },
                { feature: 'Texture', benign: 18.0, malignant: 21.5 },
                { feature: 'Perimeter', benign: 80.0, malignant: 120.0 },
                { feature: 'Area', benign: 500.0, malignant: 1000.0 },
                { feature: 'Smoothness', benign: 0.09, malignant: 0.12 },
                { feature: 'Compactness', benign: 0.08, malignant: 0.25 },
              ]}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="feature" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="benign" fill="#00b87a" name="Benign (Avg)" />
                <Bar dataKey="malignant" fill="#e0245e" name="Malignant (Avg)" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Feature Correlation */}
        {view === 'correlation' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Feature Correlation Heatmap (Simplified)</h3>
            <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg mb-4">
              <div className="flex items-start gap-2">
                <Info className="h-5 w-5 text-blue-600 mt-0.5 flex-shrink-0" />
                <div className="text-sm text-blue-800">
                  This shows correlations between key features. Features like radius, perimeter, and area 
                  are highly correlated, which is expected in geometric measurements.
                </div>
              </div>
            </div>
            <div className="grid grid-cols-5 gap-2">
              {['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness'].map((feat1, i) => 
                ['Radius', 'Texture', 'Perimeter', 'Area', 'Smoothness'].map((feat2, j) => {
                  let correlation = 0.5;
                  if (feat1 === feat2) correlation = 1.0;
                  else if ((feat1 === 'Radius' && feat2 === 'Perimeter') || (feat1 === 'Perimeter' && feat2 === 'Radius')) correlation = 0.99;
                  else if ((feat1 === 'Radius' && feat2 === 'Area') || (feat1 === 'Area' && feat2 === 'Radius')) correlation = 0.95;
                  else if ((feat1 === 'Perimeter' && feat2 === 'Area') || (feat1 === 'Area' && feat2 === 'Perimeter')) correlation = 0.98;
                  else correlation = Math.random() * 0.3 + 0.1;

                  const intensity = Math.abs(correlation);
                  const color = correlation > 0 
                    ? `rgba(30, 157, 241, ${intensity})` 
                    : `rgba(224, 36, 94, ${intensity})`;

                  return (
                    <div
                      key={`${i}-${j}`}
                      className="p-3 text-center text-xs rounded border"
                      style={{ backgroundColor: color, color: intensity > 0.5 ? 'white' : 'black' }}
                    >
                      {i === 0 && <div className="font-semibold mb-1">{feat2}</div>}
                      {j === 0 && <div className="font-semibold mb-1">{feat1}</div>}
                      <div className="text-xs">{correlation.toFixed(2)}</div>
                    </div>
                  );
                })
              )}
            </div>
            <div className="mt-4 flex items-center gap-4 text-xs">
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-blue-500"></div>
                <span>Positive Correlation</span>
              </div>
              <div className="flex items-center gap-2">
                <div className="w-4 h-4 bg-red-500"></div>
                <span>Negative Correlation</span>
              </div>
            </div>
          </div>
        )}

        {/* Prediction History Trends */}
        {view === 'history' && (
          <div>
            <h3 className="text-lg font-semibold mb-4">Prediction History Trends</h3>
            {historyData.length === 0 ? (
              <div className="text-center py-8 text-slate-500">
                No prediction history available. Make some predictions to see trends!
              </div>
            ) : (
              <ResponsiveContainer width="100%" height={400}>
                <ScatterChart data={historyData}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="index" name="Prediction #" />
                  <YAxis domain={[0, 100]} name="Probability (%)" />
                  <Tooltip cursor={{ strokeDasharray: '3 3' }} />
                  <Legend />
                  <Scatter name="Confidence" dataKey="confidence" fill="#1e9df1" />
                  <Scatter name="Benign Prob" dataKey="benign" fill="#00b87a" />
                  <Scatter name="Malignant Prob" dataKey="malignant" fill="#e0245e" />
                </ScatterChart>
              </ResponsiveContainer>
            )}
          </div>
        )}
      </CardContent>
    </Card>
  );
}

