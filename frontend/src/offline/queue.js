import { withPendingStore } from './db';
import { apiFetch } from '../services/api';

export async function enqueueOfflineRecord(record) {
  const id = record.client_record_id || crypto.randomUUID();
  await withPendingStore('readwrite', (store) => store.put({ ...record, client_record_id: id, id }));
}

export async function flushOfflineQueue() {
  const records = await withPendingStore('readonly', (store) => store.getAll());
  if (!records?.length) return 0;
  await apiFetch('/api/sync', { method: 'POST', body: { records } });
  await withPendingStore('readwrite', (store) => store.clear());
  return records.length;
}