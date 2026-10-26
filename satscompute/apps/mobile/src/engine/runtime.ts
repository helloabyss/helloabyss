import {
  ContributionEngine,
  createDefaultRegistry,
  HttpCoordinatorClient,
  MockCoordinatorClient,
  type CoordinatorClient,
  type EngineDeps,
  type LedgerEntry,
} from '@satscompute/core';
import * as SecureStore from 'expo-secure-store';
import { analytics } from '../analytics';
import { ExpoDeviceSensor } from '../device/sensor';
import { buildProfile } from '../device/profile';
import { useApp } from '../state/store';

/**
 * Process-wide wiring: one coordinator client, one foreground engine. Background windows get a
 * short-lived engine of their own (see background.ts) with a hard time budget.
 */

const COORDINATOR_URL = process.env.EXPO_PUBLIC_COORDINATOR_URL ?? '';
export const isMockBackend = !COORDINATOR_URL;

const TOKEN_KEY = 'satscompute.deviceToken';
const DEVICE_KEY = 'satscompute.deviceId';
const ACCOUNT_KEY = 'satscompute.accountId';

export interface Runtime {
  client: CoordinatorClient;
  deviceId: string;
  accountId: string;
  engine: ContributionEngine;
  createEngine(overrides: Partial<EngineDeps>): ContributionEngine;
  refresh(): Promise<void>;
}

let runtimePromise: Promise<Runtime> | null = null;

export function getRuntime(): Promise<Runtime> {
  runtimePromise ??= init().catch((e) => {
    runtimePromise = null; // allow retry after e.g. first-launch offline
    throw e;
  });
  return runtimePromise;
}

async function init(): Promise<Runtime> {
  const app = useApp.getState();
  const profile = app.profile ?? buildProfile();
  if (!app.profile) app.setProfile(profile);

  let client: CoordinatorClient;
  let deviceId: string;
  let accountId: string;
  if (isMockBackend) {
    // Seed the mock balance from the local ledger so it survives restarts.
    const avail = app.ledger.reduce((a, e) => a + (e.status === 'accepted' || e.status === 'paid' ? e.amountMsat : 0), 0);
    client = new MockCoordinatorClient(app.entitlements.feeTier, { availableMsat: Math.max(0, avail), lifetimeMsat: Math.max(0, avail) });
    deviceId = 'dev_mock';
    accountId = 'acct_mock';
  } else {
    const token = await SecureStore.getItemAsync(TOKEN_KEY);
    const http = new HttpCoordinatorClient(COORDINATOR_URL, token);
    if (token) {
      deviceId = (await SecureStore.getItemAsync(DEVICE_KEY)) ?? '';
      accountId = (await SecureStore.getItemAsync(ACCOUNT_KEY)) ?? '';
    } else {
      const r = await http.register(profile);
      deviceId = r.deviceId;
      accountId = r.accountId;
      await SecureStore.setItemAsync(TOKEN_KEY, http.getToken()!);
      await SecureStore.setItemAsync(DEVICE_KEY, deviceId);
      await SecureStore.setItemAsync(ACCOUNT_KEY, accountId);
    }
    client = http;
  }

  const executors = createDefaultRegistry();
  const onLedger = (e: LedgerEntry) => {
    useApp.getState().upsertLedger(e);
    if (e.status === 'rejected') analytics.track({ type: 'task_rejected', kind: e.taskKind ?? 'unknown' });
    else analytics.track({ type: 'task_completed', kind: e.taskKind ?? 'unknown', sats: e.amountMsat / 1000, busyMs: 0 });
    void maybeAutoPayout(client);
  };

  const createEngine = (overrides: Partial<EngineDeps>) =>
    new ContributionEngine({
      sensor: new ExpoDeviceSensor(),
      coordinator: client,
      executors,
      profile,
      deviceId,
      getPolicy: () => useApp.getState().policy,
      onLedger,
      ...overrides,
    });

  const refresh = async () => {
    const s = useApp.getState();
    const [bal, ent, market] = await Promise.allSettled([client.balance(), client.entitlements(), client.market(profile)]);
    if (bal.status === 'fulfilled') s.setBalance(bal.value);
    if (ent.status === 'fulfilled' && !isMockBackend) s.setEntitlements(ent.value);
    if (market.status === 'fulfilled') s.setMarket(market.value);
  };

  const rt: Runtime = { client, deviceId, accountId, engine: createEngine({}), createEngine, refresh };
  rt.engine.subscribe((snap) => {
    if (snap.phase === 'blocked' && snap.reasons[0]) analytics.track({ type: 'guardrail_block', reason: snap.reasons[0] });
  });
  void refresh();
  return rt;
}

let autoPayoutBusy = false;

async function maybeAutoPayout(client: CoordinatorClient) {
  const { payout, setBalance, upsertLedger } = useApp.getState();
  if (!payout.autoPayout || !payout.destination || autoPayoutBusy) return;
  autoPayoutBusy = true;
  try {
    const bal = await client.balance();
    setBalance(bal);
    if (bal.availableMsat / 1000 < payout.thresholdSats + 10) return;
    // Leave headroom for the routing-fee hold.
    const amount = Math.floor(bal.availableMsat / 1000 * 0.99) - 2;
    const p = await client.requestPayout(payout.destination, amount);
    upsertLedger(payoutLedgerEntry(p));
    analytics.track({ type: 'payout', ok: p.status === 'succeeded' });
    setBalance(await client.balance());
  } catch {
    analytics.track({ type: 'payout', ok: false });
  } finally {
    autoPayoutBusy = false;
  }
}

export function payoutLedgerEntry(p: { id: string; amountSats: number; routingFeeSats: number; status: string; createdAt: string; paymentHash?: string }): LedgerEntry {
  return {
    id: `le_${p.id}`,
    kind: 'payout',
    amountMsat: -(p.amountSats + p.routingFeeSats) * 1000,
    feeMsat: p.routingFeeSats * 1000,
    status: p.status === 'succeeded' ? 'paid' : 'failed',
    outputHash: p.paymentHash,
    at: p.createdAt,
  };
}
