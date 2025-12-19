"""
Module d'entraînement des modèles de machine learning.
Contient la fonction train_model() pour entraîner différents modèles.
"""

import numpy as np
import logging
from typing import Dict, Any, Optional
from sklearn.linear_model import SGDRegressor
from sklearn.linear_model import SGDClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier

# Tentative d'import TensorFlow (optionnel)
try:
    from tensorflow.keras.models import Sequential, Model
    from tensorflow.keras.layers import GRU, Dense, Dropout, Input, BatchNormalization
    from tensorflow.keras.callbacks import EarlyStopping
    from tensorflow.keras.optimizers import Adam
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    logging.warning("TensorFlow non disponible - GRU-SVM ne peut pas être entraîné")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def train_linear_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    **kwargs
) -> SGDRegressor:
    """
    Entraîne un modèle de régression linéaire avec SGD.
    
    Args:
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        **kwargs: Hyperparamètres additionnels
        
    Returns:
        Modèle entraîné
    """
    logger.info("Entraînement du modèle: Régression Linéaire")
    
    model = SGDRegressor(
        loss='squared_error',
        learning_rate='constant',
        eta0=kwargs.get('eta0', 1e-3),
        max_iter=kwargs.get('max_iter', 3000),
        random_state=kwargs.get('random_state', 42)
    )
    
    model.fit(X_train, y_train)
    logger.info("✓ Modèle entraîné")
    
    return model


def train_softmax_regression(
    X_train: np.ndarray,
    y_train: np.ndarray,
    **kwargs
) -> SGDClassifier:
    """
    Entraîne un modèle de régression softmax (logistic regression) avec SGD.
    
    Args:
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        **kwargs: Hyperparamètres additionnels
        
    Returns:
        Modèle entraîné
    """
    logger.info("Entraînement du modèle: Régression Softmax")
    
    model = SGDClassifier(
        loss='log_loss',
        learning_rate='constant',
        eta0=kwargs.get('eta0', 1e-3),
        max_iter=kwargs.get('max_iter', 3000),
        random_state=kwargs.get('random_state', 42)
    )
    
    model.fit(X_train, y_train)
    logger.info("✓ Modèle entraîné")
    
    return model


def train_mlp(
    X_train: np.ndarray,
    y_train: np.ndarray,
    **kwargs
) -> MLPClassifier:
    """
    Entraîne un modèle MLP (Multi-Layer Perceptron).
    
    Args:
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        **kwargs: Hyperparamètres additionnels
        
    Returns:
        Modèle entraîné
    """
    logger.info("Entraînement du modèle: MLP")
    
    model = MLPClassifier(
        hidden_layer_sizes=kwargs.get('hidden_layer_sizes', (500, 500, 500)),
        learning_rate_init=kwargs.get('learning_rate_init', 1e-2),
        alpha=kwargs.get('alpha', 0.01),
        max_iter=kwargs.get('max_iter', 3000),
        early_stopping=kwargs.get('early_stopping', True),
        validation_fraction=kwargs.get('validation_fraction', 0.1),
        random_state=kwargs.get('random_state', 42),
        verbose=kwargs.get('verbose', 0)
    )
    
    model.fit(X_train, y_train)
    logger.info("✓ Modèle entraîné")
    
    return model


def train_svm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    **kwargs
) -> SVC:
    """
    Entraîne un modèle SVM (Support Vector Machine).
    
    Args:
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        **kwargs: Hyperparamètres additionnels
        
    Returns:
        Modèle entraîné
    """
    logger.info("Entraînement du modèle: SVM")
    
    model = SVC(
        C=kwargs.get('C', 5),
        kernel=kwargs.get('kernel', 'rbf'),
        gamma=kwargs.get('gamma', 'scale'),
        probability=kwargs.get('probability', True),
        random_state=kwargs.get('random_state', 42),
        max_iter=kwargs.get('max_iter', 3000)
    )
    
    model.fit(X_train, y_train)
    logger.info("✓ Modèle entraîné")
    
    return model


def train_knn(
    X_train: np.ndarray,
    y_train: np.ndarray,
    distance: str = 'l2',
    **kwargs
) -> KNeighborsClassifier:
    """
    Entraîne un modèle KNN (K-Nearest Neighbors).
    
    Args:
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        distance: Type de distance ('l1' ou 'l2')
        **kwargs: Hyperparamètres additionnels
        
    Returns:
        Modèle entraîné
    """
    logger.info(f"Entraînement du modèle: KNN (distance {distance.upper()})")
    
    p = 1 if distance.lower() == 'l1' else 2
    
    model = KNeighborsClassifier(
        n_neighbors=kwargs.get('n_neighbors', 1),
        weights='distance',  # Pondération par distance pour des probabilités plus lisses
        metric='minkowski',
        p=p
    )
    
    model.fit(X_train, y_train)
    logger.info("✓ Modèle entraîné")
    
    return model


