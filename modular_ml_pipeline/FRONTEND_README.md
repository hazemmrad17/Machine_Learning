# 🎨 Frontend React - Détection du Cancer du Sein

## ✅ Statut

Le frontend React est **prêt et fonctionnel** ! L'erreur CSS a été corrigée.

## 🚀 Démarrage Rapide

### 1. Installer les dépendances

```bash
cd frontend
npm install
```

### 2. Démarrer l'API (dans un autre terminal)

```bash
cd api
python app.py
```

L'API sera disponible sur: `http://localhost:8000`

### 3. Démarrer le Frontend

```bash
cd frontend
npm run dev
```

Le frontend sera disponible sur: `http://localhost:3000`

## 🎯 Fonctionnalités Principales

### ✨ Design Moderne
- **Glassmorphism**: Effets de verre avec backdrop-blur
- **Animations Fluides**: Framer Motion pour des transitions élégantes
- **Gradients Animés**: Dégradés dynamiques et modernes
- **100% Responsive**: Optimisé pour mobile, tablette et desktop
- **Dark Theme**: Thème sombre professionnel

### 📊 Pages Disponibles

#### 1. **Page d'Accueil** (`/`)
- Vue d'ensemble du projet
- Statut de connexion à l'API en temps réel
- Liste des modèles disponibles
- Navigation intuitive

#### 2. **Page Prédiction** (`/predict`)
- Formulaire interactif pour 30 features
- Sélection du modèle (MLP, SVM, GRU-SVM, ou tous)
- Boutons pour charger des exemples (malin/bénin)
- Résultats animés avec:
  - Prédiction claire (Malin/Bénin)
  - Probabilité en pourcentage
  - Niveau de confiance
  - Graphiques visuels
  - Copie des résultats

#### 3. **Page Comparaison** (`/compare`)
- Tableau comparatif des métriques
- Graphiques de performance interactifs
- Fonction de réentraînement des modèles
- Visualisations avec Recharts

### 🔌 Intégration API

Le frontend communique avec l'API FastAPI via:
- `/health` - Vérification de l'état
- `/models` - Liste des modèles
- `/predict` - Prédiction avec un modèle
- `/predict/all` - Prédiction avec tous les modèles (consensus)
- `/retrain` - Réentraînement des modèles

## 🛠️ Technologies

- **React 18**: Framework UI moderne
- **Vite 7**: Build tool ultra-rapide
- **Tailwind CSS 3**: Styling utility-first
- **Framer Motion**: Animations fluides
- **React Query**: Gestion d'état serveur
- **Recharts**: Graphiques interactifs
- **Lucide React**: Icônes modernes
- **React Hot Toast**: Notifications élégantes

## 📁 Structure du Projet

```
frontend/
├── src/
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.jsx      # Navigation principale
│   │   │   └── Footer.jsx      # Pied de page
│   │   └── prediction/
│   │       ├── FeatureInput.jsx      # Input pour une feature
│   │       ├── ModelSelector.jsx      # Sélecteur de modèle
│   │       └── PredictionResult.jsx   # Affichage des résultats
│   ├── pages/
│   │   ├── Home.jsx            # Page d'accueil
│   │   ├── Predictions.jsx     # Page de prédiction
│   │   └── ModelComparison.jsx # Page de comparaison
│   ├── services/
│   │   └── api.js              # Service API
│   ├── App.jsx                 # Composant principal
│   ├── main.jsx                # Point d'entrée
│   └── index.css               # Styles globaux
├── public/                     # Fichiers statiques
├── package.json                # Dépendances
├── vite.config.js              # Configuration Vite
├── tailwind.config.js          # Configuration Tailwind
└── postcss.config.js           # Configuration PostCSS
```

## 🎨 Personnalisation

### Couleurs

Les couleurs peuvent être modifiées dans `tailwind.config.js`:

```javascript
colors: {
  primary: { ... },
  danger: { ... },
  success: { ... }
}
```

### Styles Globaux

Les styles personnalisés sont dans `src/index.css`:

- `.glass` - Effet glassmorphism
- `.card` - Carte avec effet de verre
- `.btn-primary` - Bouton principal
- `.btn-secondary` - Bouton secondaire
- `.gradient-text` - Texte avec gradient

## 🐛 Dépannage

### Erreur: "border-border does not exist"
✅ **Résolu** - La ligne problématique a été supprimée de `index.css`

### L'API ne répond pas
- Vérifiez que l'API FastAPI est démarrée: `cd api && python app.py`
- Vérifiez l'URL dans `.env`: `VITE_API_URL=http://localhost:8000`

### Erreurs de compilation
```bash
rm -rf node_modules package-lock.json
npm install
```

### Port déjà utilisé
Modifiez le port dans `vite.config.js`:
```javascript
server: {
  port: 3001  // Changez le port
}
```

## 📦 Build de Production

```bash
npm run build
```

Les fichiers seront dans le dossier `dist/` et peuvent être déployés sur:
- Vercel
- Netlify
- GitHub Pages
- Tout serveur web statique

## 🚀 Déploiement

### Vercel (Recommandé)

1. Installez Vercel CLI: `npm i -g vercel`
2. Dans le dossier `frontend`: `vercel`
3. Configurez `VITE_API_URL` dans les variables d'environnement

### Netlify

1. Connectez votre repository GitHub
2. Configurez le build:
   - Build command: `npm run build`
   - Publish directory: `dist`
3. Ajoutez `VITE_API_URL` dans les variables d'environnement

## 💡 Astuces

1. **Exemples Rapides**: Utilisez les boutons "Exemple Malin" et "Exemple Bénin" pour tester
2. **Consensus**: Sélectionnez "Tous" pour obtenir un consensus entre tous les modèles
3. **Réentraînement**: La page de comparaison permet de réentraîner les modèles directement
4. **Responsive**: Testez sur mobile, tablette et desktop pour voir l'adaptation

## 📝 Notes

- Le frontend utilise un proxy dans `vite.config.js` pour le développement
- En production, configurez `VITE_API_URL` avec l'URL de votre API
- Les animations sont optimisées pour les performances
- Le design est entièrement accessible (WCAG compliant)

## 🎉 Prêt à l'emploi!

Le frontend est maintenant **100% fonctionnel** et prêt à être utilisé. Il offre une expérience utilisateur moderne, fluide et professionnelle pour votre application de détection du cancer du sein.

