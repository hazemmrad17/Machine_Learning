# Makefile pour le pipeline ML - Détection du Cancer du Sein
# Utilisation: make <commande>

.PHONY: help venv install prepare train evaluate save api test clean

# Variables
PYTHON = python
VENV = venv
# Windows
ifeq ($(OS),Windows_NT)
    PIP = $(VENV)\Scripts\pip
    PYTHON_VENV = $(VENV)\Scripts\python
    ACTIVATE = $(VENV)\Scripts\activate
else
    # Linux/Mac
    PIP = $(VENV)/bin/pip
    PYTHON_VENV = $(VENV)/bin/python
    ACTIVATE = $(VENV)/bin/activate
endif
API_DIR = api

# Couleurs pour l'affichage
GREEN = \033[0;32m
YELLOW = \033[1;33m
NC = \033[0m # No Color

help:
	@echo "$(GREEN)=== Makefile - Pipeline ML ===$(NC)"
	@echo ""
	@echo "Commandes disponibles:"
	@echo "  $(YELLOW)make venv$(NC)          - Créer l'environnement virtuel"
	@echo "  $(YELLOW)make install$(NC)       - Installer les dépendances"
	@echo "  $(YELLOW)make prepare$(NC)       - Préparer les données"
	@echo "  $(YELLOW)make train$(NC)         - Entraîner tous les modèles"
	@echo "  $(YELLOW)make evaluate$(NC)      - Évaluer les modèles"
	@echo "  $(YELLOW)make save$(NC)          - Sauvegarder les modèles"
	@echo "  $(YELLOW)make api$(NC)           - Démarrer l'API FastAPI"
	@echo "  $(YELLOW)make test-api$(NC)      - Tester l'API"
	@echo "  $(YELLOW)make all$(NC)          - Exécuter tout le pipeline"
	@echo "  $(YELLOW)make clean$(NC)         - Nettoyer les fichiers temporaires"
	@echo ""

venv:
	@echo "$(GREEN)Création de l'environnement virtuel...$(NC)"
	$(PYTHON) -m venv $(VENV)
	@echo "$(GREEN)✓ Environnement virtuel créé$(NC)"
	@echo "$(YELLOW)Activez-le avec: .\\$(VENV)\\Scripts\\Activate.ps1$(NC)"

install: venv
	@echo "$(GREEN)Installation des dépendances...$(NC)"
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt
	$(PIP) install -r $(API_DIR)/requirements.txt
	@echo "$(GREEN)✓ Dépendances installées$(NC)"

prepare:
	@echo "$(GREEN)Préparation des données...$(NC)"
	$(PYTHON_VENV) -c "from src.data.data_preparation import prepare_data; prepare_data('data.csv')"
	@echo "$(GREEN)✓ Données préparées$(NC)"

train:
	@echo "$(GREEN)Entraînement des modèles...$(NC)"
	$(PYTHON_VENV) main.py
	@echo "$(GREEN)✓ Modèles entraînés$(NC)"

evaluate: train
	@echo "$(GREEN)Évaluation des modèles...$(NC)"
	@echo "$(YELLOW)(L'évaluation est incluse dans main.py)$(NC)"

save: train
	@echo "$(GREEN)Modèles sauvegardés dans models/$(NC)"

api:
	@echo "$(GREEN)Démarrage de l'API FastAPI...$(NC)"
	@echo "$(YELLOW)API disponible sur: http://localhost:8000$(NC)"
	@echo "$(YELLOW)Documentation: http://localhost:8000/docs$(NC)"
	$(PYTHON_VENV) -m uvicorn api.app:app --reload --host 0.0.0.0 --port 8000

api-prod:
	@echo "$(GREEN)Démarrage de l'API en mode production...$(NC)"
	$(PYTHON_VENV) -m uvicorn api.app:app --host 0.0.0.0 --port 8000 --workers 4

test-api:
	@echo "$(GREEN)Test de l'API...$(NC)"
	@echo "$(YELLOW)Test de santé...$(NC)"
	curl http://localhost:8000/health
	@echo ""
	@echo "$(YELLOW)Test de prédiction...$(NC)"
	curl -X POST "http://localhost:8000/predict?model_name=mlp" \
		-H "Content-Type: application/json" \
		-d "{\"features\": [17.99, 10.38, 122.8, 1001.0, 0.1184, 0.2776, 0.3001, 0.1471, 0.2419, 0.07871, 1.095, 0.9053, 8.589, 153.4, 0.006399, 0.04904, 0.05373, 0.01587, 0.03003, 0.006193, 25.38, 17.33, 184.6, 2019.0, 0.1622, 0.6656, 0.7119, 0.2654, 0.4601, 0.1189]}"

all: install prepare train api
	@echo "$(GREEN)=== Pipeline complet terminé! ===$(NC)"

clean:
	@echo "$(YELLOW)Nettoyage des fichiers temporaires...$(NC)"
	rm -rf __pycache__
	rm -rf src/**/__pycache__
	rm -rf *.pyc
	rm -rf .pytest_cache
	@echo "$(GREEN)✓ Nettoyage terminé$(NC)"

clean-all: clean
	@echo "$(YELLOW)Suppression de l'environnement virtuel...$(NC)"
	rm -rf $(VENV)
	@echo "$(GREEN)✓ Environnement virtuel supprimé$(NC)"

