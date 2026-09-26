import { createContext, useContext, useMemo, useState } from 'react';
import en from '../locales/en';
import hi from '../locales/hi';
import mr from '../locales/mr';

const messages = { en, hi, mr };
const LocaleContext = createContext(null);

export function LocaleProvider({ children }) {
  const [locale, setLocale] = useState(() => localStorage.getItem('smritisaathi_locale') || 'en');
  const value = useMemo(() => ({
    locale,
    setLocale: (next) => {
      localStorage.setItem('smritisaathi_locale', next);
      setLocale(next);
    },
    t: (key, vars = {}) => Object.entries(vars).reduce(
      (text, [name, replacement]) => text.replaceAll(`{${name}}`, replacement),
      messages[locale]?.[key] || en[key] || key,
    ),
  }), [locale]);
  return <LocaleContext.Provider value={value}>{children}</LocaleContext.Provider>;
}

export function useLocale() {
  const context = useContext(LocaleContext);
  if (!context) throw new Error('useLocale must be used inside LocaleProvider');
  return context;
}