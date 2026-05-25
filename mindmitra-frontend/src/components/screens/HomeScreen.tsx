import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Moon, Sun, BookOpen, MessageCircle, AlertCircle } from 'lucide-react';
import { AppContext } from '../../context/AppContext';

const HomeScreen: React.FC = () => {
  const navigate = useNavigate();
  const { darkMode, setDarkMode, userName } = useContext(AppContext);
  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} transition-colors duration-300`}>
      <div className="p-6">
        <div className="flex justify-between items-center mb-6">
          <div>
            <h1 className={`text-2xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>Hi, {userName} 👋</h1>
            <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'} mt-1`}>😊 You seem calm today</p>
          </div>
          <button
            onClick={() => setDarkMode(!darkMode)}
            className="p-2 rounded-full bg-gray-200 dark:bg-gray-700"
          >
            {darkMode ? <Sun className="w-5 h-5" /> : <Moon className="w-5 h-5" />}
          </button>
        </div>
        <div className="grid grid-cols-2 gap-4 mb-6">
          <button
            onClick={() => navigate('/journal')}
            className="bg-gradient-to-r from-green-400 to-blue-500 text-white p-6 rounded-xl shadow-lg hover:scale-105 transition-transform duration-300"
          >
            <BookOpen className="w-8 h-8 mb-2 mx-auto" />
            <p className="font-medium">New Journal Entry</p>
          </button>
          <button
            onClick={() => navigate('/chat')}
            className="bg-gradient-to-r from-purple-400 to-pink-500 text-white p-6 rounded-xl shadow-lg hover:scale-105 transition-transform duration-300"
          >
            <MessageCircle className="w-8 h-8 mb-2 mx-auto" />
            <p className="font-medium">AI Chatbot</p>
          </button>
        </div>
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-4 shadow-lg mb-6`}>
          <h3 className={`font-medium mb-3 ${darkMode ? 'text-white' : 'text-gray-800'}`}>Mood Trend</h3>
          <div className="h-32 flex items-end space-x-2">
            {[4, 3, 5, 2, 4, 5, 3].map((height, i) => (
              <div
                key={i}
                className="bg-gradient-to-t from-blue-500 to-purple-500 rounded-t flex-1"
                style={{ height: `${height * 20}%` }}
              />
            ))}
          </div>
        </div>
      </div>
      <div className="fixed bottom-6 right-6">
        <button
          onClick={() => navigate('/sos')}
          className="bg-red-500 hover:bg-red-600 text-white w-16 h-16 rounded-full shadow-2xl flex items-center justify-center animate-pulse"
        >
          <AlertCircle className="w-8 h-8" />
        </button>
      </div>
      {/* BottomNav will be included in AppRoutes layout */}
    </div>
  );
};

export default HomeScreen; 