import { motion, AnimatePresence } from 'framer-motion'
import { ChevronDown, X } from 'lucide-react'
import { useState } from 'react'

const HyperparameterInput = ({ field, value, onChange, disabled = false }) => {
  const [isOpen, setIsOpen] = useState(false)

  if (field.type === 'select') {
    return (
      <div className="relative">
        <motion.button
          whileHover={{ scale: disabled ? 1 : 1.02 }}
          whileTap={{ scale: disabled ? 1 : 0.98 }}
          onClick={() => !disabled && setIsOpen(!isOpen)}
          disabled={disabled}
          className="w-full input-field flex items-center justify-between cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
        >
          <span className="text-white">{value || field.default || 'Sélectionner...'}</span>
          <ChevronDown 
            className={`w-4 h-4 text-white/70 transition-transform ${isOpen ? 'rotate-180' : ''}`}
          />
        </motion.button>
        
        <AnimatePresence>
          {isOpen && !disabled && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="absolute z-50 w-full mt-2 glass-strong rounded-lg overflow-hidden shadow-2xl"
            >
              {field.options.map((option) => (
                <motion.button
                  key={option}
                  whileHover={{ backgroundColor: 'rgba(6, 182, 212, 0.2)' }}
                  whileTap={{ scale: 0.98 }}
                  onClick={() => {
                    onChange(option)
                    setIsOpen(false)
                  }}
                  className={`w-full px-4 py-3 text-left text-white transition-colors ${
                    value === option ? 'bg-cyan-600/30' : 'hover:bg-white/10'
                  }`}
                >
                  {option}
                </motion.button>
              ))}
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    )
  }

  if (field.type === 'toggle') {
    const isEnabled = value === 'true' || value === true || (field.default === 'true' && !value)
    return (
      <motion.button
        whileHover={{ scale: disabled ? 1 : 1.05 }}
        whileTap={{ scale: disabled ? 1 : 0.95 }}
        onClick={() => !disabled && onChange(!isEnabled ? 'true' : 'false')}
        disabled={disabled}
        className={`relative w-16 h-8 rounded-full transition-colors ${
          isEnabled 
            ? 'bg-gradient-to-r from-cyan-500 to-blue-600' 
            : 'bg-white/20'
        } disabled:opacity-50 disabled:cursor-not-allowed`}
      >
        <motion.div
          animate={{ x: isEnabled ? 32 : 4 }}
          transition={{ type: 'spring', stiffness: 500, damping: 30 }}
          className="absolute top-1 left-1 w-6 h-6 bg-white rounded-full shadow-lg"
        />
        <span className="absolute inset-0 flex items-center justify-center text-xs font-semibold text-white">
          {isEnabled ? 'ON' : 'OFF'}
        </span>
      </motion.button>
    )
  }

  return (
    <div className="relative">
      <input
        type={field.type}
        step={field.step}
        value={value || field.default || ''}
        onChange={(e) => onChange(e.target.value)}
        placeholder={field.default?.toString()}
        disabled={disabled}
        className="input-field w-full pr-8 disabled:opacity-50 disabled:cursor-not-allowed"
      />
      {value && value !== field.default && (
        <motion.button
          initial={{ opacity: 0, scale: 0 }}
          animate={{ opacity: 1, scale: 1 }}
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.9 }}
          onClick={() => onChange(field.default || '')}
          className="absolute right-2 top-1/2 -translate-y-1/2 p-1 rounded-full bg-white/10 hover:bg-white/20 transition-colors"
          title="Réinitialiser"
        >
          <X className="w-3 h-3 text-white/70" />
        </motion.button>
      )}
    </div>
  )
}

export default HyperparameterInput

