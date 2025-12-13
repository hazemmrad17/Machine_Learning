"""
Module d'évaluation des modèles.
Contient la fonction evaluate_model() pour calculer les métriques de performance.
"""

import numpy as np
import pandas as pd
from typing import Dict, Any, Optional
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    confusion_matrix,
    roc_curve
)
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def calculate_metrics(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    y_proba: Optional[np.ndarray] = None
) -> Dict[str, float]:
    """
    Calcule les métriques de performance d'un modèle.
    
    Args:
        y_true: Labels réels
        y_pred: Labels prédits
        y_proba: Probabilités prédites (optionnel, pour ROC-AUC)
        
    Returns:
        Dictionnaire contenant les métriques
    """
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, zero_division=0),
        'recall': recall_score(y_true, y_pred, zero_division=0),
        'f1_score': f1_score(y_true, y_pred, zero_division=0)
    }
    
    # ROC-AUC nécessite les probabilités
    if y_proba is not None:
        try:
            metrics['roc_auc'] = roc_auc_score(y_true, y_proba)
        except ValueError as e:
            logger.warning(f"Impossible de calculer ROC-AUC: {e}")
            metrics['roc_auc'] = None
    else:
        metrics['roc_auc'] = None
    
    # Matrice de confusion
    cm = confusion_matrix(y_true, y_pred)
    tn, fp, fn, tp = cm.ravel()
    
    metrics['confusion_matrix'] = {
        'tn': int(tn),
        'fp': int(fp),
        'fn': int(fn),
        'tp': int(tp)
    }
    
    # Métriques supplémentaires
    metrics['specificity'] = tn / (tn + fp) if (tn + fp) > 0 else 0.0
    metrics['sensitivity'] = tp / (tp + fn) if (tp + fn) > 0 else 0.0  # = recall
    metrics['fpr'] = fp / (fp + tn) if (fp + tn) > 0 else 0.0  # False Positive Rate
    metrics['fnr'] = fn / (fn + tp) if (fn + tp) > 0 else 0.0  # False Negative Rate
    
    return metrics


def get_predictions(
    model: Any,
    X_test: np.ndarray,
    model_type: str = 'standard'
) -> tuple:
    """
    Obtient les prédictions et probabilités d'un modèle.
    
    Args:
        model: Modèle entraîné
        X_test: Features de test
        model_type: Type de modèle ('standard', 'linear', 'gru_svm')
        
    Returns:
        Tuple (y_pred, y_proba)
    """
    model_type = model_type.lower()
    
    if model_type == 'linear':
        # Régression linéaire: valeurs continues, besoin de seuillage
        y_continuous = model.predict(X_test)
        y_pred = (y_continuous >= 0.5).astype(int)
        
        # Normaliser pour obtenir des probabilités [0, 1]
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        y_proba = scaler.fit_transform(y_continuous.reshape(-1, 1)).flatten()
        
        return y_pred, y_proba
    
    elif model_type == 'gru_svm':
        # GRU-SVM: modèle hybride
        if isinstance(model, dict):
            feature_extractor = model['feature_extractor']
            svm_model = model['svm_model']
            
            # Reshape pour GRU
            n_features = X_test.shape[1]
            X_test_gru = X_test.reshape(X_test.shape[0], n_features, 1)
            
            # Extraire les features
            gru_features = feature_extractor.predict(X_test_gru, verbose=0)
            
            # Prédire avec SVM
            y_pred = svm_model.predict(gru_features)
            y_proba = svm_model.predict_proba(gru_features)[:, 1]
            
            return y_pred, y_proba
        else:
            raise ValueError("GRU-SVM doit être un dictionnaire avec 'feature_extractor' et 'svm_model'")
    
    else:
        # Modèles standards (softmax, MLP, SVM, KNN)
        y_pred = model.predict(X_test)
        
        if hasattr(model, 'predict_proba'):
            y_proba = model.predict_proba(X_test)[:, 1]
        else:
            logger.warning("Le modèle n'a pas de méthode predict_proba, probabilités = None")
            y_proba = None
        
        return y_pred, y_proba


