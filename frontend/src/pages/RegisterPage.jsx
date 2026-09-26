import { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useLocale } from '../context/LocaleContext';
import LanguageSwitcher from '../components/LanguageSwitcher';

export default function RegisterPage() {
  const { register } = useAuth();
  const { locale, setLocale, t } = useLocale();
  const navigate = useNavigate();
  const [role, setRole] = useState('patient');
  const [error, setError] = useState('');
  const [busy, setBusy] = useState(false);
  const submit = async (event) => {
    event.preventDefault();
    setBusy(true);
    setError('');
    const form = new FormData(event.currentTarget);
    const submittedRole = form.get('role');
    const body = Object.fromEntries(form.entries());
    body.consent_acknowledged = form.get('consent_acknowledged') === 'on';
    for (const key of ['date_of_birth', 'gender', 'contact_phone', 'relationship_type']) if (!body[key]) body[key] = null;
    try {
      await register(body);
      navigate(submittedRole === 'patient' ? '/assessment/rudas' : submittedRole === 'caregiver' ? '/caregiver' : '/healthcare-worker', { replace: true });
    } catch (reason) { setError(reason.message); } finally { setBusy(false); }
  };
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link><div className="actions"><LanguageSwitcher /><Link to="/login">{t('signIn')}</Link></div></header>
    <section className="panel stack" style={{ maxWidth: 720, margin: '32px auto' }}><p className="eyebrow">{t('getStarted')}</p><h1>{t('createAccount')}</h1>
      <form className="stack" onSubmit={submit}><div className="form-grid">
        <label className="field">{t('role')}<select name="role" value={role} onChange={(event) => setRole(event.target.value)}><option value="patient">{t('patient')}</option><option value="caregiver">{t('caregiver')}</option><option value="hcw">{t('healthcareWorker')}</option></select></label>
        <label className="field">{t('fullName')}<input name="full_name" autoComplete="name" required maxLength="255" /></label>
        <label className="field">{t('email')}<input type="email" name="email" autoComplete="email" required /></label>
        <label className="field">{t('password')}<input type="password" name="password" autoComplete="new-password" minLength="8" required /></label>
        <label className="field">{t('dateOfBirth')}<input type="date" name="date_of_birth" /></label>
        <label className="field">{t('phone')}<input type="tel" name="contact_phone" /></label>
        {role === 'caregiver' && <label className="field">{t('relationshipToPatient')}<select name="relationship_type" required><option value="">{t('relationshipToPatient')}</option><option value="spouse">{locale === 'en' ? 'Spouse' : locale === 'hi' ? 'जीवनसाथी' : 'जोडीदार'}</option><option value="child">{locale === 'en' ? 'Child' : locale === 'hi' ? 'बेटा/बेटी' : 'मुलगा/मुलगी'}</option><option value="other">{locale === 'en' ? 'Other family member' : locale === 'hi' ? 'परिवार का अन्य सदस्य' : 'कुटुंबातील इतर सदस्य'}</option></select></label>}
        <label className="field">{t('preferredLanguage')}<select name="preferred_language" value={locale} onChange={(event) => setLocale(event.target.value)}><option value="en">English</option><option value="hi">हिन्दी</option><option value="mr">मराठी</option></select></label>
      </div>
      <label className="field"><span><input type="checkbox" name="consent_acknowledged" required /> {t('consent')}</span></label>
      {error && <p role="alert" className="notice">{error}</p>}<button className="button" disabled={busy}>{busy ? t('creatingAccount') : t('createAccount')}</button></form>
    </section>
  </main>;
}