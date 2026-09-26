const TOKEN_KEY = 'smritisaathi_token';

export async function apiFetch(path, options = {}) {
  if (!path.startsWith('/api/')) throw new Error('API requests must use /api/* paths');
  const { body, headers = {}, ...requestOptions } = options;
  const requestHeaders = new Headers(headers);
  const token = localStorage.getItem(TOKEN_KEY);
  if (token) requestHeaders.set('Authorization', `Bearer ${token}`);
  if (body !== undefined) requestHeaders.set('Content-Type', 'application/json');
  const response = await fetch(path, {
    ...requestOptions,
    headers: requestHeaders,
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json') ? await response.json() : null;
  if (!response.ok) throw new Error(payload?.detail || 'Request failed');
  return payload;
}

export { TOKEN_KEY };