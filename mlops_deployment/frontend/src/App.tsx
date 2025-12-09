import { Suspense, useState } from 'react';
import GenerativeMountainScene from '@/components/ui/mountain-scene';
import { PredictionForm } from '@/components/PredictionForm';
import { PredictionResults } from '@/components/PredictionResults';
import { CSVUpload } from '@/components/CSVUpload';
import { BatchResults } from '@/components/BatchResults';
import { PredictionHistory } from '@/components/PredictionHistory';
import { ModelPerformanceDashboard } from '@/components/ModelPerformanceDashboard';
import { EnsemblePrediction } from '@/components/EnsemblePrediction';
import { FeatureImportance } from '@/components/FeatureImportance';
import { DataVisualization } from '@/components/DataVisualization';
import { PredictionResponse, FeatureInput } from '@/services/api';
import { Activity, FileText, Home, History, BarChart3, Users, Eye } from 'lucide-react';
import { Button } from '@/components/ui/button';

type View = 'home' | 'manual' | 'csv' | 'history' | 'dashboard' | 'ensemble' | 'visualization';

function App() {
  const [currentView, setCurrentView] = useState<View>('home');
  const [predictionResult, setPredictionResult] = useState<PredictionResponse | null>(null);
  const [batchResults, setBatchResults] = useState<PredictionResponse[]>([]);
  const [predictionFeatures, setPredictionFeatures] = useState<Record<string, number> | undefined>();
  const [currentFeatures, setCurrentFeatures] = useState<FeatureInput | null>(null);

  const handlePrediction = (result: PredictionResponse, features?: Record<string, number>) => {
    setPredictionResult(result);
    setPredictionFeatures(features);
    // Convert features to FeatureInput format for ensemble
    if (features) {
      setCurrentFeatures(features as unknown as FeatureInput);
    }
    setCurrentView('home');
  };

  const handleBatchPredictions = (results: PredictionResponse[]) => {
    setBatchResults(results);
    setCurrentView('home');
  };

  return (
    <main className="relative w-full min-h-screen bg-[#0f172a] overflow-auto text-slate-100">
      <Suspense fallback={<div className="w-full h-full bg-[#0f172a]" />}>
        <GenerativeMountainScene />
      </Suspense>

      {/* Content Overlay */}
      <div className="relative z-10 min-h-screen">
        {/* Navigation */}
        <nav className="sticky top-0 z-20 bg-slate-900/80 backdrop-blur-md border-b border-slate-700/50">
          <div className="container mx-auto px-4 py-4">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <Activity className="h-6 w-6 text-blue-400" />
                <h1 className="text-xl font-bold">Breast Cancer Detection</h1>
              </div>
              <div className="flex gap-2">
                <Button
                  variant={currentView === 'home' ? 'default' : 'ghost'}
                  onClick={() => {
                    setCurrentView('home');
                    setPredictionResult(null);
                    setBatchResults([]);
                  }}
                  className="text-white"
                >
                  <Home className="h-4 w-4 mr-2" />
                  Home
                </Button>
                <Button
                  variant={currentView === 'manual' ? 'default' : 'ghost'}
                  onClick={() => setCurrentView('manual')}
                  className="text-white"
                >
                  Manual Input
                </Button>
                <Button
                  variant={currentView === 'csv' ? 'default' : 'ghost'}
                  onClick={() => setCurrentView('csv')}
                  className="text-white"
                >
                  <FileText className="h-4 w-4 mr-2" />
                  CSV Upload
                </Button>
                <Button
                  variant={currentView === 'history' ? 'default' : 'ghost'}
                  onClick={() => setCurrentView('history')}
                  className="text-white"
                >
                  <History className="h-4 w-4 mr-2" />
                  History
                </Button>
                <Button
                  variant={currentView === 'dashboard' ? 'default' : 'ghost'}
                  onClick={() => setCurrentView('dashboard')}
                  className="text-white"
                >
                  <BarChart3 className="h-4 w-4 mr-2" />
                  Dashboard
                </Button>
                <Button
                  variant={currentView === 'ensemble' ? 'default' : 'ghost'}
                  onClick={() => setCurrentView('ensemble')}
                  className="text-white"
                >
                  <Users className="h-4 w-4 mr-2" />
                  Ensemble
                </Button>
                <Button
                  variant={currentView === 'visualization' ? 'default' : 'ghost'}
                  onClick={() => setCurrentView('visualization')}
                  className="text-white"
                >
                  <Eye className="h-4 w-4 mr-2" />
                  Visualize
                </Button>
              </div>
            </div>
          </div>
        </nav>

        {/* Main Content */}
        <div className="container mx-auto px-4 py-8">
          {currentView === 'home' && (
            <div className="space-y-6">
              {/* Hero Section */}
              <div className="text-center space-y-4 mb-12">
                <h2 className="text-4xl md:text-5xl font-bold bg-gradient-to-r from-blue-400 to-cyan-400 bg-clip-text text-transparent">
                  Breast Cancer Detection System
                </h2>
                <p className="text-lg text-slate-300 max-w-2xl mx-auto">
                  Advanced machine learning model for predicting breast cancer diagnosis
                  using the Wisconsin Diagnostic Breast Cancer dataset
                </p>
              </div>

              {/* Quick Actions */}
              <div className="grid md:grid-cols-3 gap-4 max-w-6xl mx-auto mb-8">
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 hover:bg-white/15 transition-colors cursor-pointer" onClick={() => setCurrentView('manual')}>
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-3 bg-blue-500/20 rounded-lg">
                      <Activity className="h-6 w-6 text-blue-400" />
                    </div>
                    <h3 className="text-xl font-semibold">Manual Input</h3>
                  </div>
                  <p className="text-slate-300 text-sm">
                    Enter 30 features manually to get an instant prediction
                  </p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 hover:bg-white/15 transition-colors cursor-pointer" onClick={() => setCurrentView('csv')}>
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-3 bg-green-500/20 rounded-lg">
                      <FileText className="h-6 w-6 text-green-400" />
                    </div>
                    <h3 className="text-xl font-semibold">Batch Processing</h3>
                  </div>
                  <p className="text-slate-300 text-sm">
                    Upload a CSV file for batch predictions on multiple samples
                  </p>
                </div>
                <div className="bg-white/10 backdrop-blur-sm rounded-lg p-6 border border-white/20 hover:bg-white/15 transition-colors cursor-pointer" onClick={() => setCurrentView('ensemble')}>
                  <div className="flex items-center gap-3 mb-3">
                    <div className="p-3 bg-purple-500/20 rounded-lg">
                      <Users className="h-6 w-6 text-purple-400" />
                    </div>
                    <h3 className="text-xl font-semibold">Ensemble</h3>
                  </div>
                  <p className="text-slate-300 text-sm">
                    Combine predictions from all models for higher accuracy
                  </p>
                </div>
              </div>

              {/* Results Display */}
              {predictionResult && (
                <div className="mb-6">
                  <PredictionResults result={predictionResult} features={predictionFeatures} />
                </div>
              )}

              {batchResults.length > 0 && (
                <div className="mb-6">
                  <BatchResults 
                    results={batchResults} 
                    onClose={() => setBatchResults([])} 
                  />
                </div>
              )}
            </div>
          )}

          {currentView === 'manual' && (
            <div className="max-w-6xl mx-auto">
              <PredictionForm onPrediction={(result) => handlePrediction(result, undefined)} />
            </div>
          )}

          {currentView === 'csv' && (
            <div className="max-w-4xl mx-auto">
              <CSVUpload onBatchPredictions={handleBatchPredictions} />
            </div>
          )}

          {currentView === 'history' && (
            <div className="max-w-6xl mx-auto">
              <PredictionHistory />
            </div>
          )}

          {currentView === 'dashboard' && (
            <div className="max-w-6xl mx-auto">
              <ModelPerformanceDashboard />
            </div>
          )}

          {currentView === 'ensemble' && (
            <div className="max-w-4xl mx-auto space-y-6">
              <EnsemblePrediction 
                features={currentFeatures || undefined} 
              />
              {predictionFeatures && (
                <FeatureImportance features={predictionFeatures} />
              )}
            </div>
          )}

          {currentView === 'visualization' && (
            <div className="max-w-6xl mx-auto">
              <DataVisualization />
            </div>
          )}
          </div>

        {/* Footer */}
        <footer className="relative z-10 mt-16 py-8 border-t border-slate-700/50 bg-slate-900/50 backdrop-blur-sm">
          <div className="container mx-auto px-4 text-center text-slate-400 text-sm">
            <p>Breast Cancer Detection System - Machine Learning Model</p>
            <p className="mt-2 text-xs">
              This tool is for research purposes only and should not replace professional medical diagnosis.
            </p>
          </div>
        </footer>
      </div>
    </main>
  );
}

export default App;

