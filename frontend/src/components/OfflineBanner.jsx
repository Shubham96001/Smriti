import { useEffect, useState } from 'react';
import { useLocale } from '../context/LocaleContext';

export default function OfflineBanner() {
  const [online, setOnline] = useState(navigator.onLine);
  const { t } = useLocale();
  useEffect(() => {
    const onOnline = () => setOnline(true);
    const onOffline = () => setOnline(false);
    window.addEventListener('online', onOnline);
    window.addEventListener('offline', onOffline);
    return () => {
      window.removeEventListener('online', onOnline);
      window.removeEventListener('offline', onOffline);
    };
  }, []);
  return online ? null : <div className="offline-banner" role="status">{t('offline')}</div>;
}