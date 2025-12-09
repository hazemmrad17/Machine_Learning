        # Breast Cancer Detection Frontend

A modern React + TypeScript frontend for the Breast Cancer Detection system with a beautiful Three.js animated background.

## Features

- 🎨 Beautiful animated mountain scene background using Three.js
- 📝 Manual input form for single predictions
- 📊 CSV batch upload for multiple predictions
- 🎯 Real-time prediction results with confidence scores
- 📱 Responsive design with Tailwind CSS
- ⚡ Fast and modern with Vite

## Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Three.js** - 3D graphics for background
- **shadcn/ui** - UI components
- **Lucide React** - Icons

## Setup

### Prerequisites

- Node.js 18+ and npm

### Installation

1. Install dependencies:
```bash
npm install
```

2. Create a `.env` file (optional, defaults to `http://localhost:8000`):
```bash
cp .env.example .env
```

3. Start the development server:
```bash
npm run dev
```

The app will be available at `http://localhost:3000`

## Building for Production

```bash
npm run build
```

The built files will be in the `dist` directory.

## Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/              # shadcn/ui components
│   │   │   ├── mountain-scene.tsx
│   │   │   ├── button.tsx
│   │   │   ├── card.tsx
│   │   │   └── ...
│   │   ├── PredictionForm.tsx
│   │   ├── PredictionResults.tsx
│   │   └── CSVUpload.tsx
│   ├── services/
│   │   └── api.ts           # API client
│   ├── utils/
│   │   └── cn.ts            # Utility functions
│   ├── App.tsx              # Main app component
│   ├── main.tsx             # Entry point
│   └── index.css            # Global styles
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## API Integration

The frontend connects to the FastAPI backend running on port 8000 by default. Make sure the API is running before using the frontend.

## Components

### Mountain Scene
The animated background uses Three.js with custom shaders to create a generative mountain landscape that responds to mouse movement.

### Prediction Form
Allows users to input 30 features manually with example data loading for quick testing.

### CSV Upload
Enables batch processing of predictions from CSV files with proper error handling.

### Results Display
Shows prediction results with confidence scores, probabilities, and clear visual indicators.

## Development

The project uses:
- **TypeScript** for type safety
- **ESLint** for code quality
- **Tailwind CSS** for styling
- **Vite** for fast development and building

## License

Part of the Breast Cancer Detection project.

