import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';

export default function HealthCheckPage() {
  const [health, setHealth] = useState('Checking…');
  useEffect(() => { fetch('/api/health').then((response) => response.json()).then((data) => setHealth(`${data.api}: API · ${data.database}: database`)).catch(() => setHealth('Service unavailable')); }, []);
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/">SmritiSaathi</Link></header><section className="panel" style={{ marginTop: 32 }}><h1>Service status</h1><p>{health}</p></section></main>;
}