import { createHash, randomBytes, timingSafeEqual } from 'node:crypto';
import Fastify, { type FastifyReply, type FastifyRequest } from 'fastify';
import {
  applyPurchase,
  createDefaultRegistry,
  DestinationError,
  fetchInvoice,
  K_ANONYMITY,
  leasePriority,
  outputHash,
  parseDestination,
  PRODUCTS,
  resolvePayParams,
  revokePurchase,
  routingFeeLimit,
  SAMPLE_KINDS,
  sampleTask,
  selectTask,
  splitReward,
  type AnalyticsReport,
  type DeviceProfile,
  type LeaseQuery,
  type MarketQuote,
  type Payout,
  type ProductId,
  type QueuedTask,
  type TaskKind,
  type TaskResult,
} from '@satscompute/core';
import type { Config } from './config';
import { LightningPaymentError, LndRestProvider, MockLightningProvider, type LightningProvider } from './lightning/provider';
import { appendLedger, createMemoryStore, newAccount, type DeviceRecord, type Store } from './store';
import { proofMatchesOutput, verifyReplicas } from './verification';

export interface ServerDeps {
  config: Config;
  store?: Store;
  lightning?: LightningProvider;
  fetchImpl?: typeof fetch;
}

const SAMPLE_QUEUE_TARGET = 12;
const LEASE_SECONDS = 300;

