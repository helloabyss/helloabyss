import type { ContributionPolicy, DeviceClass } from './types';

/** Conservative defaults. Contribution is OFF until the user explicitly opts in. */
export function defaultPolicy(deviceClass: DeviceClass = 'phone'): ContributionPolicy {
  const isMobile = deviceClass === 'phone' || deviceClass === 'tablet';
  return {
    enabled: false,
    onlyWhenCharging: true,
    onlyOnWifi: true,
    minBatteryLevel: isMobile ? 0.8 : 0.3,
    maxThermal: 'fair',
    maxBatteryTempC: 38,
    maxCpuPercent: isMobile ? 40 : 60,
    allowGpu: !isMobile,
    quietHours: { enabled: false, start: '08:00', end: '18:00' },
    cellularDataCapMb: 0,
    allowedKinds: ['embedding', 'classification', 'filter', 'verification'],
  };
}

/** Parses "HH:MM" into minutes since midnight. Throws on malformed input so bad settings surface. */
export function parseHm(hm: string): number {
  const m = /^([01]\d|2[0-3]):([0-5]\d)$/.exec(hm);
  if (!m) throw new Error(`Invalid time "${hm}", expected HH:MM`);
  return Number(m[1]) * 60 + Number(m[2]);
}

/** True when `now` (local time) falls in [start, end). Handles windows that cross midnight. */
export function isInQuietHours(policy: ContributionPolicy, now: Date): boolean {
  if (!policy.quietHours.enabled) return false;
  const start = parseHm(policy.quietHours.start);
  const end = parseHm(policy.quietHours.end);
  const cur = now.getHours() * 60 + now.getMinutes();
  if (start === end) return false;
  return start < end ? cur >= start && cur < end : cur >= start || cur < end;
}

/** Clamp user-entered values into safe ranges. Applied whenever settings are saved or loaded. */
export function sanitizePolicy(p: ContributionPolicy): ContributionPolicy {
  const clamp = (v: number, lo: number, hi: number) => Math.min(hi, Math.max(lo, v));
  return {
    ...p,
    minBatteryLevel: clamp(p.minBatteryLevel, 0.2, 1),
    maxBatteryTempC: clamp(p.maxBatteryTempC, 30, 42),
    maxCpuPercent: Math.round(clamp(p.maxCpuPercent, 10, 100)),
    cellularDataCapMb: clamp(p.cellularDataCapMb, 0, 2048),
    allowedKinds: p.allowedKinds.length ? p.allowedKinds : ['embedding'],
  };
}
