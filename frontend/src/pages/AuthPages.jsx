import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Heart, ArrowLeft } from 'lucide-react';
import { apiFetch } from '../lib/api';

function AuthLayout({ title, description, children, onBack }) {
  return (
    <div className="container" style={{ maxWidth: '760px', paddingTop: '2rem', paddingBottom: '3rem' }}>
      <div className="card flex-col gap-lg" style={{ background: '#fff' }}>
        <div className="flex items-center gap-md" style={{ justifyContent: 'space-between' }}>
          <button className="btn btn-secondary" type="button" onClick={onBack} style={{ minWidth: 'auto', padding: '0.7rem 1rem' }}>
            <ArrowLeft size={18} />
            Back
          </button>
          <div className="flex items-center gap-sm" style={{ color: 'var(--color-primary)' }}>
            <Heart size={24} />
            <strong>SmritiSaathi</strong>
          </div>
        </div>

        <div className="text-center">
          <h1 className="title" style={{ marginBottom: '0.5rem' }}>{title}</h1>
          <p className="text-muted">{description}</p>
        </div>

        {children}
      </div>
    </div>
  );
}

function buildPatientPayload(formData) {
  return {
    email: formData.get('email'),
    password: formData.get('password'),
    full_name: formData.get('full_name'),
    date_of_birth: formData.get('date_of_birth') || null,
    gender: formData.get('gender') || null,
    preferred_language: formData.get('preferred_language') || 'en',
    contact_phone: formData.get('contact_phone') || null,
    address: formData.get('address') || null,
    emergency_contact_name: formData.get('emergency_contact_name') || null,
    emergency_contact_phone: formData.get('emergency_contact_phone') || null,
    consent_acknowledged: formData.get('consent_acknowledged') === 'on',
    caregiver_invitation_code: formData.get('caregiver_invitation_code') || null,
  };
}

function buildCaregiverPayload(formData) {
  return {
    email: formData.get('email'),
    password: formData.get('password'),
    full_name: formData.get('full_name'),
    contact_phone: formData.get('contact_phone') || null,
    relationship_type: formData.get('relationship_type') || null,
    consent_acknowledged: formData.get('consent_acknowledged') === 'on',
  };
}

function saveAuthSession(response) {
  localStorage.setItem('smritisaathi_token', response.access_token);
  localStorage.setItem(
    'smritisaathi_user',
    JSON.stringify({
      user_id: response.user_id,
      role: response.role,
      full_name: response.full_name,
      baseline_completed: response.baseline_completed,
    })
  );
}

export function PatientRegistrationPage() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formData = new FormData(event.currentTarget);
      const payload = buildPatientPayload(formData);
      const response = await apiFetch('/api/auth/register/patient', {
        method: 'POST',
        body: payload,
      });
      saveAuthSession(response);
      navigate(response.baseline_completed === false ? '/assessment' : '/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Register as Patient" description="Create your account and complete the first-time baseline check." onBack={() => navigate('/')}>
      <form className="flex-col gap-md" onSubmit={handleSubmit}>
        <div className="grid grid-cols-2" style={{ gap: '1rem' }}>
          <label className="flex-col gap-sm"><span>Full name</span><input name="full_name" required /></label>
          <label className="flex-col gap-sm"><span>Email</span><input type="email" name="email" required /></label>
          <label className="flex-col gap-sm"><span>Password</span><input type="password" name="password" minLength="8" required /></label>
          <label className="flex-col gap-sm"><span>Phone</span><input name="contact_phone" /></label>
          <label className="flex-col gap-sm"><span>Date of birth</span><input type="date" name="date_of_birth" /></label>
          <label className="flex-col gap-sm"><span>Gender</span><select name="gender"><option value="">Select</option><option value="female">Female</option><option value="male">Male</option><option value="other">Other</option></select></label>
          <label className="flex-col gap-sm"><span>Preferred language</span><input name="preferred_language" defaultValue="en" /></label>
          <label className="flex-col gap-sm"><span>Caregiver code</span><input name="caregiver_invitation_code" /></label>
        </div>

        <label className="flex-col gap-sm"><span>Address</span><textarea name="address" rows="3" /></label>
        <div className="grid grid-cols-2" style={{ gap: '1rem' }}>
          <label className="flex-col gap-sm"><span>Emergency contact</span><input name="emergency_contact_name" /></label>
          <label className="flex-col gap-sm"><span>Emergency phone</span><input name="emergency_contact_phone" /></label>
        </div>

        <label className="flex gap-sm items-center">
          <input type="checkbox" name="consent_acknowledged" required />
          <span>I agree to the terms and understand the app is for support and monitoring.</span>
        </label>

        {error ? <div className="card" style={{ border: '1px solid var(--color-error)', color: 'var(--color-error)', background: '#FEE2E2' }}>{error}</div> : null}

        <button className="btn btn-primary" disabled={loading} type="submit">
          {loading ? 'Creating account...' : 'Register patient'}
        </button>
      </form>
    </AuthLayout>
  );
}

