import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { assessmentService } from '../services/assessmentService';
import { apiFetch } from '../services/api';

export default function PatientDashboard() {
  const { user, logout } = useAuth(); const navigate = useNavigate();
  const [summary, setSummary] = useState(null); const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    assessmentService.status().then((status) => {
      if (!status.baseline_completed) navigate('/assessment/rudas', { replace: true });
      else return apiFetch('/api/ai/summary').then((data) => { if (active) setSummary(data); });
    }).catch((reason) => { if (active) setError(reason.message); });
    return () => { active = false; };
  }, [navigate]);
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link><div className="actions"><span>Hello, {user?.full_name}</span><button className="button secondary" onClick={() => { logout(); navigate('/'); }}>Sign out</button></div></header>
    <section className="hero-band"><p className="eyebrow">Your space</p><h1 className="hero-title">A little structure for today.</h1><p className="muted" style={{ marginTop: 14 }}>Choose what would be helpful right now.</p></section>
    <nav className="link-grid"><Link className="link-tile" to="/games">Play a game <span>→</span></Link><Link className="link-tile" to="/memory">Memory notes <span>→</span></Link><Link className="link-tile" to="/reminders">Reminders <span>→</span></Link><Link className="link-tile" to="/approvals">Caregiver approvals <span>→</span></Link></nav>
    <section className="panel stack" style={{ marginTop: 22 }}><h2>Recent activity</h2>{error ? <p role="alert">{error}</p> : summary ? <p className="muted">{summary.games_completed} games completed · {summary.memory_items} memory notes · {summary.active_reminders} active reminders</p> : <p className="muted">Loading activity…</p>}</section>
  </main>;
}