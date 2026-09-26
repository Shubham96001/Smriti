import { apiFetch } from './api';

export const caregiverService = {
  request: (patient_email) => apiFetch('/api/caregivers/relationships/request', { method: 'POST', body: { patient_email } }),
  relationships: () => apiFetch('/api/caregivers/relationships'),
  approvals: () => apiFetch('/api/caregivers/approvals'),
  decide: (id, approved) => apiFetch(`/api/caregivers/approvals/${id}`, { method: 'POST', body: { approved } }),
};