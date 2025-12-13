# 🚀 Guide de Démarrage Rapide - Frontend React

## ✅ Problème Résolu

L'erreur `border-border` dans `index.css` a été corrigée. Le frontend devrait maintenant démarrer sans erreur.

## 📋 Prérequis

1. **Node.js** (version 18 ou supérieure)
2. **npm** ou **yarn**
3. **API FastAPI** démarrée sur `http://localhost:8000`

## 🏃 Démarrage

### 1. Installer les dépendances

```bash
cd frontend
npm install
```

### 2. Configurer l'URL de l'API (optionnel)

Créez un fichier `.env` dans le dossier `frontend`:

```env
VITE_API_URL=http://localhost:8000
```

Par défaut, le frontend utilise `http://localhost:8000`.

### 3. Démarrer le serveur de développement

```bash
npm run dev
```

Le frontend sera accessible sur: **http://localhost:3000**

## 🎨 Fonctionnalités

### Page d'Accueil (`/`)
- Vue d'ensemble du projet
- Statut de connexion à l'API
- Liste des modèles disponibles
- Navigation vers les autres pages

### Page Prédiction (`/predict`)
- Formulaire pour saisir les 30 features
- Sélection du modèle (MLP, SVM, GRU-SVM, ou tous)
- Boutons pour charger des exemples (malin/bénin)
- Affichage animé des résultats avec:
  - Prédiction (Malin/Bénin)
  - Probabilité en pourcentage
  - Niveau de confiance
  - Graphiques visuels

### Page Comparaison (`/compare`)
- Tableau comparatif des métriques
- Graphiques de performance
- Fonction de réentraînement des modèles
- Visualisations interactives

## 🔧 Commandes Disponibles

```bash
# Développement
npm run dev

# Build de production
npm run build

# Prévisualiser le build
npm run preview

# Linter
npm run lint
```

## 🐛 Dépannage

### L'API ne répond pas
- Vérifiez que l'API FastAPI est démarrée sur le port 8000
- Vérifiez la variable d'environnement `VITE_API_URL` si vous l'avez modifiée

### Erreurs de compilation
- Supprimez `node_modules` et `package-lock.json`
- Réinstallez: `npm install`

### Erreurs de styles
- Vérifiez que Tailwind CSS est bien installé
- Vérifiez que `postcss.config.js` existe

## 📦 Technologies Utilisées

- **React 18**: Framework UI moderne
- **Vite**: Build tool ultra-rapide
- **Tailwind CSS**: Styling utility-first
- **Framer Motion**: Animations fluides
- **React Query**: Gestion d'état serveur
- **Recharts**: Graphiques interactifs
- **Lucide React**: Icônes modernes

## 🎯 Prochaines Étapes

1. Démarrer l'API FastAPI: `cd ../api && python app.py`
2. Démarrer le frontend: `cd frontend && npm run dev`
3. Ouvrir http://localhost:3000 dans votre navigateur
4. Tester les prédictions avec les exemples fournis

## 💡 Astuces

- Utilisez les boutons "Exemple Malin" et "Exemple Bénin" pour tester rapidement
- La page de comparaison permet de réentraîner les modèles directement depuis l'interface
- Les résultats sont animés pour une meilleure expérience utilisateur
- Le design est entièrement responsive (mobile, tablette, desktop)

