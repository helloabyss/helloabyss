import type { TaskKind } from '../types';

export interface ExecContext {
  signal: AbortSignal;
  /**
   * Cooperative yield point. Executors call this between small chunks of work. The engine uses
   * it to enforce the duty cycle (sleeping in proportion to busy time), re-check guardrails and
   * abort if the device became unsafe. Throws an AbortError when the task must stop.
   */
  checkpoint(progress: number): Promise<void>;
}

export interface Executor<I = unknown, O = unknown> {
  kind: TaskKind;
  /** Bumped whenever output could change, so the coordinator only cross-checks like with like. */
  version: string;
  /** Validate untrusted input from the coordinator before running anything. */
  parse(input: unknown): I;
  run(input: I, ctx: ExecContext): Promise<O>;
}

export class ExecutorRegistry {
  private executors = new Map<TaskKind, Executor>();

  register(e: Executor<any, any>): this {
    this.executors.set(e.kind, e as Executor);
    return this;
  }

  get(kind: TaskKind): Executor | undefined {
    return this.executors.get(kind);
  }

  kinds(): TaskKind[] {
    return [...this.executors.keys()];
  }
}

export class TaskInputError extends Error {
  override name = 'TaskInputError';
}

export function assertStringArray(v: unknown, field: string, max = 512): string[] {
  if (!Array.isArray(v) || v.length === 0 || v.length > max || !v.every((s) => typeof s === 'string')) {
    throw new TaskInputError(`${field} must be a non-empty string[] (max ${max})`);
  }
  return v.map((s) => s.slice(0, 4000));
}
