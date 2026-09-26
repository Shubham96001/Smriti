import { Volume2 } from 'lucide-react';
import { useSpeech } from '../hooks/useSpeech';

export default function VoiceButton({ text }) {
  const { speak, supported } = useSpeech();
  return <button type="button" className="icon-button" aria-label="Read this page aloud" title="Read aloud" disabled={!supported} onClick={() => speak(text)}><Volume2 size={20} /></button>;
}