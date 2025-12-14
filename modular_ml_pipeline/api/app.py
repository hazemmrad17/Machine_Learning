"""
API FastAPI pour exposer les fonctions predict() et retrain().
Service REST pour la prédiction du cancer du sein.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import numpy as np
import pandas as pd
from pathlib import Path
import sys
import logging
from datetime import datetime

# Ajouter le dossier parent au path pour importer les modules
parent_dir = Path(__file__).parent.parent
sys.path.insert(0, str(parent_dir))

from src.utils.model_io import load_model, save_model, load_scaler, save_scaler
from src.models.train_models import train_model
from src.data.data_preparation import prepare_data
from src.utils.evaluation import evaluate_model

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialisation de l'application FastAPI
app = FastAPI(
    title="Breast Cancer Detection API",
    description="API REST pour la prédiction du cancer du sein avec MLP, SVM et GRU-SVM",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En production, spécifiez les origines autorisées
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Chemins vers les modèles
BASE_DIR = Path(__file__).parent.parent
MODELS_DIR = BASE_DIR / "models"
DATA_PATH = BASE_DIR.parent / "data.csv"  # Chemin vers data.csv dans le dossier parent

# Variables globales pour les modèles et le scaler
models_cache: Dict[str, Any] = {}
scaler_cache = None


# ============================================================================
# MODÈLES PYDANTIC POUR VALIDATION DES DONNÉES
# ============================================================================

class FeaturesInput(BaseModel):
    """Modèle pour les features d'entrée (30 features)."""
    features: List[float] = Field(
        ...,
        description="Liste de 30 features numériques",
        min_length=30,
        max_length=30,
        example=[
            17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
            1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
            25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
        ]
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "features": [
                    17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
                    1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
                    25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
                ]
            }
        }


class PredictionResponse(BaseModel):
    """Modèle pour la réponse de prédiction."""
    model_name: str
    prediction: int = Field(..., description="0 = Bénin, 1 = Malin")
    probability: float = Field(..., description="Probabilité que la tumeur soit maligne (0-1)")
    confidence: str = Field(..., description="Niveau de confiance: Élevée, Moyenne, Faible")
    timestamp: str = Field(..., description="Horodatage de la prédiction")


class RetrainRequest(BaseModel):
    """Modèle pour la requête de réentraînement."""
    model_type: str = Field(
        ...,
        description="Type de modèle à réentraîner: 'mlp', 'svm', 'gru_svm', ou 'all'",
        example="mlp"
    )
    hyperparameters: Optional[Dict[str, Any]] = Field(
        None,
        description="Hyperparamètres personnalisés (optionnel)",
        example={"C": 10, "kernel": "rbf"}
    )


class RetrainResponse(BaseModel):
    """Modèle pour la réponse de réentraînement."""
    model_name: str
    status: str
    accuracy: Optional[float] = None
    training_time: Optional[float] = None
    message: str


# ============================================================================
# FONCTIONS UTILITAIRES
# ============================================================================

def load_models_from_disk():
    """Charge tous les modèles depuis le disque."""
    global models_cache, scaler_cache
    
    try:
        # Charger le scaler
        scaler_path = MODELS_DIR / "scaler.pkl"
        if scaler_path.exists():
            scaler_cache = load_scaler(str(scaler_path))
            logger.info("✓ Scaler chargé")
        else:
            logger.warning("⚠ Scaler non trouvé")
        
        # Charger Linear Regression
        linear_path = MODELS_DIR / "linear_model.pkl"
        if linear_path.exists():
            models_cache['linear'] = load_model(str(linear_path), model_type='standard')
            logger.info("✓ Modèle Linear Regression chargé")
        
        # Charger Softmax Regression
        softmax_path = MODELS_DIR / "softmax_model.pkl"
        if softmax_path.exists():
            models_cache['softmax'] = load_model(str(softmax_path), model_type='standard')
            logger.info("✓ Modèle Softmax Regression chargé")
        
        # Charger MLP
        mlp_path = MODELS_DIR / "mlp_model.pkl"
        if mlp_path.exists():
            models_cache['mlp'] = load_model(str(mlp_path), model_type='standard')
            logger.info("✓ Modèle MLP chargé")
        
        # Charger SVM
        svm_path = MODELS_DIR / "svm_model.pkl"
        if svm_path.exists():
            models_cache['svm'] = load_model(str(svm_path), model_type='standard')
            logger.info("✓ Modèle SVM chargé")
        
        # Charger KNN-L1
        knn_l1_path = MODELS_DIR / "knn_l1_model.pkl"
        if knn_l1_path.exists():
            models_cache['knn_l1'] = load_model(str(knn_l1_path), model_type='standard')
            logger.info("✓ Modèle KNN-L1 chargé")
        
        # Charger KNN-L2
        knn_l2_path = MODELS_DIR / "knn_l2_model.pkl"
        if knn_l2_path.exists():
            models_cache['knn_l2'] = load_model(str(knn_l2_path), model_type='standard')
            logger.info("✓ Modèle KNN-L2 chargé")
        
        # Fallback: Charger KNN (ancien format)
        knn_path = MODELS_DIR / "knn_model.pkl"
        if knn_path.exists() and 'knn_l1' not in models_cache and 'knn_l2' not in models_cache:
            models_cache['knn'] = load_model(str(knn_path), model_type='standard')
            logger.info("✓ Modèle KNN (ancien format) chargé")
        
        # Charger GRU-SVM
        gru_svm_path = MODELS_DIR / "gru_svm_model.pkl"
        if gru_svm_path.exists():
            try:
                models_cache['gru_svm'] = load_model(str(gru_svm_path), model_type='gru_svm')
                logger.info("✓ Modèle GRU-SVM chargé")
            except Exception as e:
                logger.warning(f"⚠ Erreur lors du chargement de GRU-SVM: {e}")
        
    except Exception as e:
        logger.error(f"❌ Erreur lors du chargement des modèles: {e}")


