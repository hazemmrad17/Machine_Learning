import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom'
import { motion } from 'framer-motion'
import Home from './pages/Home'
import Predictions from './pages/Predictions'
import ModelComparison from './pages/ModelComparison'
import Navbar from './components/layout/Navbar'
import Footer from './components/layout/Footer'
import NeuralBackground from './components/ui/neural-background'

function AppContent() {
  const location = useLocation()
  const isHome = location.pathname === '/'

  return (
    <div className="min-h-screen flex flex-col relative bg-black">
      {/* Neural Network Background for all pages except Home */}
      {!isHome && <NeuralBackground />}
      
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
  )
}

function App() {
  return (
    <Router>
      <AppContent />
    </Router>
  )
}

export default App

