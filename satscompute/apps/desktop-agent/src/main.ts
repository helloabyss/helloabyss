import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { cpus, homedir, loadavg, platform, totalmem } from 'node:os';
import { join } from 'node:path';
import {
  benchmarkFallback,
  ContributionEngine,
  createDefaultRegistry,
  defaultPolicy,
  HttpCoordinatorClient,
  REASON_COPY,
  type DeviceProfile,
  type DeviceSensor,
} from '@satscompute/core';

/**
 * Desktop agent (v0). Proves the engine is platform-agnostic: only the sensor differs.
 * Roadmap: worker_threads for multi-core, GPU executors (ONNX Runtime / llama.cpp), a pruned
 * Bitcoin Core node for "Bitcoin mode", battery + thermal readings per OS.
 */

const URL = process.env.COORDINATOR_URL ?? 'http://127.0.0.1:8787';
const STATE = join(homedir(), '.satscompute');
const CRED = join(STATE, 'agent.json');

/** "User active" proxy: 1-minute load well above what our own worker adds. */
class NodeSensor implements DeviceSensor {
  async sample() {
    const busy = loadavg()[0]! / cpus().length > 0.7;
    return {
      batteryLevel: 1,
      isCharging: true, // desktops; laptops: read /sys/class/power_supply or pmset (TODO)
      isLowPowerMode: false,
      thermal: 'unknown' as const, // TODO per-OS sensors; guardrails derate to 50% meanwhile
      batteryTempC: null,
      network: 'ethernet' as const,
      isMetered: false,
      isUserIdle: !busy,
      now: new Date(),
    };
  }
}

const profile: DeviceProfile = {
  deviceClass: 'desktop',
  platform: platform() === 'darwin' ? 'macos' : platform() === 'win32' ? 'windows' : 'linux',
  cpuCores: cpus().length,
  memoryMb: Math.round(totalmem() / 1024 ** 2),
  hasGpu: false,
  benchmarkUnitsPerSec: benchmarkFallback(),
  appVersion: 'agent-0.1.0',
};

mkdirSync(STATE, { recursive: true });
let cred: { token: string; deviceId: string } | null = null;
try {
  cred = JSON.parse(readFileSync(CRED, 'utf8'));
} catch {}
const client = new HttpCoordinatorClient(URL, cred?.token ?? null);
if (!cred) {
  const r = await client.register(profile);
  cred = { token: client.getToken()!, deviceId: r.deviceId };
  writeFileSync(CRED, JSON.stringify(cred), { mode: 0o600 });
}

const engine = new ContributionEngine({
  sensor: new NodeSensor(),
  coordinator: client,
  executors: createDefaultRegistry(),
  profile,
  deviceId: cred.deviceId,
  getPolicy: () => ({ ...defaultPolicy('desktop'), enabled: true, onlyWhenCharging: false }),
  onLedger: (e) => console.log(`${e.status.padEnd(20)} ${(e.amountMsat / 1000).toFixed(3)} sats  ${e.explainer ?? ''}`),
});

let last = '';
engine.subscribe((s) => {
  const line = s.phase === 'blocked' ? `paused: ${s.reasons.map((r) => REASON_COPY[r]).join(' ')}` : s.phase;
  if (line !== last) console.log(`[${new Date().toISOString()}] ${(last = line)}`);
});
process.on('SIGINT', () => void engine.stop().then(() => process.exit(0)));
await engine.start();
