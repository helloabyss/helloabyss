import { parseHeader, verifyHeaderChain } from '@satscompute/core';
import { useState } from 'react';
import { Banner, Button, Card, Screen, T, ToggleRow } from '../src/components/ui';
import { useApp } from '../src/state/store';
import { colors } from '../src/theme';

/** Public Esplora API. Any Esplora instance works; we verify the data, so we don't trust it. */
const ESPLORA = 'https://mempool.space/api';
const DEPTH = 6;

interface Result {
  ok: boolean;
  tipHash: string;
  tipTime: number;
  checked: number;
}

async function fetchRecentHeaders(n: number): Promise<string[]> {
  const get = async (path: string) => {
    const r = await fetch(`${ESPLORA}${path}`);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    return (await r.text()).trim();
  };
  let hash = await get('/blocks/tip/hash');
  const headers: string[] = [];
  for (let i = 0; i < n; i++) {
    const hex = await get(`/block/${hash}/header`);
    headers.unshift(hex);
    hash = parseHeader(hex).prevHash;
  }
  return headers;
}

export default function BitcoinMode() {
  const on = useApp((s) => s.bitcoinMode);
  const setOn = useApp((s) => s.setBitcoinMode);
  const [busy, setBusy] = useState(false);
  const [res, setRes] = useState<Result | null>(null);
  const [err, setErr] = useState<string | null>(null);

  const run = async () => {
    setBusy(true);
    setErr(null);
    try {
      const hs = await fetchRecentHeaders(DEPTH);
      const v = verifyHeaderChain(hs);
      const tip = parseHeader(hs[hs.length - 1]!);
      setRes({ ok: v.ok, tipHash: tip.hash, tipTime: tip.time, checked: hs.length });
    } catch (e) {
      setErr((e as Error).message);
    } finally {
      setBusy(false);
    }
  };

  return (
    <Screen>
      <Card>
        <T v="heading">What this does</T>
        <T v="small">
          Downloads the last {DEPTH} Bitcoin block headers and checks the proof-of-work and chain links on your phone. It's a small way to verify the network yourself
          instead of trusting someone else's word.
        </T>
        <T v="small">It is not mining, earns nothing, and doesn't strengthen the network. Running a full or pruned node does — that's planned for the desktop agent.</T>
        <ToggleRow label="Show Bitcoin mode on the dashboard" value={on} onChange={setOn} />
      </Card>
      <Button title="Verify latest blocks" loading={busy} onPress={() => void run()} />
      {err && <Banner tone="danger" text={`Couldn't fetch headers: ${err}`} />}
      {res && (
        <Card tone={res.ok ? 'accent' : 'danger'}>
          <T v="heading" style={{ color: res.ok ? colors.positive : colors.danger }}>
            {res.ok ? `✓ ${res.checked} headers verified` : 'Verification failed'}
          </T>
          <T v="small">Tip mined {new Date(res.tipTime * 1000).toLocaleString()}</T>
          <T v="mono" selectable>
            {res.tipHash}
          </T>
        </Card>
      )}
    </Screen>
  );
}
