/**
 * Privacy-preserving developer analytics.
 *
 *  - Opt-in only. Nothing is buffered if consent is false.
 *  - No device id, no user id, no IP-derived data, no task contents. Each flush is an
 *    independent bag of counters; reports can't be linked to each other or to a payout address.
 *  - Values are bucketed (sats, durations) so outliers can't fingerprint a device.
 *  - The coordinator only publishes aggregates over >= K_ANONYMITY reports.
 */

export const K_ANONYMITY = 50;

export type AnalyticsEvent =
  | { type: 'task_completed'; kind: string; sats: number; busyMs: number }
  | { type: 'task_rejected'; kind: string }
  | { type: 'task_aborted'; reason: string }
  | { type: 'guardrail_block'; reason: string }
  | { type: 'payout'; ok: boolean }
  | { type: 'app_open'; dayOfInstall: number }
  | { type: 'iap'; product: string };

export interface AnalyticsReport {
  schema: 1;
  appVersion: string;
  platform: string;
  /** Coarse: week of year only. */
  week: string;
  counters: Record<string, number>;
}

export function bucket(n: number, edges: number[]): string {
  for (const e of edges) if (n < e) return `<${e}`;
  return `>=${edges[edges.length - 1]}`;
}

/** Retention bucket: d0, d1, d7, d30... instead of exact install date. */
export function retentionBucket(dayOfInstall: number): string {
  return bucket(dayOfInstall, [1, 2, 8, 31, 91]);
}

function isoWeek(d: Date): string {
  const t = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
  const day = t.getUTCDay() || 7;
  t.setUTCDate(t.getUTCDate() + 4 - day);
  const y = new Date(Date.UTC(t.getUTCFullYear(), 0, 1));
  const w = Math.ceil(((t.getTime() - y.getTime()) / 86_400_000 + 1) / 7);
  return `${t.getUTCFullYear()}-W${String(w).padStart(2, '0')}`;
}

export class AnalyticsBuffer {
  private counters: Record<string, number> = {};

  constructor(
    private readonly consent: () => boolean,
    private readonly meta: { appVersion: string; platform: string },
  ) {}

  track(e: AnalyticsEvent) {
    if (!this.consent()) return;
    const inc = (k: string) => (this.counters[k] = (this.counters[k] ?? 0) + 1);
    switch (e.type) {
      case 'task_completed':
        inc(`task.ok.${e.kind}`);
        inc(`task.sats.${bucket(e.sats, [1, 5, 20, 100])}`);
        inc(`task.busy.${bucket(e.busyMs, [1000, 5000, 20000, 60000])}`);
        break;
      case 'task_rejected':
        inc(`task.rejected.${e.kind}`);
        break;
      case 'task_aborted':
        inc(`task.aborted.${e.reason}`);
        break;
      case 'guardrail_block':
        inc(`guard.${e.reason}`);
        break;
      case 'payout':
        inc(`payout.${e.ok ? 'ok' : 'fail'}`);
        break;
      case 'app_open':
        inc(`retention.${retentionBucket(e.dayOfInstall)}`);
        break;
      case 'iap':
        inc(`iap.${e.product}`);
        break;
    }
  }

  /** Returns a report and clears the buffer, or null if there is nothing (or no consent). */
  flush(now = new Date()): AnalyticsReport | null {
    if (!this.consent() || !Object.keys(this.counters).length) {
      this.counters = {};
      return null;
    }
    const r: AnalyticsReport = { schema: 1, ...this.meta, week: isoWeek(now), counters: this.counters };
    this.counters = {};
    return r;
  }
}
