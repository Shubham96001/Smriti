import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { assessmentService } from '../services/assessmentService';

export default function RudasPage() {
  const navigate = useNavigate();
  const [session, setSession] = useState(null);
  const [index, setIndex] = useState(0);
  const [answer, setAnswer] = useState('');
  const [busy, setBusy] = useState(true);
  const [error, setError] = useState('');
  useEffect(() => {
    let active = true;
    assessmentService.status().then(async (status) => {
      if (status.baseline_completed) { navigate('/patient', { replace: true }); return; }
      const result = await assessmentService.start();
      if (active) { setSession(result); setIndex(Math.min(status.completed_items, result.items.length - 1)); }
    }).catch((reason) => { if (active) setError(reason.message); }).finally(() => { if (active) setBusy(false); });
    return () => { active = false; };
  }, [navigate]);
  const persist = async (leave = false) => {
    if (!session || !session.items[index] || !answer) return;
    setBusy(true); setError('');
    try {
      const result = await assessmentService.save({ session_id: session.session_id, item_id: session.items[index].id, response_text: answer });
      if (leave || result.completed) navigate('/patient', { replace: true });
      else { setIndex((current) => current + 1); setAnswer(''); }
    } catch (reason) { setError(reason.message); } finally { setBusy(false); }
  };
  if (busy && !session) return <main className="page-shell"><p>Loading assessment…</p></main>;
  const item = session?.items[index];
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/patient">SmritiSaathi</Link><span>{session ? `Item ${index + 1} of ${session.items.length}` : ''}</span></header>
    <section className="panel stack" style={{ maxWidth: 760, margin: '28px auto' }}><p className="eyebrow">Development placeholder · {session?.version || 'placeholder-v1'}</p><h1>Baseline activity</h1>
      <p className="notice">These are generic development placeholders, not the real RUDAS. This activity is not a diagnosis and does not measure or diagnose a medical condition.</p>
      {item && <><h2 style={{ fontSize: 30 }}>{item.prompt}</h2><div className="stack">{item.response_options.map((option) => <button key={option} type="button" className={`button ${answer === option ? '' : 'secondary'}`} style={{ minHeight: 68, justifyContent: 'flex-start', textAlign: 'left' }} aria-pressed={answer === option} onClick={() => setAnswer(option)}>{option}</button>)}</div></>}
      {error && <p role="alert" className="notice">{error}</p>}
      <div className="actions"><button className="button" disabled={busy || !answer} onClick={() => persist(false)}>{index === (session?.items.length || 1) - 1 ? 'Finish' : 'Save and next'}</button><button className="button secondary" disabled={busy || !answer} onClick={() => persist(true)}>Save &amp; finish later</button></div>
    </section>
  </main>;
}