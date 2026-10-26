import * as BackgroundTask from 'expo-background-task';
import * as TaskManager from 'expo-task-manager';
import { ExpoDeviceSensor } from '../device/sensor';
import { useApp } from '../state/store';
import { getRuntime } from './runtime';

/**
 * Opportunistic background contribution.
 *
 * iOS: BGTaskScheduler decides when (and whether) this runs — typically while charging and
 * idle, often overnight. There is no guarantee. Android: WorkManager, minimum every 15 min.
 * Each window does at most a few short tasks under a hard 25 s budget, with the same
 * guardrails as the foreground. We never try to keep the app alive beyond what the OS grants.
 */
export const BACKGROUND_TASK = 'satscompute.contribute';

const BUDGET_MS = 25_000;

TaskManager.defineTask(BACKGROUND_TASK, async () => {
  // Zustand persist may not have rehydrated in a cold background launch.
  if (!useApp.getState().hydrated) await useApp.persist.rehydrate();
  if (!useApp.getState().policy.enabled) return BackgroundTask.BackgroundTaskResult.Success;
  try {
    const rt = await getRuntime();
    if (rt.engine.running) return BackgroundTask.BackgroundTaskResult.Success;
    const engine = rt.createEngine({
      sensor: new ExpoDeviceSensor({ background: true }),
      budgetMs: BUDGET_MS,
      maxTasks: 3,
      blockedPollMs: BUDGET_MS, // if blocked, give up this window rather than spin
    });
    const sub = BackgroundTask.addExpirationListener(() => void engine.stop());
    await engine.start();
    sub.remove();
    return BackgroundTask.BackgroundTaskResult.Success;
  } catch {
    return BackgroundTask.BackgroundTaskResult.Failed;
  }
});

export async function syncBackgroundRegistration(enabled: boolean) {
  const status = await BackgroundTask.getStatusAsync();
  if (status !== BackgroundTask.BackgroundTaskStatus.Available) return false;
  const registered = await TaskManager.isTaskRegisteredAsync(BACKGROUND_TASK);
  if (enabled && !registered) await BackgroundTask.registerTaskAsync(BACKGROUND_TASK, { minimumInterval: 15 });
  if (!enabled && registered) await BackgroundTask.unregisterTaskAsync(BACKGROUND_TASK);
  return true;
}
