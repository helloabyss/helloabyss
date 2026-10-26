import type { MarketQuote } from './estimator';
import { splitReward } from './fees';
import { outputHash } from './proof';
import type { LeaseRequest } from './scheduler';
import { SAMPLE_KINDS, sampleTask } from './tasks/samples';
import type { DeviceProfile, Entitlements, FeeTier, TaskOutcome, TaskResult, TaskSpec } from './types';

export interface SubmitReceipt {
  outcome: TaskOutcome;
  /** Net credited to the user once verified (0 while pending). */
  creditedMsat: number;
  /** Net that will be credited if verification passes. */
  pendingMsat: number;
  feeMsat: number;
}

export interface Balance {
  availableMsat: number;
  pendingMsat: number;
  lifetimeMsat: number;
}

export type PayoutStatus = 'queued' | 'in-flight' | 'succeeded' | 'failed';

export interface Payout {
  id: string;
  amountSats: number;
  routingFeeSats: number;
  destination: string;
  status: PayoutStatus;
  /** Lightning payment preimage, hex. Proof the payment was received. */
  preimage?: string;
  paymentHash?: string;
  error?: string;
  createdAt: string;
}

/** Opt-in leaderboard row: chosen handle + weekly sats rounded to the nearest 100. */
export interface LeaderboardRow {
  handle: string;
  satsRounded: number;
}

export type LeaseQuery = Omit<LeaseRequest, 'deviceId' | 'entitlements'>;

export interface CoordinatorClient {
  register(profile: DeviceProfile): Promise<{ deviceId: string; accountId: string }>;
  market(profile: DeviceProfile): Promise<MarketQuote>;
  lease(q: LeaseQuery): Promise<TaskSpec | null>;
  release(taskId: string, reason: string): Promise<void>;
  submit(result: TaskResult): Promise<SubmitReceipt>;
  balance(): Promise<Balance>;
  requestPayout(destination: string, amountSats: number): Promise<Payout>;
  payout(id: string): Promise<Payout>;
  entitlements(): Promise<Entitlements>;
  leaderboard(): Promise<LeaderboardRow[]>;
  /** null opts out and deletes the handle server-side. */
  setLeaderboardHandle(handle: string | null): Promise<void>;
}

export class CoordinatorError extends Error {
  constructor(
    message: string,
    readonly status: number,
    readonly code?: string,
  ) {
    super(message);
    this.name = 'CoordinatorError';
  }
  get retryable(): boolean {
    return this.status === 0 || this.status === 429 || this.status >= 500;
  }
}

/** Production client. Auth is a per-device bearer token minted at registration. */
export class HttpCoordinatorClient implements CoordinatorClient {
  constructor(
    private readonly baseUrl: string,
    private token: string | null = null,
    private readonly fetchImpl: typeof fetch = fetch,
  ) {}

  private async req<T>(method: string, path: string, body?: unknown): Promise<T> {
    let res: Response;
    try {
      res = await this.fetchImpl(`${this.baseUrl}${path}`, {
        method,
        headers: {
          'content-type': 'application/json',
          ...(this.token ? { authorization: `Bearer ${this.token}` } : {}),
        },
        body: body === undefined ? undefined : JSON.stringify(body),
      });
    } catch (e) {
      throw new CoordinatorError(`Network error: ${(e as Error).message}`, 0);
    }
    if (res.status === 204) return undefined as T;
    const json = (await res.json().catch(() => ({}))) as { error?: string; code?: string };
    if (!res.ok) throw new CoordinatorError(json.error ?? res.statusText, res.status, json.code);
    return json as T;
  }

  async register(profile: DeviceProfile) {
    const r = await this.req<{ deviceId: string; accountId: string; token: string }>('POST', '/v1/devices', { profile });
    this.token = r.token;
    return { deviceId: r.deviceId, accountId: r.accountId };
  }
  getToken() {
    return this.token;
  }
  market(profile: DeviceProfile) {
    return this.req<MarketQuote>('GET', `/v1/market?deviceClass=${profile.deviceClass}`);
  }
  async lease(q: LeaseQuery) {
    const r = await this.req<{ task: TaskSpec | null }>('POST', '/v1/tasks/lease', q);
    return r.task;
  }
  release(taskId: string, reason: string) {
    return this.req<void>('POST', `/v1/tasks/${encodeURIComponent(taskId)}/release`, { reason });
  }
  submit(result: TaskResult) {
    return this.req<SubmitReceipt>('POST', `/v1/tasks/${encodeURIComponent(result.taskId)}/result`, result);
  }
  balance() {
    return this.req<Balance>('GET', '/v1/balance');
  }
  requestPayout(destination: string, amountSats: number) {
    return this.req<Payout>('POST', '/v1/payouts', { destination, amountSats });
  }
  payout(id: string) {
    return this.req<Payout>('GET', `/v1/payouts/${encodeURIComponent(id)}`);
  }
  entitlements() {
    return this.req<Entitlements>('GET', '/v1/entitlements');
  }
  async leaderboard() {
    return (await this.req<{ rows: LeaderboardRow[] }>('GET', '/v1/leaderboard')).rows;
  }
  setLeaderboardHandle(handle: string | null) {
    return this.req<void>('PUT', '/v1/leaderboard/me', { handle });
  }
}

