"""
Script principal pour exécuter le pipeline ML complet.
Orchestre toutes les étapes: préparation, entraînement, évaluation et sauvegarde.
"""

import sys
from pathlib import Path

# Ajouter le dossier src au path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from src.data.data_preparation import prepare_data
from src.models.train_models import train_model
from src.utils.evaluation import evaluate_model, compare_models
from src.utils.model_io import save_model, save_scaler, load_model, load_scaler
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def main():
    """
    Fonction principale qui exécute le pipeline ML complet.
    """
    logger.info("=" * 80)
    logger.info("PIPELINE ML - DÉTECTION DU CANCER DU SEIN")
    logger.info("=" * 80)
    
    # ========================================================================
    # ÉTAPE 1: PRÉPARATION DES DONNÉES
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ÉTAPE 1: PRÉPARATION DES DONNÉES")
    logger.info("=" * 80)
    
    data_path = 'data.csv'  # Chemin relatif depuis le dossier racine du projet
    data = prepare_data(
        data_path=data_path,
        target_column='diagnosis',
        test_size=0.3,
        random_state=42
    )
    
    # Sauvegarder le scaler
    models_dir = Path(__file__).parent / "models"
    models_dir.mkdir(exist_ok=True)
    save_scaler(data['scaler'], models_dir / "scaler.pkl")
    
    # ========================================================================
    # ÉTAPE 2: ENTRAÎNEMENT DES MODÈLES
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ÉTAPE 2: ENTRAÎNEMENT DES MODÈLES")
    logger.info("=" * 80)
    
    # Hyperparamètres exacts du notebook original
    models_to_train = {
        'Linear': ('linear', {
            'eta0': 1e-3,
            'max_iter': 3000,
            'random_state': 42
        }),
        'Softmax': ('softmax', {
            'eta0': 1e-3,
            'max_iter': 3000,
            'random_state': 42
        }),
        'MLP': ('mlp', {
            'hidden_layer_sizes': (500, 500, 500),
            'learning_rate_init': 1e-2,
            'alpha': 0.01,
            'max_iter': 3000,
            'early_stopping': True,
            'validation_fraction': 0.1,
            'random_state': 42
        }),
        'SVM': ('svm', {
            'C': 5,
            'kernel': 'rbf',
            'probability': True,
            'random_state': 42,
            'max_iter': 3000
        }),
        'KNN-L1': ('knn', {
            'n_neighbors': 1,
            'distance': 'l1'  # L1 (Manhattan) distance
        }),
        'KNN-L2': ('knn', {
            'n_neighbors': 1,
            'distance': 'l2'  # L2 (Euclidean) distance
        }),
        'GRU-SVM': ('gru_svm', {
            'epochs': 500,
            'batch_size': 128,
            'patience': 30,
            'learning_rate': 1e-3,
            'svm_C': 5,
            'random_state': 42
        })
    }
    
    trained_models = {}
    
    for model_name, (model_type, kwargs) in models_to_train.items():
        try:
            logger.info(f"\n--- Entraînement: {model_name} ---")
            
            if model_type == 'gru_svm':
                model = train_model(
                    model_type=model_type,
                    X_train=data['X_train_scaled'],
                    y_train=data['y_train'],
                    X_test=data['X_test_scaled'],
                    **kwargs
                )
            else:
                model = train_model(
                    model_type=model_type,
                    X_train=data['X_train_scaled'],
                    y_train=data['y_train'],
                    **kwargs
                )
            
            trained_models[model_name] = {
                'model': model,
                'type': model_type
            }
            
            # Sauvegarder le modèle
            model_path = models_dir / f"{model_name.lower().replace('-', '_')}_model.pkl"
            if model_type == 'gru_svm':
                save_model(model, model_path, model_type='gru_svm')
            else:
                save_model(model, model_path, model_type='standard')
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'entraînement de {model_name}: {e}")
            continue
    
    # ========================================================================
    # ÉTAPE 3: ÉVALUATION DES MODÈLES
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ÉTAPE 3: ÉVALUATION DES MODÈLES")
    logger.info("=" * 80)
    
    evaluation_results = {}
    
    for model_name, model_info in trained_models.items():
        try:
            result = evaluate_model(
                model=model_info['model'],
                X_test=data['X_test_scaled'],
                y_test=data['y_test'],
                model_type=model_info['type'],
                model_name=model_name
            )
            evaluation_results[model_name] = result
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'évaluation de {model_name}: {e}")
            continue
    
    # ========================================================================
    # ÉTAPE 4: COMPARAISON DES MODÈLES
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("ÉTAPE 4: COMPARAISON DES MODÈLES")
    logger.info("=" * 80)
    
    if evaluation_results:
        comparison_df = compare_models(evaluation_results)
        print("\n" + "=" * 80)
        print("TABLEAU COMPARATIF DES MODÈLES")
        print("=" * 80)
        print(comparison_df.to_string(index=False))
        print("=" * 80)
        
        # Sauvegarder le tableau comparatif
        comparison_path = models_dir / "model_comparison.csv"
        comparison_df.to_csv(comparison_path, index=False)
        logger.info(f"\n✓ Tableau comparatif sauvegardé dans {comparison_path}")
        
        # Identifier le meilleur modèle
        best_model = comparison_df.iloc[0]['Model']
        best_accuracy = comparison_df.iloc[0]['Accuracy']
        logger.info(f"\n🏆 MEILLEUR MODÈLE: {best_model} (Accuracy: {best_accuracy:.4f})")
    
    # ========================================================================
    # RÉSUMÉ FINAL
    # ========================================================================
    logger.info("\n" + "=" * 80)
    logger.info("RÉSUMÉ FINAL")
    logger.info("=" * 80)
    logger.info(f"✓ Modèles entraînés: {len(trained_models)}")
    logger.info(f"✓ Modèles évalués: {len(evaluation_results)}")
    logger.info(f"✓ Fichiers sauvegardés dans: {models_dir.absolute()}")
    logger.info("=" * 80)
    logger.info("✅ PIPELINE TERMINÉ AVEC SUCCÈS!")
    logger.info("=" * 80)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("\n⚠️ Pipeline interrompu par l'utilisateur")
        sys.exit(0)
    except Exception as e:
        logger.error(f"\n❌ Erreur fatale: {e}", exc_info=True)
        sys.exit(1)

