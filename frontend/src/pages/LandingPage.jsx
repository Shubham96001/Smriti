import { ArrowRight, Heart } from 'lucide-react';
import { Link } from 'react-router-dom';
import LanguageSwitcher from '../components/LanguageSwitcher';
import VoiceButton from '../components/VoiceButton';
import { useLocale } from '../context/LocaleContext';

export default function LandingPage() {
  const { t } = useLocale();
  return <main className="page-shell">
    <header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link><div className="actions"><LanguageSwitcher /><Link className="button secondary" to="/login">{t('signIn')}</Link></div></header>
    <section className="hero-band">
      <p className="eyebrow">{t('heroEyebrow')}</p>
      <h1 className="hero-title">{t('heroTitle')}</h1>
      <p className="muted" style={{ maxWidth: 620, marginTop: 18 }}>{t('heroDescription')}</p>
      <div className="actions" style={{ marginTop: 28 }}><Link className="button" to="/register">{t('createAccount')} <ArrowRight size={18} /></Link><VoiceButton text={`${t('heroTitle')} ${t('disclaimer')}`} /></div>
    </section>
    <section className="link-grid" aria-label="What you can do">
      <div className="panel stack"><Heart color="var(--coral)" /><h2>Daily activities</h2><p className="muted">Practice at a comfortable pace with brief, approachable games.</p></div>
      <div className="panel stack"><h2>Memory notes</h2><p className="muted">Keep personal notes and familiar details in one place.</p></div>
      <div className="panel stack"><h2>Shared support</h2><p className="muted">Caregiver access stays under the patient’s approval.</p></div>
      <div className="panel stack"><h2>Gentle reminders</h2><p className="muted">Keep routine prompts visible throughout the day.</p></div>
    </section>
    <p className="notice" style={{ marginTop: 24 }}>SmritiSaathi is not a diagnostic medical system and does not provide a diagnosis.</p>
  </main>;
}
