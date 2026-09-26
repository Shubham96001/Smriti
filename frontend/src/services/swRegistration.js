export async function registerServiceWorker() {
  if (!('serviceWorker' in navigator) || !import.meta.env.PROD) return null;
  return navigator.serviceWorker.register('/sw.js');
}