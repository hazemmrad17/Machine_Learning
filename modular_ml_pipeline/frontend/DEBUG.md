# Debugging Frontend Issues

## Common Issues and Solutions

### 1. Check Browser Console
Open browser DevTools (F12) and check the Console tab for errors.

### 2. Check Terminal Output
Look for compilation errors in the terminal where `npm run dev` is running.

### 3. Common Fixes

#### If you see "Cannot find module" errors:
```bash
cd modular_ml_pipeline/frontend
npm install
```

#### If you see Three.js/WebGL errors:
The shader might not work on all browsers. The component has fallbacks.

#### If the page is blank:
- Check if the dev server is running on the correct port
- Check browser console for React errors
- Try clearing browser cache

### 4. Test Basic Loading
If the app doesn't load, try temporarily commenting out the NeuralNetworkHero import in Home.jsx to see if the app loads without it.

### 5. Check Dependencies
Make sure all packages are installed:
```bash
npm install gsap @gsap/react @react-three/fiber @react-three/drei three
```

