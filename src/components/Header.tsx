import React from 'react';
import { MessageCircle, Menu } from 'lucide-react';

const Header: React.FC = () => {
  return (
    <header className="bg-white border-b-2 border-gent-primary sticky top-0 z-50">
      {/* Top bar */}
      <div className="gent-gradient">
        <div className="max-w-7xl mx-auto px-4 py-2">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="hidden md:block text-white text-sm">
                AI Assistant Platform
              </div>
            </div>
            <div className="text-white text-sm hidden md:block">
              assistant.app
            </div>
          </div>
        </div>
      </div>

      {/* Main navigation */}
      <div className="bg-white">
        <div className="max-w-7xl mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="flex items-center space-x-3">
                <div className="w-12 h-12 bg-gent-primary rounded-lg flex items-center justify-center">
                  <MessageCircle className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-heading font-semibold text-gent-dark-gray">
                    AI Assistant
                  </h1>
                  <p className="text-sm text-gent-gray">
                    Your intelligent helper
                  </p>
                </div>
              </div>
            </div>
            
            <div className="hidden md:flex items-center space-x-6">
              <div className="flex items-center space-x-2 text-sm text-gent-gray">
                <div className="w-2 h-2 bg-green-500 rounded-full"></div>
                <span>Online</span>
              </div>
              <button className="md:hidden">
                <Menu className="w-6 h-6 text-gent-primary" />
              </button>
            </div>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;