def get_confidence(probability: float) -> str:
    """Détermine le niveau de confiance basé sur la probabilité."""
    if probability < 0.3 or probability > 0.7:
        return "Élevée"
    elif probability < 0.4 or probability > 0.6:
        return "Moyenne"
    else:
        return "Faible"


def predict_with_model(model: Any, model_type: str, features_scaled: np.ndarray) -> tuple:
    """
    Fait une prédiction avec un modèle.
    
    Returns:
        Tuple (prediction, probability)
    """
    if model_type == 'linear':
        # Régression linéaire
        y_continuous = model.predict(features_scaled)[0]
        prediction = int(y_continuous >= 0.5)
        
        # Probabilité avec sigmoid pour une meilleure calibration
        import math
        probability = 1 / (1 + math.exp(-y_continuous))
        
        return prediction, probability
    
    elif model_type == 'gru_svm':
        # GRU-SVM
        if isinstance(model, dict):
            feature_extractor = model['feature_extractor']
            svm_model = model['svm_model']
            
            n_features = features_scaled.shape[1]
            features_gru = features_scaled.reshape(1, n_features, 1)
            
            gru_features = feature_extractor.predict(features_gru, verbose=0)
            gru_features_reshaped = gru_features.reshape(1, -1)
            
            prediction = svm_model.predict(gru_features_reshaped)[0]
            probability = svm_model.predict_proba(gru_features_reshaped)[0][1]
            
            return int(prediction), float(probability)
        else:
            raise ValueError("GRU-SVM doit être un dictionnaire")
    
    elif model_type in ['knn_l1', 'knn_l2']:
        # KNN models (L1 or L2)
        prediction = model.predict(features_scaled)[0]
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(features_scaled)[0][1]
        else:
            probability = 0.5
        return int(prediction), float(probability)
    
    else:
        # Modèles standards (softmax, mlp, svm)
        prediction = model.predict(features_scaled)[0]
        
        if hasattr(model, 'predict_proba'):
            probability = model.predict_proba(features_scaled)[0][1]
        else:
            probability = 0.5  # Valeur par défaut
        
        return int(prediction), float(probability)


# ============================================================================
# ROUTES API
# ============================================================================

@app.on_event("startup")
async def startup_event():
    """Événement au démarrage: charge les modèles."""
    logger.info("=" * 60)
    logger.info("DÉMARRAGE DE L'API")
    logger.info("=" * 60)
    load_models_from_disk()
    logger.info("=" * 60)


@app.get("/")
async def root():
    """Endpoint racine avec informations sur l'API."""
    return {
        "message": "Breast Cancer Detection API",
        "version": "1.0.0",
        "available_models": list(models_cache.keys()),
        "scaler_loaded": scaler_cache is not None,
        "endpoints": {
            "/predict": "POST - Prédiction avec un modèle spécifique",
            "/predict/all": "POST - Prédiction avec tous les modèles",
            "/retrain": "POST - Réentraîner un modèle",
            "/health": "GET - Statut de santé de l'API",
            "/models": "GET - Liste des modèles disponibles",
            "/docs": "GET - Documentation interactive (Swagger UI)"
        }
    }


