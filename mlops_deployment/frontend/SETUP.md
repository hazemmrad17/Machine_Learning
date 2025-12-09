# Frontend Setup Instructions

## Prerequisites

1. **Node.js and npm**: Make sure you have Node.js 18+ installed
   ```bash
   node --version  # Should be v18 or higher
   npm --version
   ```

## Installation Steps

### 1. Navigate to Frontend Directory
```bash
cd mlops_deployment/frontend
```

### 2. Install Dependencies
```bash
npm install
```

This will install all required packages including:
- React, TypeScript, Vite
- Three.js (for the mountain scene)
- Tailwind CSS
- shadcn/ui components
- Lucide React icons
- PapaParse (for CSV parsing)

### 3. Environment Configuration (Optional)

Create a `.env` file in the `frontend` directory if you need to change the API URL:
```
VITE_API_URL=http://localhost:8000
```

By default, it will use `http://localhost:8000`.

### 4. Start Development Server
```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Project Structure

The frontend follows shadcn/ui project structure:

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/                    # shadcn/ui components
│   │   │   ├── mountain-scene.tsx  # Three.js animated background
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   ├── input.tsx
│   │   │   └── label.tsx
│   │   ├── PredictionForm.tsx     # Manual input form
│   │   ├── PredictionResults.tsx   # Results display
│   │   └── CSVUpload.tsx           # Batch CSV upload
│   ├── services/
│   │   └── api.ts                  # FastAPI client
│   ├── utils/
│   │   └── cn.ts                   # Utility functions
│   ├── App.tsx                     # Main app component
│   ├── main.tsx                    # Entry point
│   └── index.css                   # Global styles with Tailwind
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## Important Notes

### shadcn/ui Components

The project uses shadcn/ui component structure. Components are in `/components/ui` folder. This is important because:
- shadcn/ui follows a specific directory structure
- Components are copied (not installed) for customization
- All components use the `cn()` utility for className merging

### Mountain Scene Component

The `mountain-scene.tsx` component uses Three.js with custom shaders. It:
- Creates an animated 3D mountain landscape
- Responds to mouse movement for lighting
- Uses WebGL for performance
- Is fully typed with TypeScript

### API Integration

The frontend connects to the FastAPI backend. Make sure:
1. The API is running on port 8000 (or update `.env`)
2. CORS is enabled in the API (already configured)
3. The model is trained and loaded

## Building for Production

```bash
npm run build
```

This creates optimized production files in the `dist` directory.

## Troubleshooting

### Port Already in Use
If port 3000 is in use, Vite will automatically try the next available port.

### API Connection Errors
- Check that the API is running: `http://localhost:8000/health`
- Verify CORS settings in the API
- Check the browser console for errors

### TypeScript Errors
- Run `npm install` again to ensure all types are installed
- Check that `@types/papaparse` is installed for CSV parsing

### Three.js Not Loading
- Ensure `three` package is installed
- Check browser console for WebGL support

## Development Tips

1. **Hot Module Replacement**: Changes are reflected instantly
2. **TypeScript**: All components are fully typed
3. **Tailwind**: Use utility classes for styling
4. **Components**: Reusable shadcn/ui components throughout

## Next Steps

After setup:
1. Start the API: `python scripts/run_api.py`
2. Start the frontend: `npm run dev`
3. Open `http://localhost:3000` in your browser

Enjoy the beautiful animated background and smooth user experience! 🎨

