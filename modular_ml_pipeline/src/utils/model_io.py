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
    model_type = model_type.lower()
    
    # Pour gru_svm, le fichier de base n'existe pas, mais les fichiers composants existent
    # On vérifie l'existence seulement pour les autres types
    if model_type != 'gru_svm' and not filepath.exists():
        raise FileNotFoundError(f"Fichier {filepath} non trouvé")
    
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
        
        # Construire les chemins des fichiers
        base_dir = filepath.parent
        base_name = filepath.stem  # "gru_svm_model" si filepath = "gru_svm_model.pkl"
        
        # Charger les métadonnées
        metadata_path = base_dir / f"{base_name}_metadata.pkl"
        if metadata_path.exists():
            try:
                metadata = joblib.load(metadata_path)
                gru_path_str = metadata.get('gru_path', f"{base_name}_gru.h5")
                svm_path_str = metadata.get('svm_path', f"{base_name}_svm.pkl")
                
                # Les chemins dans metadata peuvent être relatifs au projet ou absolus
                gru_path = Path(gru_path_str)
                svm_path = Path(svm_path_str)
                
                # Si le chemin n'existe pas, essayer depuis base_dir
                if not gru_path.exists():
                    # Essayer comme chemin relatif depuis base_dir
                    gru_path_alt = base_dir / gru_path.name
                    if gru_path_alt.exists():
                        gru_path = gru_path_alt
                    else:
                        # Essayer avec le nom de base
                        gru_path = base_dir / f"{base_name}_gru.h5"
                
                if not svm_path.exists():
                    # Essayer comme chemin relatif depuis base_dir
                    svm_path_alt = base_dir / svm_path.name
                    if svm_path_alt.exists():
                        svm_path = svm_path_alt
                    else:
                        # Essayer avec le nom de base
                        svm_path = base_dir / f"{base_name}_svm.pkl"
                        
                logger.info(f"  Chemins résolus: GRU={gru_path}, SVM={svm_path}")
            except Exception as e:
                logger.warning(f"  ⚠ Erreur lors du chargement des métadonnées: {e}")
                gru_path = base_dir / f"{base_name}_gru.h5"
                svm_path = base_dir / f"{base_name}_svm.pkl"
        else:
            # Essayer les noms par défaut
            gru_path = base_dir / f"{base_name}_gru.h5"
            svm_path = base_dir / f"{base_name}_svm.pkl"
            logger.info(f"  Chemins par défaut: GRU={gru_path}, SVM={svm_path}")
        
        model = {}
        
        # Charger le GRU
        if not gru_path.exists():
            raise FileNotFoundError(f"Fichier GRU non trouvé: {gru_path}")
        if not TENSORFLOW_AVAILABLE:
            raise ImportError("TensorFlow n'est pas disponible pour charger le modèle GRU")
        
        try:
            model['gru_model'] = tf_load_model(str(gru_path))
            logger.info(f"  ✓ GRU chargé depuis {gru_path}")
            
            # Reconstruire le feature extractor
            # Note: layers[-4] car l'architecture est: GRU -> Dropout -> BatchNorm -> Dense(24) -> Dropout -> BatchNorm -> Dense(1)
            # On veut la sortie de Dense(24) qui est à l'index -4
            from tensorflow.keras.models import Model
            model_input = model['gru_model'].layers[0].input
            model['feature_extractor'] = Model(
                inputs=model_input,
                outputs=model['gru_model'].layers[-4].output  # Dense(24) layer - index ajusté pour la nouvelle architecture
            )
            logger.info(f"  ✓ Feature extractor créé")
        except Exception as e:
            logger.error(f"  ❌ Erreur lors du chargement du GRU: {e}")
            raise
        
        # Charger le SVM
        if not svm_path.exists():
            raise FileNotFoundError(f"Fichier SVM non trouvé: {svm_path}")
        
        try:
            model['svm_model'] = joblib.load(svm_path)
            logger.info(f"  ✓ SVM chargé depuis {svm_path}")
        except Exception as e:
            logger.error(f"  ❌ Erreur lors du chargement du SVM: {e}")
            raise
        
        # Vérifier que le modèle est complet
        if 'gru_model' in model and 'svm_model' in model and 'feature_extractor' in model:
            logger.info("✓ Modèle GRU-SVM chargé avec succès")
        else:
            missing = [k for k in ['gru_model', 'svm_model', 'feature_extractor'] if k not in model]
            raise ValueError(f"Modèle GRU-SVM incomplet. Composants manquants: {missing}")
        
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

