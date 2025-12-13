# 🎨 Frontend React - Détection du Cancer du Sein

Frontend moderne, responsive et animé pour l'API de détection du cancer du sein.

## ✨ Fonctionnalités

- 🎯 **UI/UX Moderne**: Design glassmorphism avec gradients et animations fluides
- 📱 **100% Responsive**: Optimisé pour mobile, tablette et desktop
- 🎬 **Animations Fluides**: Framer Motion pour des transitions élégantes
- 📊 **Visualisations**: Graphiques interactifs avec Recharts
- 🔄 **État Avancé**: React Query pour la gestion des données
- 🎨 **Thème Sombre**: Design moderne avec glassmorphism
- ⚡ **Performance**: Vite pour un build ultra-rapide

## 🚀 Installation

```bash
cd frontend
npm install
```

## 🏃 Démarrage

```bash
# Mode développement
npm run dev

# Build de production
npm run build

# Prévisualiser le build
npm run preview
```

L'application sera disponible sur: http://localhost:3000

## 🔧 Configuration

Créez un fichier `.env`:

```env
VITE_API_URL=http://localhost:8000
```

## 📦 Technologies

- **React 18**: Framework UI
- **Vite**: Build tool ultra-rapide
- **Tailwind CSS**: Styling utility-first
- **Framer Motion**: Animations fluides
- **React Query**: Gestion d'état serveur
- **Recharts**: Graphiques interactifs
- **Lucide React**: Icônes modernes
- **React Hot Toast**: Notifications élégantes

## 🎨 Design

- **Glassmorphism**: Effets de verre avec backdrop-blur
- **Gradients Animés**: Dégradés dynamiques
- **Micro-interactions**: Animations au survol et au clic
- **Dark Theme**: Thème sombre moderne
- **Responsive Grid**: Layout adaptatif

## 📱 Pages

1. **Home** (`/`): Page d'accueil avec présentation
2. **Predictions** (`/predict`): Formulaire de prédiction
3. **Model Comparison** (`/compare`): Comparaison des modèles

## 🎯 Fonctionnalités Principales

### Page Prédiction
- Saisie des 30 features
- Sélection du modèle (MLP, SVM, GRU-SVM, ou tous)
- Chargement d'exemples
- Affichage des résultats avec animations
- Graphiques de probabilité

### Page Comparaison
- Tableau comparatif des métriques
- Graphiques de performance
- Réentraînement des modèles via API
- Visualisations interactives

## 🚀 Déploiement

### Build de Production

```bash
npm run build
```

Les fichiers seront dans le dossier `dist/`.

### Déploiement sur Vercel/Netlify

1. Connectez votre repository
2. Configurez la variable d'environnement `VITE_API_URL`
3. Déployez!

### Déploiement avec Docker

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

## 🎨 Personnalisation

Les couleurs et styles peuvent être modifiés dans:
- `tailwind.config.js`: Configuration Tailwind
- `src/index.css`: Styles globaux
- Composants individuels pour des styles spécifiques

## 📝 Notes

- Assurez-vous que l'API FastAPI est démarrée sur le port 8000
- Le proxy est configuré dans `vite.config.js` pour le développement
- En production, configurez `VITE_API_URL` avec l'URL de votre API

