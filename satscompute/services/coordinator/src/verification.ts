import { cosine, outputHash, type QueuedTask, type TaskResult } from '@satscompute/core';

/**
 * Replica verification. Every task goes to `replication` independent devices. Payment only
 * clears when a majority agree. Disagreement adds one more replica as a tie-breaker (up to 3);
 * the minority is not paid and loses reputation.
 */

export type Verdict =
  | { status: 'waiting' }
  | { status: 'resolved'; accepted: string[]; rejected: string[] }
  | { status: 'escalate' };

const MAX_REPLICATION = 3;

/** Two results agree if their hashes match, or (embeddings only) vectors are near-identical. */
function agree(task: QueuedTask, a: TaskResult, b: TaskResult): boolean {
  if (a.proof.outputHash === b.proof.outputHash) return true;
  if (task.kind !== 'embedding') return false;
  const va = (a.output as { vectors?: number[][] }).vectors ?? [];
  const vb = (b.output as { vectors?: number[][] }).vectors ?? [];
  return va.length === vb.length && va.every((v, i) => cosine(v, vb[i]!) >= 0.99);
}

/** The device-reported hash must match what it actually sent. Cheap, catches lazy forgeries. */
export function proofMatchesOutput(task: QueuedTask, r: TaskResult): boolean {
  return outputHash(task.id, task.kind, r.output) === r.proof.outputHash;
}

export function verifyReplicas(task: QueuedTask, results: TaskResult[]): Verdict {
  if (results.length < task.replication) return { status: 'waiting' };
  // Group results into agreement clusters.
  const clusters: TaskResult[][] = [];
  for (const r of results) {
    const c = clusters.find((cl) => agree(task, cl[0]!, r));
    if (c) c.push(r);
    else clusters.push([r]);
  }
  clusters.sort((a, b) => b.length - a.length);
  const top = clusters[0]!;
  const majority = top.length > results.length / 2;
  if (majority) {
    const accepted = top.map((r) => r.deviceId);
    return { status: 'resolved', accepted, rejected: results.map((r) => r.deviceId).filter((d) => !accepted.includes(d)) };
  }
  if (task.replication < MAX_REPLICATION) return { status: 'escalate' };
  return { status: 'resolved', accepted: [], rejected: results.map((r) => r.deviceId) };
}
