import type { Entitlements } from './types';

/**
 * In-app product catalogue. Shared by the app (store screen) and coordinator (webhook grants)
 * so the effect of a purchase is defined in exactly one place.
 *
 * `affectsEarnings` products are behind a platform flag: App Store / Play review may treat
 * "pay money to earn more crypto" differently from cosmetics and analytics. See
 * docs/STORE-COMPLIANCE.md before enabling them on a store build.
 */

export type ProductId =
  | 'boost_24h'
  | 'boost_7d'
  | 'analytics_pro'
  | 'tier_plus_monthly'
  | 'tier_pro_monthly'
  | 'premium_tasks_monthly'
  | 'setup_pack'
  | 'theme_obsidian'
  | 'theme_copper';

export interface Product {
  id: ProductId;
  title: string;
  description: string;
  type: 'consumable' | 'non-consumable' | 'subscription';
  /** Placeholder display price; the store's localised price always wins at runtime. */
  fallbackPrice: string;
  affectsEarnings: boolean;
  group: 'boost' | 'tier' | 'insight' | 'setup' | 'cosmetic';
}

export const PRODUCTS: Product[] = [
  {
    id: 'boost_24h',
    title: 'Priority Boost · 24 hours',
    description: 'Your device is first in line when work is scarce. It cannot create demand — if there are no tasks, there is nothing to boost.',
    type: 'consumable',
    fallbackPrice: '$0.99',
    affectsEarnings: true,
    group: 'boost',
  },
  {
    id: 'boost_7d',
    title: 'Priority Boost · 7 days',
    description: 'Same as the 24-hour boost, for a week.',
    type: 'consumable',
    fallbackPrice: '$3.99',
    affectsEarnings: true,
    group: 'boost',
  },
  {
    id: 'tier_plus_monthly',
    title: 'Plus · 15% platform fee',
    description: 'Lowers the platform fee on every task from 20% to 15%.',
    type: 'subscription',
    fallbackPrice: '$1.99/mo',
    affectsEarnings: true,
    group: 'tier',
  },
  {
    id: 'tier_pro_monthly',
    title: 'Pro · 10% platform fee',
    description: 'Lowers the platform fee to 10%. Only worth it if you earn more than the subscription costs — the app shows you the break-even.',
    type: 'subscription',
    fallbackPrice: '$4.99/mo',
    affectsEarnings: true,
    group: 'tier',
  },
  {
    id: 'premium_tasks_monthly',
    title: 'Premium task types',
    description: 'Opt in to larger model tasks (small LLM calls) on capable devices.',
    type: 'subscription',
    fallbackPrice: '$2.99/mo',
    affectsEarnings: true,
    group: 'tier',
  },
  {
    id: 'analytics_pro',
    title: 'Advanced Analytics',
    description: 'Detailed earnings charts, per-task-type breakdown, thermal and duty-cycle history.',
    type: 'non-consumable',
    fallbackPrice: '$2.99',
    affectsEarnings: false,
    group: 'insight',
  },
  {
    id: 'setup_pack',
    title: 'Wallet Setup Pack',
    description: 'Guided walkthrough to set up a self-custodial Lightning wallet and test payout.',
    type: 'non-consumable',
    fallbackPrice: '$1.99',
    affectsEarnings: false,
    group: 'setup',
  },
  {
    id: 'theme_obsidian',
    title: 'Obsidian theme',
    description: 'Cosmetic. Changes nothing about earnings.',
    type: 'non-consumable',
    fallbackPrice: '$0.99',
    affectsEarnings: false,
    group: 'cosmetic',
  },
  {
    id: 'theme_copper',
    title: 'Copper theme',
    description: 'Cosmetic. Changes nothing about earnings.',
    type: 'non-consumable',
    fallbackPrice: '$0.99',
    affectsEarnings: false,
    group: 'cosmetic',
  },
];

/** Apply a purchase to entitlements. Subscription expiry arrives later as a revoke event. */
export function applyPurchase(e: Entitlements, id: ProductId, now: Date): Entitlements {
  const extend = (hours: number) => {
    const base = e.priorityBoostUntil && Date.parse(e.priorityBoostUntil) > now.getTime() ? new Date(e.priorityBoostUntil) : now;
    return new Date(base.getTime() + hours * 3_600_000).toISOString();
  };
  switch (id) {
    case 'boost_24h':
      return { ...e, priorityBoostUntil: extend(24) };
    case 'boost_7d':
      return { ...e, priorityBoostUntil: extend(24 * 7) };
    case 'tier_plus_monthly':
      return e.feeTier === 'pro' ? e : { ...e, feeTier: 'plus' };
    case 'tier_pro_monthly':
      return { ...e, feeTier: 'pro' };
    case 'premium_tasks_monthly':
      return { ...e, premiumTasks: true };
    case 'analytics_pro':
      return { ...e, advancedAnalytics: true };
    case 'setup_pack':
      return { ...e, setupPack: true };
    case 'theme_obsidian':
    case 'theme_copper':
      return e.cosmetics.includes(id) ? e : { ...e, cosmetics: [...e.cosmetics, id] };
  }
}

/** Revoke on subscription expiry / refund. */
export function revokePurchase(e: Entitlements, id: ProductId): Entitlements {
  switch (id) {
    case 'tier_plus_monthly':
      return e.feeTier === 'plus' ? { ...e, feeTier: 'standard' } : e;
    case 'tier_pro_monthly':
      return e.feeTier === 'pro' ? { ...e, feeTier: 'standard' } : e;
    case 'premium_tasks_monthly':
      return { ...e, premiumTasks: false };
    case 'analytics_pro':
      return { ...e, advancedAnalytics: false };
    default:
      return e;
  }
}

/** Monthly net sats at which a fee-tier subscription pays for itself. */
export function breakEvenSatsPerMonth(priceUsd: number, btcUsd: number, feeSavingBps: number): number {
  const priceSats = (priceUsd / btcUsd) * 1e8;
  return Math.ceil(priceSats / (feeSavingBps / 10_000));
}
