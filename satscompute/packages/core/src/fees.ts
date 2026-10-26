import type { FeeTier, MilliSats, Sats } from './types';

/**
 * Platform economics. All values are configuration, not promises — the coordinator serves the
 * live values from /v1/market and the app shows whatever it receives.
 */
export const FEE_BPS: Record<FeeTier, number> = {
  standard: 2000, // 20% platform fee
  plus: 1500,
  pro: 1000,
};

export const PAYOUT = {
  /** Default minimum balance before a payout can be requested. */
  minSats: 250,
  /** Users may raise their own auto-payout threshold, never lower than minSats. */
  maxThresholdSats: 100_000,
  /** Routing fee budget we allow the Lightning node to spend, as bps of the payout. */
  routingFeeLimitBps: 50,
  /** Flat routing fee floor so tiny payouts can still route. */
  routingFeeFloorSats: 2,
} as const;

/** Split a gross task reward into user net and platform fee. Fee rounds down in the user's favour. */
export function splitReward(grossMsat: MilliSats, tier: FeeTier): { netMsat: MilliSats; feeMsat: MilliSats } {
  const feeMsat = Math.floor((grossMsat * FEE_BPS[tier]) / 10_000);
  return { netMsat: grossMsat - feeMsat, feeMsat };
}

/** Maximum routing fee the user pays for a payout (deducted from the payout amount). */
export function routingFeeLimit(amountSats: Sats): Sats {
  return Math.max(PAYOUT.routingFeeFloorSats, Math.ceil((amountSats * PAYOUT.routingFeeLimitBps) / 10_000));
}

export function msatToSats(msat: MilliSats): Sats {
  return Math.floor(msat / 1000);
}

export function formatSats(sats: number): string {
  return `${Math.floor(sats).toLocaleString('en-US')} sats`;
}
