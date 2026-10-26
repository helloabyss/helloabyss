import { estimateTaskSeconds } from './guardrails';
import type { DeviceProfile, Entitlements, TaskKind, TaskSpec, ThermalState } from './types';

/**
 * Coordinator-side task assignment. Given a device's lease request, pick the best task from the
 * open queue. The device re-checks fit locally (guardrails.checkTaskFit), so this is about
 * efficiency and fairness, not safety.
 */

export interface LeaseRequest {
  deviceId: string;
  profile: DeviceProfile;
  allowedKinds: TaskKind[];
  dutyCycle: number;
  thermal: ThermalState;
  batteryLevel: number;
  isCharging: boolean;
  network: 'wifi' | 'cellular' | 'ethernet' | 'unknown';
  entitlements: Pick<Entitlements, 'priorityBoostUntil' | 'premiumTasks'>;
}

export interface QueuedTask extends TaskSpec {
  premium?: boolean;
  /** Device ids that already hold or held a replica — never give one device two replicas. */
  assignedTo: string[];
  postedAt: string;
}

const MAX_SECONDS: Record<DeviceProfile['deviceClass'], number> = { phone: 45, tablet: 60, laptop: 240, desktop: 600 };

export function scoreTask(task: QueuedTask, req: LeaseRequest, now: Date): number | null {
  if (!req.allowedKinds.includes(task.kind)) return null;
  if (task.assignedTo.includes(req.deviceId)) return null;
  if (task.assignedTo.length >= task.replication) return null;
  if (task.premium && !req.entitlements.premiumTasks) return null;
  if (task.requirements.needsGpu && !req.profile.hasGpu) return null;
  if (task.requirements.minMemoryMb > req.profile.memoryMb / 4) return null;
  if (req.network === 'cellular' && task.requirements.payloadKb > 256) return null;

  const secs = estimateTaskSeconds(task, req.profile, req.dutyCycle);
  // Leave thermal headroom: a warm device only gets short jobs.
  const cap = MAX_SECONDS[req.profile.deviceClass] * (req.thermal === 'fair' || req.thermal === 'unknown' ? 0.5 : 1);
  if (secs > cap) return null;
  if (Date.parse(task.leaseExpiresAt) - now.getTime() < secs * 1500) return null;

  // Prefer: paid well per second of device time, older (fairness to requesters), and replicas
  // that complete a verification set.
  const satsPerSec = task.rewardMsat / Math.max(1, secs);
  const ageMin = (now.getTime() - Date.parse(task.postedAt)) / 60_000;
  const completesSet = task.assignedTo.length === task.replication - 1 ? 1.2 : 1;
  // Low battery while charging: prefer short tasks so we can stop quickly.
  const shortBias = req.batteryLevel < 0.5 ? 1 / (1 + secs / 10) : 1;
  return satsPerSec * completesSet * shortBias * (1 + Math.min(ageMin, 60) / 60);
}

export function selectTask(queue: QueuedTask[], req: LeaseRequest, now = new Date()): QueuedTask | null {
  let best: QueuedTask | null = null;
  let bestScore = -Infinity;
  for (const t of queue) {
    const s = scoreTask(t, req, now);
    if (s !== null && s > bestScore) {
      best = t;
      bestScore = s;
    }
  }
  return best;
}

/**
 * Priority Boost does not change which tasks a device is eligible for or how much they pay; it
 * moves the device ahead in the lease order when several devices poll at once and work is scarce.
 */
export function leasePriority(req: LeaseRequest, now = new Date()): number {
  const boosted = req.entitlements.priorityBoostUntil && Date.parse(req.entitlements.priorityBoostUntil) > now.getTime();
  return (boosted ? 2 : 1) * (req.isCharging ? 1 : 0.5);
}
