import { apiFetch } from './api';

export const assessmentService = {
  status: () => apiFetch('/api/assessments/rudas/status'),
  start: () => apiFetch('/api/assessments/rudas/start', { method: 'POST' }),
  save: (body) => apiFetch('/api/assessments/rudas', { method: 'POST', body }),
};