def evaluate_model(
    model: Any,
    X_test: np.ndarray,
    y_test: np.ndarray,
    model_type: str = 'standard',
    model_name: str = 'Model'
) -> Dict[str, Any]:
    """
    Fonction principale pour évaluer un modèle.
    
    Args:
        model: Modèle entraîné
        X_test: Features de test
        y_test: Labels de test
        model_type: Type de modèle ('standard', 'linear', 'softmax', 'mlp', 'svm', 'knn', 'gru_svm')
        model_name: Nom du modèle (pour l'affichage)
        
    Returns:
        Dictionnaire contenant toutes les métriques et informations
    """
    logger.info("=" * 60)
    logger.info(f"ÉVALUATION DU MODÈLE: {model_name}")
    logger.info("=" * 60)
    
    # Obtenir les prédictions
    y_pred, y_proba = get_predictions(model, X_test, model_type)
    
    # Calculer les métriques
    metrics = calculate_metrics(y_test, y_pred, y_proba)
    
    # Afficher les résultats
    logger.info(f"\n📊 Résultats pour {model_name}:")
    logger.info(f"  Accuracy:  {metrics['accuracy']:.4f} ({metrics['accuracy']*100:.2f}%)")
    logger.info(f"  Precision: {metrics['precision']:.4f}")
    logger.info(f"  Recall:    {metrics['recall']:.4f}")
    logger.info(f"  F1-Score:  {metrics['f1_score']:.4f}")
    if metrics['roc_auc'] is not None:
        logger.info(f"  ROC-AUC:   {metrics['roc_auc']:.4f}")
    
    logger.info(f"\n📋 Matrice de confusion:")
    logger.info(f"  Vrais Négatifs (TN): {metrics['confusion_matrix']['tn']}")
    logger.info(f"  Faux Positifs (FP):  {metrics['confusion_matrix']['fp']}")
    logger.info(f"  Faux Négatifs (FN):  {metrics['confusion_matrix']['fn']}")
    logger.info(f"  Vrais Positifs (TP): {metrics['confusion_matrix']['tp']}")
    
    # Ajouter les informations du modèle
    result = {
        'model_name': model_name,
        'model_type': model_type,
        'metrics': metrics,
        'y_pred': y_pred,
        'y_proba': y_proba
    }
    
    logger.info("=" * 60)
    logger.info("✓ ÉVALUATION TERMINÉE")
    logger.info("=" * 60)
    
    return result


def compare_models(results: Dict[str, Dict[str, Any]]) -> pd.DataFrame:
    """
    Compare plusieurs modèles et retourne un DataFrame avec les métriques.
    
    Args:
        results: Dictionnaire {nom_modèle: résultats_evaluation}
        
    Returns:
        DataFrame pandas avec les métriques comparées
    """
    comparison_data = []
    
    for model_name, result in results.items():
        metrics = result['metrics']
        comparison_data.append({
            'Model': model_name,
            'Accuracy': metrics['accuracy'],
            'Precision': metrics['precision'],
            'Recall': metrics['recall'],
            'F1-Score': metrics['f1_score'],
            'ROC-AUC': metrics['roc_auc'] if metrics['roc_auc'] is not None else np.nan
        })
    
    df = pd.DataFrame(comparison_data)
    df = df.sort_values('Accuracy', ascending=False)
    
    return df


if __name__ == "__main__":
    # Test du module
    from sklearn.ensemble import RandomForestClassifier
    from ..data.data_preparation import prepare_data
    
    data = prepare_data()
    
    # Créer un modèle simple pour test
    model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(data['X_train_scaled'], data['y_train'])
    
    result = evaluate_model(model, data['X_test_scaled'], data['y_test'], 'standard', 'RandomForest')
    print(f"\nRésultat: {result['metrics']['accuracy']:.4f}")

