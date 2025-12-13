/**
 * Service API pour communiquer avec le backend FastAPI
 */

import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 30000, // 30 secondes
})

// Intercepteur pour les erreurs
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Erreur de réponse du serveur
      const message = error.response.data?.detail || error.message
      return Promise.reject(new Error(message))
    } else if (error.request) {
      // Requête envoyée mais pas de réponse
      return Promise.reject(new Error('Le serveur ne répond pas. Vérifiez que l\'API est démarrée.'))
    } else {
      // Erreur lors de la configuration de la requête
      return Promise.reject(error)
    }
  }
)

/**
 * Vérifie l'état de santé de l'API
 */
export const checkHealth = async () => {
  const response = await api.get('/health')
  return response.data
}

/**
 * Liste les modèles disponibles
 */
export const getModels = async () => {
  const response = await api.get('/models')
  return response.data
}

/**
 * Fait une prédiction avec un modèle spécifique
 * @param {string} modelName - Nom du modèle ('linear', 'softmax', 'mlp', 'svm', 'knn', 'gru_svm')
 * @param {number[]} features - Array de 30 features
 */
export const predict = async (modelName, features) => {
  const response = await api.post(`/predict?model_name=${modelName}`, {
    features,
  })
  return response.data
}

/**
 * Fait une prédiction avec tous les modèles et retourne un consensus
 * @param {number[]} features - Array de 30 features
 */
export const predictAll = async (features) => {
  const response = await api.post('/predict/all', {
    features,
  })
  return response.data
}

/**
 * Réentraîne un modèle
 * @param {string} modelType - Type de modèle ('linear', 'softmax', 'mlp', 'svm', 'knn', 'gru_svm', 'all')
 * @param {object} hyperparameters - Hyperparamètres optionnels
 */
export const retrain = async (modelType, hyperparameters = {}) => {
  const response = await api.post('/retrain', {
    model_type: modelType,
    hyperparameters,
  })
  return response.data
}

export default api

