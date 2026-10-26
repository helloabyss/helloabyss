import type { EngineSnapshot } from '@satscompute/core';

export function phaseCopy(snap: EngineSnapshot | null): { label: string; tone: 'muted' | 'accent' | 'positive' | 'warn' } {
  switch (snap?.phase) {
    case 'running':
      return { label: 'Working', tone: 'positive' };
    case 'submitting':
      return { label: 'Submitting', tone: 'positive' };
    case 'waiting-for-work':
      return { label: 'Looking for work', tone: 'accent' };
    case 'blocked':
      return { label: 'Paused', tone: 'warn' };
    case 'backoff':
      return { label: 'Reconnecting', tone: 'warn' };
    default:
      return { label: 'Idle', tone: 'muted' };
  }
}
