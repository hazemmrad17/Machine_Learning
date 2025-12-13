# 🎨 Configuration Shader Animation

## ✅ Modifications Effectuées

### 1. TypeScript Configuration
- Ajout de `typescript` et `@types/three` dans `package.json`
- Création de `tsconfig.json` et `tsconfig.node.json`
- Configuration de l'alias `@/` dans `vite.config.js`

### 2. Three.js Installation
- Ajout de `three` dans les dépendances
- Ajout de `@types/three` dans les devDependencies

### 3. Composant Shader
- Création de `/src/components/ui/shader-animation.tsx`
- Intégration comme arrière-plan global dans `App.jsx`
- Position fixe avec `z-index: -10` pour rester en arrière-plan

### 4. Adaptation des Couleurs
Toutes les couleurs ont été changées de **purple/pink** vers **cyan/blue**:
- Boutons: `from-cyan-500 to-blue-600`
- Textes gradient: `from-cyan-400 via-blue-400 to-cyan-300`
- Bordures: `border-cyan-500/30`
- Scrollbar: `bg-cyan-600`
- Navigation active: `from-cyan-500 to-blue-600`

### 5. Modèles Ajoutés
Tous les modèles sont maintenant disponibles:
- ✅ Linear Regression
- ✅ Softmax Regression
- ✅ MLP
- ✅ SVM
- ✅ KNN
- ✅ GRU-SVM

## 🚀 Installation

```bash
cd frontend
npm install
```

Cela installera:
- `three` (Three.js pour le shader)
- `typescript` (support TypeScript)
- `@types/three` (types TypeScript pour Three.js)

## 📁 Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/
│   │   │   └── shader-animation.tsx  ← Nouveau composant shader
│   │   └── ...
│   └── ...
├── tsconfig.json                      ← Configuration TypeScript
└── package.json                       ← Dépendances mises à jour
```

## 🎨 Utilisation

Le shader est automatiquement intégré comme arrière-plan global dans `App.jsx`. Il s'affiche derrière tout le contenu avec un fond noir.

### Personnalisation

Pour modifier le shader, éditez `/src/components/ui/shader-animation.tsx`:
- **Fragment Shader**: Modifie l'apparence visuelle
- **Uniforms**: Contrôle les paramètres (time, resolution)
- **Animation Speed**: Change `uniforms.time.value += 0.05`

## 🔧 Dépannage

### Erreur TypeScript
Si vous avez des erreurs TypeScript, vérifiez que:
- `tsconfig.json` existe
- Les types sont installés: `npm install @types/three`

### Shader ne s'affiche pas
- Vérifiez que Three.js est installé: `npm list three`
- Vérifiez la console du navigateur pour les erreurs
- Assurez-vous que le composant est bien importé dans `App.jsx`

### Performance
Le shader utilise `requestAnimationFrame` pour une animation fluide. Si vous avez des problèmes de performance:
- Réduisez la complexité du fragment shader
- Diminuez `setPixelRatio` dans le renderer

## 📝 Notes

- Le shader utilise WebGL via Three.js
- Compatible avec tous les navigateurs modernes
- Responsive automatiquement (s'adapte à la taille de la fenêtre)
- Nettoyage automatique des ressources au démontage du composant


