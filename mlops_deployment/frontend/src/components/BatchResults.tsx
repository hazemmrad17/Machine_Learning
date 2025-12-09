import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { PredictionResponse } from '@/services/api';
import { Download, X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { Select } from '@/components/ui/select';
import { Label } from '@/components/ui/label';
import { useState } from 'react';
import { exportUtils } from '@/utils/exportUtils';

interface BatchResultsProps {
  results: PredictionResponse[];
  onClose: () => void;
}

export function BatchResults({ results, onClose }: BatchResultsProps) {
  const [filterPrediction, setFilterPrediction] = useState<string>('all');
  const [sortBy, setSortBy] = useState<string>('index');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredAndSorted = results
    .map((r, i) => ({ ...r, index: i }))
    .filter(r => {
      if (filterPrediction !== 'all' && r.prediction !== parseInt(filterPrediction)) return false;
      if (searchTerm && !r.prediction_label.toLowerCase().includes(searchTerm.toLowerCase())) return false;
      return true;
    })
    .sort((a, b) => {
      if (sortBy === 'confidence') return b.confidence - a.confidence;
      if (sortBy === 'index') return a.index - b.index;
      return 0;
    });


  const stats = {
    total: filteredAndSorted.length,
    benign: filteredAndSorted.filter(r => r.prediction === 0).length,
    malignant: filteredAndSorted.filter(r => r.prediction === 1).length,
    avgConfidence: filteredAndSorted.reduce((sum, r) => sum + r.confidence, 0) / (filteredAndSorted.length || 1)
  };

  return (
    <Card className="w-full max-w-6xl mx-auto bg-white/90 backdrop-blur-sm">
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <CardTitle className="text-2xl font-bold">Batch Prediction Results</CardTitle>
            <CardDescription>
              {stats.total} sample{stats.total !== 1 ? 's' : ''} processed
            </CardDescription>
          </div>
          <div className="flex gap-2">
            <Button onClick={() => exportUtils.exportBatchToExcel(results)} variant="outline" size="sm">
              <Download className="h-4 w-4 mr-2" />
              Export Excel
            </Button>
            <Button onClick={onClose} variant="ghost" size="sm">
              <X className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        {/* Filters */}
        <div className="flex gap-2 items-end">
          <div className="flex-1">
            <Label htmlFor="batch-search">Search</Label>
            <Input
              id="batch-search"
              placeholder="Search predictions..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="w-40">
            <Label htmlFor="batch-filter">Filter</Label>
            <Select
              id="batch-filter"
              value={filterPrediction}
              onChange={(e) => setFilterPrediction(e.target.value)}
            >
              <option value="all">All</option>
              <option value="0">Benign</option>
              <option value="1">Malignant</option>
            </Select>
          </div>
          <div className="w-40">
            <Label htmlFor="batch-sort">Sort By</Label>
            <Select
              id="batch-sort"
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value)}
            >
              <option value="index">Original Order</option>
              <option value="confidence">Confidence (High to Low)</option>
            </Select>
          </div>
        </div>
        {/* Statistics */}
        <div className="grid grid-cols-4 gap-4">
          <div className="p-3 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="text-xs text-blue-600 mb-1">Total Samples</div>
            <div className="text-2xl font-bold text-blue-800">{stats.total}</div>
          </div>
          <div className="p-3 bg-green-50 border border-green-200 rounded-lg">
            <div className="text-xs text-green-600 mb-1">Benign</div>
            <div className="text-2xl font-bold text-green-800">{stats.benign}</div>
            <div className="text-xs text-green-600">({((stats.benign / stats.total) * 100).toFixed(1)}%)</div>
          </div>
          <div className="p-3 bg-red-50 border border-red-200 rounded-lg">
            <div className="text-xs text-red-600 mb-1">Malignant</div>
            <div className="text-2xl font-bold text-red-800">{stats.malignant}</div>
            <div className="text-xs text-red-600">({((stats.malignant / stats.total) * 100).toFixed(1)}%)</div>
          </div>
          <div className="p-3 bg-purple-50 border border-purple-200 rounded-lg">
            <div className="text-xs text-purple-600 mb-1">Avg Confidence</div>
            <div className="text-2xl font-bold text-purple-800">{(stats.avgConfidence * 100).toFixed(1)}%</div>
          </div>
        </div>

        {/* Results List */}
        <div className="space-y-2 max-h-96 overflow-y-auto">
          {filteredAndSorted.map((result) => (
            <div key={result.index} className={`p-3 rounded border ${
              result.prediction === 1 
                ? 'bg-red-50 border-red-200' 
                : 'bg-green-50 border-green-200'
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-3">
                  <span className="font-semibold text-slate-700">Sample {result.index + 1}</span>
                  <span className={`font-medium ${
                    result.prediction === 1 ? 'text-red-700' : 'text-green-700'
                  }`}>
                    {result.prediction_label}
                  </span>
                  {result.model_type && (
                    <span className="text-xs text-slate-500">({result.model_type.toUpperCase()})</span>
                  )}
                </div>
                <div className="flex items-center gap-4 text-sm">
                  <span className="text-slate-600">
                    Benign: <span className="font-semibold">{(result.probability_benign * 100).toFixed(1)}%</span>
                  </span>
                  <span className="text-slate-600">
                    Malignant: <span className="font-semibold">{(result.probability_malignant * 100).toFixed(1)}%</span>
                  </span>
                  <span className="font-semibold text-slate-700">
                    Confidence: {(result.confidence * 100).toFixed(1)}%
                  </span>
                </div>
              </div>
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}

