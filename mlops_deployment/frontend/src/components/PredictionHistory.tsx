import { useState, useEffect } from 'react';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { predictionHistory, PredictionHistoryItem } from '@/utils/predictionHistory';
import { History, Trash2, Download } from 'lucide-react';

const formatDate = (timestamp: number): string => {
  const date = new Date(timestamp);
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit'
  });
};

export function PredictionHistory() {
  const [history, setHistory] = useState<PredictionHistoryItem[]>([]);
  const [filteredHistory, setFilteredHistory] = useState<PredictionHistoryItem[]>([]);
  const [filterModel, setFilterModel] = useState<string>('all');
  const [filterPrediction, setFilterPrediction] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    loadHistory();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [history, filterModel, filterPrediction, searchTerm]);

  const loadHistory = () => {
    const all = predictionHistory.getAll();
    setHistory(all);
    setFilteredHistory(all);
  };

  const applyFilters = () => {
    let filtered = [...history];

    if (filterModel !== 'all') {
      filtered = filtered.filter(item => item.model_type === filterModel);
    }

    if (filterPrediction !== 'all') {
      filtered = filtered.filter(item => item.prediction === parseInt(filterPrediction));
    }

    if (searchTerm) {
      const term = searchTerm.toLowerCase();
      filtered = filtered.filter(item =>
        item.prediction_label.toLowerCase().includes(term) ||
        item.model_type?.toLowerCase().includes(term) ||
        item.id.includes(term)
      );
    }

    // Sort by timestamp (newest first)
    filtered.sort((a, b) => b.timestamp - a.timestamp);
    setFilteredHistory(filtered);
  };

  const handleDelete = (id: string) => {
    predictionHistory.delete(id);
    loadHistory();
  };

  const handleClearAll = () => {
    if (confirm('Are you sure you want to clear all prediction history?')) {
      predictionHistory.clear();
      loadHistory();
    }
  };

  const handleExport = () => {
    const csv = [
      ['ID', 'Timestamp', 'Model', 'Prediction', 'Label', 'Benign Prob', 'Malignant Prob', 'Confidence'],
      ...filteredHistory.map(item => [
        item.id,
        formatDate(item.timestamp),
        item.model_type || 'N/A',
        item.prediction,
        item.prediction_label,
        (item.probability_benign * 100).toFixed(2),
        (item.probability_malignant * 100).toFixed(2),
        (item.confidence * 100).toFixed(2)
      ])
    ].map(row => row.join(',')).join('\n');

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `prediction_history_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const stats = predictionHistory.getStats();
  const availableModels = Array.from(new Set(history.map(h => h.model_type).filter(Boolean)));

  return (
    <Card className="w-full max-w-6xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-2xl font-bold flex items-center gap-2">
              <History className="h-6 w-6" />
              Prediction History
            </CardTitle>
            <CardDescription>
              {filteredHistory.length} of {history.length} predictions
            </CardDescription>
          </div>
          <div className="flex gap-2">
            <Button onClick={handleExport} variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export
            </Button>
            <Button onClick={handleClearAll} variant="destructive" size="sm">
              <Trash2 className="h-4 w-4 mr-2" />
              Clear All
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Statistics */}
        <div className="grid grid-cols-4 gap-4">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="text-xs text-blue-600 mb-1">Total</div>
            <div className="text-2xl font-bold text-blue-800">{stats.total}</div>
          </div>
          <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
            <div className="text-xs text-green-600 mb-1">Benign</div>
            <div className="text-2xl font-bold text-green-800">{stats.benign}</div>
          </div>
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="text-xs text-red-600 mb-1">Malignant</div>
            <div className="text-2xl font-bold text-red-800">{stats.malignant}</div>
          </div>
          <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
            <div className="text-xs text-purple-600 mb-1">Models Used</div>
            <div className="text-2xl font-bold text-purple-800">{availableModels.length}</div>
          </div>
        </div>

        {/* Filters */}
        <div className="flex gap-2 items-end">
          <div className="flex-1">
            <Label htmlFor="search">Search</Label>
            <Input
              id="search"
              placeholder="Search predictions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="w-40">
            <Label htmlFor="model-filter">Model</Label>
            <Select
              id="model-filter"
              value={filterModel}
              onChange={(e) => setFilterModel(e.target.value)}
            >
              <option value="all">All Models</option>
              {availableModels.map(model => (
                <option key={model || 'unknown'} value={model || 'unknown'}>{model?.toUpperCase() || 'UNKNOWN'}</option>
              ))}
            </Select>
          </div>
          <div className="w-40">
            <Label htmlFor="prediction-filter">Prediction</Label>
            <Select
              id="prediction-filter"
              value={filterPrediction}
              onChange={(e) => setFilterPrediction(e.target.value)}
            >
              <option value="all">All</option>
              <option value="0">Benign</option>
              <option value="1">Malignant</option>
            </Select>
          </div>
        </div>

        {/* History List */}
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {filteredHistory.length === 0 ? (
            <div className="text-center py-8 text-slate-500">
              No predictions found. Make some predictions to see them here!
            </div>
          ) : (
            filteredHistory.map((item) => (
              <div
                key={item.id}
                className={`p-3 rounded border ${
                  item.prediction === 1
                    ? 'bg-red-50 border-red-200'
                    : 'bg-green-50 border-green-200'
                }`}
              >
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-3">
                    <div>
                      <div className="font-semibold">
                        {item.prediction_label}
                        <span className="ml-2 text-xs text-slate-500">
                          ({item.model_type?.toUpperCase() || 'MLP'})
                        </span>
                      </div>
                      <div className="text-xs text-slate-600 mt-1">
                        {formatDate(item.timestamp)}
                      </div>
                    </div>
                  </div>
                  <div className="flex items-center gap-4">
                    <div className="text-sm">
                      <span className="text-slate-600">Confidence: </span>
                      <span className="font-semibold">{(item.confidence * 100).toFixed(1)}%</span>
                    </div>
                    <Button
                      onClick={() => handleDelete(item.id)}
                      variant="ghost"
                      size="sm"
                      className="text-red-600 hover:text-red-700"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="text-xs text-slate-500 mt-2 flex gap-4">
                  <span>Benign: {(item.probability_benign * 100).toFixed(2)}%</span>
                  <span>Malignant: {(item.probability_malignant * 100).toFixed(2)}%</span>
                </div>
              </div>
            ))
          )}
        </div>
      </CardContent>
    </Card>
  );
}

