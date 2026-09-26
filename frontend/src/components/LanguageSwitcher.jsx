import { useLocale } from '../context/LocaleContext';

export default function LanguageSwitcher() {
  const { locale, setLocale } = useLocale();
  return <label className="language-control"><span>Language</span><select value={locale} onChange={(event) => setLocale(event.target.value)}>
    <option value="en">English</option><option value="hi">हिन्दी</option><option value="mr">मराठी</option>
  </select></label>;
}