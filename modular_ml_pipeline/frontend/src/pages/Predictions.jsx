import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useMutation, useQuery } from '@tanstack/react-query'
import { predict, predictAll, getModels } from '../services/api'
import toast from 'react-hot-toast'
import { 
  Send, Loader2, CheckCircle, XCircle, 
  TrendingUp, AlertTriangle, Sparkles,
  Copy, Download
} from 'lucide-react'
import PredictionResult from '../components/prediction/PredictionResult'
import FeatureInput from '../components/prediction/FeatureInput'
import ModelSelector from '../components/prediction/ModelSelector'
import ModelVisualization from '../components/visualization/ModelVisualization'

const FEATURE_NAMES = [
  'radius_mean', 'texture_mean', 'perimeter_mean', 'area_mean', 'smoothness_mean',
  'compactness_mean', 'concavity_mean', 'concave_points_mean', 'symmetry_mean', 'fractal_dimension_mean',
  'radius_se', 'texture_se', 'perimeter_se', 'area_se', 'smoothness_se',
  'compactness_se', 'concavity_se', 'concave_points_se', 'symmetry_se', 'fractal_dimension_se',
  'radius_worst', 'texture_worst', 'perimeter_worst', 'area_worst', 'smoothness_worst',
  'compactness_worst', 'concavity_worst', 'concave_points_worst', 'symmetry_worst', 'fractal_dimension_worst'
]

const EXAMPLE_FEATURES = {
  malignant: [
    17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
    1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
    25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
  ],
  benign: [
    13.54, 14.36, 87.46, 566.3, 0.09779, 0.08129, 0.06664, 0.04781, 0.1885, 0.05766,
    0.2699, 0.7886, 2.058, 23.56, 0.008462, 0.0146, 0.02387, 0.01315, 0.0198, 0.0023,
    15.11, 19.26, 99.7, 711.2, 0.144, 0.1773, 0.239, 0.1288, 0.2977, 0.07259
  ]
}

