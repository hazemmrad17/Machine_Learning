# 🔬 Pipeline ML Modulaire - Détection du Cancer du Sein

Version modulaire du projet de détection du cancer du sein avec API FastAPI.

## 📁 Structure du Projet

```
modular_ml_pipeline/
├── src/
│   ├── data/
│   │   └── data_preparation.py    # prepare_data()
│   ├── models/
│   │   └── train_models.py        # train_model()
│   └── utils/
│       ├── evaluation.py          # evaluate_model()
│       └── model_io.py            # save_model(), load_model()
├── api/
│   ├── app.py                     # API FastAPI
│   ├── test_api.py                # Tests de l'API
│   └── requirements.txt           # Dépendances API
├── models/                        # Modèles sauvegardés
├── data/                          # Données
├── main.py                        # Script principal
├── Makefile                       # Automatisation
└── requirements.txt               # Dépendances principales
```

## 🚀 Démarrage Rapide

### 1. Créer et activer l'environnement virtuel

```powershell
# Créer le venv
python -m venv venv

# Activer (PowerShell)
.\venv\Scripts\Activate.ps1

# Si erreur d'exécution:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### 2. Installer les dépendances

```powershell
pip install -r requirements.txt
pip install -r api/requirements.txt
```

### 3. Exécuter le pipeline complet

```powershell
# Avec Makefile (recommandé)
make all

# Ou manuellement
python main.py
```

### 4. Démarrer l'API

```powershell
# Avec Makefile
make api

# Ou manuellement
python -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Makefile - Commandes Disponibles

```bash
make help          # Affiche l'aide
make venv          # Créer l'environnement virtuel
make install       # Installer les dépendances
make prepare       # Préparer les données
make train         # Entraîner les modèles
make evaluate      # Évaluer les modèles
make save          # Sauvegarder les modèles
make api           # Démarrer l'API (mode développement)
make api-prod      # Démarrer l'API (mode production)
make test-api      # Tester l'API
make all           # Exécuter tout le pipeline
make clean         # Nettoyer les fichiers temporaires
```

## 🔌 API FastAPI

### Endpoints Principaux

- **`GET /`**: Informations sur l'API
- **`GET /health`**: État de santé
- **`GET /models`**: Liste des modèles
- **`POST /predict`**: Prédiction avec un modèle spécifique
- **`POST /predict/all`**: Prédiction avec tous les modèles + consensus
- **`POST /retrain`**: Réentraîner un modèle ⭐

### Documentation Interactive

Une fois l'API démarrée:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### Exemple de Requête

```bash
curl -X POST "http://localhost:8000/predict?model_name=mlp" \
  -H "Content-Type: application/json" \
  -d '{
    "features": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]
  }'
```

## 📚 Documentation Complète

- **API**: Voir `api/README.md`
- **Pipeline**: Voir les docstrings dans chaque module
- **Exemples**: Voir `api/test_api.py`

## 🎯 Fonctionnalités

### Pipeline ML
✅ Préparation des données modulaire
✅ Entraînement de 6 types de modèles
✅ Évaluation complète avec métriques
✅ Sauvegarde/chargement des modèles

### API REST
✅ Prédiction avec modèles individuels
✅ Prédiction avec consensus de tous les modèles
✅ Réentraînement via API ⭐
✅ Documentation interactive
✅ Validation des données
✅ Gestion d'erreurs complète

## 📝 Notes

- **TensorFlow**: Requis pour GRU-SVM
- **Données**: Le fichier `data.csv` doit être dans le dossier parent
- **Production**: Utilisez `make api-prod` ou un serveur WSGI

## 🐛 Dépannage

Voir `api/README.md` pour les problèmes courants de l'API.

