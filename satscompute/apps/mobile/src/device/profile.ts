import { benchmarkFallback, type DeviceProfile } from '@satscompute/core';
import Constants from 'expo-constants';
import * as Device from 'expo-device';
import { Platform } from 'react-native';

export function buildProfile(): DeviceProfile {
  const isTablet = Device.deviceType === Device.DeviceType.TABLET;
  return {
    deviceClass: isTablet ? 'tablet' : 'phone',
    platform: Platform.OS === 'ios' ? 'ios' : 'android',
    // Expo doesn't expose core count; it doesn't matter yet because JS executors are single-threaded.
    cpuCores: 1,
    memoryMb: Math.round((Device.totalMemory ?? 2 * 1024 ** 3) / 1024 ** 2),
    // Phones never take GPU work in the MVP (thermals). Desktop agent will.
    hasGpu: false,
    benchmarkUnitsPerSec: benchmarkFallback(),
    appVersion: Constants.expoConfig?.version ?? '0.0.0',
  };
}
