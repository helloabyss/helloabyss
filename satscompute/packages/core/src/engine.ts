import { CoordinatorError, type CoordinatorClient, type SubmitReceipt } from './coordinator-client';
import { checkTaskFit, evaluateGuardrails, type BlockReason, type GuardrailVerdict } from './guardrails';
import { outputHash } from './proof';
import type { ExecContext, ExecutorRegistry } from './tasks/executor';
import type { ContributionPolicy, DeviceProfile, DeviceState, LedgerEntry, TaskSpec } from './types';

/**
 * The contribution loop, shared by every platform. Platforms supply a DeviceSensor; the engine
 * owns safety (guardrails before and DURING each task), the duty cycle, and the ledger.
 */

export interface DeviceSensor {
  sample(): Promise<DeviceState>;
}

export type EnginePhase = 'stopped' | 'blocked' | 'waiting-for-work' | 'running' | 'submitting' | 'backoff';

export interface SessionStats {
  startedAt: string;
  tasksCompleted: number;
  tasksRejected: number;
  creditedMsat: number;
  pendingMsat: number;
  busyMs: number;
}

export interface EngineSnapshot {
  phase: EnginePhase;
  reasons: BlockReason[];
  dutyCycle: number;
  current: { task: TaskSpec; progress: number; estSeconds: number } | null;
  session: SessionStats;
  lastError: string | null;
  lastState: DeviceState | null;
}

export interface EngineDeps {
  sensor: DeviceSensor;
  coordinator: CoordinatorClient;
  executors: ExecutorRegistry;
  profile: DeviceProfile;
  deviceId: string;
  getPolicy: () => ContributionPolicy;
  onLedger: (e: LedgerEntry) => void;
  /** Injected for tests. */
  sleep?: (ms: number, signal?: AbortSignal) => Promise<void>;
  now?: () => number;
  /** How often to re-sample the device while a task is running. */
  recheckMs?: number;
  /** How long to wait while blocked before re-checking. */
  blockedPollMs?: number;
  /** Stop after N tasks — used by short background windows (iOS BGTask, Android WorkManager). */
  maxTasks?: number;
  /** Hard wall-clock budget for this run, ms. */
  budgetMs?: number;
}

export class AbortError extends Error {
  override name = 'AbortError';
  constructor(readonly reason: BlockReason | 'stopped' | 'budget') {
    super(`Aborted: ${reason}`);
  }
}

export const defaultSleep = (ms: number, signal?: AbortSignal) =>
  new Promise<void>((resolve) => {
    if (signal?.aborted) return resolve();
    const t = setTimeout(resolve, ms);
    signal?.addEventListener('abort', () => (clearTimeout(t), resolve()), { once: true });
  });

const emptySession = (now: number): SessionStats => ({
  startedAt: new Date(now).toISOString(),
  tasksCompleted: 0,
  tasksRejected: 0,
  creditedMsat: 0,
  pendingMsat: 0,
  busyMs: 0,
});

export class ContributionEngine {
  private ctrl: AbortController | null = null;
  private listeners = new Set<(s: EngineSnapshot) => void>();
  private snap: EngineSnapshot;
  private readonly sleep: NonNullable<EngineDeps['sleep']>;
  private readonly now: () => number;
  private loopDone: Promise<void> = Promise.resolve();
  private loopStartedAt = 0;

  constructor(private readonly d: EngineDeps) {
    this.sleep = d.sleep ?? defaultSleep;
    this.now = d.now ?? Date.now;
    this.snap = {
      phase: 'stopped',
      reasons: [],
      dutyCycle: 0,
      current: null,
      session: emptySession(this.now()),
      lastError: null,
      lastState: null,
    };
  }

  subscribe(fn: (s: EngineSnapshot) => void): () => void {
    this.listeners.add(fn);
    fn(this.snap);
    return () => this.listeners.delete(fn);
  }

  get snapshot(): EngineSnapshot {
    return this.snap;
  }

  get running(): boolean {
    return this.ctrl !== null;
  }

  private emit(patch: Partial<EngineSnapshot>) {
    this.snap = { ...this.snap, ...patch };
    for (const l of this.listeners) l(this.snap);
  }

  /** Start the loop. Resolves when the loop exits (stop(), budget, or maxTasks). */
  start(): Promise<void> {
    if (this.ctrl) return this.loopDone;
    this.ctrl = new AbortController();
    this.emit({ session: emptySession(this.now()), lastError: null });
    this.loopDone = this.loop(this.ctrl.signal).finally(() => {
      this.ctrl = null;
      this.emit({ phase: 'stopped', current: null, dutyCycle: 0 });
    });
    return this.loopDone;
  }

  async stop(): Promise<void> {
    this.ctrl?.abort();
    await this.loopDone;
  }

  private overBudget(): boolean {
    return this.d.budgetMs !== undefined && this.now() - this.loopStartedAt > this.d.budgetMs;
  }

  private async check(): Promise<{ state: DeviceState; verdict: GuardrailVerdict }> {
    const state = await this.d.sensor.sample();
    const verdict = evaluateGuardrails(state, this.d.getPolicy());
    this.emit({ lastState: state, reasons: verdict.reasons, dutyCycle: verdict.dutyCycle });
    return { state, verdict };
  }

