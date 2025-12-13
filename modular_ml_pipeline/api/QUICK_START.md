# 🚀 Guide de Démarrage Rapide - API FastAPI

## Étape 1: Préparer les Modèles

Assurez-vous d'avoir entraîné et sauvegardé les modèles:

```bash
# Depuis le dossier modular_ml_pipeline
python main.py
```

Cela créera les fichiers dans `models/`:
- `scaler.pkl`
- `mlp_model.pkl`
- `svm_model.pkl`
- `gru_svm_model_*.pkl` (si TensorFlow disponible)

## Étape 2: Installer les Dépendances de l'API

```powershell
# Activer le venv
.\venv\Scripts\Activate.ps1

# Installer les dépendances
pip install -r api/requirements.txt
```

## Étape 3: Démarrer l'API

### Option A: Script Automatique (Recommandé)

**Windows PowerShell:**
```powershell
.\start_api.ps1
```

**Windows CMD:**
```cmd
start_api.bat
```

### Option B: Manuellement

```powershell
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

### Option C: Avec Makefile

```bash
make api
```

## Étape 4: Tester l'API

### Dans le navigateur
- **Documentation**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health

### Avec curl
```bash
curl http://localhost:8000/health
```

### Avec Python
```bash
python api/test_api.py
```

## 📝 Exemple de Prédiction

### Python
```python
import requests

response = requests.post(
    "http://localhost:8000/predict?model_name=mlp",
    json={
        "features": [
            17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
            1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
            25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
        ]
    }
)

result = response.json()
print(f"Prédiction: {'Malin' if result['prediction'] == 1 else 'Bénin'}")
print(f"Probabilité: {result['probability']:.4f}")
```

### curl
```bash
curl -X POST "http://localhost:8000/predict?model_name=mlp" \
  -H "Content-Type: application/json" \
  -d "{\"features\": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}"
```

## ⭐ Réentraîner un Modèle (Excellence)

```python
import requests

response = requests.post(
    "http://localhost:8000/retrain",
    json={
        "model_type": "mlp",
        "hyperparameters": {
            "learning_rate_init": 0.01
        }
    }
)

result = response.json()
print(f"Status: {result['status']}")
print(f"Accuracy: {result['accuracy']:.4f}")
```

## ❓ Problèmes Courants

### Erreur: "Modèles non chargés"
- Vérifiez que `python main.py` a été exécuté
- Vérifiez que les fichiers existent dans `models/`

### Erreur: "Port 8000 déjà utilisé"
- Changez le port: `--port 8001`
- Ou arrêtez l'autre processus utilisant le port

### Erreur: "Module non trouvé"
- Assurez-vous d'être dans le dossier `modular_ml_pipeline`
- Vérifiez que le venv est activé

