import React from 'react';
import { useNavigate } from 'react-router-dom';

const LoginScreen: React.FC = () => {
  const navigate = useNavigate();
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center p-4">
      <div className="bg-white rounded-2xl shadow-xl p-8 w-full max-w-md">
        <div className="text-center mb-8">
          <div className="text-4xl mb-4">🌊</div>
          <h2 className="text-2xl font-bold text-gray-800">Welcome to MindMitra</h2>
        </div>
        <div className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <input
            type="password"
            placeholder="Password"
            className="w-full p-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={() => navigate('/home')}
            className="w-full bg-gradient-to-r from-blue-500 to-purple-600 text-white py-3 rounded-lg font-medium hover:from-blue-600 hover:to-purple-700 transition-all duration-300"
          >
            Login
          </button>
          <button className="w-full bg-white border-2 border-gray-300 py-3 rounded-lg font-medium hover:bg-gray-50 transition-all duration-300">
            Sign in with Google
          </button>
          <p className="text-center text-blue-500 text-sm cursor-pointer hover:underline">
            Forgot password?
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginScreen; 