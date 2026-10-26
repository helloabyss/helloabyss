import type { EngineSnapshot } from '@satscompute/core';
import { useEffect, useState } from 'react';
import { getRuntime, type Runtime } from './runtime';

export interface EngineView {
  runtime: Runtime | null;
  snap: EngineSnapshot | null;
  error: string | null;
  retry: () => void;
}

export function useEngine(): EngineView {
  const [runtime, setRuntime] = useState<Runtime | null>(null);
  const [snap, setSnap] = useState<EngineSnapshot | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [attempt, setAttempt] = useState(0);

  useEffect(() => {
    let unsub: (() => void) | undefined;
    let alive = true;
    getRuntime()
      .then((rt) => {
        if (!alive) return;
        setRuntime(rt);
        setError(null);
        unsub = rt.engine.subscribe(setSnap);
      })
      .catch((e: Error) => alive && setError(e.message));
    return () => {
      alive = false;
      unsub?.();
    };
  }, [attempt]);

  return { runtime, snap, error, retry: () => setAttempt((n) => n + 1) };
}
