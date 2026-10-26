import { AnalyticsBuffer } from '@satscompute/core';
import Constants from 'expo-constants';
import { Platform } from 'react-native';
import { useApp } from '../state/store';

const URL =
  process.env.EXPO_PUBLIC_ANALYTICS_URL ||
  (process.env.EXPO_PUBLIC_COORDINATOR_URL ? `${process.env.EXPO_PUBLIC_COORDINATOR_URL}/v1/analytics` : '');

export const analytics = new AnalyticsBuffer(() => useApp.getState().privacy.analytics, {
  appVersion: Constants.expoConfig?.version ?? '0.0.0',
  platform: Platform.OS,
});

/** Fire-and-forget. Failures drop the report — we never retry-queue analytics on device. */
export async function flushAnalytics() {
  const report = analytics.flush();
  if (!report || !URL) return;
  await fetch(URL, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(report) }).catch(() => {});
}
