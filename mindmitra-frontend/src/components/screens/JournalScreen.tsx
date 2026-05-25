import React, { useState, useContext } from 'react';
import { AppContext } from '../../context/AppContext';

const JournalScreen: React.FC = () => {
  const { darkMode } = useContext(AppContext);
  const [currentMood, setCurrentMood] = useState(3);
  const [journalText, setJournalText] = useState('');
  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} p-6`}>
      <div className="max-w-md mx-auto">
        <h2 className={`text-2xl font-bold mb-6 text-center ${darkMode ? 'text-white' : 'text-gray-800'}`}>How are you feeling?</h2>
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg mb-6`}>
          <div className="flex justify-center items-center space-x-4 mb-6">
            <span className="text-2xl">😢</span>
            <input
              type="range"
              min="1"
              max="5"
              value={currentMood}
              onChange={e => setCurrentMood(Number(e.target.value))}
              className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer"
            />
            <span className="text-2xl">😊</span>
          </div>
          <div className="text-center mb-4">
            <span className="text-3xl">
              {currentMood === 1 ? '😢' : currentMood === 2 ? '😕' : currentMood === 3 ? '😐' : currentMood === 4 ? '🙂' : '😊'}
            </span>
          </div>
          <textarea
            value={journalText}
            onChange={e => setJournalText(e.target.value)}
            placeholder="Write about your mood..."
            className={`w-full h-32 p-3 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent ${darkMode ? 'bg-gray-700 text-white border-gray-600' : ''}`}
          />
          <button
            onClick={() => { setJournalText(''); }}
            className="w-full mt-4 bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-medium transition-all duration-300"
          >
            Save Entry
          </button>
        </div>
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg`}>
          <h3 className={`font-medium mb-3 ${darkMode ? 'text-white' : 'text-gray-800'}`}>Recent Entries</h3>
          <div className="grid grid-cols-7 gap-2">
            {Array.from({ length: 14 }, (_, i) => (
              <div
                key={i}
                className={`aspect-square rounded-lg flex items-center justify-center text-sm ${
                  i % 3 === 0 ? 'bg-green-100 text-green-600' :
                  i % 3 === 1 ? 'bg-yellow-100 text-yellow-600' :
                  'bg-red-100 text-red-600'
                }`}
              >
                {20 - i}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default JournalScreen; 