import React, { useState, useRef, useEffect } from 'react'
import ChatInterface from './components/ChatInterface'
import './App.css'

function App() {
  return (
    <div className="App">
      <div className="top-left-header">
        <img 
          src="/logo.png" 
          alt="SpeechLP Logo" 
          className="main-logo"
          onLoad={() => console.log('Logo loaded successfully')}
          onError={(e) => {
            console.error('Logo failed to load from:', e.target.src);
            e.target.style.display = 'none';
          }}
        />
        <h1 className="parlez-title">Parlez Coding Challenge</h1>
      </div>
      <ChatInterface />
    </div>
  )
}

export default App

