import { motion } from 'framer-motion'
import { X, CheckCircle, XCircle, TrendingUp, AlertTriangle, Copy } from 'lucide-react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'
import toast from 'react-hot-toast'

const PredictionResult = ({ result, onClose }) => {
  const isSingle = result.type === 'single'
  const data = result.data

  const getPredictionColor = (prediction) => {
    return prediction === 1 ? '#ef4444' : '#22c55e'
  }

  const getConfidenceColor = (confidence) => {
    if (confidence === 'Élevée') return '#22c55e'
    if (confidence === 'Moyenne') return '#f59e0b'
    return '#ef4444'
  }

  const copyToClipboard = () => {
    const text = JSON.stringify(data, null, 2)
    navigator.clipboard.writeText(text)
    toast.success('Résultat copié dans le presse-papiers!')
  }

  if (isSingle) {
    const isMalignant = data.prediction === 1
    const probabilityPercent = (data.probability * 100).toFixed(2)

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="card space-y-4"
      >
        {/* En-tête */}
        <div className="flex items-center justify-between">
          <h3 className="text-xl font-bold text-white">Résultat</h3>
          <motion.button
            whileHover={{ scale: 1.1, rotate: 90 }}
            whileTap={{ scale: 0.9 }}
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-white/70" />
          </motion.button>
        </div>

        {/* Prédiction principale */}
        <motion.div
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ type: 'spring', stiffness: 200, damping: 15 }}
          className={`p-6 rounded-xl border-2 ${
            isMalignant
              ? 'bg-red-500/20 border-red-500/50'
              : 'bg-green-500/20 border-green-500/50'
          }`}
        >
          <div className="flex items-center justify-center space-x-3 mb-4">
            {isMalignant ? (
              <XCircle className="w-8 h-8 text-red-400" />
            ) : (
              <CheckCircle className="w-8 h-8 text-green-400" />
            )}
            <h4 className="text-2xl font-bold text-white">
              {isMalignant ? '🔴 Malin' : '🟢 Bénin'}
            </h4>
          </div>

          <div className="text-center">
            <p className="text-white/60 text-sm mb-2">Modèle: {data.model_name}</p>
            <div className="text-3xl font-bold gradient-text mb-2">
              {probabilityPercent}%
            </div>
            <p className="text-white/70 text-sm">Probabilité de malignité</p>
          </div>
        </motion.div>

        {/* Barre de probabilité */}
        <div className="space-y-2">
          <div className="flex justify-between text-sm">
            <span className="text-white/70">Probabilité</span>
            <span className="text-white font-semibold">{probabilityPercent}%</span>
          </div>
          <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden">
            <motion.div
              initial={{ width: 0 }}
              animate={{ width: `${probabilityPercent}%` }}
              transition={{ duration: 1, ease: 'easeOut' }}
              className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500"
            />
          </div>
        </div>

        {/* Confiance */}
        <div className="flex items-center justify-between p-3 glass rounded-lg">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-5 h-5 text-white/70" />
            <span className="text-white/70">Confiance:</span>
          </div>
          <span
            className="font-semibold"
            style={{ color: getConfidenceColor(data.confidence) }}
          >
            {data.confidence}
          </span>
        </div>

        {/* Avertissement */}
        <div className="flex items-start space-x-2 p-3 bg-yellow-500/20 border border-yellow-500/30 rounded-lg">
          <AlertTriangle className="w-5 h-5 text-yellow-400 mt-0.5 flex-shrink-0" />
          <p className="text-xs text-yellow-200">
            Cette prédiction est à titre informatif uniquement et ne remplace pas un diagnostic médical professionnel.
          </p>
        </div>

        {/* Actions */}
        <motion.button
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={copyToClipboard}
          className="w-full btn-secondary flex items-center justify-center space-x-2"
        >
          <Copy className="w-4 h-4" />
          <span>Copier le résultat</span>
        </motion.button>
      </motion.div>
    )
  } else {
    // Résultat avec tous les modèles
    const { predictions, consensus } = data
    const chartData = Object.entries(predictions)
      .filter(([_, pred]) => !pred.error)
      .map(([model, pred]) => ({
        model,
        probabilité: (pred.probability * 100).toFixed(1),
        prédiction: pred.prediction === 1 ? 'Malin' : 'Bénin',
      }))

    return (
      <motion.div
        initial={{ opacity: 0, scale: 0.9 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.9 }}
        className="card space-y-4 max-h-[calc(100vh-200px)] overflow-y-auto"
      >
        {/* En-tête */}
        <div className="flex items-center justify-between sticky top-0 bg-slate-900/80 backdrop-blur-sm pb-2 border-b border-white/10">
          <h3 className="text-xl font-bold text-white">Résultats Multi-Modèles</h3>
          <motion.button
            whileHover={{ scale: 1.1, rotate: 90 }}
            whileTap={{ scale: 0.9 }}
            onClick={onClose}
            className="p-2 hover:bg-white/10 rounded-lg transition-colors"
          >
            <X className="w-5 h-5 text-white/70" />
          </motion.button>
        </div>

        {/* Consensus */}
        {consensus && (
          <motion.div
            initial={{ scale: 0.9 }}
            animate={{ scale: 1 }}
            className={`p-4 rounded-xl border-2 ${
              consensus.prediction === 1
                ? 'bg-red-500/20 border-red-500/50'
                : 'bg-green-500/20 border-green-500/50'
            }`}
          >
            <div className="text-center">
              <h4 className="text-lg font-bold text-white mb-2">Consensus</h4>
              <div className="text-3xl font-bold gradient-text mb-1">
                {consensus.prediction === 1 ? '🔴 Malin' : '🟢 Bénin'}
              </div>
              <div className="text-sm text-white/70">
                Accord: {consensus.agreement}% | Confiance: {consensus.confidence}
              </div>
            </div>
          </motion.div>
        )}

        {/* Graphique */}
        {chartData.length > 0 && (
          <div className="glass rounded-xl p-4">
            <h4 className="text-sm font-semibold text-white/90 mb-3">Comparaison des Modèles</h4>
            <ResponsiveContainer width="100%" height={200}>
              <BarChart data={chartData}>
                <XAxis dataKey="model" tick={{ fill: '#fff', fontSize: 12 }} />
                <YAxis tick={{ fill: '#fff', fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: 'rgba(15, 23, 42, 0.95)',
                    border: '1px solid rgba(255, 255, 255, 0.2)',
                    borderRadius: '8px',
                    color: '#fff',
                  }}
                />
                <Bar dataKey="probabilité">
                  {chartData.map((entry, index) => (
                    <Cell
                      key={`cell-${index}`}
                      fill={entry.prédiction === 'Malin' ? '#ef4444' : '#22c55e'}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Détails par modèle */}
        <div className="space-y-2">
          {Object.entries(predictions).map(([model, pred]) => (
            <motion.div
              key={model}
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              className="glass rounded-lg p-3"
            >
              {pred.error ? (
                <div className="flex items-center space-x-2 text-red-400">
                  <XCircle className="w-4 h-4" />
                  <span className="text-sm">{model}: {pred.error}</span>
                </div>
              ) : (
                <div className="flex items-center justify-between">
                  <span className="text-white font-medium text-sm">{model}</span>
                  <div className="flex items-center space-x-3">
                    <span className={`text-sm font-semibold ${
                      pred.prediction === 1 ? 'text-red-400' : 'text-green-400'
                    }`}>
                      {pred.prediction === 1 ? 'Malin' : 'Bénin'}
                    </span>
                    <span className="text-white/70 text-sm">
                      {(pred.probability * 100).toFixed(1)}%
                    </span>
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>

        {/* Avertissement */}
        <div className="flex items-start space-x-2 p-3 bg-yellow-500/20 border border-yellow-500/30 rounded-lg">
          <AlertTriangle className="w-5 h-5 text-yellow-400 mt-0.5 flex-shrink-0" />
          <p className="text-xs text-yellow-200">
            Cette prédiction est à titre informatif uniquement et ne remplace pas un diagnostic médical professionnel.
          </p>
        </div>
      </motion.div>
    )
  }
}

export default PredictionResult

