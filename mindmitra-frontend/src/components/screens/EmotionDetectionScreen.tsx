import React, { useState, useContext } from 'react';
import { Camera, Heart } from 'lucide-react';
import { AppContext } from '../../context/AppContext';

const EmotionDetectionScreen: React.FC = () => {
  const { darkMode } = useContext(AppContext);
  const [isRecording, setIsRecording] = useState(false);
  return (
    <div className={`min-h-screen ${darkMode ? 'bg-gray-900' : 'bg-gray-50'} p-6`}>
      <div className="max-w-md mx-auto">
        <h2 className={`text-2xl font-bold mb-6 text-center ${darkMode ? 'text-white' : 'text-gray-800'}`}>Emotion Detection</h2>
        <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg mb-6`}>
          <div className="aspect-square bg-gray-200 rounded-lg flex items-center justify-center mb-4 relative overflow-hidden">
            {isRecording ? (
              <div className="absolute inset-0 bg-blue-500 opacity-20 animate-pulse" />
            ) : null}
            <Camera className="w-16 h-16 text-gray-400" />
          </div>
          <button
            onClick={() => setIsRecording(!isRecording)}
            className={`w-full py-3 rounded-lg font-medium transition-all duration-300 ${
              isRecording ? 'bg-red-500 hover:bg-red-600 text-white' : 'bg-blue-500 hover:bg-blue-600 text-white'
            }`}
          >
            {isRecording ? 'Stop Analysis' : 'Start Analysis'}
          </button>
        </div>
        {isRecording && (
          <div className={`${darkMode ? 'bg-gray-800' : 'bg-white'} rounded-xl p-6 shadow-lg text-center`}>
            <div className="animate-bounce mb-4">
              <div className="w-16 h-16 bg-gradient-to-r from-blue-400 to-purple-600 rounded-full mx-auto flex items-center justify-center">
                <Heart className="w-8 h-8 text-white animate-pulse" />
              </div>
            </div>
            <p className={`text-lg font-medium ${darkMode ? 'text-white' : 'text-gray-800'}`}>Detected Emotion: Anxious 😟</p>
            <div className="flex space-x-3 mt-4">
              <button
                onClick={() => setIsRecording(false)}
                className="flex-1 py-2 bg-gray-500 hover:bg-gray-600 text-white rounded-lg"
              >
                Try Again
              </button>
              <button className="flex-1 py-2 bg-green-500 hover:bg-green-600 text-white rounded-lg">
                Save Result
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EmotionDetectionScreen; 