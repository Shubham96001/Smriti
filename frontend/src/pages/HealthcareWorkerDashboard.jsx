import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function HealthcareWorkerDashboard() {
  const { user, logout } = useAuth();
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link><button className="button secondary" onClick={logout}>Sign out</button></header><section className="panel stack" style={{ marginTop: 32 }}><p className="eyebrow">Healthcare worker</p><h1>Welcome, {user?.full_name}</h1><p className="muted">Patient information is available only after a patient has approved a scoped access request.</p><p>No approved patient scopes are currently connected to this account.</p></section></main>;
}