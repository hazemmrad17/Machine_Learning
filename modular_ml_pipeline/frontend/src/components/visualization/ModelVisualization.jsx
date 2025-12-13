import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Play, Pause, RotateCcw } from 'lucide-react'
import { predict } from '../../services/api'

const ModelVisualization = ({ modelName, features }) => {
  const [isPlaying, setIsPlaying] = useState(false)
  const [currentPrediction, setCurrentPrediction] = useState(null)
  const [history, setHistory] = useState([])
  const intervalRef = useRef(null)

  useEffect(() => {
    if (isPlaying && features) {
      intervalRef.current = setInterval(async () => {
        try {
          const result = await predict(modelName, features)
          setCurrentPrediction(result)
          setHistory(prev => [...prev.slice(-9), result])
        } catch (error) {
          console.error('Prediction error:', error)
        }
      }, 1000)
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current)
      }
    }
  }, [isPlaying, modelName, features])

  const handleReset = () => {
    setHistory([])
    setCurrentPrediction(null)
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="card"
    >
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-xl font-bold text-white">
          Visualisation: {modelName.toUpperCase()}
        </h3>
        <div className="flex space-x-2">
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={() => setIsPlaying(!isPlaying)}
            className={`p-2 rounded-lg ${
              isPlaying 
                ? 'bg-red-500/20 text-red-400 hover:bg-red-500/30' 
                : 'bg-cyan-500/20 text-cyan-400 hover:bg-cyan-500/30'
            } transition-colors`}
          >
            {isPlaying ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleReset}
            className="p-2 rounded-lg bg-white/10 text-white/70 hover:bg-white/20 transition-colors"
          >
            <RotateCcw className="w-4 h-4" />
          </motion.button>
        </div>
      </div>

      {currentPrediction && (
        <motion.div
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          className="space-y-4"
        >
          <div className="grid grid-cols-2 gap-4">
            <div className="glass rounded-lg p-4">
              <div className="text-sm text-white/60 mb-1">Prédiction</div>
              <div className={`text-2xl font-bold ${
                currentPrediction.prediction === 1 
                  ? 'text-red-400' 
                  : 'text-green-400'
              }`}>
                {currentPrediction.prediction === 1 ? 'MALIN' : 'BÉNIN'}
              </div>
            </div>
            <div className="glass rounded-lg p-4">
              <div className="text-sm text-white/60 mb-1">Probabilité</div>
              <div className="text-2xl font-bold gradient-text">
                {(currentPrediction.probability * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          {/* Probability Bar */}
          <div className="glass rounded-lg p-4">
            <div className="flex items-center justify-between mb-2">
              <span className="text-sm text-white/70">Confiance</span>
              <span className="text-sm text-white/70">{currentPrediction.confidence}</span>
            </div>
            <div className="w-full h-3 bg-white/10 rounded-full overflow-hidden">
              <motion.div
                initial={{ width: 0 }}
                animate={{ width: `${currentPrediction.probability * 100}%` }}
                transition={{ duration: 0.5 }}
                className={`h-full ${
                  currentPrediction.prediction === 1
                    ? 'bg-gradient-to-r from-red-500 to-red-600'
                    : 'bg-gradient-to-r from-green-500 to-green-600'
                }`}
              />
            </div>
          </div>

          {/* History */}
          {history.length > 0 && (
            <div className="glass rounded-lg p-4">
              <div className="text-sm text-white/70 mb-2">Historique</div>
              <div className="flex space-x-2 overflow-x-auto">
                {history.map((pred, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, scale: 0.8 }}
                    animate={{ opacity: 1, scale: 1 }}
                    className={`min-w-[60px] h-12 rounded-lg flex items-center justify-center text-xs font-semibold ${
                      pred.prediction === 1
                        ? 'bg-red-500/20 text-red-400'
                        : 'bg-green-500/20 text-green-400'
                    }`}
                  >
                    {(pred.probability * 100).toFixed(0)}%
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </motion.div>
      )}

      {!currentPrediction && (
        <div className="text-center py-8 text-white/50">
          Cliquez sur Play pour démarrer la visualisation
        </div>
      )}
    </motion.div>
  )
}

export default ModelVisualization

