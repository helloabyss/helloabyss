import type { DeviceSensor, DeviceState, NetworkType } from '@satscompute/core';
import * as Battery from 'expo-battery';
import * as Network from 'expo-network';
import { AppState } from 'react-native';
import { getBatteryTemperatureC, getThermalState } from '../../modules/thermal-state';

/**
 * What "idle" means on a phone:
 *  - a Nightstand session is open (user explicitly started contributing and put the phone
 *    down; screen dimmed and kept awake), or
 *  - the app is in the background and the OS granted us a background processing window.
 * Any other foreground use counts as "user active" and pauses work.
 */
let nightstand = false;
let appState: string | null = AppState.currentState ?? null;
AppState.addEventListener('change', (s) => (appState = s));

export function setNightstandActive(on: boolean) {
  nightstand = on;
}

function mapNetwork(t: Network.NetworkStateType | undefined, connected: boolean | undefined): NetworkType {
  if (!connected) return 'none';
  switch (t) {
    case Network.NetworkStateType.WIFI:
      return 'wifi';
    case Network.NetworkStateType.ETHERNET:
      return 'ethernet';
    case Network.NetworkStateType.CELLULAR:
      return 'cellular';
    case Network.NetworkStateType.NONE:
      return 'none';
    default:
      return 'unknown';
  }
}

export class ExpoDeviceSensor implements DeviceSensor {
  constructor(private readonly opts: { background?: boolean } = {}) {}

  async sample(): Promise<DeviceState> {
    const [level, state, lowPower, net] = await Promise.all([
      Battery.getBatteryLevelAsync().catch(() => -1),
      Battery.getBatteryStateAsync().catch(() => Battery.BatteryState.UNKNOWN),
      Battery.isLowPowerModeEnabledAsync().catch(() => false),
      Network.getNetworkStateAsync().catch(() => null),
    ]);
    const network = mapNetwork(net?.type, net?.isConnected ?? undefined);
    return {
      // -1 = unavailable (simulator). Treat as low so guardrails stay conservative.
      batteryLevel: level < 0 ? 0 : level,
      isCharging: state === Battery.BatteryState.CHARGING || state === Battery.BatteryState.FULL,
      isLowPowerMode: lowPower,
      thermal: getThermalState(),
      batteryTempC: getBatteryTemperatureC(),
      network,
      isMetered: network === 'cellular',
      isUserIdle: nightstand || (this.opts.background === true && appState !== 'active'),
      now: new Date(),
    };
  }
}
