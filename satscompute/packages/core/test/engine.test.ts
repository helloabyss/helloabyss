import { describe, expect, it } from 'vitest';
import {
  ContributionEngine,
  createDefaultRegistry,
  defaultPolicy,
  MockCoordinatorClient,
  type DeviceState,
  type LedgerEntry,
} from '../src';

const state = (over: Partial<DeviceState> = {}): DeviceState => ({
  batteryLevel: 0.95,
  isCharging: true,
  isLowPowerMode: false,
  thermal: 'nominal',
  batteryTempC: 30,
  network: 'wifi',
  isMetered: false,
  isUserIdle: true,
  now: new Date(),
  ...over,
});

function setup(sample: () => DeviceState, maxTasks = 3) {
  const ledger: LedgerEntry[] = [];
  const coordinator = new MockCoordinatorClient();
  let clock = 0;
  const engine = new ContributionEngine({
    sensor: { sample: async () => sample() },
    coordinator,
    executors: createDefaultRegistry(),
    profile: { deviceClass: 'phone', platform: 'ios', cpuCores: 6, memoryMb: 4096, hasGpu: false, benchmarkUnitsPerSec: 200, appVersion: 't' },
    deviceId: 'dev_test',
    getPolicy: () => ({ ...defaultPolicy('phone'), enabled: true }),
    onLedger: (e) => ledger.push(e),
    // Virtual time: sleeping advances the clock instantly.
    sleep: async (ms) => {
      clock += ms;
      await new Promise((r) => setTimeout(r, 0));
    },
    now: () => (clock += 1),
    recheckMs: 0,
    maxTasks,
  });
  return { engine, ledger, coordinator };
}

describe('ContributionEngine', () => {
  it('runs sample tasks end to end and credits the ledger', async () => {
    const { engine, ledger, coordinator } = setup(() => state());
    await engine.start();
    expect(ledger).toHaveLength(3);
    expect(ledger.every((e) => e.status === 'accepted' && e.amountMsat > 0)).toBe(true);
    expect((await coordinator.balance()).availableMsat).toBe(ledger.reduce((a, e) => a + e.amountMsat, 0));
    expect(engine.snapshot.phase).toBe('stopped');
  });

  it('aborts mid-task when the device overheats and pays nothing for it', async () => {
    let calls = 0;
    const { engine, ledger } = setup(() => {
      calls++;
      // First sample (pre-task) is fine; the in-task re-check sees a hot device.
      return calls === 1 ? state() : state({ thermal: 'serious' });
    }, 1);
    const run = engine.start();
    // Let it reach the blocked state, then stop.
    await new Promise((r) => setTimeout(r, 20));
    await engine.stop();
    await run;
    expect(ledger).toHaveLength(0);
  });
});