const Predictions = () => {
  const [features, setFeatures] = useState(Array(30).fill(''))
  const [modelType, setModelType] = useState('all')
  const [showAdvanced, setShowAdvanced] = useState(false)
  const [results, setResults] = useState(null)

  // Récupérer les modèles disponibles
  const { data: modelsData } = useQuery({
    queryKey: ['models'],
    queryFn: getModels,
  })

  // Mutation pour prédiction simple
  const predictMutation = useMutation({
    mutationFn: ({ modelName, features }) => predict(modelName, features),
    onSuccess: (data) => {
      setResults({ type: 'single', data })
      toast.success('Prédiction effectuée avec succès!')
    },
    onError: (error) => {
      toast.error(error.message || 'Erreur lors de la prédiction')
    },
  })

  // Mutation pour prédiction avec tous les modèles
  const predictAllMutation = useMutation({
    mutationFn: (features) => predictAll(features),
    onSuccess: (data) => {
      setResults({ type: 'all', data })
      toast.success('Prédictions effectuées avec succès!')
    },
    onError: (error) => {
      toast.error(error.message || 'Erreur lors de la prédiction')
    },
  })

  const handleFeatureChange = (index, value) => {
    const newFeatures = [...features]
    newFeatures[index] = value
    setFeatures(newFeatures)
  }

  const loadExample = (type) => {
    const example = EXAMPLE_FEATURES[type]
    setFeatures(example.map(f => f.toString()))
    toast.success(`Exemple ${type === 'malignant' ? 'malin' : 'bénin'} chargé`)
  }

  const handleSubmit = (e) => {
    e.preventDefault()
    
    const featuresArray = features.map(f => parseFloat(f) || 0)
    
    if (featuresArray.some(f => isNaN(f) || f === 0)) {
      toast.error('Veuillez remplir tous les champs avec des nombres valides')
      return
    }

    if (modelType === 'all') {
      predictAllMutation.mutate(featuresArray)
    } else {
      predictMutation.mutate({ modelName: modelType, features: featuresArray })
    }
  }

  const isLoading = predictMutation.isPending || predictAllMutation.isPending

  return (
    <div className="container mx-auto px-4 py-8 max-w-7xl">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        className="mb-8"
      >
        <h1 className="text-4xl md:text-5xl font-bold mb-4">
          <span className="gradient-text">Prédiction</span>
          <span className="text-white"> en Temps Réel</span>
        </h1>
        <p className="text-white/70 text-lg">
          Entrez les caractéristiques de la tumeur pour obtenir une prédiction
        </p>
      </motion.div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Formulaire */}
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5 }}
          className="lg:col-span-2"
        >
          <form onSubmit={handleSubmit} className="card space-y-6">
            {/* En-tête avec actions */}
            <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
              <div>
                <h2 className="text-2xl font-bold text-white mb-2">
                  Caractéristiques de la Tumeur
                </h2>
                <p className="text-white/60 text-sm">
                  30 features numériques requises
                </p>
              </div>
              
              <div className="flex flex-wrap gap-2">
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => loadExample('malignant')}
                  className="px-4 py-2 bg-red-500/20 hover:bg-red-500/30 text-red-300 rounded-lg text-sm border border-red-500/30 transition-colors"
                >
                  Exemple Malin
                </motion.button>
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => loadExample('benign')}
                  className="px-4 py-2 bg-green-500/20 hover:bg-green-500/30 text-green-300 rounded-lg text-sm border border-green-500/30 transition-colors"
                >
                  Exemple Bénin
                </motion.button>
                <motion.button
                  type="button"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  onClick={() => setShowAdvanced(!showAdvanced)}
                  className="px-4 py-2 glass rounded-lg text-sm text-white/70 hover:text-white transition-colors"
                >
                  {showAdvanced ? 'Masquer' : 'Afficher'} noms
                </motion.button>
              </div>
            </div>

            {/* Sélecteur de modèle */}
            <ModelSelector
              modelType={modelType}
              setModelType={setModelType}
              availableModels={modelsData?.available_models || []}
            />

            {/* Grille de features */}
            <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3 max-h-96 overflow-y-auto p-2">
              {features.map((feature, index) => (
                <FeatureInput
                  key={index}
                  index={index}
                  value={feature}
                  onChange={handleFeatureChange}
                  featureName={showAdvanced ? FEATURE_NAMES[index] : `Feature ${index + 1}`}
                  showAdvanced={showAdvanced}
                />
              ))}
            </div>

            {/* Bouton de soumission */}
            <motion.button
              type="submit"
              disabled={isLoading}
              whileHover={{ scale: isLoading ? 1 : 1.02 }}
              whileTap={{ scale: isLoading ? 1 : 0.98 }}
              className="btn-primary w-full flex items-center justify-center space-x-2 text-lg py-4 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isLoading ? (
                <>
                  <Loader2 className="w-5 h-5 animate-spin" />
                  <span>Prédiction en cours...</span>
                </>
              ) : (
                <>
                  <Send className="w-5 h-5" />
                  <span>Faire une Prédiction</span>
                </>
              )}
            </motion.button>
          </form>
        </motion.div>

        {/* Résultats */}
        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
          className="lg:col-span-1"
        >
          <AnimatePresence mode="wait">
            {results ? (
              <PredictionResult
                key={results.type}
                result={results}
                onClose={() => setResults(null)}
              />
            ) : (
              <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="card text-center"
              >
                <div className="flex flex-col items-center justify-center py-12">
                  <motion.div
                    animate={{ 
                      scale: [1, 1.2, 1],
                      rotate: [0, 180, 360]
                    }}
                    transition={{ 
                      duration: 3,
                      repeat: Infinity,
                      ease: "easeInOut"
                    }}
                    className="w-16 h-16 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-full flex items-center justify-center mb-4"
                  >
                    <Sparkles className="w-8 h-8 text-white" />
                  </motion.div>
                  <h3 className="text-xl font-bold text-white mb-2">
                    Prêt pour la Prédiction
                  </h3>
                  <p className="text-white/60 text-sm">
                    Remplissez le formulaire et cliquez sur "Faire une Prédiction"
                  </p>
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </motion.div>
      </div>

      {/* Visualisation en temps réel */}
      {results && modelType !== 'all' && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
          className="mt-6"
        >
          <ModelVisualization
            modelName={modelType}
            features={features.map(f => parseFloat(f) || 0)}
          />
        </motion.div>
      )}
    </div>
  )
}

export default Predictions

