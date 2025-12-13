import { motion } from 'framer-motion'

const FeatureInput = ({ index, value, onChange, featureName, showAdvanced }) => {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ delay: index * 0.01 }}
      whileHover={{ scale: 1.05 }}
      className="flex flex-col"
    >
      <label className="text-xs text-white/60 mb-1 truncate" title={featureName}>
        {showAdvanced ? featureName : `F${index + 1}`}
      </label>
      <input
        type="number"
        step="any"
        value={value}
        onChange={(e) => onChange(index, e.target.value)}
        placeholder="0.0"
        className="input-field text-sm w-full"
        required
      />
    </motion.div>
  )
}

export default FeatureInput

