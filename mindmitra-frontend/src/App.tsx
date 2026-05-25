
import { AppProvider } from './context/AppContext';
import MindMitraApp from './components/MindMitraApp';

export default function App() {
  return (
    <AppProvider>
      <MindMitraApp />
    </AppProvider>
  );
}
