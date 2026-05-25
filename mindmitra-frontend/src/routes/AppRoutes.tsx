import React from 'react';
import { Routes, Route, Outlet, useLocation } from 'react-router-dom';
import SplashScreen from '../components/screens/SplashScreen';
import LoginScreen from '../components/screens/LoginScreen';
import HomeScreen from '../components/screens/HomeScreen';
import JournalScreen from '../components/screens/JournalScreen';
import ChatScreen from '../components/screens/ChatScreen';
import EmotionDetectionScreen from '../components/screens/EmotionDetectionScreen';
import SOSScreen from '../components/screens/SOSScreen';
import ProfileScreen from '../components/screens/ProfileScreen';
import TrendsScreen from '../components/screens/TrendsScreen';
import BottomNav from '../components/navigation/BottomNav';

const MainLayout: React.FC = () => {
  const location = useLocation();
  // Hide BottomNav on splash and login
  const hideNav = location.pathname === '/' || location.pathname === '/login';
  return (
    <>
      <Outlet />
      {!hideNav && <BottomNav />}
    </>
  );
};

const AppRoutes: React.FC = () => (
  <Routes>
    <Route path="/" element={<SplashScreen />} />
    <Route path="/login" element={<LoginScreen />} />
    <Route element={<MainLayout />}>
      <Route path="/home" element={<HomeScreen />} />
      <Route path="/journal" element={<JournalScreen />} />
      <Route path="/chat" element={<ChatScreen />} />
      <Route path="/emotion" element={<EmotionDetectionScreen />} />
      <Route path="/sos" element={<SOSScreen />} />
      <Route path="/profile" element={<ProfileScreen />} />
      <Route path="/trends" element={<TrendsScreen />} />
    </Route>
  </Routes>
);

export default AppRoutes; 