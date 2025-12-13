# 🚀 API FastAPI - Détection du Cancer du Sein

API REST pour exposer les fonctions `predict()` et `retrain()` via FastAPI.

## 📋 Endpoints Disponibles

### `GET /`
Informations sur l'API et les endpoints disponibles.

### `GET /health`
Vérifie l'état de santé de l'API et des modèles chargés.

### `GET /models`
Liste les modèles disponibles et leurs informations.

### `POST /predict`
Fait une prédiction avec un modèle spécifique.

**Paramètres:**
- `model_name` (query): Nom du modèle (`mlp`, `svm`, `gru_svm`)

**Body:**
```json
{
  "features": [17.99, 10.38, 122.8, ...]  // 30 features
}
```

**Response:**
```json
{
  "model_name": "MLP",
  "prediction": 1,
  "probability": 0.95,
  "confidence": "Élevée",
  "timestamp": "2025-12-13T12:00:00"
}
```

### `POST /predict/all`
Fait une prédiction avec tous les modèles disponibles et calcule un consensus.

**Body:**
```json
{
  "features": [17.99, 10.38, 122.8, ...]  // 30 features
}
```

**Response:**
```json
{
  "predictions": {
    "MLP": {"prediction": 1, "probability": 0.95, "confidence": "Élevée"},
    "SVM": {"prediction": 1, "probability": 0.92, "confidence": "Élevée"},
    "GRU_SVM": {"prediction": 1, "probability": 0.94, "confidence": "Élevée"}
  },
  "consensus": {
    "prediction": 1,
    "probability": 0.9367,
    "confidence": "Élevée",
    "agreement": 100.0
  },
  "timestamp": "2025-12-13T12:00:00"
}
```

### `POST /retrain` ⭐ (Excellence)
Réentraîne un modèle avec les données disponibles.

**Body:**
```json
{
  "model_type": "mlp",  // "mlp", "svm", "gru_svm", ou "all"
  "hyperparameters": {  // Optionnel
    "C": 10,
    "kernel": "rbf"
  }
}
```

**Response:**
```json
{
  "model_name": "MLP",
  "status": "success",
  "accuracy": 0.9649,
  "training_time": 45.23,
  "message": "Modèle MLP réentraîné avec succès"
}
```

## 🚀 Démarrage

### Option 1: Avec Makefile (Recommandé)

```bash
# Démarrer l'API
make api

# Ou en mode production
make api-prod
```

### Option 2: Manuellement

```bash
# Activer l'environnement virtuel
.\venv\Scripts\Activate.ps1

# Installer les dépendances de l'API
pip install -r api/requirements.txt

# Démarrer l'API
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

## 📚 Documentation Interactive

Une fois l'API démarrée, accédez à:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🧪 Tests

### Test avec curl

```bash
# Test de santé
curl http://localhost:8000/health

# Test de prédiction
curl -X POST "http://localhost:8000/predict?model_name=mlp" \
  -H "Content-Type: application/json" \
  -d "{\"features\": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}"
```

### Test avec Python

```bash
python api/test_api.py
```

## 📝 Exemples d'Utilisation

### Python (requests)

```python
import requests

# Prédiction avec MLP
response = requests.post(
    "http://localhost:8000/predict?model_name=mlp",
    json={
        "features": [17.99, 10.38, 122.8, ...]  # 30 features
    }
)
result = response.json()
print(f"Prédiction: {result['prediction']}")
print(f"Probabilité: {result['probability']}")

# Prédiction avec tous les modèles
response = requests.post(
    "http://localhost:8000/predict/all",
    json={"features": [...]}
)
result = response.json()
print(f"Consensus: {result['consensus']}")

# Réentraîner un modèle
response = requests.post(
    "http://localhost:8000/retrain",
    json={
        "model_type": "mlp",
        "hyperparameters": {"learning_rate_init": 0.01}
    }
)
result = response.json()
print(f"Accuracy: {result['accuracy']}")
```

### JavaScript (fetch)

```javascript
// Prédiction
const response = await fetch('http://localhost:8000/predict?model_name=mlp', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    features: [17.99, 10.38, 122.8, ...]  // 30 features
  })
});

const result = await response.json();
console.log(`Prédiction: ${result.prediction}`);
console.log(`Probabilité: ${result.probability}`);
```

## 🔧 Configuration

L'API charge automatiquement les modèles depuis `models/` au démarrage.

Assurez-vous que les fichiers suivants existent:
- `models/scaler.pkl`
- `models/mlp_model.pkl`
- `models/svm_model.pkl`
- `models/gru_svm_model_*.pkl` (pour GRU-SVM)

## ⚠️ Notes Importantes

1. **Réentraînement**: L'endpoint `/retrain` peut prendre plusieurs minutes selon le modèle
2. **Données**: Le fichier `data.csv` doit être dans le dossier parent du projet
3. **TensorFlow**: GRU-SVM nécessite TensorFlow
4. **Production**: Utilisez `make api-prod` ou un serveur WSGI (Gunicorn) pour la production

## 🎯 Fonctionnalités d'Excellence

✅ **Endpoint `/retrain`**: Permet de réentraîner les modèles via l'API
✅ **Consensus**: Calcul automatique d'un consensus entre tous les modèles
✅ **Validation**: Validation automatique des données d'entrée avec Pydantic
✅ **Documentation**: Documentation interactive avec Swagger UI
✅ **Gestion d'erreurs**: Gestion complète des erreurs avec messages clairs
✅ **Logging**: Logging détaillé pour le débogage

