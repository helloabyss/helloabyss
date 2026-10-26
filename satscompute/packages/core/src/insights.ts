import { dayKey } from './gamification';
import type { LedgerEntry, TaskKind } from './types';

const accepted = (l: LedgerEntry[]) => l.filter((e) => e.kind === 'task' && e.status === 'accepted');
const sats = (l: LedgerEntry[]) => Math.floor(l.reduce((a, e) => a + e.amountMsat, 0) / 1000);

/** Earnings between 20:00 yesterday and 08:00 today while charging. */
export function overnightSummary(ledger: LedgerEntry[], now = new Date()): { sats: number; tasks: number } | null {
  const end = new Date(now);
  end.setHours(8, 0, 0, 0); // this morning; entries after `now` can't exist yet
  const start = new Date(end);
  start.setDate(start.getDate() - 1);
  start.setHours(20, 0, 0, 0);
  const rows = accepted(ledger).filter((e) => {
    const t = Date.parse(e.at);
    return e.whileCharging && t >= start.getTime() && t < end.getTime();
  });
  return rows.length ? { sats: sats(rows), tasks: rows.length } : null;
}

export function dailySeries(ledger: LedgerEntry[], days: number, now = new Date()): { day: string; sats: number }[] {
  const by = new Map<string, number>();
  for (const e of accepted(ledger)) {
    const k = dayKey(new Date(e.at));
    by.set(k, (by.get(k) ?? 0) + e.amountMsat);
  }
  const out: { day: string; sats: number }[] = [];
  for (let i = days - 1; i >= 0; i--) {
    const d = new Date(now);
    d.setDate(d.getDate() - i);
    const k = dayKey(d);
    out.push({ day: k, sats: Math.floor((by.get(k) ?? 0) / 1000) });
  }
  return out;
}

export function kindBreakdown(ledger: LedgerEntry[]): { kind: TaskKind; sats: number; tasks: number }[] {
  const by = new Map<TaskKind, { sats: number; tasks: number }>();
  for (const e of accepted(ledger)) {
    if (!e.taskKind) continue;
    const cur = by.get(e.taskKind) ?? { sats: 0, tasks: 0 };
    cur.sats += e.amountMsat / 1000;
    cur.tasks++;
    by.set(e.taskKind, cur);
  }
  return [...by.entries()].map(([kind, v]) => ({ kind, sats: Math.floor(v.sats), tasks: v.tasks })).sort((a, b) => b.sats - a.sats);
}

/** One-line insights for the dashboard. Plain statements of fact, no hype. */
export function headlineInsights(ledger: LedgerEntry[], now = new Date()): string[] {
  const out: string[] = [];
  const night = overnightSummary(ledger, now);
  if (night) out.push(`You earned ${night.sats.toLocaleString('en-US')} sats while charging overnight (${night.tasks} tasks).`);
  const week = dailySeries(ledger, 7, now);
  const weekSats = week.reduce((a, d) => a + d.sats, 0);
  if (weekSats > 0) {
    const best = week.reduce((a, d) => (d.sats > a.sats ? d : a));
    out.push(`${weekSats.toLocaleString('en-US')} sats in the last 7 days. Best day: ${best.day}.`);
  }
  const top = kindBreakdown(ledger)[0];
  if (top) out.push(`Most of your work has been ${KIND_LABEL[top.kind].toLowerCase()}.`);
  return out;
}

export const KIND_LABEL: Record<TaskKind, string> = {
  embedding: 'Search embeddings',
  classification: 'Text classification',
  filter: 'Dataset cleanup',
  verification: 'Result verification',
  'llm-small': 'Small language model',
};

export const KIND_EXPLAINER: Record<TaskKind, string> = {
  embedding: 'Turns text into numbers so search tools can find similar documents.',
  classification: 'Sorts short texts (reviews, tickets) into categories a requester chose.',
  filter: 'Removes junk and near-duplicates from datasets before they are used for AI.',
  verification: "Re-runs another device's task to check its answer, so nobody gets paid for fake work.",
  'llm-small': 'Runs a small language model on a short prompt. Needs a capable device.',
};
