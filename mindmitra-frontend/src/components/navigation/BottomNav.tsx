import React from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Home, Camera, BookOpen, BarChart3, User } from 'lucide-react';

const navItems = [
  { icon: Home, path: '/home', label: 'Home' },
  { icon: Camera, path: '/emotion', label: 'Detect' },
  { icon: BookOpen, path: '/journal', label: 'Journal' },
  { icon: BarChart3, path: '/trends', label: 'Trends' },
  { icon: User, path: '/profile', label: 'Profile' },
];

const BottomNav: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  return (
    <div className={`fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 px-6 py-3`}> {/* Add dark mode if needed */}
      <div className="flex justify-around max-w-md mx-auto">
        {navItems.map(({ icon: Icon, path, label }) => (
          <button
            key={path}
            onClick={() => navigate(path)}
            className={`flex flex-col items-center space-y-1 p-2 rounded-lg transition-colors duration-300 ${
              location.pathname === path ? 'text-blue-500' : 'text-gray-600 hover:text-gray-800'
            }`}
          >
            <Icon className="w-5 h-5" />
            <span className="text-xs">{label}</span>
          </button>
        ))}
      </div>
    </div>
  );
};

export default BottomNav; 