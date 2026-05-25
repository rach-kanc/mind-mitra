import React, { createContext, useState, useContext } from 'react';

type AppContextType = {
  darkMode: boolean;
  setDarkMode: (v: boolean) => void;
  userName: string;
};

export const AppContext = createContext<AppContextType>({
  darkMode: false,
  setDarkMode: () => {},
  userName: 'Alex',
});

export const AppProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [darkMode, setDarkMode] = useState(false);
  const [userName] = useState('Alex');
  return (
    <AppContext.Provider value={{ darkMode, setDarkMode, userName }}>
      {children}
    </AppContext.Provider>
  );
};

export const useAppContext = () => useContext(AppContext); 