/**
 * Offline/dev client. Generates sample tasks locally and auto-verifies them, so the app's full
 * flow works with no backend. Never used in production builds (see EXPO_PUBLIC_COORDINATOR_URL).
 */
export class MockCoordinatorClient implements CoordinatorClient {
  private outstanding = new Map<string, TaskSpec>();
  private bal: Balance = { availableMsat: 0, pendingMsat: 0, lifetimeMsat: 0 };
  private payouts = new Map<string, Payout>();
  private i = 0;

  constructor(
    private tier: FeeTier = 'standard',
    initial?: Partial<Balance>,
  ) {
    Object.assign(this.bal, initial);
  }

  async register() {
    return { deviceId: 'dev_mock', accountId: 'acct_mock' };
  }
  async market(): Promise<MarketQuote> {
    return { msatPerUnit: 2, utilization: { p10: 0.15, p50: 0.45, p90: 0.8 }, btcUsd: null, asOf: new Date().toISOString() };
  }
  async lease(q: LeaseQuery) {
    const kinds = SAMPLE_KINDS.filter((k) => q.allowedKinds.includes(k));
    if (!kinds.length) return null;
    const t = sampleTask(kinds[this.i++ % kinds.length]!);
    this.outstanding.set(t.id, t);
    return t;
  }
  async release(taskId: string) {
    this.outstanding.delete(taskId);
  }
  async submit(result: TaskResult): Promise<SubmitReceipt> {
    const t = this.outstanding.get(result.taskId);
    if (!t) return { outcome: 'rejected', creditedMsat: 0, pendingMsat: 0, feeMsat: 0 };
    this.outstanding.delete(t.id);
    // Mock "verification": recompute the hash we expect for the declared output.
    if (outputHash(t.id, t.kind, result.output) !== result.proof.outputHash) {
      return { outcome: 'rejected', creditedMsat: 0, pendingMsat: 0, feeMsat: 0 };
    }
    const { netMsat, feeMsat } = splitReward(t.rewardMsat, this.tier);
    this.bal.availableMsat += netMsat;
    this.bal.lifetimeMsat += netMsat;
    return { outcome: 'accepted', creditedMsat: netMsat, pendingMsat: 0, feeMsat };
  }
  async balance() {
    return { ...this.bal };
  }
  async requestPayout(destination: string, amountSats: number): Promise<Payout> {
    if (amountSats * 1000 > this.bal.availableMsat) throw new CoordinatorError('Insufficient balance', 400, 'insufficient');
    this.bal.availableMsat -= amountSats * 1000;
    const p: Payout = {
      id: `po_${Date.now().toString(36)}`,
      amountSats,
      routingFeeSats: 0,
      destination,
      status: 'succeeded',
      preimage: '00'.repeat(32),
      paymentHash: 'mock',
      createdAt: new Date().toISOString(),
    };
    this.payouts.set(p.id, p);
    return p;
  }
  async payout(id: string) {
    const p = this.payouts.get(id);
    if (!p) throw new CoordinatorError('Not found', 404);
    return p;
  }
  async entitlements(): Promise<Entitlements> {
    return {
      feeTier: this.tier,
      priorityBoostUntil: null,
      advancedAnalytics: false,
      premiumTasks: false,
      setupPack: false,
      cosmetics: [],
    };
  }
  private handle: string | null = null;
  async leaderboard(): Promise<LeaderboardRow[]> {
    return this.handle ? [{ handle: this.handle, satsRounded: Math.round(this.bal.lifetimeMsat / 100_000) * 100 }] : [];
  }
  async setLeaderboardHandle(handle: string | null) {
    this.handle = handle;
  }
}