@app.get("/health")
async def health_check():
    """Vérifie l'état de santé de l'API et des modèles."""
    return {
        "status": "healthy" if scaler_cache is not None else "degraded",
        "scaler_loaded": scaler_cache is not None,
        "models_loaded": {
            model: model in models_cache 
            for model in ['linear', 'softmax', 'mlp', 'svm', 'knn_l1', 'knn_l2', 'gru_svm']
        },
        "timestamp": datetime.now().isoformat()
    }


@app.get("/models")
async def list_models():
    """Liste les modèles disponibles."""
    return {
        "available_models": list(models_cache.keys()),
        "models_info": {
            model_name: {
                "loaded": True,
                "type": type(model).__name__ if not isinstance(model, dict) else "GRU-SVM"
            }
            for model_name, model in models_cache.items()
        }
    }


@app.post("/predict", response_model=PredictionResponse)
async def predict(
    input_data: FeaturesInput,
    model_name: str = "mlp"
):
    """
    Fait une prédiction avec un modèle spécifique.
    
    Args:
        input_data: Features de la tumeur (30 valeurs)
        model_name: Nom du modèle ('linear', 'softmax', 'mlp', 'svm', 'knn', 'gru_svm')
    
    Returns:
        Prédiction avec probabilité et niveau de confiance
    """
    if scaler_cache is None:
        raise HTTPException(status_code=503, detail="Scaler non chargé")
    
    if model_name.lower() not in models_cache:
        raise HTTPException(
            status_code=404,
            detail=f"Modèle '{model_name}' non disponible. Modèles disponibles: {list(models_cache.keys())}"
        )
    
    try:
        # Préprocessing
        features_array = np.array(input_data.features).reshape(1, -1)
        features_scaled = scaler_cache.transform(features_array)
        
        # Prédiction
        model = models_cache[model_name.lower()]
        prediction, probability = predict_with_model(model, model_name.lower(), features_scaled)
        
        return PredictionResponse(
            model_name=model_name.upper(),
            prediction=prediction,
            probability=probability,
            confidence=get_confidence(probability),
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.post("/predict/all")
async def predict_all(input_data: FeaturesInput):
    """
    Fait une prédiction avec tous les modèles disponibles et calcule un consensus.
    
    Args:
        input_data: Features de la tumeur (30 valeurs)
    
    Returns:
        Prédictions de tous les modèles + consensus
    """
    if scaler_cache is None:
        raise HTTPException(status_code=503, detail="Scaler non chargé")
    
    if not models_cache:
        raise HTTPException(status_code=503, detail="Aucun modèle chargé")
    
    try:
        # Préprocessing
        features_array = np.array(input_data.features).reshape(1, -1)
        features_scaled = scaler_cache.transform(features_array)
        
        # Prédictions avec tous les modèles
        predictions = {}
        
        for model_name, model in models_cache.items():
            try:
                prediction, probability = predict_with_model(model, model_name, features_scaled)
                predictions[model_name.upper()] = {
                    "prediction": prediction,
                    "probability": probability,
                    "confidence": get_confidence(probability)
                }
            except Exception as e:
                logger.warning(f"Erreur avec le modèle {model_name}: {e}")
                predictions[model_name.upper()] = {"error": str(e)}
        
        # Calcul du consensus
        valid_predictions = [
            p for p in predictions.values()
            if "error" not in p
        ]
        
        if valid_predictions:
            consensus_pred = int(
                sum(p["prediction"] for p in valid_predictions) > len(valid_predictions) / 2
            )
            avg_prob = sum(p["probability"] for p in valid_predictions) / len(valid_predictions)
            agreement = sum(
                1 for p in valid_predictions if p["prediction"] == consensus_pred
            ) / len(valid_predictions)
        else:
            consensus_pred = None
            avg_prob = None
            agreement = 0.0
        
        return {
            "predictions": predictions,
            "consensus": {
                "prediction": consensus_pred,
                "probability": round(avg_prob, 4) if avg_prob else None,
                "confidence": get_confidence(avg_prob) if avg_prob else "N/A",
                "agreement": round(agreement * 100, 1)  # Pourcentage
            },
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur de prédiction: {str(e)}")


@app.post("/retrain", response_model=RetrainResponse)
async def retrain(request: RetrainRequest):
    """
    Réentraîne un modèle avec les données disponibles.
    
    Args:
        request: Requête contenant le type de modèle et les hyperparamètres
    
    Returns:
        Statut du réentraînement avec métriques
    """
    import time
    
    model_type = request.model_type.lower()
    
    valid_models = ['linear', 'softmax', 'mlp', 'svm', 'knn', 'knn_l1', 'knn_l2', 'gru_svm', 'all']
    if model_type not in valid_models:
        raise HTTPException(
            status_code=400,
            detail=f"Type de modèle invalide: {model_type}. Options: {', '.join(valid_models)}"
        )
    
    if not DATA_PATH.exists():
        raise HTTPException(
            status_code=404,
            detail=f"Fichier de données non trouvé: {DATA_PATH}"
        )
    
    try:
        start_time = time.time()
        
        # Préparer les données
        logger.info(f"Préparation des données pour réentraînement de {model_type}...")
        data = prepare_data(data_path=str(DATA_PATH))
        
        # Sauvegarder le nouveau scaler
        save_scaler(data['scaler'], MODELS_DIR / "scaler.pkl")
        
        # Hyperparamètres
        hyperparams = request.hyperparameters or {}
        
        # Réentraîner le(s) modèle(s)
        if model_type == 'all':
            models_to_retrain = ['linear', 'softmax', 'mlp', 'svm', 'knn_l1', 'knn_l2']
            if 'gru_svm' in models_cache:
                models_to_retrain.append('gru_svm')
        elif model_type == 'knn':
            # Si 'knn' est demandé, entraîner les deux versions
            models_to_retrain = ['knn_l1', 'knn_l2']
        else:
            models_to_retrain = [model_type]
        
        results = []
        
        for model_name in models_to_retrain:
            logger.info(f"Réentraînement du modèle {model_name}...")
            
            try:
                if model_name == 'gru_svm':
                    model = train_model(
                        model_type=model_name,
                        X_train=data['X_train_scaled'],
                        y_train=data['y_train'],
                        X_test=data['X_test_scaled'],
                        **hyperparams
                    )
                elif model_name in ['knn_l1', 'knn_l2']:
                    # Extract distance from model name
                    distance = 'l1' if model_name == 'knn_l1' else 'l2'
                    model = train_model(
                        model_type='knn',
                        X_train=data['X_train_scaled'],
                        y_train=data['y_train'],
                        distance=distance,
                        **hyperparams
                    )
                else:
                    model = train_model(
                        model_type=model_name,
                        X_train=data['X_train_scaled'],
                        y_train=data['y_train'],
                        **hyperparams
                    )
                
                # Évaluer le modèle
                eval_result = evaluate_model(
                    model=model if not isinstance(model, dict) else model['svm_model'],
                    X_test=data['X_test_scaled'],
                    y_test=data['y_test'],
                    model_type=model_name,
                    model_name=model_name.upper()
                )
                
                accuracy = eval_result['metrics']['accuracy']
                
                # Sauvegarder le modèle
                model_path = MODELS_DIR / f"{model_name}_model.pkl"
                if model_name == 'gru_svm':
                    save_model(model, str(model_path), model_type='gru_svm')
                else:
                    save_model(model, str(model_path), model_type='standard')
                
                # Mettre à jour le cache
                models_cache[model_name] = model
                
                results.append({
                    "model_name": model_name.upper(),
                    "status": "success",
                    "accuracy": accuracy,
                    "message": f"Modèle {model_name.upper()} réentraîné avec succès"
                })
                
            except Exception as e:
                logger.error(f"Erreur lors du réentraînement de {model_name}: {e}")
                results.append({
                    "model_name": model_name.upper(),
                    "status": "error",
                    "accuracy": None,
                    "message": f"Erreur: {str(e)}"
                })
        
        training_time = time.time() - start_time
        
        # Retourner le résultat
        if len(results) == 1:
            result = results[0]
            return RetrainResponse(
                model_name=result["model_name"],
                status=result["status"],
                accuracy=result["accuracy"],
                training_time=round(training_time, 2),
                message=result["message"]
            )
        else:
            # Plusieurs modèles
            return RetrainResponse(
                model_name="ALL",
                status="success",
                accuracy=sum(r["accuracy"] for r in results if r["accuracy"]) / len([r for r in results if r["accuracy"]]),
                training_time=round(training_time, 2),
                message=f"{len([r for r in results if r['status'] == 'success'])}/{len(results)} modèles réentraînés avec succès"
            )
    
    except Exception as e:
        logger.error(f"Erreur lors du réentraînement: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Erreur de réentraînement: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

