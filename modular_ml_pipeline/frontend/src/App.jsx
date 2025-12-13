import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { motion } from 'framer-motion'
import Home from './pages/Home'
import Predictions from './pages/Predictions'
import ModelComparison from './pages/ModelComparison'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import DotScreenShader from './components/ui/dot-shader-background'

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col relative overflow-hidden">
        {/* Dot Shader Background */}
        <div className="fixed inset-0 -z-10 w-full h-full">
          <DotScreenShader />
        </div>
        
        {/* Content Overlay */}
        <div className="relative z-10 flex flex-col min-h-screen">
          <Navbar />
          <motion.main
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5 }}
            className="flex-1"
          >
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/predict" element={<Predictions />} />
              <Route path="/compare" element={<ModelComparison />} />
            </Routes>
          </motion.main>
          <Footer />
        </div>
      </div>
    </Router>
  )
}

export default App

