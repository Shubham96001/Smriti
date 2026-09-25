import { useEffect, useState } from 'react';
import { Navigate, Link, useNavigate } from 'react-router-dom';
import { Brain, Bell, Heart, Users, LogOut } from 'lucide-react';
import { apiFetch } from '../lib/api';

function DashboardPage() {
  const navigate = useNavigate();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    const token = localStorage.getItem('smritisaathi_token');
    if (!token) {
      navigate('/');
      return;
    }

    const loadProfile = async () => {
      try {
        const data = await apiFetch('/api/auth/me');
        setProfile(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    loadProfile();
  }, [navigate]);

  const userSession = JSON.parse(localStorage.getItem('smritisaathi_user') || '{}');
  const isPatient = userSession.role === 'patient';

  if (!localStorage.getItem('smritisaathi_token')) {
    return <Navigate to="/" replace />;
  }

  const handleLogout = () => {
    localStorage.removeItem('smritisaathi_token');
    localStorage.removeItem('smritisaathi_user');
    navigate('/');
  };

  if (loading) {
    return <div className="container text-center" style={{ paddingTop: '4rem' }}><p className="subtitle">Loading your dashboard...</p></div>;
  }

  if (error) {
    return <div className="container text-center" style={{ paddingTop: '4rem' }}><p className="subtitle" style={{ color: 'var(--color-error)' }}>{error}</p></div>;
  }

  return (
    <div className="container flex-col gap-lg" style={{ paddingTop: '2rem', paddingBottom: '3rem' }}>
      <header className="card flex items-center justify-center" style={{ justifyContent: 'space-between' }}>
        <div className="flex items-center gap-md">
          <Heart size={28} color="var(--color-primary)" />
          <div>
            <h1 className="title" style={{ margin: 0, fontSize: '2rem' }}>SmritiSaathi Dashboard</h1>
            <p className="text-muted">Welcome back, {profile?.email || userSession.full_name || 'User'}</p>
          </div>
        </div>

        <button className="btn btn-secondary" type="button" onClick={handleLogout}>
          <LogOut size={18} /> Logout
        </button>
      </header>

      <div className="grid grid-cols-2 gap-lg">
        <div className="card flex-col gap-md">
          <div className="flex items-center gap-md">
            <Brain size={28} color="var(--color-secondary)" />
            <h2 className="subtitle" style={{ margin: 0 }}>Baseline status</h2>
          </div>
          <p className="text-muted">
            {isPatient
              ? userSession.baseline_completed === false
                ? 'Your first-time baseline RUDAS assessment is still required.'
                : 'Your baseline has been recorded and updated with later activity.'
              : 'Caregiver overview active.'}
          </p>
          {isPatient && userSession.baseline_completed === false ? (
            <Link to="/assessment" className="btn btn-primary btn-block">Start baseline assessment</Link>
          ) : (
            <Link to="/" className="btn btn-secondary btn-block">Return home</Link>
          )}
        </div>

        <div className="card flex-col gap-md">
          <div className="flex items-center gap-md">
            <Bell size={28} color="var(--color-primary-light)" />
            <h2 className="subtitle" style={{ margin: 0 }}>Daily routine</h2>
          </div>
          <p className="text-muted">Medication reminders, hydration cues, and memory prompts are available for the next activity cycle.</p>
          <button className="btn btn-secondary btn-block" type="button">View reminders</button>
        </div>

        <div className="card flex-col gap-md">
          <div className="flex items-center gap-md">
            <Users size={28} color="var(--color-primary)" />
            <h2 className="subtitle" style={{ margin: 0 }}>Caregiver support</h2>
          </div>
          <p className="text-muted">Caregivers can review schedules and assist with updates when consent is active.</p>
          <button className="btn btn-secondary btn-block" type="button">Manage access</button>
        </div>

        <div className="card flex-col gap-md">
          <div className="flex items-center gap-md">
            <Heart size={28} color="var(--color-success)" />
            <h2 className="subtitle" style={{ margin: 0 }}>Cognitive health</h2>
          </div>
          <p className="text-muted">Future game and activity data will be stored in the local PostgreSQL database for follow-up tracking.</p>
          <button className="btn btn-primary btn-block" type="button">Open activities</button>
        </div>
      </div>
    </div>
  );
}

export default DashboardPage;
