import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LoginForm from './LoginForm';
import TradingSettings from './TradingSettings';

import { Navigate } from 'react-router-dom';

function App() {
  return (
    <Router>
      <Routes>
       
      
        <Route path="/login" element={<LoginForm />} />
        <Route path="/settings" element={<TradingSettings />} />
        <Route path="*" element={<Navigate to="/login" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
