import { requireOptionalNativeModule } from 'expo-modules-core';
import type { ThermalState } from '@satscompute/core';

/**
 * Thermal + battery temperature readings. Expo has no built-in thermal API, so this local
 * module wraps:
 *  - iOS:     ProcessInfo.processInfo.thermalState
 *  - Android: PowerManager.getCurrentThermalStatus() (API 29+) and the sticky
 *             ACTION_BATTERY_CHANGED intent's EXTRA_TEMPERATURE.
 *
 * In Expo Go (no custom native code) the module is absent and we return 'unknown'; the
 * guardrails then halve the duty cycle rather than assume the device is cool.
 */
interface NativeThermal {
  getThermalState(): string;
  getBatteryTemperatureC(): number | null;
}

const native = requireOptionalNativeModule<NativeThermal>('ThermalState');

const MAP: Record<string, ThermalState> = {
  nominal: 'nominal',
  fair: 'fair',
  serious: 'serious',
  critical: 'critical',
};

export function getThermalState(): ThermalState {
  try {
    return MAP[native?.getThermalState() ?? ''] ?? 'unknown';
  } catch {
    return 'unknown';
  }
}

export function getBatteryTemperatureC(): number | null {
  try {
    const t = native?.getBatteryTemperatureC();
    return typeof t === 'number' && t > -50 && t < 100 ? t : null;
  } catch {
    return null;
  }
}

export const hasNativeThermal = native !== null;
