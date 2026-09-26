import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { caregiverService } from '../services/caregiverService';

export default function ApprovalsPage() {
  const [items, setItems] = useState([]); const [error, setError] = useState('');
  const load = () => caregiverService.approvals().then(setItems).catch((reason) => setError(reason.message));
  useEffect(() => { load(); }, []);
  const decide = async (id, approved) => { try { await caregiverService.decide(id, approved); await load(); } catch (reason) { setError(reason.message); } };
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/patient">SmritiSaathi</Link><Link to="/patient">Dashboard</Link></header><section className="stack" style={{ marginTop: 28 }}><p className="eyebrow">Shared support</p><h1>Caregiver approvals</h1><p className="muted">Review each request before sharing access to your information.</p>{error && <p className="notice" role="alert">{error}</p>}
    {items.map((item) => <article className="panel actions" key={item.id}><strong>{item.caregiver_name}</strong><button className="button" onClick={() => decide(item.id, true)}>Approve</button><button className="button secondary" onClick={() => decide(item.id, false)}>Decline</button></article>)}{!items.length && <p className="muted">No pending requests.</p>}
  </section></main>;
}