export function buildServer({ config, store = createMemoryStore(), lightning, fetchImpl = fetch }: ServerDeps) {
  const app = Fastify({ logger: process.env.NODE_ENV !== 'test', bodyLimit: 2 * 1024 * 1024 });
  const ln: LightningProvider =
    lightning ??
    (config.lightning.provider === 'lnd'
      ? new LndRestProvider(config.lightning.restUrl, config.lightning.macaroonHex, fetchImpl)
      : new MockLightningProvider());
  const executors = createDefaultRegistry();
  const payoutLocks = new Set<string>();
  const idempotency = new Map<string, Payout>();
  /** `${taskId}|${deviceId}` -> lease expiry (ms). Expired leases free the replica slot. */
  const leases = new Map<string, number>();

  const hashToken = (t: string) => createHash('sha256').update(config.tokenPepper).update(t).digest('hex');

  // ------------------------------------------------------------------ helpers

  function auth(req: FastifyRequest): DeviceRecord {
    const h = req.headers.authorization ?? '';
    const token = h.startsWith('Bearer ') ? h.slice(7) : '';
    const id = token && store.devicesByToken.get(hashToken(token));
    const dev = id ? store.devices.get(id) : undefined;
    if (!dev) throw httpError(401, 'Unauthorized', 'unauthorized');
    dev.lastSeenAt = new Date().toISOString();
    return dev;
  }

  function account(dev: DeviceRecord) {
    return store.accounts.get(dev.accountId)!;
  }

  function sweep(now: Date) {
    for (const [key, exp] of leases) {
      if (exp > now.getTime()) continue;
      leases.delete(key);
      const [taskId, deviceId] = key.split('|') as [string, string];
      const t = store.queue.get(taskId);
      const submitted = store.results.get(taskId)?.some((r) => r.deviceId === deviceId);
      if (t && !submitted) t.assignedTo = t.assignedTo.filter((d) => d !== deviceId);
    }
  }

  function topUpSamples(now: Date) {
    if (!config.seedSampleTasks) return;
    for (const [id, t] of store.queue) if (Date.parse(t.leaseExpiresAt) < now.getTime()) store.queue.delete(id);
    let i = store.queue.size;
    while (store.queue.size < SAMPLE_QUEUE_TARGET) {
      const t = sampleTask(SAMPLE_KINDS[i++ % SAMPLE_KINDS.length]!, now, 3600);
      // Sample tasks are single-replica; the coordinator spot-checks them itself (houseVerify).
      store.queue.set(t.id, { ...t, replication: 1, assignedTo: [], postedAt: now.toISOString() });
    }
  }

  /** Coordinator re-executes the task itself. Used for every sample task, and a % of real ones. */
  async function houseVerify(task: QueuedTask, r: TaskResult): Promise<boolean> {
    const ex = executors.get(task.kind);
    if (!ex) return false;
    const out = await ex.run(ex.parse(task.input), { signal: new AbortController().signal, checkpoint: async () => {} });
    return outputHash(task.id, task.kind, out) === r.proof.outputHash;
  }

  /** Settle replicas. `close` removes the task; false is used to reject one bad submission only. */
  function settle(task: QueuedTask, accepted: string[], rejected: string[], close = true) {
    for (const deviceId of [...accepted, ...rejected]) {
      const dev = store.devices.get(deviceId);
      if (!dev) continue;
      const acct = account(dev);
      const ok = accepted.includes(deviceId);
      const { netMsat, feeMsat } = splitReward(task.rewardMsat, acct.entitlements.feeTier);
      // Pending was booked at submit time; move it to available or drop it.
      acct.pendingMsat = Math.max(0, acct.pendingMsat - netMsat);
      if (ok) {
        acct.availableMsat += netMsat;
        acct.lifetimeMsat += netMsat;
        acct.reputation = Math.min(1, acct.reputation + 0.01);
      } else {
        acct.reputation = Math.max(0, acct.reputation - 0.1);
      }
      const entry = (store.ledger.get(acct.id) ?? []).find((e) => e.taskId === task.id && e.kind === 'task');
      if (entry) {
        entry.status = ok ? 'accepted' : 'rejected';
        entry.amountMsat = ok ? netMsat : 0;
        entry.feeMsat = ok ? feeMsat : 0;
      }
    }
    if (!close) return;
    store.queue.delete(task.id);
    store.results.delete(task.id);
    for (const key of leases.keys()) if (key.startsWith(`${task.id}|`)) leases.delete(key);
  }

  // ------------------------------------------------------------------ routes

  app.setErrorHandler((err: Error & { statusCode?: number; code?: string }, _req, reply) => {
    const status = err.statusCode ?? (err instanceof DestinationError ? 422 : err.name === 'TaskInputError' ? 400 : 500);
    if (status >= 500) app.log.error(err);
    reply.status(status).send({ error: status >= 500 ? 'Internal error' : err.message, code: err.code });
  });

  app.get('/healthz', async () => ({ ok: true, lightning: ln.name }));

  app.post('/v1/devices', async (req) => {
    const { profile } = (req.body ?? {}) as { profile?: DeviceProfile };
    if (!profile || !['phone', 'tablet', 'laptop', 'desktop'].includes(profile.deviceClass)) {
      throw httpError(400, 'profile.deviceClass required');
    }
    const id = `dev_${randomBytes(9).toString('base64url')}`;
    const token = randomBytes(32).toString('base64url');
    const accountId = `acct_${randomBytes(9).toString('base64url')}`;
    const now = new Date().toISOString();
    store.accounts.set(accountId, newAccount(accountId));
    store.devices.set(id, { id, tokenHash: hashToken(token), profile: sanitizeProfile(profile), accountId, createdAt: now, lastSeenAt: now });
    store.devicesByToken.set(hashToken(token), id);
    return { deviceId: id, accountId, token };
  });

  app.get('/v1/market', async (req): Promise<MarketQuote> => {
    const cls = (req.query as { deviceClass?: string }).deviceClass ?? 'phone';
    // Placeholder curve. In production: derived from the trailing 7d of leases per device class.
    const util = cls === 'phone' ? { p10: 0.1, p50: 0.35, p90: 0.7 } : { p10: 0.2, p50: 0.5, p90: 0.85 };
    return { msatPerUnit: 2, utilization: util, btcUsd: config.btcUsdReference, asOf: new Date().toISOString() };
  });

  app.post('/v1/tasks/lease', async (req) => {
    const dev = auth(req);
    const q = req.body as LeaseQuery;
    const now = new Date();
    sweep(now);
    topUpSamples(now);
    const acct = account(dev);
    const leaseReq = { ...q, profile: dev.profile, deviceId: dev.id, entitlements: acct.entitlements };
    // Scarcity handling: when the queue is thin, un-boosted, unplugged devices wait a round.
    if (store.queue.size < 3 && leasePriority(leaseReq, now) < 1) return { task: null };
    const pick = selectTask([...store.queue.values()], leaseReq, now);
    if (!pick) return { task: null };
    pick.assignedTo.push(dev.id);
    const expires = Math.min(Date.parse(pick.leaseExpiresAt), now.getTime() + LEASE_SECONDS * 1000);
    leases.set(`${pick.id}|${dev.id}`, expires);
    const { assignedTo: _a, postedAt: _p, premium: _pr, ...spec } = pick;
    return { task: { ...spec, leaseExpiresAt: new Date(expires).toISOString() } };
  });

  app.post('/v1/tasks/:id/release', async (req, reply) => {
    const dev = auth(req);
    const t = store.queue.get((req.params as { id: string }).id);
    if (t) t.assignedTo = t.assignedTo.filter((d) => d !== dev.id);
    if (t) leases.delete(`${t.id}|${dev.id}`);
    return reply.status(204).send();
  });

  app.post('/v1/tasks/:id/result', async (req) => {
    const dev = auth(req);
    const acct = account(dev);
    const r = req.body as TaskResult;
    const task = store.queue.get((req.params as { id: string }).id);
    if (!task || !task.assignedTo.includes(dev.id) || r.deviceId !== dev.id) throw httpError(409, 'Task not leased to this device', 'not-leased');
    const results = store.results.get(task.id) ?? [];
    if (results.some((x) => x.deviceId === dev.id)) throw httpError(409, 'Already submitted', 'duplicate');

    const { netMsat, feeMsat } = splitReward(task.rewardMsat, acct.entitlements.feeTier);
    appendLedger(store, acct.id, {
      id: `le_${task.id}_${dev.id}`,
      kind: 'task',
      taskId: task.id,
      taskKind: task.kind,
      explainer: task.explainer,
      amountMsat: netMsat,
      feeMsat,
      outputHash: r.proof.outputHash,
      status: 'pending-verification',
      at: new Date().toISOString(),
    });
    acct.pendingMsat += netMsat;

    if (!proofMatchesOutput(task, r)) {
      // Reject this submission only; free the slot so an honest device can take it.
      settle(task, [], [dev.id], false);
      task.assignedTo = task.assignedTo.filter((d) => d !== dev.id);
      leases.delete(`${task.id}|${dev.id}`);
      return { outcome: 'rejected', creditedMsat: 0, pendingMsat: 0, feeMsat: 0 };
    }

    results.push(r);
    store.results.set(task.id, results);

    if (task.replication === 1) {
      const ok = await houseVerify(task, r);
      settle(task, ok ? [dev.id] : [], ok ? [] : [dev.id]);
      return ok ? { outcome: 'accepted', creditedMsat: netMsat, pendingMsat: 0, feeMsat } : { outcome: 'rejected', creditedMsat: 0, pendingMsat: 0, feeMsat: 0 };
    }

    const v = verifyReplicas(task, results);
    if (v.status === 'resolved') {
      settle(task, v.accepted, v.rejected);
      const ok = v.accepted.includes(dev.id);
      return { outcome: ok ? 'accepted' : 'rejected', creditedMsat: ok ? netMsat : 0, pendingMsat: 0, feeMsat: ok ? feeMsat : 0 };
    }
    if (v.status === 'escalate') task.replication++;
    return { outcome: 'pending-verification', creditedMsat: 0, pendingMsat: netMsat, feeMsat };
  });

  app.get('/v1/balance', async (req) => {
    const a = account(auth(req));
    return { availableMsat: a.availableMsat, pendingMsat: a.pendingMsat, lifetimeMsat: a.lifetimeMsat };
  });

  app.get('/v1/ledger', async (req) => {
    const dev = auth(req);
    return { entries: (store.ledger.get(dev.accountId) ?? []).slice(-500).reverse() };
  });

  app.post('/v1/payouts', async (req) => {
    const dev = auth(req);
    const acct = account(dev);
    const { destination, amountSats } = (req.body ?? {}) as { destination?: string; amountSats?: number };
    const idemKey = req.headers['idempotency-key'];
    if (typeof idemKey === 'string' && idempotency.has(`${acct.id}:${idemKey}`)) return idempotency.get(`${acct.id}:${idemKey}`);

    if (!destination || !Number.isInteger(amountSats)) throw httpError(400, 'destination and integer amountSats required');
    const amount = amountSats!;
    if (amount < config.payoutMinSats) throw httpError(400, `Minimum payout is ${config.payoutMinSats} sats`, 'below-minimum');
    const maxFee = routingFeeLimit(amount);
    if ((amount + maxFee) * 1000 > acct.availableMsat) {
      throw httpError(400, `Balance too low: ${amount} sats + up to ${maxFee} sats routing fee`, 'insufficient');
    }
    if (payoutLocks.has(acct.id)) throw httpError(409, 'A payout is already in progress', 'in-progress');

    payoutLocks.add(acct.id);
    const hold = (amount + maxFee) * 1000;
    acct.availableMsat -= hold;
    const payout: Payout & { accountId: string } = {
      id: `po_${randomBytes(9).toString('base64url')}`,
      accountId: acct.id,
      amountSats: amount,
      routingFeeSats: 0,
      destination,
      status: 'in-flight',
      createdAt: new Date().toISOString(),
    };
    store.payouts.set(payout.id, payout);
    try {
      const d = parseDestination(destination);
      let invoice: string;
      let amtForZeroInvoice: number | undefined;
      if (d.type === 'bolt11') {
        if (d.network !== 'mainnet' && config.lightning.provider !== 'mock') throw new DestinationError('Invoice is not for Bitcoin mainnet');
        if (d.amountMsat !== null && d.amountMsat !== amount * 1000) throw new DestinationError(`Invoice is for ${d.amountMsat / 1000} sats, not ${amount}`);
        if (d.amountMsat === null) amtForZeroInvoice = amount;
        invoice = d.value;
      } else {
        const params = await resolvePayParams(d, fetchImpl);
        invoice = await fetchInvoice(params, amount * 1000, 'SatsCompute payout', fetchImpl);
      }
      const res = await ln.payInvoice(invoice, { maxFeeSats: maxFee, amountSats: amtForZeroInvoice });
      // Return the unused part of the fee budget.
      acct.availableMsat += (maxFee - res.feeSats) * 1000;
      Object.assign(payout, { status: 'succeeded', routingFeeSats: res.feeSats, preimage: res.preimageHex, paymentHash: res.paymentHashHex });
      appendLedger(store, acct.id, {
        id: `le_${payout.id}`,
        kind: 'payout',
        amountMsat: -(amount + res.feeSats) * 1000,
        feeMsat: res.feeSats * 1000,
        status: 'paid',
        at: new Date().toISOString(),
      });
    } catch (e) {
      acct.availableMsat += hold;
      Object.assign(payout, { status: 'failed', error: (e as Error).message });
      if (!(e instanceof DestinationError) && !(e instanceof LightningPaymentError)) throw e;
    } finally {
      payoutLocks.delete(acct.id);
    }
    const { accountId: _acc, ...out } = payout;
    if (typeof idemKey === 'string') idempotency.set(`${acct.id}:${idemKey}`, out);
    return out;
  });

  app.get('/v1/payouts/:id', async (req) => {
    const dev = auth(req);
    const p = store.payouts.get((req.params as { id: string }).id);
    if (!p || p.accountId !== dev.accountId) throw httpError(404, 'Not found');
    const { accountId: _a, ...out } = p;
    return out;
  });

  app.get('/v1/entitlements', async (req) => account(auth(req)).entitlements);

  /**
   * RevenueCat webhook. The app sets RevenueCat appUserID = accountId, so purchases map to
   * accounts without the coordinator ever seeing store receipts or Apple/Google identities.
   */
  app.post('/v1/iap/revenuecat', async (req: FastifyRequest, reply: FastifyReply) => {
    if (!config.revenueCatSecret || !safeEqual(req.headers.authorization ?? '', `Bearer ${config.revenueCatSecret}`)) {
      throw httpError(401, 'Unauthorized');
    }
    const ev = (req.body as { event?: { type: string; app_user_id: string; product_id: string } }).event;
    const acct = ev && store.accounts.get(ev.app_user_id);
    const product = ev && PRODUCTS.find((p) => p.id === ev.product_id);
    if (!ev || !acct || !product) return reply.status(200).send({ ignored: true });
    const now = new Date();
    if (['INITIAL_PURCHASE', 'RENEWAL', 'NON_RENEWING_PURCHASE', 'UNCANCELLATION'].includes(ev.type)) {
      acct.entitlements = applyPurchase(acct.entitlements, product.id as ProductId, now);
    } else if (['EXPIRATION', 'REFUND' /* RevenueCat sends CANCELLATION with reason for refunds */].includes(ev.type)) {
      acct.entitlements = revokePurchase(acct.entitlements, product.id as ProductId);
    }
    return { ok: true };
  });

  /** Marketplace (v0): AI developers post paid work. Billing/escrow is out of scope for MVP. */
  app.post('/v1/requester/tasks', async (req) => {
    const key = req.headers['x-api-key'];
    if (typeof key !== 'string' || !config.requesterApiKeys.some((k) => safeEqual(k, key))) throw httpError(401, 'Unauthorized');
    const b = req.body as { kind: TaskKind; explainer: string; requester: string; input: unknown; workUnits: number; rewardMsat: number; replication?: number };
    const ex = executors.get(b.kind);
    if (!ex || b.kind === 'verification') throw httpError(400, `Unsupported kind ${b.kind}`);
    ex.parse(b.input); // throws TaskInputError → 400
    if (!(b.rewardMsat > 0) || !(b.workUnits > 0) || !b.explainer) throw httpError(400, 'rewardMsat, workUnits, explainer required');
    const now = new Date();
    const id = `t_req_${randomBytes(9).toString('base64url')}`;
    store.queue.set(id, {
      id,
      kind: b.kind,
      explainer: b.explainer.slice(0, 160),
      requester: b.requester.slice(0, 60),
      requirements: { minMemoryMb: 64, needsGpu: false, workUnits: b.workUnits, payloadKb: Math.ceil(JSON.stringify(b.input).length / 1024) },
      rewardMsat: Math.floor(b.rewardMsat),
      leaseExpiresAt: new Date(now.getTime() + 24 * 3_600_000).toISOString(),
      replication: Math.min(3, Math.max(2, b.replication ?? 2)),
      input: b.input,
      assignedTo: [],
      postedAt: now.toISOString(),
    });
    return { id };
  });

  app.put('/v1/leaderboard/me', async (req, reply) => {
    const acct = account(auth(req));
    const { handle } = (req.body ?? {}) as { handle?: string | null };
    if (handle !== null && (typeof handle !== 'string' || !/^[a-z0-9_]{3,20}$/i.test(handle))) throw httpError(400, 'Handle must be 3–20 letters, numbers or _');
    const taken = handle && [...store.accounts.values()].some((a) => a.id !== acct.id && a.leaderboardHandle?.toLowerCase() === handle.toLowerCase());
    if (taken) throw httpError(409, 'Handle taken', 'taken');
    acct.leaderboardHandle = handle;
    return reply.status(204).send();
  });

  /** Opt-in only, last 7 days, rounded to 100 sats so exact earnings aren't exposed. */
  app.get('/v1/leaderboard', async (req) => {
    auth(req);
    const since = Date.now() - 7 * 86_400_000;
    const rows = [...store.accounts.values()]
      .filter((a) => a.leaderboardHandle)
      .map((a) => {
        const msat = (store.ledger.get(a.id) ?? [])
          .filter((e) => e.kind === 'task' && e.status === 'accepted' && Date.parse(e.at) >= since)
          .reduce((x, e) => x + e.amountMsat, 0);
        return { handle: a.leaderboardHandle!, satsRounded: Math.round(msat / 100_000) * 100 };
      })
      .sort((a, b) => b.satsRounded - a.satsRounded)
      .slice(0, 25);
    return { rows };
  });

  /** Anonymous, unauthenticated by design: reports carry no identifiers (see core/analytics). */
  app.post('/v1/analytics', async (req, reply) => {
    const r = req.body as AnalyticsReport;
    if (r?.schema !== 1 || typeof r.week !== 'string' || typeof r.counters !== 'object') throw httpError(400, 'bad report');
    const agg = store.analytics.get(r.week) ?? { __reports: 0 };
    agg.__reports = (agg.__reports ?? 0) + 1;
    for (const [k, v] of Object.entries(r.counters)) if (Number.isFinite(v) && v >= 0 && v < 1e6) agg[k] = (agg[k] ?? 0) + v;
    store.analytics.set(r.week, agg);
    return reply.status(204).send();
  });

  app.get('/v1/admin/metrics', async (req) => {
    if (!process.env.ADMIN_TOKEN || !safeEqual(req.headers.authorization ?? '', `Bearer ${process.env.ADMIN_TOKEN}`)) throw httpError(401, 'Unauthorized');
    const weeks = [...store.analytics.entries()].filter(([, a]) => (a.__reports ?? 0) >= K_ANONYMITY);
    return { weeks: Object.fromEntries(weeks), suppressedWeeks: store.analytics.size - weeks.length };
  });

  return app;
}

function sanitizeProfile(p: DeviceProfile): DeviceProfile {
  return {
    deviceClass: p.deviceClass,
    platform: p.platform,
    cpuCores: Math.min(128, Math.max(1, Math.floor(p.cpuCores || 1))),
    memoryMb: Math.min(1_048_576, Math.max(256, Math.floor(p.memoryMb || 256))),
    hasGpu: Boolean(p.hasGpu),
    benchmarkUnitsPerSec: Math.min(100_000, Math.max(1, Number(p.benchmarkUnitsPerSec) || 1)),
    appVersion: String(p.appVersion ?? '').slice(0, 32),
  };
}

function safeEqual(a: string, b: string): boolean {
  const ab = Buffer.from(a);
  const bb = Buffer.from(b);
  return ab.length === bb.length && timingSafeEqual(ab, bb);
}

function httpError(statusCode: number, message: string, code?: string) {
  return Object.assign(new Error(message), { statusCode, code });
}
