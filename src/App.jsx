import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Navbar } from './components/Navbar'
import Chat from './components/Chat'
import Pacientes from './components/Pacientes'
import Informes from './components/Informes'

const App = () => {
  return (
    <div className="container mt-4">
      <Router>
        <Navbar />
        <Routes>
          <Route path="/chat" exact element={<Chat />} />
          <Route path="/pacientes" element={<Pacientes />} />
          <Route path="/informes" element={<Informes />} />
        </Routes>
      </Router>
    </div>
  )
}

export default App
