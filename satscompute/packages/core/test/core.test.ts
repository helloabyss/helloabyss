import { describe, expect, it } from 'vitest';
import {
  bitsToTarget,
  bolt11AmountMsat,
  checkTaskFit,
  contributionStreak,
  createDefaultRegistry,
  defaultPolicy,
  embed,
  evaluateGuardrails,
  isInQuietHours,
  outputHash,
  parseDestination,
  parseHeader,
  projectSatsPerHour,
  sampleTask,
  selectTask,
  splitReward,
  verifyHeaderChain,
  AnalyticsBuffer,
  type ContributionPolicy,
  type DeviceProfile,
  type DeviceState,
  type LedgerEntry,
  type QueuedTask,
} from '../src';

const profile: DeviceProfile = {
  deviceClass: 'phone',
  platform: 'android',
  cpuCores: 8,
  memoryMb: 6144,
  hasGpu: false,
  benchmarkUnitsPerSec: 150,
  appVersion: 'test',
};

const goodState = (over: Partial<DeviceState> = {}): DeviceState => ({
  batteryLevel: 0.9,
  isCharging: true,
  isLowPowerMode: false,
  thermal: 'nominal',
  batteryTempC: 30,
  network: 'wifi',
  isMetered: false,
  isUserIdle: true,
  now: new Date('2026-10-26T02:00:00'),
  ...over,
});

const onPolicy = (over: Partial<ContributionPolicy> = {}): ContributionPolicy => ({ ...defaultPolicy('phone'), enabled: true, ...over });

describe('guardrails', () => {
  it('is off by default', () => {
    expect(evaluateGuardrails(goodState(), defaultPolicy()).reasons).toContain('disabled');
  });

  it('allows a safe, charging, idle device on Wi-Fi', () => {
    const v = evaluateGuardrails(goodState(), onPolicy());
    expect(v.allowed).toBe(true);
    expect(v.dutyCycle).toBeCloseTo(0.4);
  });

  it.each([
    [{ isCharging: false }, 'not-charging'],
    [{ thermal: 'serious' as const }, 'thermal'],
    [{ thermal: 'critical' as const }, 'thermal'],
    [{ batteryTempC: 41 }, 'battery-hot'],
    [{ network: 'cellular' as const }, 'not-wifi'],
    [{ network: 'none' as const }, 'no-network'],
    [{ isLowPowerMode: true }, 'low-power-mode'],
    [{ isUserIdle: false }, 'user-active'],
    [{ batteryLevel: 0.5 }, 'battery-low'],
  ])('blocks %o', (over, reason) => {
    const v = evaluateGuardrails(goodState(over), onPolicy());
    expect(v.allowed).toBe(false);
    expect(v.reasons).toContain(reason);
  });

  it('derates when warm or when the thermal sensor is unavailable', () => {
    expect(evaluateGuardrails(goodState({ thermal: 'fair' }), onPolicy()).dutyCycle).toBeCloseTo(0.24);
    const u = evaluateGuardrails(goodState({ thermal: 'unknown' }), onPolicy());
    expect(u.allowed).toBe(true);
    expect(u.reasons).toContain('thermal-unknown-throttled');
    expect(u.dutyCycle).toBeCloseTo(0.2);
  });

  it('handles quiet hours across midnight', () => {
    const p = onPolicy({ quietHours: { enabled: true, start: '22:00', end: '06:00' } });
    expect(isInQuietHours(p, new Date('2026-10-26T23:30:00'))).toBe(true);
    expect(isInQuietHours(p, new Date('2026-10-26T05:59:00'))).toBe(true);
    expect(isInQuietHours(p, new Date('2026-10-26T06:00:00'))).toBe(false);
  });

  it('rejects tasks that would run too long on a phone', () => {
    const t = sampleTask('embedding', goodState().now);
    t.requirements.workUnits = 1_000_000;
    const fit = checkTaskFit(t, profile, goodState(), onPolicy(), 0.4);
    expect(fit).toEqual({ ok: false, reason: 'too-long' });
  });
});

describe('executors + proof', () => {
  const ctx = { signal: new AbortController().signal, checkpoint: async () => {} };

  it('embeddings are deterministic and quantised', () => {
    const a = embed('hello lightning world');
    expect(a).toEqual(embed('hello lightning world'));
    expect(a).toHaveLength(256);
    expect(a.every((x) => Number.isInteger(x) && x >= -127 && x <= 127)).toBe(true);
  });

  it('replicas produce identical hashes; verification detects a forged hash', async () => {
    const reg = createDefaultRegistry();
    const t = sampleTask('classification');
    const ex = reg.get('classification')!;
    const out = await ex.run(ex.parse(t.input), ctx);
    const out2 = await ex.run(ex.parse(t.input), ctx);
    expect(outputHash(t.id, t.kind, out)).toBe(outputHash(t.id, t.kind, out2));
    expect((out as { labels: string[] }).labels[3]).toBe('refund');

    const v = reg.get('verification')!;
    const target = { taskId: t.id, kind: t.kind, input: t.input };
    expect(await v.run(v.parse({ target, claimedHash: outputHash(t.id, t.kind, out) }), ctx)).toEqual({ match: true });
    expect(await v.run(v.parse({ target, claimedHash: 'deadbeef' }), ctx)).toEqual({ match: false });
  });

  it('filter drops short lines and near-duplicates', async () => {
    const ex = createDefaultRegistry().get('filter')!;
    const out = (await ex.run(ex.parse(sampleTask('filter').input), ctx)) as { keep: number[]; dropped: Record<string, number> };
    expect(out.dropped.short).toBe(2);
    expect(out.dropped.duplicate).toBeGreaterThanOrEqual(1);
  });
});

