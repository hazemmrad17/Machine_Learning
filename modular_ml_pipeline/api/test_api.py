"""
Script de test pour l'API FastAPI.
Teste les endpoints /predict et /retrain.
"""

import requests
import json
from typing import Dict, Any

BASE_URL = "http://localhost:8000"


def test_health():
    """Teste l'endpoint /health"""
    print("=" * 60)
    print("TEST: /health")
    print("=" * 60)
    
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    print()


def test_predict(model_name: str = "mlp"):
    """Teste l'endpoint /predict"""
    print("=" * 60)
    print(f"TEST: /predict (modèle: {model_name})")
    print("=" * 60)
    
    # Exemple de features (cas malin)
    features = [
        17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
        1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
        25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
    ]
    
    payload = {"features": features}
    
    response = requests.post(
        f"{BASE_URL}/predict?model_name={model_name}",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Modèle: {result['model_name']}")
        print(f"Prédiction: {'🔴 Malin' if result['prediction'] == 1 else '🟢 Bénin'}")
        print(f"Probabilité: {result['probability']:.4f} ({result['probability']*100:.2f}%)")
        print(f"Confiance: {result['confidence']}")
        print(f"Timestamp: {result['timestamp']}")
    else:
        print(f"Erreur: {response.text}")
    print()


def test_predict_all():
    """Teste l'endpoint /predict/all"""
    print("=" * 60)
    print("TEST: /predict/all (tous les modèles)")
    print("=" * 60)
    
    features = [
        17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871,
        1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193,
        25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189
    ]
    
    payload = {"features": features}
    
    response = requests.post(
        f"{BASE_URL}/predict/all",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print("\n📊 Prédictions individuelles:")
        for model, pred in result['predictions'].items():
            if 'error' not in pred:
                print(f"  {model}: {'🔴 Malin' if pred['prediction'] == 1 else '🟢 Bénin'} "
                      f"(Prob: {pred['probability']:.4f}, Conf: {pred['confidence']})")
            else:
                print(f"  {model}: ❌ {pred['error']}")
        
        print("\n🎯 Consensus:")
        consensus = result['consensus']
        print(f"  Prédiction: {'🔴 Malin' if consensus['prediction'] == 1 else '🟢 Bénin'}")
        print(f"  Probabilité moyenne: {consensus['probability']:.4f}")
        print(f"  Confiance: {consensus['confidence']}")
        print(f"  Accord entre modèles: {consensus['agreement']}%")
    else:
        print(f"Erreur: {response.text}")
    print()


def test_retrain(model_type: str = "mlp", hyperparameters: Dict[str, Any] = None):
    """Teste l'endpoint /retrain"""
    print("=" * 60)
    print(f"TEST: /retrain (modèle: {model_type})")
    print("=" * 60)
    print("⚠️  Attention: Cette opération peut prendre plusieurs minutes...")
    print()
    
    payload = {
        "model_type": model_type,
        "hyperparameters": hyperparameters or {}
    }
    
    response = requests.post(
        f"{BASE_URL}/retrain",
        json=payload
    )
    
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Modèle: {result['model_name']}")
        print(f"Statut: {result['status']}")
        if result['accuracy']:
            print(f"Accuracy: {result['accuracy']:.4f}")
        if result['training_time']:
            print(f"Temps d'entraînement: {result['training_time']} secondes")
        print(f"Message: {result['message']}")
    else:
        print(f"Erreur: {response.text}")
    print()


def main():
    """Exécute tous les tests"""
    print("\n" + "=" * 60)
    print("TESTS DE L'API BREAST CANCER DETECTION")
    print("=" * 60)
    print()
    
    try:
        # Test 1: Health check
        test_health()
        
        # Test 2: Prédiction avec MLP
        test_predict("mlp")
        
        # Test 3: Prédiction avec SVM
        test_predict("svm")
        
        # Test 4: Prédiction avec tous les modèles
        test_predict_all()
        
        # Test 5: Réentraînement (optionnel, commenté car long)
        # test_retrain("mlp")
        
        print("=" * 60)
        print("✅ TOUS LES TESTS TERMINÉS")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Erreur: Impossible de se connecter à l'API")
        print("💡 Assurez-vous que l'API est démarrée: make api")
    except Exception as e:
        print(f"❌ Erreur: {e}")


if __name__ == "__main__":
    main()

