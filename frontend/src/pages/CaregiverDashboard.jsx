import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { caregiverDashboardService } from '../services/caregiverDashboardService';
import { caregiverService } from '../services/caregiverService';

export default function CaregiverDashboard() {
  const { user, logout } = useAuth(); const navigate = useNavigate();
  const [patients, setPatients] = useState([]); const [error, setError] = useState('');
  const load = () => caregiverDashboardService.patients().then(setPatients).catch((reason) => setError(reason.message));
  useEffect(() => { load(); }, []);
  const submit = async (event) => { event.preventDefault(); setError(''); const form = new FormData(event.currentTarget); try { await caregiverService.request(form.get('patient_email')); event.currentTarget.reset(); await load(); } catch (reason) { setError(reason.message); } };
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link><div className="actions"><span>{user?.full_name}</span><button className="button secondary" onClick={() => { logout(); navigate('/'); }}>Sign out</button></div></header><section className="stack" style={{ marginTop: 28 }}><p className="eyebrow">Caregiver space</p><h1>People you support</h1>
    <form className="panel actions" onSubmit={submit}><label className="field" style={{ flex: 1 }}>Patient email<input type="email" name="patient_email" required /></label><button className="button">Request access</button></form>
    {error && <p className="notice" role="alert">{error}</p>}{patients.map((patient) => <article className="item-row" key={patient.id}><h2>{patient.full_name}</h2><p className="muted">Access: {patient.status}</p>{patient.status === 'approved' && <Link to={`/caregiver/patients/${patient.id}`}>View permitted activity</Link>}</article>)}
  </section></main>;
}