import { createContext, useContext, useEffect } from 'react';
import { flushOfflineQueue } from './queue';

const OfflineContext = createContext({ flush: async () => 0 });

export function OfflineProvider({ children }) {
  useEffect(() => {
    const sync = () => flushOfflineQueue().catch(() => {});
    window.addEventListener('online', sync);
    if (navigator.onLine) sync();
    return () => window.removeEventListener('online', sync);
  }, []);
  return <OfflineContext.Provider value={{ flush: flushOfflineQueue }}>{children}</OfflineContext.Provider>;
}

export function useOffline() {
  return useContext(OfflineContext);
}