"""
Module pour sauvegarder et charger les modèles.
Contient les fonctions save_model() et load_model().
"""

import joblib
import pickle
from pathlib import Path
from typing import Any, Optional, Dict
import logging

# Tentative d'import TensorFlow (optionnel)
try:
    from tensorflow.keras.models import load_model as tf_load_model, save_model as tf_save_model
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def save_model(
    model: Any,
    filepath: str,
    model_type: str = 'standard',
    additional_data: Optional[Dict] = None
) -> None:
    """
    Sauvegarde un modèle entraîné sur le disque.
    
    Args:
        model: Modèle à sauvegarder
        filepath: Chemin où sauvegarder le modèle
        model_type: Type de modèle ('standard', 'gru_svm', 'gru')
        additional_data: Données additionnelles à sauvegarder (optionnel)
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    model_type = model_type.lower()
    
    if model_type == 'gru':
        # Modèle TensorFlow/Keras
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow n'est pas disponible pour sauvegarder le modèle GRU")
        
        logger.info(f"Sauvegarde du modèle GRU dans {filepath}")
        tf_save_model(model, str(filepath))
        logger.info("✓ Modèle GRU sauvegardé")
        
    elif model_type == 'gru_svm':
        # Modèle hybride: sauvegarder GRU et SVM séparément
        if not isinstance(model, dict):
            raise ValueError("GRU-SVM doit être un dictionnaire avec 'gru_model' et 'svm_model'")
        
        logger.info(f"Sauvegarde du modèle GRU-SVM...")
        
        # Sauvegarder le GRU
        gru_path = filepath.parent / f"{filepath.stem}_gru.h5"
        if TENSORFLOW_AVAILABLE and 'gru_model' in model:
            tf_save_model(model['gru_model'], str(gru_path))
            logger.info(f"  ✓ GRU sauvegardé dans {gru_path}")
        
        # Sauvegarder le SVM
        svm_path = filepath.parent / f"{filepath.stem}_svm.pkl"
        if 'svm_model' in model:
            joblib.dump(model['svm_model'], svm_path)
            logger.info(f"  ✓ SVM sauvegardé dans {svm_path}")
        
        # Sauvegarder les métadonnées
        metadata = {
            'model_type': 'gru_svm',
            'gru_path': str(gru_path),
            'svm_path': str(svm_path)
        }
        if additional_data:
            metadata.update(additional_data)
        
        metadata_path = filepath.parent / f"{filepath.stem}_metadata.pkl"
        joblib.dump(metadata, metadata_path)
        logger.info(f"  ✓ Métadonnées sauvegardées dans {metadata_path}")
        
    else:
        # Modèles standards (scikit-learn)
        logger.info(f"Sauvegarde du modèle dans {filepath}")
        joblib.dump(model, filepath)
        logger.info("✓ Modèle sauvegardé")


def load_model(
    filepath: str,
    model_type: str = 'standard'
) -> Any:
    """
    Charge un modèle sauvegardé depuis le disque.
    
    Args:
        filepath: Chemin vers le fichier du modèle
        model_type: Type de modèle ('standard', 'gru_svm', 'gru')
        
    Returns:
        Modèle chargé
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Fichier {filepath} non trouvé")
    
    model_type = model_type.lower()
    
    if model_type == 'gru':
        # Modèle TensorFlow/Keras
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow n'est pas disponible pour charger le modèle GRU")
        
        logger.info(f"Chargement du modèle GRU depuis {filepath}")
        model = tf_load_model(str(filepath))
        logger.info("✓ Modèle GRU chargé")
        return model
        
    elif model_type == 'gru_svm':
        # Modèle hybride: charger GRU et SVM séparément
        logger.info(f"Chargement du modèle GRU-SVM...")
        
        # Charger les métadonnées
        metadata_path = filepath.parent / f"{filepath.stem}_metadata.pkl"
        if metadata_path.exists():
            metadata = joblib.load(metadata_path)
            gru_path = Path(metadata['gru_path'])
            svm_path = Path(metadata['svm_path'])
        else:
            # Essayer les noms par défaut
            gru_path = filepath.parent / f"{filepath.stem}_gru.h5"
            svm_path = filepath.parent / f"{filepath.stem}_svm.pkl"
        
        model = {}
        
        # Charger le GRU
        if gru_path.exists() and TENSORFLOW_AVAILABLE:
            model['gru_model'] = tf_load_model(str(gru_path))
            logger.info(f"  ✓ GRU chargé depuis {gru_path}")
            
            # Reconstruire le feature extractor
            from tensorflow.keras.models import Model
            model_input = model['gru_model'].layers[0].input
            model['feature_extractor'] = Model(
                inputs=model_input,
                outputs=model['gru_model'].layers[-3].output
            )
        else:
            logger.warning(f"  ⚠ GRU non trouvé ou TensorFlow non disponible")
        
        # Charger le SVM
        if svm_path.exists():
            model['svm_model'] = joblib.load(svm_path)
            logger.info(f"  ✓ SVM chargé depuis {svm_path}")
        else:
            logger.warning(f"  ⚠ SVM non trouvé")
        
        logger.info("✓ Modèle GRU-SVM chargé")
        return model
        
    else:
        # Modèles standards (scikit-learn)
        logger.info(f"Chargement du modèle depuis {filepath}")
        model = joblib.load(filepath)
        logger.info("✓ Modèle chargé")
        return model


def save_scaler(scaler: Any, filepath: str) -> None:
    """
    Sauvegarde un scaler (StandardScaler, etc.).
    
    Args:
        scaler: Scaler à sauvegarder
        filepath: Chemin où sauvegarder
    """
    filepath = Path(filepath)
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    logger.info(f"Sauvegarde du scaler dans {filepath}")
    joblib.dump(scaler, filepath)
    logger.info("✓ Scaler sauvegardé")


def load_scaler(filepath: str) -> Any:
    """
    Charge un scaler sauvegardé.
    
    Args:
        filepath: Chemin vers le fichier du scaler
        
    Returns:
        Scaler chargé
    """
    filepath = Path(filepath)
    
    if not filepath.exists():
        raise FileNotFoundError(f"Fichier {filepath} non trouvé")
    
    logger.info(f"Chargement du scaler depuis {filepath}")
    scaler = joblib.load(filepath)
    logger.info("✓ Scaler chargé")
    return scaler


if __name__ == "__main__":
    # Test du module
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    
    # Test avec un modèle simple
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    test_path = Path(__file__).parent.parent.parent / "models" / "test_model.pkl"
    
    save_model(model, test_path)
    loaded_model = load_model(test_path)
    print(f"\nModèle sauvegardé et chargé: {type(loaded_model).__name__}")
    
    # Nettoyer
    test_path.unlink()

