import React, { useContext } from 'react';
import { AppContext } from '../../context/AppContext';

const TrendsScreen: React.FC = () => {
  const { darkMode } = useContext(AppContext);
  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} p-6`}>
      <div className="max-w-md mx-auto">
        <h2 className={`text-2xl font-bold mb-6 text-center ${darkMode ? 'text-white' : 'text-gray-800'}`}>Mood Trends</h2>
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg mb-6`}>
          <div className="h-48 flex items-end space-x-2 mb-4">
            {[4, 3, 5, 2, 4, 5, 3, 4, 2, 5, 4, 3, 5].map((height, i) => (
              <div
                key={i}
                className="bg-gradient-to-t from-blue-500 to-purple-500 rounded-t flex-1"
                style={{ height: `${height * 20}%` }}
              />
            ))}
          </div>
          <div className="flex justify-center space-x-3 mb-4">
            <button className="px-4 py-2 bg-blue-500 text-white rounded-lg text-sm">Week</button>
            <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">Month</button>
            <button className="px-4 py-2 bg-gray-200 text-gray-700 rounded-lg text-sm">Custom</button>
          </div>
          <button className="w-full bg-green-500 hover:bg-green-600 text-white py-3 rounded-lg font-medium transition-colors duration-300">
            Export/Share
          </button>
        </div>
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg`}>
          <h3 className={`font-medium mb-3 ${darkMode ? 'text-white' : 'text-gray-800'}`}>Insights</h3>
          <div className="space-y-3">
            <div className="p-3 bg-green-50 rounded-lg">
              <p className="text-sm text-green-700">📈 Your mood has improved 15% this week!</p>
            </div>
            <div className="p-3 bg-blue-50 rounded-lg">
              <p className="text-sm text-blue-700">🌅 You feel best in the mornings</p>
            </div>
            <div className="p-3 bg-yellow-50 rounded-lg">
              <p className="text-sm text-yellow-700">💭 Journaling helps boost your mood</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TrendsScreen; 