export function CaregiverRegistrationPage() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    setLoading(true);
    setError('');

    try {
      const formData = new FormData(event.currentTarget);
      const payload = buildCaregiverPayload(formData);
      const response = await apiFetch('/api/auth/register/caregiver', {
        method: 'POST',
        body: payload,
      });
      saveAuthSession(response);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Register as Caregiver" description="Create a caregiver account to monitor loved ones and their routines." onBack={() => navigate('/')}>
      <form className="flex-col gap-md" onSubmit={handleSubmit}>
        <div className="grid grid-cols-2" style={{ gap: '1rem' }}>
          <label className="flex-col gap-sm"><span>Full name</span><input name="full_name" required /></label>
          <label className="flex-col gap-sm"><span>Email</span><input type="email" name="email" required /></label>
          <label className="flex-col gap-sm"><span>Password</span><input type="password" name="password" minLength="8" required /></label>
          <label className="flex-col gap-sm"><span>Phone</span><input name="contact_phone" /></label>
          <label className="flex-col gap-sm"><span>Relationship</span><input name="relationship_type" placeholder="Daughter / Son / Spouse" /></label>
        </div>

        <label className="flex gap-sm items-center">
          <input type="checkbox" name="consent_acknowledged" required />
          <span>I consent to caregiver access and understand the data access rules.</span>
        </label>

        {error ? <div className="card" style={{ border: '1px solid var(--color-error)', color: 'var(--color-error)', background: '#FEE2E2' }}>{error}</div> : null}

        <button className="btn btn-primary" disabled={loading} type="submit">
          {loading ? 'Creating caregiver account...' : 'Register caregiver'}
        </button>
      </form>
    </AuthLayout>
  );
}

export function PatientLoginPage() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setLoading(true);
    setError('');

    try {
      const response = await apiFetch('/api/auth/login', {
        method: 'POST',
        body: {
          email: formData.get('email'),
          password: formData.get('password'),
        },
      });

      saveAuthSession(response);
      navigate(response.baseline_completed === false ? '/assessment' : '/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Patient Login" description="Sign in to continue your cognitive routine and view updates." onBack={() => navigate('/')}>
      <form className="flex-col gap-md" onSubmit={handleSubmit}>
        <label className="flex-col gap-sm"><span>Email</span><input type="email" name="email" required /></label>
        <label className="flex-col gap-sm"><span>Password</span><input type="password" name="password" required /></label>
        {error ? <div className="card" style={{ border: '1px solid var(--color-error)', color: 'var(--color-error)', background: '#FEE2E2' }}>{error}</div> : null}
        <button className="btn btn-primary" type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Login'}</button>
      </form>
    </AuthLayout>
  );
}

export function CaregiverLoginPage() {
  const navigate = useNavigate();
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    setLoading(true);
    setError('');

    try {
      const response = await apiFetch('/api/auth/login', {
        method: 'POST',
        body: {
          email: formData.get('email'),
          password: formData.get('password'),
        },
      });

      saveAuthSession(response);
      navigate('/dashboard');
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <AuthLayout title="Caregiver Login" description="Access your caregiver dashboard and patient overview." onBack={() => navigate('/')}>
      <form className="flex-col gap-md" onSubmit={handleSubmit}>
        <label className="flex-col gap-sm"><span>Email</span><input type="email" name="email" required /></label>
        <label className="flex-col gap-sm"><span>Password</span><input type="password" name="password" required /></label>
        {error ? <div className="card" style={{ border: '1px solid var(--color-error)', color: 'var(--color-error)', background: '#FEE2E2' }}>{error}</div> : null}
        <button className="btn btn-primary" type="submit" disabled={loading}>{loading ? 'Signing in...' : 'Login'}</button>
      </form>
    </AuthLayout>
  );
}