def train_gru_svm(
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: np.ndarray,
    **kwargs
) -> Dict[str, Any]:
    """
    Entraîne un modèle hybride GRU-SVM.
    
    Args:
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        X_test: Features de test (pour extraction des features)
        **kwargs: Hyperparamètres additionnels
        
    Returns:
        Dictionnaire contenant:
        - 'gru_model': Modèle GRU
        - 'svm_model': Modèle SVM
        - 'feature_extractor': Modèle pour extraire les features
    """
    if not TENSORFLOW_AVAILABLE:
        raise ImportError("TensorFlow n'est pas disponible. Installez-le avec: pip install tensorflow")
    
    logger.info("Entraînement du modèle: GRU-SVM")
    
    # Convertir en arrays numpy si nécessaire (gérer les DataFrames pandas)
    if hasattr(X_train, 'values'):
        X_train = X_train.values
    if hasattr(X_test, 'values'):
        X_test = X_test.values
    if hasattr(y_train, 'values'):
        y_train = y_train.values
    
    # Convertir en arrays numpy si ce sont des listes ou autres types
    X_train = np.array(X_train)
    X_test = np.array(X_test)
    y_train = np.array(y_train)
    
    # Reshape pour GRU (30 features × 1)
    n_features = X_train.shape[1]
    X_train_gru = X_train.reshape(X_train.shape[0], n_features, 1)
    X_test_gru = X_test.reshape(X_test.shape[0], n_features, 1)
    
    # 1. Création et entraînement du GRU (architecture optimisée anti-overfitting)
    logger.info("  → Entraînement du GRU...")
    from tensorflow.keras.regularizers import l2
    
    gru_model = Sequential([
        Input(shape=(n_features, 1)),
        GRU(48, return_sequences=False, kernel_regularizer=l2(0.01), recurrent_regularizer=l2(0.01)),
        Dropout(0.5),
        BatchNormalization(),
        Dense(24, activation='relu', kernel_regularizer=l2(0.01)),
        Dropout(0.4),
        BatchNormalization(),
        Dense(1, activation='sigmoid')
    ])
    
    gru_model.compile(
        optimizer=Adam(learning_rate=kwargs.get('learning_rate', 5e-4)),
        loss='binary_crossentropy',
        metrics=['accuracy']
    )
    
    early_stopping = EarlyStopping(
        monitor='val_loss',
        patience=kwargs.get('patience', 20),
        restore_best_weights=True,
        min_delta=1e-4,
        verbose=kwargs.get('verbose', 1)
    )
    
    gru_model.fit(
        X_train_gru, y_train,
        epochs=kwargs.get('epochs', 300),
        batch_size=kwargs.get('batch_size', 64),
        validation_split=kwargs.get('validation_split', 0.2),
        verbose=kwargs.get('verbose', 1),
        callbacks=[early_stopping]
    )
    
    # 2. Extraction des features
    logger.info("  → Extraction des features...")
    model_input = gru_model.layers[0].input
    feature_extractor = Model(
        inputs=model_input,
        outputs=gru_model.layers[-4].output  # Dense(24) - index ajusté pour la nouvelle architecture
    )
    
    gru_train_features = feature_extractor.predict(X_train_gru, verbose=0)
    gru_test_features = feature_extractor.predict(X_test_gru, verbose=0)
    
    # 3. Entraînement du SVM
    logger.info("  → Entraînement du SVM sur les features extraites...")
    svm_model = SVC(
        kernel='rbf',
        C=kwargs.get('svm_C', 5),
        gamma='scale',  # Régularisation pour éviter l'overfitting
        probability=True,
        random_state=kwargs.get('random_state', 42)
    )
    svm_model.fit(gru_train_features, y_train)
    
    logger.info("✓ Modèle GRU-SVM entraîné")
    
    return {
        'gru_model': gru_model,
        'svm_model': svm_model,
        'feature_extractor': feature_extractor,
        'gru_train_features': gru_train_features,
        'gru_test_features': gru_test_features
    }


def train_model(
    model_type: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_test: Optional[np.ndarray] = None,
    **kwargs
) -> Any:
    """
    Fonction principale pour entraîner un modèle.
    
    Args:
        model_type: Type de modèle ('linear', 'softmax', 'mlp', 'svm', 'knn', 'gru_svm')
        X_train: Features d'entraînement
        y_train: Labels d'entraînement
        X_test: Features de test (requis pour GRU-SVM)
        **kwargs: Hyperparamètres spécifiques au modèle
        
    Returns:
        Modèle entraîné (ou dictionnaire pour GRU-SVM)
    """
    logger.info("=" * 60)
    logger.info(f"ENTRAÎNEMENT DU MODÈLE: {model_type.upper()}")
    logger.info("=" * 60)
    
    model_type = model_type.lower()
    
    if model_type == 'linear':
        return train_linear_regression(X_train, y_train, **kwargs)
    elif model_type == 'softmax':
        return train_softmax_regression(X_train, y_train, **kwargs)
    elif model_type == 'mlp':
        return train_mlp(X_train, y_train, **kwargs)
    elif model_type == 'svm':
        return train_svm(X_train, y_train, **kwargs)
    elif model_type == 'knn':
        distance = kwargs.pop('distance', 'l2')
        return train_knn(X_train, y_train, distance=distance, **kwargs)
    elif model_type == 'gru_svm':
        if X_test is None:
            raise ValueError("X_test est requis pour GRU-SVM")
        return train_gru_svm(X_train, y_train, X_test, **kwargs)
    else:
        raise ValueError(
            f"Type de modèle inconnu: {model_type}. "
            f"Options: 'linear', 'softmax', 'mlp', 'svm', 'knn', 'gru_svm'"
        )


if __name__ == "__main__":
    # Test du module
    from ..data.data_preparation import prepare_data
    
    data = prepare_data()
    model = train_model('mlp', data['X_train_scaled'], data['y_train'])
    print(f"\nModèle entraîné: {type(model).__name__}")

