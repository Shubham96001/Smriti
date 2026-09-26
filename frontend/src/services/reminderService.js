import { apiFetch } from './api';

export const reminderService = {
  list: () => apiFetch('/api/reminders'),
  create: (body) => apiFetch('/api/reminders', { method: 'POST', body }),
};