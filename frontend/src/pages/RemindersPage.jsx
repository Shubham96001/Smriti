import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { reminderService } from '../services/reminderService';

export default function RemindersPage() {
  const [items, setItems] = useState([]); const [error, setError] = useState('');
  const load = () => reminderService.list().then(setItems).catch((reason) => setError(reason.message));
  useEffect(() => { load(); }, []);
  const submit = async (event) => { event.preventDefault(); setError(''); const form = new FormData(event.currentTarget); try { await reminderService.create({ title: form.get('title'), description: form.get('description'), remind_at: new Date(form.get('remind_at')).toISOString(), recurrence: form.get('recurrence') }); event.currentTarget.reset(); await load(); } catch (reason) { setError(reason.message); } };
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/patient">SmritiSaathi</Link><Link to="/patient">Dashboard</Link></header><section className="stack" style={{ marginTop: 28 }}><p className="eyebrow">Daily routine</p><h1>Reminders</h1>
    <form className="panel stack" onSubmit={submit}><label className="field">Reminder<input name="title" required maxLength="160" /></label><label className="field">Details<input name="description" maxLength="1000" /></label><label className="field">Date and time<input type="datetime-local" name="remind_at" required /></label><label className="field">Repeat<select name="recurrence"><option value="once">Once</option><option value="daily">Daily</option><option value="weekly">Weekly</option></select></label><button className="button">Add reminder</button></form>
    {error && <p className="notice" role="alert">{error}</p>}{items.map((item) => <article className="item-row" key={item.id}><h2>{item.title}</h2><p>{item.description}</p><time className="muted">{new Date(item.remind_at).toLocaleString()}</time></article>)}
  </section></main>;
}