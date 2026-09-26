import { useMemo, useState } from 'react';
import { useGameSession } from '../useGameSession';

const symbols = ['🌿', '☀️', '🪷', '🍎', '🪁', '🐦', '🌻', '🎵'];

export default function MemoryMatchGame() {
  const { session, error, recordEvent, complete } = useGameSession();
  const [opened, setOpened] = useState([]);
  const [matched, setMatched] = useState([]);
  const [moves, setMoves] = useState(0);
  const cards = useMemo(() => {
    if (!session) return [];
    const chosen = symbols.slice(0, Math.min(4, 2 + session.difficulty));
    return [...chosen, ...chosen].map((symbol, index) => ({ id: index, symbol })).sort((a, b) => a.id - b.id);
  }, [session]);

  const flip = (card) => {
    if (opened.length === 2 || opened.includes(card.id) || matched.includes(card.symbol)) return;
    const next = [...opened, card.id];
    setOpened(next);
    recordEvent('card_flipped', { card_id: card.id });
    if (next.length === 2) {
      setMoves((count) => count + 1);
      const first = cards.find((entry) => entry.id === next[0]);
      if (first.symbol === card.symbol) {
        const nextMatched = [...matched, card.symbol];
        setMatched(nextMatched);
        recordEvent('pair_matched', { symbol: card.symbol });
        if (nextMatched.length === cards.length / 2) complete({ moves: moves + 1, pairs: nextMatched.length }).catch(() => {});
        window.setTimeout(() => setOpened([]), 450);
      } else window.setTimeout(() => setOpened([]), 850);
    }
  };

  if (error) return <p role="alert">{error}</p>;
  if (!session) return <p>Preparing your game...</p>;
  return <section className="game-board" aria-label="Memory Match game">
    <p>Moves: {moves} · Matches: {matched.length} / {cards.length / 2}</p>
    <div className="memory-grid">{cards.map((card) => {
      const visible = opened.includes(card.id) || matched.includes(card.symbol);
      return <button key={card.id} type="button" className="memory-tile" aria-label={visible ? card.symbol : `Card ${card.id + 1}`} aria-pressed={visible} onClick={() => flip(card)}>{visible ? card.symbol : '?'}</button>;
    })}</div>
    {matched.length === cards.length / 2 && <p role="status">Game complete. Take a moment to celebrate.</p>}
  </section>;
}