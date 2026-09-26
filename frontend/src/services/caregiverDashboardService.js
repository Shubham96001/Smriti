import { apiFetch } from './api';

export const caregiverDashboardService = {
  patients: () => apiFetch('/api/caregivers/relationships'),
  activity: (patientId) => apiFetch(`/api/caregivers/patients/${patientId}/activity`),
};