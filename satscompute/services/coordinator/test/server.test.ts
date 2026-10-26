import { createDefaultRegistry, outputHash, type TaskSpec } from '@satscompute/core';
import { describe, expect, it } from 'vitest';
import { loadConfig } from '../src/config';
import { buildServer } from '../src/server';
import { createMemoryStore } from '../src/store';

process.env.NODE_ENV = 'test';
const executors = createDefaultRegistry();
const profile = { deviceClass: 'laptop', platform: 'linux', cpuCores: 8, memoryMb: 16384, hasGpu: false, benchmarkUnitsPerSec: 2000, appVersion: 't' };
const leaseBody = { allowedKinds: ['embedding', 'classification', 'filter'], dutyCycle: 0.6, thermal: 'nominal', batteryLevel: 1, isCharging: true, network: 'wifi' };

async function setup(over = {}) {
  const store = createMemoryStore();
  const app = buildServer({ store, config: loadConfig({ requesterApiKeys: ['rk_test'], payoutMinSats: 250, ...over }) });
  const register = async () => {
    const r = (await app.inject({ method: 'POST', url: '/v1/devices', payload: { profile } })).json();
    const headers = { authorization: `Bearer ${r.token}` };
    return { ...r, headers };
  };
  return { app, register, store };
}

async function work(task: TaskSpec, forge = false) {
  const ex = executors.get(task.kind)!;
  const output = await ex.run(ex.parse(task.input), { signal: new AbortController().signal, checkpoint: async () => {} });
  const bad = forge ? { vectors: [[1]] } : output;
  return { output: bad, hash: outputHash(task.id, task.kind, bad) };
}

describe('coordinator', () => {
  it('leases a sample task, house-verifies it and credits the account', async () => {
    const { app, register } = await setup();
    const d = await register();
    const { task } = (await app.inject({ method: 'POST', url: '/v1/tasks/lease', headers: d.headers, payload: leaseBody })).json();
    expect(task).toBeTruthy();
    const { output, hash } = await work(task);
    const res = await app.inject({
      method: 'POST',
      url: `/v1/tasks/${task.id}/result`,
      headers: d.headers,
      payload: { taskId: task.id, deviceId: d.deviceId, output, proof: { outputHash: hash, busyMs: 10, executorVersion: 'x' }, completedAt: new Date().toISOString() },
    });
    expect(res.json().outcome).toBe('accepted');
    const bal = (await app.inject({ url: '/v1/balance', headers: d.headers })).json();
    expect(bal.availableMsat).toBe(Math.ceil(task.rewardMsat * 0.8));
  });

  it('pays only the majority on a replicated requester task', async () => {
    const { app, register } = await setup({ seedSampleTasks: false });
    const post = await app.inject({
      method: 'POST',
      url: '/v1/requester/tasks',
      headers: { 'x-api-key': 'rk_test' },
      payload: { kind: 'embedding', explainer: 'Test', requester: 'Acme', workUnits: 100, rewardMsat: 50_000, input: { texts: ['a b c', 'd e f'] }, replication: 2 },
    });
    expect(post.statusCode).toBe(200);

    const devs = [await register(), await register(), await register()];
    const outcomes: string[] = [];
    // Device 0 honest, device 1 cheats (consistent but wrong), device 2 honest tie-breaker.
    for (const [i, d] of devs.entries()) {
      const { task } = (await app.inject({ method: 'POST', url: '/v1/tasks/lease', headers: d.headers, payload: leaseBody })).json();
      expect(task, `device ${i} got a task`).toBeTruthy();
      const { output, hash } = await work(task, i === 1);
      const r = await app.inject({
        method: 'POST',
        url: `/v1/tasks/${task.id}/result`,
        headers: d.headers,
        payload: { taskId: task.id, deviceId: d.deviceId, output, proof: { outputHash: hash, busyMs: 10, executorVersion: 'x' }, completedAt: '' },
      });
      outcomes.push(r.json().outcome);
    }
    expect(outcomes).toEqual(['pending-verification', 'pending-verification', 'accepted']);
    const bal = async (d: (typeof devs)[number]) => (await app.inject({ url: '/v1/balance', headers: d.headers })).json();
    expect((await bal(devs[0]!)).availableMsat).toBe(40_000);
    expect((await bal(devs[1]!)).availableMsat).toBe(0);
    expect((await bal(devs[1]!)).pendingMsat).toBe(0);
  });

  it('enforces the payout minimum, holds the fee budget and refunds failures', async () => {
    const { app, register, store } = await setup();
    const d = await register();
    store.accounts.get(d.accountId)!.availableMsat = 300_000;
    const before = (await app.inject({ url: '/v1/balance', headers: d.headers })).json().availableMsat;
    expect(before).toBeGreaterThan(260_000);

    const tooSmall = await app.inject({ method: 'POST', url: '/v1/payouts', headers: d.headers, payload: { destination: 'lnbc1pzzzz', amountSats: 100 } });
    expect(tooSmall.json().code).toBe('below-minimum');

    const failed = (await app.inject({ method: 'POST', url: '/v1/payouts', headers: d.headers, payload: { destination: 'lnbc1pzzzz', amountSats: 250 } })).json();
    expect(failed.status).toBe('failed');
    expect((await app.inject({ url: '/v1/balance', headers: d.headers })).json().availableMsat).toBe(before);

    const ok = (await app.inject({ method: 'POST', url: '/v1/payouts', headers: { ...d.headers, 'idempotency-key': 'k1' }, payload: { destination: 'lnbc1pqqqq', amountSats: 250 } })).json();
    expect(ok.status).toBe('succeeded');
    expect(ok.preimage).toMatch(/^[0-9a-f]{64}$/);
    const again = (await app.inject({ method: 'POST', url: '/v1/payouts', headers: { ...d.headers, 'idempotency-key': 'k1' }, payload: { destination: 'lnbc1pqqqq', amountSats: 250 } })).json();
    expect(again.id).toBe(ok.id);
    expect((await app.inject({ url: '/v1/balance', headers: d.headers })).json().availableMsat).toBe(before - 250_000);
  });

  it('rejects unauthenticated calls', async () => {
    const { app } = await setup();
    expect((await app.inject({ url: '/v1/balance' })).statusCode).toBe(401);
  });
});
