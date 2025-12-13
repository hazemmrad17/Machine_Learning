import { motion } from 'framer-motion'
import { Github, Code, Heart } from 'lucide-react'

const Footer = () => {
  return (
    <motion.footer
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      transition={{ delay: 0.5 }}
      className="glass-strong border-t border-white/20 mt-auto"
    >
      <div className="container mx-auto px-4 py-6">
        <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
          <div className="flex items-center space-x-2 text-white/60">
            <Code className="w-5 h-5" />
            <span>Détection du Cancer du Sein - ML Pipeline</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <motion.a
              href="https://github.com"
              target="_blank"
              rel="noopener noreferrer"
              whileHover={{ scale: 1.1, y: -2 }}
              whileTap={{ scale: 0.9 }}
              className="p-2 glass rounded-lg hover:bg-white/20 transition-colors"
            >
              <Github className="w-5 h-5 text-white/70" />
            </motion.a>
            
            <div className="flex items-center space-x-1 text-white/60 text-sm">
              <span>Fait avec</span>
              <motion.div
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 1, repeat: Infinity }}
              >
                <Heart className="w-4 h-4 text-pink-500 fill-pink-500" />
              </motion.div>
              <span>pour la santé</span>
            </div>
          </div>
        </div>
        
        <div className="mt-4 pt-4 border-t border-white/10 text-center text-white/40 text-sm">
          <p>⚠️ Cette application est à titre éducatif uniquement. Ne remplace pas un diagnostic médical professionnel.</p>
        </div>
      </div>
    </motion.footer>
  )
}

export default Footer

