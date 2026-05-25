import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';
import { AlertCircle, Sun, Moon, Settings } from 'lucide-react';

const ProfileScreen: React.FC = () => {
  const { darkMode, setDarkMode, userName } = useContext(AppContext);
  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} p-6`}>
      <div className="max-w-md mx-auto">
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg mb-6 text-center`}>
          <div className="w-20 h-20 bg-gradient-to-r from-blue-500 to-purple-600 rounded-full flex items-center justify-center text-white text-2xl font-bold mx-auto mb-4">
            {userName[0]}
          </div>
          <h3 className={`text-xl font-bold ${darkMode ? 'text-white' : 'text-gray-800'}`}>{userName} Doe</h3>
          <p className={`${darkMode ? 'text-gray-300' : 'text-gray-600'}`}>alex@email.com</p>
        </div>
        <div className="space-y-3">
          <button className={`w-full ${darkMode ? 'bg-gray-800 text-white' : 'bg-white'} p-4 rounded-xl shadow-lg text-left hover:scale-105 transition-transform duration-300`}>
            <div className="flex items-center">
              <AlertCircle className="w-5 h-5 mr-3 text-red-500" />
              <span>Edit Emergency Contacts</span>
            </div>
          </button>
          <button 
            onClick={() => setDarkMode(!darkMode)}
            className={`w-full ${darkMode ? 'bg-gray-800 text-white' : 'bg-white'} p-4 rounded-xl shadow-lg text-left hover:scale-105 transition-transform duration-300`}
          >
            <div className="flex items-center">
              {darkMode ? <Sun className="w-5 h-5 mr-3 text-yellow-500" /> : <Moon className="w-5 h-5 mr-3 text-blue-500" />}
              <span>Theme: {darkMode ? 'Dark' : 'Light'}</span>
            </div>
          </button>
          <button
            onClick={() => window.location.href = '/login'}
            className={`w-full ${darkMode ? 'bg-gray-800 text-white' : 'bg-white'} p-4 rounded-xl shadow-lg text-left hover:scale-105 transition-transform duration-300`}
          >
            <div className="flex items-center">
              <Settings className="w-5 h-5 mr-3 text-gray-500" />
              <span>Log out</span>
            </div>
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProfileScreen; 