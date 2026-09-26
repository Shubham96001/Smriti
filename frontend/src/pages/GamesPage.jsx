import { Link } from 'react-router-dom';
import MemoryMatchGame from '../games/MemoryMatch/MemoryMatchGame';

export default function GamesPage() {
  return <main className="page-shell"><header className="topbar"><Link className="brand" to="/patient">SmritiSaathi</Link><Link to="/patient">Dashboard</Link></header><section className="stack" style={{ marginTop: 28 }}><p className="eyebrow">Games</p><h1>Memory Match</h1><p className="muted">Find matching pairs at your own pace.</p><MemoryMatchGame /></section></main>;
}