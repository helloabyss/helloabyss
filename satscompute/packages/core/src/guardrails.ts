import { isInQuietHours } from './policy';
import type { ContributionPolicy, DeviceProfile, DeviceState, TaskSpec, ThermalState } from './types';

/**
 * Local guardrails. These run ON the device and are the final authority: the coordinator can
 * suggest work, but the device refuses anything that would breach the user's limits.
 */

export type BlockReason =
  | 'disabled'
  | 'not-charging'
  | 'battery-low'
  | 'low-power-mode'
  | 'thermal'
  | 'battery-hot'
  | 'thermal-unknown-throttled'
  | 'no-network'
  | 'not-wifi'
  | 'quiet-hours'
  | 'user-active';

export interface GuardrailVerdict {
  allowed: boolean;
  reasons: BlockReason[];
  /** Effective duty cycle (0..1) after thermal/battery derating. 0 when blocked. */
  dutyCycle: number;
}

const THERMAL_RANK: Record<ThermalState, number> = {
  nominal: 0,
  fair: 1,
  serious: 2,
  critical: 3,
  unknown: 1,
};

export const REASON_COPY: Record<BlockReason, string> = {
  disabled: 'Sharing is turned off.',
  'not-charging': 'Waiting for a charger.',
  'battery-low': 'Battery below your minimum.',
  'low-power-mode': 'Low Power Mode is on.',
  thermal: 'Device is warm — cooling down.',
  'battery-hot': 'Battery is warm — cooling down.',
  'thermal-unknown-throttled': 'Thermal sensor unavailable — running at reduced speed.',
  'no-network': 'Offline.',
  'not-wifi': 'Waiting for Wi-Fi.',
  'quiet-hours': 'Inside your quiet hours.',
  'user-active': 'You are using the device.',
};

export function evaluateGuardrails(state: DeviceState, policy: ContributionPolicy): GuardrailVerdict {
  const reasons: BlockReason[] = [];

  if (!policy.enabled) reasons.push('disabled');
  if (policy.onlyWhenCharging && !state.isCharging) reasons.push('not-charging');
  // When charging, allow the battery to be slightly under the minimum: it is rising, not draining.
  const minBattery = state.isCharging ? policy.minBatteryLevel - 0.1 : policy.minBatteryLevel;
  if (state.batteryLevel < minBattery) reasons.push('battery-low');
  if (state.isLowPowerMode) reasons.push('low-power-mode');
  if (state.thermal !== 'unknown' && THERMAL_RANK[state.thermal] > THERMAL_RANK[policy.maxThermal]) {
    reasons.push('thermal');
  }
  if (state.batteryTempC !== null && state.batteryTempC > policy.maxBatteryTempC) reasons.push('battery-hot');
  if (state.network === 'none') reasons.push('no-network');
  else if (policy.onlyOnWifi && state.network !== 'wifi' && state.network !== 'ethernet') reasons.push('not-wifi');
  if (isInQuietHours(policy, state.now)) reasons.push('quiet-hours');
  if (!state.isUserIdle) reasons.push('user-active');

  if (reasons.length) return { allowed: false, reasons, dutyCycle: 0 };

  // Derating: run cooler as we approach limits rather than hitting them and stopping hard.
  let duty = policy.maxCpuPercent / 100;
  if (state.thermal === 'fair') duty *= 0.6;
  if (state.thermal === 'unknown') duty *= 0.5;
  if (state.batteryTempC !== null && state.batteryTempC > policy.maxBatteryTempC - 3) duty *= 0.5;
  if (!state.isCharging) duty *= 0.5;

  const info: BlockReason[] = state.thermal === 'unknown' ? ['thermal-unknown-throttled'] : [];
  return { allowed: true, reasons: info, dutyCycle: Math.max(0.05, Math.min(1, duty)) };
}

export type TaskRejection =
  | 'kind-not-allowed'
  | 'needs-gpu'
  | 'insufficient-memory'
  | 'too-long'
  | 'payload-too-large'
  | 'lease-too-short';

/** Max wall time a single task may take on this device class before we refuse it. */
const MAX_TASK_SECONDS = { phone: 60, tablet: 90, laptop: 300, desktop: 900 } as const;

/** Estimated wall-clock seconds for a task, given device throughput and duty cycle. */
export function estimateTaskSeconds(task: TaskSpec, profile: DeviceProfile, dutyCycle: number): number {
  const busy = task.requirements.workUnits / Math.max(1, profile.benchmarkUnitsPerSec);
  return busy / Math.max(0.05, dutyCycle);
}

/** Per-task check: does this specific job fit within this device's limits right now? */
export function checkTaskFit(
  task: TaskSpec,
  profile: DeviceProfile,
  state: DeviceState,
  policy: ContributionPolicy,
  dutyCycle: number,
): { ok: true; estSeconds: number } | { ok: false; reason: TaskRejection } {
  if (!policy.allowedKinds.includes(task.kind)) return { ok: false, reason: 'kind-not-allowed' };
  if (task.requirements.needsGpu && (!profile.hasGpu || !policy.allowGpu)) return { ok: false, reason: 'needs-gpu' };
  // Never ask for more than a quarter of device memory.
  if (task.requirements.minMemoryMb > profile.memoryMb / 4) return { ok: false, reason: 'insufficient-memory' };
  const est = estimateTaskSeconds(task, profile, dutyCycle);
  if (est > MAX_TASK_SECONDS[profile.deviceClass]) return { ok: false, reason: 'too-long' };
  const payloadCap = state.network === 'cellular' ? 256 : 4096;
  if (task.requirements.payloadKb > payloadCap) return { ok: false, reason: 'payload-too-large' };
  const leaseLeft = (Date.parse(task.leaseExpiresAt) - state.now.getTime()) / 1000;
  if (leaseLeft < est * 1.5) return { ok: false, reason: 'lease-too-short' };
  return { ok: true, estSeconds: est };
}
