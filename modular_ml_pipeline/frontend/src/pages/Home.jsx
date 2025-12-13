import { motion } from 'framer-motion'
import { Link } from 'react-router-dom'
import { ArrowRight, Activity, BarChart3, Zap, Shield, TrendingUp } from 'lucide-react'
import { useQuery } from '@tanstack/react-query'
import { checkHealth, getModels } from '../services/api'
import toast from 'react-hot-toast'

const Home = () => {
  // Vérifier la santé de l'API
  const { data: health, isLoading: healthLoading } = useQuery({
    queryKey: ['health'],
    queryFn: checkHealth,
    refetchInterval: 30000, // Vérifier toutes les 30 secondes
    onError: () => {
      toast.error('Impossible de se connecter à l\'API')
    },
  })

  // Récupérer les modèles disponibles
  const { data: models } = useQuery({
    queryKey: ['models'],
    queryFn: getModels,
    enabled: !!health, // Seulement si l'API est accessible
  })

  const features = [
    {
      icon: Activity,
      title: 'Prédiction en Temps Réel',
      description: 'Obtenez des prédictions instantanées avec nos modèles ML avancés',
      color: 'from-cyan-500 to-blue-500',
    },
    {
      icon: BarChart3,
      title: 'Comparaison Multi-Modèles',
      description: 'Comparez les résultats de MLP, SVM et GRU-SVM avec consensus',
      color: 'from-blue-500 to-cyan-500',
    },
    {
      icon: Zap,
      title: 'Réentraînement Dynamique',
      description: 'Réentraînez vos modèles via l\'API avec de nouveaux hyperparamètres',
      color: 'from-yellow-500 to-orange-500',
    },
    {
      icon: Shield,
      title: 'Confiance et Fiabilité',
      description: 'Niveaux de confiance et probabilités détaillées pour chaque prédiction',
      color: 'from-green-500 to-emerald-500',
    },
  ]

  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.1,
      },
    },
  }

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.5,
      },
    },
  }

  return (
    <div className="container mx-auto px-4 py-12">
        {/* Hero Section */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        animate="visible"
        className="text-center mb-16"
      >
        <motion.div
          variants={itemVariants}
          className="inline-block mb-4"
        >
          <motion.div
            animate={{ 
              scale: [1, 1.1, 1],
              rotate: [0, 5, -5, 0]
            }}
            transition={{ 
              duration: 3,
              repeat: Infinity,
              repeatType: 'reverse'
            }}
            className="inline-block p-4 bg-gradient-to-br from-cyan-500 to-blue-600 rounded-2xl mb-6"
          >
            <Activity className="w-16 h-16 text-white" />
          </motion.div>
        </motion.div>

        <motion.h1
          variants={itemVariants}
          className="text-5xl md:text-7xl font-bold mb-6"
        >
          <span className="gradient-text">Détection du Cancer</span>
          <br />
          <span className="text-white">du Sein</span>
        </motion.h1>

        <motion.p
          variants={itemVariants}
          className="text-xl md:text-2xl text-white/70 mb-8 max-w-3xl mx-auto"
        >
          Application MLOps avancée utilisant l'apprentissage automatique pour 
          prédire la malignité des tumeurs avec une précision exceptionnelle
        </motion.p>

        {/* Status de l'API */}
        <motion.div
          variants={itemVariants}
          className="flex items-center justify-center space-x-4 mb-8"
        >
          <div className={`flex items-center space-x-2 px-4 py-2 rounded-full ${
            health?.status === 'healthy' 
              ? 'bg-green-500/20 text-green-400 border border-green-500/30'
              : 'bg-red-500/20 text-red-400 border border-red-500/30'
          }`}>
            <div className={`w-2 h-2 rounded-full ${
              health?.status === 'healthy' ? 'bg-green-400 animate-pulse' : 'bg-red-400'
            }`} />
            <span className="text-sm font-medium">
              {healthLoading ? 'Connexion...' : health?.status === 'healthy' ? 'API Connectée' : 'API Déconnectée'}
            </span>
          </div>
          
          {models && (
            <div className="flex items-center space-x-2 px-4 py-2 rounded-full bg-blue-500/20 text-blue-400 border border-blue-500/30">
              <TrendingUp className="w-4 h-4" />
              <span className="text-sm font-medium">
                {Object.keys(models.available_models || {}).length} Modèles Disponibles
              </span>
            </div>
          )}
        </motion.div>

        <motion.div
          variants={itemVariants}
          className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4"
        >
          <Link to="/predict">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary flex items-center space-x-2 text-lg px-8 py-4"
            >
              <span>Commencer une Prédiction</span>
              <ArrowRight className="w-5 h-5" />
            </motion.button>
          </Link>
          
          <Link to="/compare">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-secondary flex items-center space-x-2 text-lg px-8 py-4"
            >
              <BarChart3 className="w-5 h-5" />
              <span>Comparer les Modèles</span>
            </motion.button>
          </Link>
        </motion.div>
      </motion.div>

      {/* Features Grid */}
      <motion.div
        variants={containerVariants}
        initial="hidden"
        whileInView="visible"
        viewport={{ once: true }}
        className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-16"
      >
        {features.map((feature, index) => {
          const Icon = feature.icon
          return (
            <motion.div
              key={index}
              variants={itemVariants}
              whileHover={{ y: -10, scale: 1.02 }}
              className="card group cursor-pointer"
            >
              <div className={`w-12 h-12 rounded-xl bg-gradient-to-br ${feature.color} p-3 mb-4 group-hover:scale-110 transition-transform duration-300`}>
                <Icon className="w-full h-full text-white" />
              </div>
              <h3 className="text-xl font-bold mb-2 text-white">{feature.title}</h3>
              <p className="text-white/70">{feature.description}</p>
            </motion.div>
          )
        })}
      </motion.div>

      {/* Modèles Disponibles */}
      {models && models.available_models && (
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
          className="card max-w-4xl mx-auto"
        >
          <h2 className="text-2xl font-bold mb-6 gradient-text text-center">
            Modèles Disponibles
          </h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {models.available_models.map((model, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ scale: 1.05 }}
                className="glass rounded-xl p-4 text-center border border-white/20"
              >
                <div className="text-2xl font-bold gradient-text mb-2">{model}</div>
                <div className="text-sm text-white/60">
                  {models.models_info[model]?.loaded ? '✓ Chargé' : '✗ Non disponible'}
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  )
}

export default Home