  private async loop(signal: AbortSignal) {
    this.loopStartedAt = this.now();
    let backoffMs = 2_000;
    const overBudget = () => this.overBudget();

    while (!signal.aborted && !overBudget()) {
      if (this.d.maxTasks !== undefined && this.snap.session.tasksCompleted >= this.d.maxTasks) return;

      const { state, verdict } = await this.check();
      if (!verdict.allowed) {
        this.emit({ phase: 'blocked' });
        await this.sleep(this.d.blockedPollMs ?? 30_000, signal);
        continue;
      }

      let task: TaskSpec | null;
      try {
        this.emit({ phase: 'waiting-for-work' });
        const policy = this.d.getPolicy();
        task = await this.d.coordinator.lease({
          profile: this.d.profile,
          allowedKinds: policy.allowedKinds.filter((k) => this.d.executors.get(k)),
          dutyCycle: verdict.dutyCycle,
          thermal: state.thermal,
          batteryLevel: state.batteryLevel,
          isCharging: state.isCharging,
          network: state.network === 'none' ? 'unknown' : state.network,
        });
        backoffMs = 2_000;
      } catch (e) {
        backoffMs = await this.backoff(e, backoffMs, signal);
        continue;
      }

      if (!task) {
        // No demand right now. Be honest about it in the UI; poll gently.
        await this.sleep(20_000, signal);
        continue;
      }

      const fit = checkTaskFit(task, this.d.profile, state, this.d.getPolicy(), verdict.dutyCycle);
      if (!fit.ok) {
        await this.d.coordinator.release(task.id, fit.reason).catch(() => {});
        continue;
      }

      await this.runTask(task, fit.estSeconds, verdict.dutyCycle, state.isCharging, signal);
    }
  }

  private async backoff(e: unknown, ms: number, signal: AbortSignal): Promise<number> {
    const msg = e instanceof Error ? e.message : String(e);
    this.emit({ phase: 'backoff', lastError: msg });
    if (e instanceof CoordinatorError && !e.retryable) {
      // Auth or validation problem — retrying won't help. Surface and wait long.
      await this.sleep(5 * 60_000, signal);
      return ms;
    }
    await this.sleep(ms + Math.random() * 500, signal);
    return Math.min(ms * 2, 5 * 60_000);
  }

  private async runTask(task: TaskSpec, estSeconds: number, initialDuty: number, charging: boolean, outer: AbortSignal) {
    const executor = this.d.executors.get(task.kind)!;
    const ctrl = new AbortController();
    const onOuter = () => ctrl.abort();
    outer.addEventListener('abort', onOuter, { once: true });

    let duty = initialDuty;
    let busyMs = 0;
    let sliceStart = this.now();
    let lastCheck = this.now();

    const ctx: ExecContext = {
      signal: ctrl.signal,
      checkpoint: async (progress) => {
        const t = this.now();
        const slice = t - sliceStart;
        busyMs += slice;
        this.emit({ current: { task, progress, estSeconds } });
        // Duty cycle: if allowed 40% busy, rest 1.5× as long as we just worked.
        const rest = slice * (1 / duty - 1);
        if (rest > 1) await this.sleep(rest, ctrl.signal);
        if (outer.aborted) throw new AbortError('stopped');
        if (this.overBudget()) throw new AbortError('budget');
        if (this.now() - lastCheck >= (this.d.recheckMs ?? 2_000)) {
          lastCheck = this.now();
          const { verdict } = await this.check();
          if (!verdict.allowed) throw new AbortError(verdict.reasons[0] ?? 'stopped');
          duty = verdict.dutyCycle;
        }
        sliceStart = this.now();
      },
    };

    this.emit({ phase: 'running', current: { task, progress: 0, estSeconds } });
    try {
      const input = executor.parse(task.input);
      const output = await executor.run(input, ctx);
      busyMs += this.now() - sliceStart;

      this.emit({ phase: 'submitting', current: { task, progress: 1, estSeconds } });
      const hash = outputHash(task.id, task.kind, output);
      const receipt: SubmitReceipt = await this.d.coordinator.submit({
        taskId: task.id,
        deviceId: this.d.deviceId,
        output,
        proof: { outputHash: hash, busyMs, executorVersion: executor.version },
        completedAt: new Date(this.now()).toISOString(),
      });
      this.record(task, receipt, hash, busyMs, charging);
    } catch (e) {
      if (e instanceof AbortError) {
        await this.d.coordinator.release(task.id, e.reason).catch(() => {});
      } else {
        // Executor or input error: release so another device can try; don't loop hot.
        await this.d.coordinator.release(task.id, 'error').catch(() => {});
        this.emit({ lastError: e instanceof Error ? e.message : String(e) });
        await this.sleep(5_000, outer);
      }
    } finally {
      outer.removeEventListener('abort', onOuter);
      this.emit({ current: null });
    }
  }

  private record(task: TaskSpec, r: SubmitReceipt, hash: string, busyMs: number, whileCharging: boolean) {
    const s = this.snap.session;
    const accepted = r.outcome !== 'rejected';
    this.emit({
      session: {
        ...s,
        tasksCompleted: s.tasksCompleted + (accepted ? 1 : 0),
        tasksRejected: s.tasksRejected + (accepted ? 0 : 1),
        creditedMsat: s.creditedMsat + r.creditedMsat,
        pendingMsat: s.pendingMsat + r.pendingMsat,
        busyMs: s.busyMs + busyMs,
      },
    });
    this.d.onLedger({
      id: `le_${task.id}`,
      kind: 'task',
      taskId: task.id,
      taskKind: task.kind,
      explainer: task.explainer,
      amountMsat: r.creditedMsat || r.pendingMsat,
      feeMsat: r.feeMsat,
      outputHash: hash,
      status: r.outcome,
      at: new Date(this.now()).toISOString(),
      whileCharging,
    });
  }
}
