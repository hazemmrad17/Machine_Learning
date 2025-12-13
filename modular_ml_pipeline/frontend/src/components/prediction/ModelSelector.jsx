import { motion } from 'framer-motion'
import { Brain, Zap, Layers } from 'lucide-react'

const ModelSelector = ({ modelType, setModelType, availableModels }) => {
  // Debug: Log available models to help troubleshoot
  if (availableModels && availableModels.length > 0) {
    console.log('Available models from API:', availableModels)
  }
  
  const models = [
    { value: 'all', label: 'Tous (Consensus)', icon: Layers, color: 'from-cyan-500 to-blue-500' },
    { value: 'linear', label: 'Linear', icon: Brain, color: 'from-blue-400 to-cyan-400' },
    { value: 'softmax', label: 'Softmax', icon: Brain, color: 'from-cyan-400 to-blue-400' },
    { value: 'mlp', label: 'MLP', icon: Brain, color: 'from-blue-500 to-cyan-500' },
    { value: 'svm', label: 'SVM', icon: Zap, color: 'from-yellow-500 to-orange-500' },
    { value: 'knn_l1', label: 'KNN-L1', icon: Zap, color: 'from-orange-500 to-red-500' },
    { value: 'knn_l2', label: 'KNN-L2', icon: Zap, color: 'from-red-500 to-pink-500' },
    { value: 'gru_svm', label: 'GRU-SVM', icon: Layers, color: 'from-green-500 to-emerald-500' },
  ]

  return (
    <div className="glass rounded-xl p-4">
      <label className="block text-sm font-semibold text-white/90 mb-3">
        Modèle à utiliser:
      </label>
      <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-2">
        {models.map((model) => {
          const Icon = model.icon
          // Check if model is available - API returns lowercase model names like 'linear', 'knn_l1', 'gru_svm'
          // Normalize both the model value and available models to lowercase for comparison
          const normalizedModelValue = model.value.toLowerCase()
          const normalizedAvailable = Array.isArray(availableModels) 
            ? availableModels.map(m => String(m).toLowerCase().trim())
            : []
          
          // Debug specific model
          if (model.value === 'gru_svm') {
            console.log('GRU-SVM check:', {
              modelValue: model.value,
              normalizedValue: normalizedModelValue,
              availableModels: normalizedAvailable,
              matches: normalizedAvailable.filter(a => a.includes('gru') || a.includes('svm'))
            })
          }
          
          // Check for exact match or partial match (for gru_svm, check for 'gru' or 'svm' in the name)
          const isAvailable = model.value === 'all' || 
            normalizedAvailable.includes(normalizedModelValue) ||
            normalizedAvailable.includes(normalizedModelValue.replace('_', '-')) ||
            normalizedAvailable.includes(normalizedModelValue.replace('-', '_')) ||
            (model.value === 'gru_svm' && normalizedAvailable.some(a => a.includes('gru') && a.includes('svm')))
          const isSelected = modelType === model.value
          
          return (
            <motion.button
              key={model.value}
              type="button"
              onClick={() => setModelType(model.value)}
              disabled={!isAvailable}
              whileHover={{ scale: isAvailable ? 1.05 : 1 }}
              whileTap={{ scale: isAvailable ? 0.95 : 1 }}
              className={`relative p-3 rounded-lg transition-all duration-300 ${
                isSelected
                  ? `bg-gradient-to-br ${model.color} text-white shadow-lg`
                  : isAvailable
                  ? 'glass hover:bg-white/20 text-white/70 hover:text-white'
                  : 'bg-white/5 text-white/30 cursor-not-allowed'
              }`}
            >
              <Icon className="w-5 h-5 mx-auto mb-1" />
              <div className="text-xs font-medium">{model.label}</div>
              {isSelected && (
                <motion.div
                  layoutId="selectedModel"
                  className="absolute inset-0 border-2 border-white/50 rounded-lg"
                  transition={{ type: 'spring', stiffness: 500, damping: 30 }}
                />
              )}
              {!isAvailable && (
                <div className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full" />
              )}
            </motion.button>
          )
        })}
      </div>
    </div>
  )
}

export default ModelSelector