describe('scheduler', () => {
  it('never gives one device two replicas and honours premium gating', () => {
    const now = new Date();
    const mk = (over: Partial<QueuedTask>): QueuedTask => ({ ...sampleTask('embedding', now), assignedTo: [], postedAt: now.toISOString(), ...over });
    const req = {
      deviceId: 'd1',
      profile,
      allowedKinds: ['embedding' as const],
      dutyCycle: 0.4,
      thermal: 'nominal' as const,
      batteryLevel: 0.9,
      isCharging: true,
      network: 'wifi' as const,
      entitlements: { priorityBoostUntil: null, premiumTasks: false },
    };
    const mine = mk({ assignedTo: ['d1'] });
    const premium = mk({ premium: true, rewardMsat: 10_000_000 });
    const open = mk({});
    expect(selectTask([mine, premium, open], req, now)?.id).toBe(open.id);
  });
});

describe('fees + estimator', () => {
  it('rounds the fee in the user’s favour', () => {
    expect(splitReward(999, 'standard')).toEqual({ netMsat: 800, feeMsat: 199 });
  });

  it('returns an ordered range, never a single figure', () => {
    const r = projectSatsPerHour(profile, 0.4, { msatPerUnit: 2, utilization: { p10: 0.1, p50: 0.4, p90: 0.8 }, btcUsd: null, asOf: '' }, 'standard');
    expect(r.low).toBeLessThan(r.mid);
    expect(r.mid).toBeLessThan(r.high);
  });
});

describe('lightning destinations', () => {
  it('parses addresses, lnurl and invoices', () => {
    expect(parseDestination('Alice@Wallet.Example.com').type).toBe('lightning-address');
    expect(parseDestination('lightning:LNURL1DP68GURN8GHJ7').type).toBe('lnurl');
    const inv = parseDestination('lnbc2500u1pvjluezpp5qqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqqqsyqcyq5rqwzqfqypq');
    expect(inv).toMatchObject({ type: 'bolt11', network: 'mainnet', amountMsat: 250_000_000 });
    expect(() => parseDestination('not a wallet')).toThrow();
  });

  it('converts bolt11 amounts', () => {
    expect(bolt11AmountMsat('1m')).toBe(100_000_000);
    expect(bolt11AmountMsat('10n')).toBe(1_000);
    expect(bolt11AmountMsat('10p')).toBe(1);
  });
});

describe('bitcoin header verification', () => {
  const GENESIS =
    '0100000000000000000000000000000000000000000000000000000000000000000000003ba3edfd7a7b12b27ac72c3e67768f617fc81bc3888a51323a9fb8aa4b1e5e4a29ab5f49ffff001d1dac2b7c';

  it('verifies the genesis block proof-of-work', () => {
    const h = parseHeader(GENESIS);
    expect(h.hash).toBe('000000000019d6689c085ae165831e934ff763ae46a2a6c172b3f1b60a8ce26f');
    expect(bitsToTarget(0x1d00ffff)).toBe(0xffffn << 208n);
    expect(verifyHeaderChain([GENESIS]).ok).toBe(true);
  });

  it('rejects a tampered header', () => {
    expect(verifyHeaderChain([GENESIS.slice(0, -2) + '00']).ok).toBe(false);
  });
});

describe('gamification + analytics', () => {
  it('counts a streak through yesterday', () => {
    const at = (d: string): LedgerEntry => ({ id: d, kind: 'task', amountMsat: 1000, feeMsat: 0, status: 'accepted', at: `${d}T12:00:00` });
    const ledger = [at('2026-10-23'), at('2026-10-24'), at('2026-10-25')];
    expect(contributionStreak(ledger, new Date('2026-10-26T07:00:00'))).toBe(3);
    expect(contributionStreak(ledger, new Date('2026-10-28T07:00:00'))).toBe(0);
  });

  it('records nothing without consent and never includes identifiers', () => {
    let consent = false;
    const a = new AnalyticsBuffer(() => consent, { appVersion: '1', platform: 'ios' });
    a.track({ type: 'payout', ok: true });
    expect(a.flush()).toBeNull();
    consent = true;
    a.track({ type: 'task_completed', kind: 'embedding', sats: 3, busyMs: 1200 });
    const r = a.flush()!;
    expect(Object.keys(r).sort()).toEqual(['appVersion', 'counters', 'platform', 'schema', 'week']);
    expect(r.counters['task.sats.<5']).toBe(1);
  });
});

describe('lnurl', () => {
  it('decodes the LUD-01 example', async () => {
    const { decodeLnurl } = await import('../src');
    expect(
      decodeLnurl('LNURL1DP68GURN8GHJ7UM9WFMXJCM99E3K7MF0V9CXJ0M385EKVCENXC6R2C35XVUKXEFCV5MKVV34X5EKZD3EV56NYD3HXQURZEPEXEJXXEPNXSCRVWFNV9NXZCN9XQ6XYEFHVGCXXCMYXYMNSERXFQ5FNS'),
    ).toBe('https://service.com/api?q=3fc3645b439ce8e7f2553a69e5267081d96dcd340693afabe04be7b0ccd178df');
  });
});
