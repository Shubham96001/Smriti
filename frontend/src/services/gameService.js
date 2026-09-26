import { apiFetch } from './api';

export const gameService = {
  list: () => apiFetch('/api/games'),
  start: (game_id) => apiFetch('/api/games/sessions', { method: 'POST', body: { game_id } }),
  events: (sessionId, events) => apiFetch(`/api/games/sessions/${sessionId}/events`, { method: 'POST', body: { events } }),
  complete: (sessionId, result) => apiFetch(`/api/games/sessions/${sessionId}/complete`, { method: 'POST', body: { result } }),
};