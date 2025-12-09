# Installation Guide - React Frontend

## Quick Start

1. **Install Node.js** (if not already installed)
   - Download from https://nodejs.org/ (v18 or higher)
   - Verify installation: `node --version` and `npm --version`

2. **Install Dependencies**
   ```bash
   cd mlops_deployment/frontend
   npm install
   ```

3. **Start Development Server**
   ```bash
   npm run dev
   ```

4. **Open Browser**
   - Navigate to `http://localhost:3000`
   - Make sure the API is running on `http://localhost:8000`

## Using the Python Script

Alternatively, you can use the provided Python script:

```bash
cd mlops_deployment
python scripts/run_web_ui.py
```

This script will:
- Check if Node.js/npm is installed
- Automatically install dependencies if needed
- Start the React development server

## What Gets Installed

The `npm install` command installs:

### Core Dependencies
- **react** & **react-dom** - React framework
- **three** - 3D graphics library for the animated background
- **lucide-react** - Icon library
- **papaparse** - CSV parsing for batch uploads

### UI Libraries
- **tailwindcss** - Utility-first CSS framework
- **clsx** & **tailwind-merge** - Class name utilities
- **class-variance-authority** - Component variants

### Development Tools
- **typescript** - Type safety
- **vite** - Fast build tool and dev server
- **@vitejs/plugin-react** - React plugin for Vite
- **eslint** - Code linting

### Type Definitions
- **@types/react**, **@types/react-dom** - React types
- **@types/three** - Three.js types
- **@types/papaparse** - PapaParse types

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components (mountain-scene, button, card, etc.)
│   │   ├── PredictionForm.tsx
│   │   ├── PredictionResults.tsx
│   │   └── CSVUpload.tsx
│   ├── services/
│   │   └── api.ts           # API client for FastAPI
│   ├── utils/
│   │   └── cn.ts            # className utility
│   ├── App.tsx              # Main application
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Features

✅ **Animated Background** - Three.js mountain scene with mouse interaction  
✅ **Manual Input** - Form for entering 30 features with example data  
✅ **CSV Upload** - Batch processing from CSV files  
✅ **Results Display** - Beautiful cards showing predictions and confidence  
✅ **Responsive Design** - Works on desktop and mobile  
✅ **TypeScript** - Full type safety  
✅ **Modern UI** - shadcn/ui components with Tailwind CSS  

## Troubleshooting

### npm install fails
- Make sure Node.js 18+ is installed
- Try deleting `node_modules` and `package-lock.json`, then run `npm install` again
- Check your internet connection

### Port 3000 already in use
- Vite will automatically try the next available port
- Or manually change the port in `vite.config.ts`

### API connection errors
- Ensure the FastAPI backend is running: `python scripts/run_api.py`
- Check API health: `http://localhost:8000/health`
- Verify CORS is enabled in the API

### TypeScript errors
- Run `npm install` to ensure all type definitions are installed
- Check that all imports are correct

## Next Steps

After installation:
1. Start the API: `python scripts/run_api.py` (in mlops_deployment directory)
2. Start the frontend: `npm run dev` (in frontend directory)
3. Open `http://localhost:3000` in your browser
4. Try the "Load Benign Example" or "Load Malignant Example" buttons to test

Enjoy! 🎉

