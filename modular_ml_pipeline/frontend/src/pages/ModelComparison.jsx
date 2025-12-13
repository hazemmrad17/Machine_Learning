import { useState, useEffect } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useMutation } from '@tanstack/react-query'
import { retrain, predictAll } from '../services/api'
import toast from 'react-hot-toast'
import { 
  RefreshCw, Settings, TrendingUp, Clock,
  CheckCircle, XCircle, Loader2, Eye, ChevronDown
} from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts'
import HyperparameterInput from '../components/ui/HyperparameterInput'

const ModelComparison = () => {
  const [retrainModel, setRetrainModel] = useState('mlp')
  const [retrainResults, setRetrainResults] = useState(null)
  const [showHyperparams, setShowHyperparams] = useState(false)
  const [hyperparams, setHyperparams] = useState({})

  // Mutation pour réentraîner
  const retrainMutation = useMutation({
    mutationFn: ({ modelType, hyperparameters }) => retrain(modelType, hyperparameters),
    onSuccess: (data) => {
      setRetrainResults(data)
      toast.success(`Modèle ${data.model_name} réentraîné avec succès!`)
    },
    onError: (error) => {
      toast.error(error.message || 'Erreur lors du réentraînement')
    },
  })

  const handleRetrain = (modelType, hyperparameters = {}) => {
    // Convert string values to appropriate types
    const processedHyperparams = {}
    for (const [key, value] of Object.entries(hyperparameters)) {
      if (value === '' || value === null || value === undefined) continue
      
      // Try to parse as number
      const numValue = parseFloat(value)
      if (!isNaN(numValue) && isFinite(value)) {
        processedHyperparams[key] = numValue
      } else if (value === 'true' || value === 'false') {
        processedHyperparams[key] = value === 'true'
      } else if (value.startsWith('[') && value.endsWith(']')) {
        // Handle tuple/array format like "[500, 500, 500]"
        try {
          processedHyperparams[key] = JSON.parse(value)
        } catch {
          processedHyperparams[key] = value
        }
      } else {
        processedHyperparams[key] = value
      }
    }
    
    retrainMutation.mutate({ modelType, hyperparameters: processedHyperparams })
  }

  // Default hyperparameters for each model (from notebook)
  const defaultHyperparams = {
    linear: { eta0: 0.001, max_iter: 3000, random_state: 42 },
    softmax: { eta0: 0.001, max_iter: 3000, random_state: 42 },
    mlp: { 
      hidden_layer_sizes: '[500, 500, 500]', 
      learning_rate_init: 0.01, 
      alpha: 0.01, 
      max_iter: 3000, 
      early_stopping: 'true',
      validation_fraction: 0.1,
      random_state: 42 
    },
    svm: { C: 5, kernel: 'rbf', probability: 'true', random_state: 42, max_iter: 3000 },
    knn_l1: { n_neighbors: 1, distance: 'l1' },
    knn_l2: { n_neighbors: 1, distance: 'l2' },
    gru_svm: { 
      epochs: 500, 
      batch_size: 128, 
      patience: 30, 
      learning_rate: 0.001, 
      svm_C: 5, 
      random_state: 42 
    }
  }

  const updateHyperparam = (key, value) => {
    setHyperparams(prev => ({ ...prev, [key]: value }))
  }

  const resetToDefaults = () => {
    setHyperparams(defaultHyperparams[retrainModel] || {})
  }

  // Initialize hyperparams when model changes
  useEffect(() => {
    setHyperparams(defaultHyperparams[retrainModel] || {})
  }, [retrainModel])

  const getHyperparamFields = () => {
    const fields = {
      linear: [
        { key: 'eta0', label: 'Learning Rate (eta0)', type: 'number', step: '0.0001', default: 0.001 },
        { key: 'max_iter', label: 'Max Iterations', type: 'number', step: '100', default: 3000 },
        { key: 'random_state', label: 'Random State', type: 'number', step: '1', default: 42 }
      ],
      softmax: [
        { key: 'eta0', label: 'Learning Rate (eta0)', type: 'number', step: '0.0001', default: 0.001 },
        { key: 'max_iter', label: 'Max Iterations', type: 'number', step: '100', default: 3000 },
        { key: 'random_state', label: 'Random State', type: 'number', step: '1', default: 42 }
      ],
      mlp: [
        { key: 'hidden_layer_sizes', label: 'Hidden Layers (e.g., [500, 500, 500])', type: 'text', default: '[500, 500, 500]' },
        { key: 'learning_rate_init', label: 'Learning Rate', type: 'number', step: '0.001', default: 0.01 },
        { key: 'alpha', label: 'L2 Regularization (alpha)', type: 'number', step: '0.001', default: 0.01 },
        { key: 'max_iter', label: 'Max Iterations', type: 'number', step: '100', default: 3000 },
        { key: 'early_stopping', label: 'Early Stopping', type: 'select', options: ['true', 'false'], default: 'true' },
        { key: 'validation_fraction', label: 'Validation Fraction', type: 'number', step: '0.01', default: 0.1 },
        { key: 'random_state', label: 'Random State', type: 'number', step: '1', default: 42 }
      ],
      svm: [
        { key: 'C', label: 'Regularization (C)', type: 'number', step: '0.1', default: 5 },
        { key: 'kernel', label: 'Kernel', type: 'select', options: ['rbf', 'linear', 'poly', 'sigmoid'], default: 'rbf' },
        { key: 'probability', label: 'Probability', type: 'select', options: ['true', 'false'], default: 'true' },
        { key: 'max_iter', label: 'Max Iterations', type: 'number', step: '100', default: 3000 },
        { key: 'random_state', label: 'Random State', type: 'number', step: '1', default: 42 }
      ],
      knn_l1: [
        { key: 'n_neighbors', label: 'Number of Neighbors', type: 'number', step: '1', default: 1 },
        { key: 'distance', label: 'Distance Metric', type: 'select', options: ['l1'], default: 'l1' }
      ],
      knn_l2: [
        { key: 'n_neighbors', label: 'Number of Neighbors', type: 'number', step: '1', default: 1 },
        { key: 'distance', label: 'Distance Metric', type: 'select', options: ['l2'], default: 'l2' }
      ],
      gru_svm: [
        { key: 'epochs', label: 'Epochs', type: 'number', step: '10', default: 500 },
        { key: 'batch_size', label: 'Batch Size', type: 'number', step: '8', default: 128 },
        { key: 'patience', label: 'Early Stopping Patience', type: 'number', step: '5', default: 30 },
        { key: 'learning_rate', label: 'Learning Rate', type: 'number', step: '0.0001', default: 0.001 },
        { key: 'svm_C', label: 'SVM C Parameter', type: 'number', step: '0.1', default: 5 },
        { key: 'random_state', label: 'Random State', type: 'number', step: '1', default: 42 }
      ]
    }
    return fields[retrainModel] || []
  }

  // Données d'exemple pour la comparaison (à remplacer par de vraies données)
  const comparisonData = [
    { model: 'Linear', accuracy: 0.9123, precision: 0.9234, recall: 0.8889, f1: 0.9058, roc_auc: 0.9542 },
    { model: 'Softmax', accuracy: 0.9474, precision: 0.9444, recall: 0.9444, f1: 0.9444, roc_auc: 0.9789 },
    { model: 'MLP', accuracy: 0.9649, precision: 0.9714, recall: 0.9444, f1: 0.9577, roc_auc: 0.9873 },
    { model: 'SVM', accuracy: 0.9649, precision: 0.9444, recall: 0.9722, f1: 0.9581, roc_auc: 0.9873 },
    { model: 'KNN', accuracy: 0.9474, precision: 0.9444, recall: 0.9444, f1: 0.9444, roc_auc: 0.9789 },
    { model: 'GRU-SVM', accuracy: 0.9825, precision: 0.9722, recall: 0.9861, f1: 0.9791, roc_auc: 0.9956 },
  ]

  const chartData = comparisonData.map(m => ({
    ...m,
    accuracy: (m.accuracy * 100).toFixed(1),
    precision: (m.precision * 100).toFixed(1),
    recall: (m.recall * 100).toFixed(1),
    f1: (m.f1 * 100).toFixed(1),
    roc_auc: (m.roc_auc * 100).toFixed(1),
  }))

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gradient-text">Comparaison</span>
          <span className="text-white"> des Modèles</span>
        </h1>
        <p className="text-white/70 text-lg">
          Analysez et comparez les performances de tous les modèles
        </p>
      </motion.div>

      {/* Graphique de comparaison */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.1 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold text-white mb-6">Métriques de Performance</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={chartData}>
            <XAxis dataKey="model" tick={{ fill: '#fff' }} />
            <YAxis tick={{ fill: '#fff' }} label={{ value: 'Pourcentage (%)', angle: -90, position: 'insideLeft', fill: '#fff' }} />
            <Tooltip
              contentStyle={{
                backgroundColor: 'rgba(15, 23, 42, 0.95)',
                border: '1px solid rgba(255, 255, 255, 0.2)',
                borderRadius: '8px',
                color: '#fff',
              }}
            />
            <Legend wrapperStyle={{ color: '#fff' }} />
            <Bar dataKey="accuracy" fill="#06b6d4" name="Accuracy" />
            <Bar dataKey="precision" fill="#3b82f6" name="Precision" />
            <Bar dataKey="recall" fill="#0ea5e9" name="Recall" />
            <Bar dataKey="f1" fill="#22c55e" name="F1-Score" />
            <Bar dataKey="roc_auc" fill="#f59e0b" name="ROC-AUC" />
          </BarChart>
        </ResponsiveContainer>
      </motion.div>

      {/* Tableau de comparaison */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.2 }}
        className="card mb-6"
      >
        <h2 className="text-2xl font-bold text-white mb-6">Tableau Comparatif</h2>
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="border-b border-white/20">
                <th className="text-left py-3 px-4 text-white/90 font-semibold">Modèle</th>
                <th className="text-right py-3 px-4 text-white/90 font-semibold">Accuracy</th>
                <th className="text-right py-3 px-4 text-white/90 font-semibold">Precision</th>
                <th className="text-right py-3 px-4 text-white/90 font-semibold">Recall</th>
                <th className="text-right py-3 px-4 text-white/90 font-semibold">F1-Score</th>
                <th className="text-right py-3 px-4 text-white/90 font-semibold">ROC-AUC</th>
              </tr>
            </thead>
            <tbody>
              {comparisonData.map((model, index) => (
                <motion.tr
                  key={model.model}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.1 }}
                  className="border-b border-white/10 hover:bg-white/5 transition-colors"
                >
                  <td className="py-4 px-4">
                    <div className="flex items-center space-x-2">
                      <div className={`w-3 h-3 rounded-full ${
                        index === 0 ? 'bg-cyan-500' : index === 1 ? 'bg-blue-500' : index === 2 ? 'bg-cyan-400' : index === 3 ? 'bg-blue-400' : index === 4 ? 'bg-yellow-500' : 'bg-green-500'
                      }`} />
                      <span className="font-semibold text-white">{model.model}</span>
                    </div>
                  </td>
                  <td className="text-right py-4 px-4 text-white/90">
                    {(model.accuracy * 100).toFixed(2)}%
                  </td>
                  <td className="text-right py-4 px-4 text-white/90">
                    {(model.precision * 100).toFixed(2)}%
                  </td>
                  <td className="text-right py-4 px-4 text-white/90">
                    {(model.recall * 100).toFixed(2)}%
                  </td>
                  <td className="text-right py-4 px-4 text-white/90">
                    {(model.f1 * 100).toFixed(2)}%
                  </td>
                  <td className="text-right py-4 px-4 text-white/90">
                    {(model.roc_auc * 100).toFixed(2)}%
                  </td>
                </motion.tr>
              ))}
            </tbody>
          </table>
        </div>
      </motion.div>

      {/* Section Réentraînement */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5, delay: 0.3 }}
        className="card"
      >
        <div className="flex items-center space-x-2 mb-6">
          <Settings className="w-6 h-6 text-cyan-400" />
          <h2 className="text-2xl font-bold text-white">Réentraîner un Modèle</h2>
        </div>

        <div className="space-y-4">
          <div>
            <label className="block text-sm font-semibold text-white/90 mb-2">
              Sélectionner le modèle à réentraîner:
            </label>
            <div className="grid grid-cols-3 lg:grid-cols-7 gap-3">
              {['linear', 'softmax', 'mlp', 'svm', 'knn_l1', 'knn_l2', 'gru_svm'].map((model) => (
                <motion.button
                  key={model}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => {
                    setRetrainModel(model)
                    setHyperparams(defaultHyperparams[model] || {})
                  }}
                  disabled={retrainMutation.isPending}
                  className={`p-3 rounded-lg font-semibold transition-all ${
                    retrainModel === model
                      ? 'bg-gradient-to-br from-cyan-500 to-blue-600 text-white'
                      : 'glass text-white/70 hover:text-white'
                  } disabled:opacity-50`}
                >
                  {model.toUpperCase()}
                </motion.button>
              ))}
            </div>
          </div>

          {/* Hyperparameters Section */}
          <div className="space-y-3">
            <div className="flex items-center justify-between">
              <label className="block text-sm font-semibold text-white/90">
                Hyperparamètres (Expérimentation)
              </label>
              <div className="flex space-x-2">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={resetToDefaults}
                  className="text-xs px-3 py-1 glass rounded-lg text-white/70 hover:text-white transition-colors"
                >
                  Réinitialiser
                </motion.button>
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowHyperparams(!showHyperparams)}
                  className="text-xs px-3 py-1 glass rounded-lg text-white/70 hover:text-white transition-colors"
                >
                  {showHyperparams ? 'Masquer' : 'Afficher'}
                </motion.button>
              </div>
            </div>

            {showHyperparams && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                exit={{ opacity: 0, height: 0 }}
                className="glass rounded-lg p-4 space-y-3"
              >
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {getHyperparamFields().map((field, idx) => (
                    <motion.div
                      key={field.key}
                      initial={{ opacity: 0, y: 10 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: idx * 0.05 }}
                    >
                      <label className="block text-xs font-semibold text-white/80 mb-2 flex items-center justify-between">
                        <span>{field.label}</span>
                        {field.default && (
                          <span className="text-xs text-white/40 font-normal">
                            Défaut: {field.default}
                          </span>
                        )}
                      </label>
                      <HyperparameterInput
                        field={field}
                        value={hyperparams[field.key]}
                        onChange={(val) => updateHyperparam(field.key, val)}
                        disabled={retrainMutation.isPending}
                      />
                    </motion.div>
                  ))}
                </div>
                <p className="text-xs text-white/50 italic">
                  💡 Laissez les champs vides pour utiliser les valeurs par défaut du notebook
                </p>
              </motion.div>
            )}
          </div>

          <motion.button
            whileHover={{ scale: 1.02 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => handleRetrain(retrainModel, hyperparams)}
            disabled={retrainMutation.isPending}
            className="btn-primary w-full flex items-center justify-center space-x-2 disabled:opacity-50"
          >
            {retrainMutation.isPending ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Réentraînement en cours...</span>
              </>
            ) : (
              <>
                <RefreshCw className="w-5 h-5" />
                <span>Réentraîner le Modèle</span>
              </>
            )}
          </motion.button>

          {retrainResults && (
            <motion.div
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              className="glass rounded-xl p-4 space-y-3"
            >
              <div className="flex items-center space-x-2 text-green-400">
                <CheckCircle className="w-5 h-5" />
                <span className="font-semibold">{retrainResults.message}</span>
              </div>
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <div className="text-sm text-white/60 mb-1">Accuracy</div>
                  <div className="text-2xl font-bold gradient-text">
                    {(retrainResults.accuracy * 100).toFixed(2)}%
                  </div>
                </div>
                <div>
                  <div className="text-sm text-white/60 mb-1">Temps d'entraînement</div>
                  <div className="text-2xl font-bold text-white flex items-center space-x-1">
                    <Clock className="w-5 h-5" />
                    <span>{retrainResults.training_time}s</span>
                  </div>
                </div>
              </div>
            </motion.div>
          )}
        </div>
      </motion.div>
    </div>
  )
}

export default ModelComparison
