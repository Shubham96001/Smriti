import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLocale } from '../context/LocaleContext';
import LanguageSwitcher from '../components/LanguageSwitcher';

export default function LoginPage() {
  const { login } = useAuth();
  const { t } = useLocale();
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const submit = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    const form = new FormData(event.currentTarget);
    try {
      const user = await login({ email: form.get('email'), password: form.get('password') });
      navigate(user.role === 'patient' ? (user.baseline_completed ? '/patient' : '/assessment/rudas') : user.role === 'caregiver' ? '/caregiver' : '/healthcare-worker', { replace: true });
    } catch (reason) { setError(reason.message); } finally { setBusy(false); }
  };
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link><div className="actions"><LanguageSwitcher /><Link to="/register">{t('createAccount')}</Link></div></header>
    <section className="panel stack" style={{ maxWidth: 560, margin: '40px auto' }}><p className="eyebrow">{t('welcomeBack')}</p><h1>{t('signIn')}</h1>
      <form className="stack" onSubmit={submit}><label className="field">{t('email')}<input type="email" name="email" autoComplete="email" required /></label><label className="field">{t('password')}<input type="password" name="password" autoComplete="current-password" required /></label>
        {error && <p role="alert" className="notice">{error}</p>}<button className="button" disabled={busy}>{busy ? t('signingIn') : t('signIn')}</button></form>
      <p className="muted">{t('newHere')} <Link to="/register">{t('createAccount')}</Link></p>
    </section>
  </main>;
}