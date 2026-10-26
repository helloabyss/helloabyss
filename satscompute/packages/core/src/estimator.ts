import { FEE_BPS } from './fees';
import type { DeviceProfile, FeeTier } from './types';

/** Live market quote served by the coordinator. */
export interface MarketQuote {
  /** Average gross price per work unit, msat. Driven by what requesters are paying. */
  msatPerUnit: number;
  /** Fraction of online time a device of this class actually had work (demand-side). p10/p50/p90. */
  utilization: { p10: number; p50: number; p90: number };
  /** Optional BTC/USD reference so the UI can show a rough fiat figure. Clearly labelled as such. */
  btcUsd: number | null;
  asOf: string;
}

export interface EarningsRange {
  low: number;
  mid: number;
  high: number;
}

/**
 * Projected net sats per hour for a device, as a range. We deliberately never return a single
 * number: earnings depend on demand we don't control, and the UI must show the spread.
 */
export function projectSatsPerHour(
  profile: DeviceProfile,
  dutyCycle: number,
  market: MarketQuote,
  tier: FeeTier,
  priorityBoost = false,
): EarningsRange {
  const unitsPerHour = profile.benchmarkUnitsPerSec * dutyCycle * 3600;
  const netShare = 1 - FEE_BPS[tier] / 10_000;
  // Boost raises the chance of getting work when demand is thin; it can't create demand.
  const u = market.utilization;
  const boost = (x: number) => (priorityBoost ? Math.min(1, x * 1.25) : x);
  const sats = (util: number) => (unitsPerHour * util * market.msatPerUnit * netShare) / 1000;
  return { low: sats(boost(u.p10)), mid: sats(boost(u.p50)), high: sats(boost(u.p90)) };
}

export function projectSession(perHour: EarningsRange, hours: number): EarningsRange {
  return { low: perHour.low * hours, mid: perHour.mid * hours, high: perHour.high * hours };
}

/** Live session estimate: what's been credited plus what's pending verification. */
export function sessionEstimate(creditedMsat: number, pendingMsat: number): { confirmed: number; pending: number } {
  return { confirmed: Math.floor(creditedMsat / 1000), pending: Math.floor(pendingMsat / 1000) };
}

export function satsToUsd(sats: number, btcUsd: number | null): number | null {
  return btcUsd ? (sats / 1e8) * btcUsd : null;
}
