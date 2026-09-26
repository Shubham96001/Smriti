import { apiFetch } from './api';

export const memoryService = {
  list: () => apiFetch('/api/memory'),
  create: (body) => apiFetch('/api/memory', { method: 'POST', body }),
};