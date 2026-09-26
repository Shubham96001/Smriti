import { apiFetch } from './api';

export const authService = {
  register: (data) => apiFetch('/api/auth/register', { method: 'POST', body: data }),
  login: (data) => apiFetch('/api/auth/login', { method: 'POST', body: data }),
  me: () => apiFetch('/api/auth/me'),
};