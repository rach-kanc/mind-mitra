import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const SplashScreen: React.FC = () => {
  const navigate = useNavigate();
  useEffect(() => {
    const timer = setTimeout(() => navigate('/login'), 3000);
    return () => clearTimeout(timer);
  }, [navigate]);
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-100 via-purple-50 to-pink-100 flex items-center justify-center">
      <div className="text-center">
        <div className="mb-8 relative">
          <div className="text-6xl mb-4 animate-pulse">🌊</div>
          <h1 className="text-4xl font-bold text-gray-800 mb-2">MindMitra</h1>
          <p className="text-gray-600 text-lg">"Your companion for emotional wellness"</p>
        </div>
        <div className="flex space-x-2 justify-center mb-6">
          <div className="w-3 h-3 bg-blue-500 rounded-full animate-bounce"></div>
          <div className="w-3 h-3 bg-purple-500 rounded-full animate-bounce delay-100"></div>
          <div className="w-3 h-3 bg-pink-500 rounded-full animate-bounce delay-200"></div>
        </div>
      </div>
    </div>
  );
};

export default SplashScreen; 