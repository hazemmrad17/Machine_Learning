import { motion } from 'framer-motion'
import { ChevronUp, ChevronDown } from 'lucide-react'
import { useState } from 'react'

const FeatureInput = ({ index, value, onChange, featureName, showAdvanced }) => {
  const [isFocused, setIsFocused] = useState(false)
  const numValue = parseFloat(value) || 0

  const handleIncrement = (e) => {
    e.preventDefault()
    const step = numValue >= 1 ? 1 : numValue >= 0.1 ? 0.1 : 0.01
    onChange(index, (numValue + step).toFixed(step < 1 ? 2 : 0))
  }

  const handleDecrement = (e) => {
    e.preventDefault()
    const step = numValue >= 1 ? 1 : numValue >= 0.1 ? 0.1 : 0.01
    onChange(index, Math.max(0, numValue - step).toFixed(step < 1 ? 2 : 0))
  }

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.01 }}
      whileHover={{ scale: 1.02 }}
      className="flex flex-col"
    >
      <label className="text-xs text-white/60 mb-1.5 truncate font-medium" title={featureName}>
        {showAdvanced ? featureName : `F${index + 1}`}
      </label>
      <div className="relative group">
        <input
          type="number"
          step="any"
          value={value}
          onChange={(e) => onChange(index, e.target.value)}
          onFocus={() => setIsFocused(true)}
          onBlur={() => setIsFocused(false)}
          placeholder="0.00"
          className="input-field text-sm w-full pr-20 bg-white/5 border border-white/10 rounded-lg px-3 py-2.5 text-white placeholder-white/30 focus:outline-none focus:ring-2 focus:ring-cyan-500/50 focus:border-cyan-500/50 transition-all"
          required
        />
        <div className="absolute right-1 top-1/2 -translate-y-1/2 flex flex-col gap-0.5">
          <motion.button
            type="button"
            onClick={handleIncrement}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="w-7 h-6 flex items-center justify-center bg-white/10 hover:bg-cyan-500/30 rounded-t-md border border-white/20 hover:border-cyan-500/50 transition-colors group/btn"
            title="Augmenter"
          >
            <ChevronUp className="w-4 h-4 text-white/70 group-hover/btn:text-cyan-300" />
          </motion.button>
          <motion.button
            type="button"
            onClick={handleDecrement}
            whileHover={{ scale: 1.1 }}
            whileTap={{ scale: 0.9 }}
            className="w-7 h-6 flex items-center justify-center bg-white/10 hover:bg-cyan-500/30 rounded-b-md border border-white/20 hover:border-cyan-500/50 transition-colors group/btn"
            title="Diminuer"
          >
            <ChevronDown className="w-4 h-4 text-white/70 group-hover/btn:text-cyan-300" />
          </motion.button>
        </div>
        {isFocused && (
          <motion.div
            initial={{ opacity: 0, y: -5 }}
            animate={{ opacity: 1, y: 0 }}
            className="absolute -top-8 left-0 right-0 text-xs text-cyan-400 text-center pointer-events-none"
          >
            {featureName}
          </motion.div>
        )}
      </div>
    </motion.div>
  )
}

export default FeatureInput

