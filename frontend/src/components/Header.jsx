import React from 'react';

const Header = () => {
  return (
    <header className="bg-primary-700 text-white shadow-lg">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center">
              <span className="text-2xl">🏛️</span>
            </div>
            <div>
              <h1 className="text-xl font-bold">Stadt Rüsselsheim</h1>
              <p className="text-sm text-primary-100">Bürgerservice Assistent</p>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-4">
            <span className="text-sm text-primary-100">
              Powered by Claude AI
            </span>
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
