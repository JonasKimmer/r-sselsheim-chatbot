import { useState } from 'react'
import ChatContainer from './components/ChatContainer'
import Header from './components/Header'

function App() {
  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <Header />
      <main className="flex-1 overflow-hidden">
        <ChatContainer />
      </main>
    </div>
  )
}

export default App
