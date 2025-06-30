import React from 'react';
import ChatInterface from './components/ChatInterface';
import Header from './components/Header';
import Footer from './components/Footer';

function App() {
  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      <Header />
      <main className="flex-1 flex flex-col">
        <ChatInterface />
      </main>
      <Footer />
    </div>
  );
}

export default App;