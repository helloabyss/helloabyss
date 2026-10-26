import type { LedgerEntry } from './types';

/** Local calendar day key, YYYY-MM-DD. */
export function dayKey(d: Date): string {
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

/**
 * Consecutive days (ending today, or yesterday if nothing yet today) with at least one accepted
 * task. Yesterday counts so a streak doesn't look broken first thing in the morning.
 */
export function contributionStreak(ledger: LedgerEntry[], now = new Date()): number {
  const days = new Set(ledger.filter((e) => e.kind === 'task' && e.status === 'accepted').map((e) => dayKey(new Date(e.at))));
  const cursor = new Date(now);
  if (!days.has(dayKey(cursor))) cursor.setDate(cursor.getDate() - 1);
  let n = 0;
  while (days.has(dayKey(cursor))) {
    n++;
    cursor.setDate(cursor.getDate() - 1);
  }
  return n;
}

export interface Badge {
  id: string;
  title: string;
  description: string;
}

export interface BadgeStats {
  lifetimeSats: number;
  tasks: number;
  streak: number;
  payouts: number;
  kinds: number;
}

const BADGES: (Badge & { earned: (s: BadgeStats) => boolean })[] = [
  { id: 'first-task', title: 'First job', description: 'Completed your first AI task.', earned: (s) => s.tasks >= 1 },
  { id: 'sats-100', title: '100 sats', description: 'Earned your first 100 sats.', earned: (s) => s.lifetimeSats >= 100 },
  { id: 'sats-1000', title: '1,000 sats', description: 'Earned 1,000 sats.', earned: (s) => s.lifetimeSats >= 1_000 },
  { id: 'sats-21000', title: '21k club', description: 'Earned 21,000 sats.', earned: (s) => s.lifetimeSats >= 21_000 },
  { id: 'tasks-100', title: 'Centurion', description: '100 tasks completed.', earned: (s) => s.tasks >= 100 },
  { id: 'streak-7', title: '7-day streak', description: 'Contributed 7 days in a row.', earned: (s) => s.streak >= 7 },
  { id: 'streak-30', title: '30-day streak', description: 'Contributed 30 days in a row.', earned: (s) => s.streak >= 30 },
  { id: 'first-payout', title: 'Stacked', description: 'First payout to your own wallet.', earned: (s) => s.payouts >= 1 },
  { id: 'all-rounder', title: 'All-rounder', description: 'Ran three different task types.', earned: (s) => s.kinds >= 3 },
];

export function badgeStats(ledger: LedgerEntry[], now = new Date()): BadgeStats {
  const tasks = ledger.filter((e) => e.kind === 'task' && e.status === 'accepted');
  return {
    lifetimeSats: Math.floor(tasks.reduce((a, e) => a + e.amountMsat, 0) / 1000),
    tasks: tasks.length,
    streak: contributionStreak(ledger, now),
    payouts: ledger.filter((e) => e.kind === 'payout' && e.status === 'paid').length,
    kinds: new Set(tasks.map((e) => e.taskKind)).size,
  };
}

export function earnedBadges(stats: BadgeStats): Badge[] {
  return BADGES.filter((b) => b.earned(stats)).map(({ earned: _e, ...b }) => b);
}

export function allBadges(): Badge[] {
  return BADGES.map(({ earned: _e, ...b }) => b);
}
