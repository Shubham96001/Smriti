import { useCallback } from 'react';

export function useSpeech() {
  const supported = typeof window !== 'undefined' && 'speechSynthesis' in window;
  const speak = useCallback((text) => {
    if (!supported) return;
    window.speechSynthesis.cancel();
    window.speechSynthesis.speak(new SpeechSynthesisUtterance(text));
  }, [supported]);
  return { speak, supported };
}