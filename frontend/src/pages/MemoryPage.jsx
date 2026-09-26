import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { memoryService } from '../services/memoryService';

export default function MemoryPage() {
  const [items, setItems] = useState([]); const [error, setError] = useState(''); const [busy, setBusy] = useState(false);
  const load = () => memoryService.list().then(setItems).catch((reason) => setError(reason.message));
  useEffect(() => { load(); }, []);
  const submit = async (event) => { event.preventDefault(); setBusy(true); setError(''); const form = new FormData(event.currentTarget); try { await memoryService.create({ title: form.get('title'), body: form.get('body') }); event.currentTarget.reset(); await load(); } catch (reason) { setError(reason.message); } finally { setBusy(false); } };
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/patient">SmritiSaathi</Link><Link to="/patient">Dashboard</Link></header><section className="stack" style={{ marginTop: 28 }}><p className="eyebrow">Memory notes</p><h1>Keep a note close</h1>
    <form className="panel stack" onSubmit={submit}><label className="field">Title<input name="title" required maxLength="160" /></label><label className="field">Details<textarea name="body" maxLength="4000" /></label><button className="button" disabled={busy}>Add note</button></form>
    {error && <p className="notice" role="alert">{error}</p>}<div>{items.map((item) => <article className="item-row" key={item.id}><h2>{item.title}</h2><p className="muted">{item.body}</p></article>)}</div>
  </section></main>;
}