import { useCallback, useEffect, useRef, useState } from 'react';
import { enqueueOfflineRecord } from '../offline/queue';
import { gameService } from '../services/gameService';

export function useGameSession(gameId = 'memory_match') {
  const [session, setSession] = useState(null);
  const [error, setError] = useState('');
  const pending = useRef([]);

  useEffect(() => {
    let active = true;
    gameService.start(gameId).then((value) => { if (active) setSession(value); }).catch((reason) => { if (active) setError(reason.message); });
    return () => { active = false; };
  }, [gameId]);

  const flush = useCallback(async () => {
    if (!pending.current.length) return;
    const events = pending.current.splice(0);
    if (!navigator.onLine || !session) {
      await Promise.all(events.map((event) => enqueueOfflineRecord({ resource_type: 'game_event', payload: { session_id: session?.id, ...event } })));
      return;
    }
    try {
      await gameService.events(session.id, events);
    } catch (reason) {
      pending.current.unshift(...events);
      throw reason;
    }
  }, [session]);

  useEffect(() => {
    const timer = window.setInterval(() => { flush().catch(() => {}); }, 1500);
    return () => window.clearInterval(timer);
  }, [flush]);

  const recordEvent = useCallback((event_type, payload = {}) => {
    pending.current.push({ event_id: crypto.randomUUID(), event_type, payload });
  }, []);

  const complete = useCallback(async (result) => {
    await flush();
    if (!session) return;
    if (!navigator.onLine) {
      await enqueueOfflineRecord({ resource_type: 'game_complete', payload: { session_id: session.id, result } });
      return;
    }
    await gameService.complete(session.id, result);
  }, [flush, session]);

  return { session, error, recordEvent, flush, complete };
}