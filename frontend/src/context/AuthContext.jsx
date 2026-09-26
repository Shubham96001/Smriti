import { createContext, useContext, useEffect, useState } from 'react';
import { authService } from '../services/authService';
import { TOKEN_KEY } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(Boolean(localStorage.getItem(TOKEN_KEY)));

  useEffect(() => {
    if (!localStorage.getItem(TOKEN_KEY)) return;
    authService.me().then(setUser).catch(() => {
      localStorage.removeItem(TOKEN_KEY);
      setUser(null);
    }).finally(() => setLoading(false));
  }, []);

  const authenticate = async (request) => {
    const response = await request;
    localStorage.setItem(TOKEN_KEY, response.access_token);
    setUser(response.user);
    return response.user;
  };

  const value = {
    user,
    loading,
    register: (data) => authenticate(authService.register(data)),
    login: (data) => authenticate(authService.login(data)),
    logout: () => {
      localStorage.removeItem(TOKEN_KEY);
      setUser(null);
    },
  };
  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used inside AuthProvider');
  return context;
}