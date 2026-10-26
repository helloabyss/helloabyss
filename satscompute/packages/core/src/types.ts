// Shared domain types. Everything that crosses the device <-> coordinator boundary lives here
// so the mobile app, the coordinator and the future desktop agent agree on one contract.

export type Sats = number; // integer satoshis
export type MilliSats = number; // integer msat, used for sub-sat task accrual

export type DeviceClass = 'phone' | 'tablet' | 'laptop' | 'desktop';
export type NetworkType = 'wifi' | 'cellular' | 'ethernet' | 'none' | 'unknown';

/** Normalised thermal state. Maps iOS ProcessInfo.thermalState and Android PowerManager thermal status. */
export type ThermalState = 'nominal' | 'fair' | 'serious' | 'critical' | 'unknown';

/** Static capability profile, measured once by a short benchmark and refreshed occasionally. */
export interface DeviceProfile {
  deviceClass: DeviceClass;
  platform: 'ios' | 'android' | 'macos' | 'windows' | 'linux';
  cpuCores: number;
  memoryMb: number;
  hasGpu: boolean;
  /** Benchmark score: embeddings-equivalent work units per second on one core. */
  benchmarkUnitsPerSec: number;
  appVersion: string;
}

/** Live device state, sampled before every task and between task chunks. */
export interface DeviceState {
  batteryLevel: number; // 0..1
  isCharging: boolean;
  isLowPowerMode: boolean;
  thermal: ThermalState;
  /** Battery temperature in °C where the platform exposes it (Android); null otherwise. */
  batteryTempC: number | null;
  network: NetworkType;
  isMetered: boolean;
  /** True when the OS/app considers the user away (app backgrounded, screen dim, no input). */
  isUserIdle: boolean;
  now: Date;
}

/** User-controlled contribution policy. Every field is a hard limit enforced by guardrails. */
export interface ContributionPolicy {
  enabled: boolean;
  onlyWhenCharging: boolean;
  onlyOnWifi: boolean;
  /** Minimum battery to start or keep running. */
  minBatteryLevel: number; // 0..1
  /** Highest thermal state at which work may continue. */
  maxThermal: Exclude<ThermalState, 'unknown' | 'critical'>;
  /** Battery temperature ceiling (°C) where measurable. */
  maxBatteryTempC: number;
  /** Duty cycle: percentage of wall time the worker may be busy. */
  maxCpuPercent: number; // 10..100
  allowGpu: boolean;
  /** Quiet hours, local time, "HH:MM". Work is paused inside the window. */
  quietHours: { enabled: boolean; start: string; end: string };
  /** Monthly cellular data cap for task payloads, MB. Only used if onlyOnWifi is false. */
  cellularDataCapMb: number;
  /** Task kinds the user has opted in to. */
  allowedKinds: TaskKind[];
}

export type TaskKind = 'embedding' | 'classification' | 'filter' | 'verification' | 'llm-small';

export interface TaskRequirements {
  minMemoryMb: number;
  needsGpu: boolean;
  /** Estimated work units; divided by device throughput to estimate duration. */
  workUnits: number;
  /** Input + output payload size, KB. */
  payloadKb: number;
}

/** A unit of paid work, leased to a single device for a bounded time. */
export interface TaskSpec {
  id: string;
  kind: TaskKind;
  /** Human-readable, shown on the dashboard: what this work is for. */
  explainer: string;
  /** Who posted it (marketplace buyer), shown as a plain name. */
  requester: string;
  requirements: TaskRequirements;
  /** Gross price paid by the requester for this task, msat. Platform fee is taken from this. */
  rewardMsat: MilliSats;
  leaseExpiresAt: string; // ISO
  /** Redundancy: how many devices get this task for cross-verification. */
  replication: number;
  input: unknown;
}

export interface WorkProof {
  /** sha256 over canonical(taskId, kind, output). Coordinator compares across replicas. */
  outputHash: string;
  /** Wall time spent busy, ms. */
  busyMs: number;
  executorVersion: string;
}

export interface TaskResult {
  taskId: string;
  deviceId: string;
  output: unknown;
  proof: WorkProof;
  completedAt: string;
}

export type TaskOutcome = 'accepted' | 'rejected' | 'pending-verification';

export interface LedgerEntry {
  id: string;
  kind: 'task' | 'payout' | 'adjustment';
  taskId?: string;
  taskKind?: TaskKind;
  explainer?: string;
  /** Net to the user after platform fee (positive for earnings, negative for payouts). */
  amountMsat: MilliSats;
  feeMsat: MilliSats;
  outputHash?: string;
  status: TaskOutcome | 'paid' | 'failed';
  at: string;
  /** Was the device charging when this was earned — powers "while charging overnight" insights. */
  whileCharging?: boolean;
}

export type FeeTier = 'standard' | 'plus' | 'pro';

export interface Entitlements {
  feeTier: FeeTier;
  priorityBoostUntil: string | null;
  advancedAnalytics: boolean;
  premiumTasks: boolean;
  setupPack: boolean;
  cosmetics: string[];
}

export const DEFAULT_ENTITLEMENTS: Entitlements = {
  feeTier: 'standard',
  priorityBoostUntil: null,
  advancedAnalytics: false,
  premiumTasks: false,
  setupPack: false,
  cosmetics: [],
};
