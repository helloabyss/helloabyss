import {
  DEFAULT_ENTITLEMENTS,
  type DeviceProfile,
  type Entitlements,
  type LedgerEntry,
  type Payout,
  type QueuedTask,
  type TaskResult,
} from '@satscompute/core';

/**
 * Persistence boundary. MemoryStore is for dev and tests; production implements the same
 * interface on Postgres (balances and payouts MUST be transactional — see docs/ARCHITECTURE.md).
 */

export interface DeviceRecord {
  id: string;
  tokenHash: string;
  profile: DeviceProfile;
  /** Account the device earns for. One account can have several devices (phone + laptop). */
  accountId: string;
  createdAt: string;
  lastSeenAt: string;
}

export interface AccountRecord {
  id: string;
  availableMsat: number;
  pendingMsat: number;
  lifetimeMsat: number;
  entitlements: Entitlements;
  /** Lowest reputation devices get more verification replicas. 0..1 */
  reputation: number;
  /** Opt-in leaderboard handle; null = not listed. */
  leaderboardHandle: string | null;
}

export interface Store {
  devices: Map<string, DeviceRecord>;
  devicesByToken: Map<string, string>;
  accounts: Map<string, AccountRecord>;
  queue: Map<string, QueuedTask>;
  results: Map<string, TaskResult[]>;
  ledger: Map<string, LedgerEntry[]>; // by account
  payouts: Map<string, Payout & { accountId: string }>;
  analytics: Map<string, Record<string, number>>; // by week
}

export function createMemoryStore(): Store {
  return {
    devices: new Map(),
    devicesByToken: new Map(),
    accounts: new Map(),
    queue: new Map(),
    results: new Map(),
    ledger: new Map(),
    payouts: new Map(),
    analytics: new Map(),
  };
}

export function newAccount(id: string): AccountRecord {
  return { id, availableMsat: 0, pendingMsat: 0, lifetimeMsat: 0, entitlements: { ...DEFAULT_ENTITLEMENTS }, reputation: 0.5, leaderboardHandle: null };
}

export function appendLedger(store: Store, accountId: string, e: LedgerEntry) {
  const l = store.ledger.get(accountId) ?? [];
  l.push(e);
  store.ledger.set(accountId, l);
}
