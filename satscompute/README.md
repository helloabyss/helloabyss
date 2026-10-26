# SatsCompute

Share your device's idle compute for **real AI work** and get paid in **bitcoin (sats) over
Lightning**. SatsCompute does **not** mine Bitcoin. Phones can't mine profitably, and the app
never says or implies they do.

```
satscompute/
├── packages/core          Platform-agnostic engine: guardrails, scheduler, executors,
│                          estimator, proofs, Lightning helpers, IAP catalogue, analytics
├── services/coordinator   Fastify API: devices, task queue, replica verification, ledger,
│                          Lightning payouts (LND/Voltage), RevenueCat webhook, leaderboard
├── apps/mobile            Expo (React Native) app for iOS + Android
├── apps/desktop-agent     Headless Node agent: same engine, different sensor
└── docs/                  ARCHITECTURE.md, STORE-COMPLIANCE.md
```

## Status

| Area | State |
|---|---|
| Contribution engine (guardrails before **and during** tasks, duty cycle, abort, backoff) | Working, tested |
| Built-in executors: embeddings, zero-shot classification, dataset filter, verification | Working, deterministic across devices. Embeddings are a feature-hashing baseline, **not** a neural model. |
| Coordinator: lease → result → replica/house verification → ledger | Working, tested. In-memory store. |
| Lightning payouts: Lightning Address, LNURL-pay, BOLT11 → LND REST | Implemented. Tested against a mock node only. |
| Mobile: onboarding, dashboard, Nightstand session, controls, earnings, payout, store, settings, Bitcoin mode | Typechecks and bundles for Android (Hermes). **Not yet run on a physical device.** |
| Native thermal module (iOS `thermalState`, Android `currentThermalStatus` + battery temp) | Written. Needs a dev build (`expo prebuild`) to compile; untested on device. |
| IAP via RevenueCat | Wired. Mock store in dev. Earnings-affecting products are off by default. |
| Real requester marketplace, billing, Postgres, payout worker queue | **Not built.** See "Production gaps" below. |

## Quick start

Requires Node 20 or newer.

```bash
cd satscompute
npm install
npm test                       # core: 29 tests
npm test -w @satscompute/coordinator   # coordinator: 4 tests
npm run typecheck
```

### Run the app fully offline (no backend)

```bash
npm run mobile                 # expo start
```

Leave `EXPO_PUBLIC_COORDINATOR_URL` blank. The app then uses `MockCoordinatorClient`: sample
tasks, auto-verified, simulated payouts. A "Demo mode" banner stays on screen while this is
active.

Expo Go works for UI work, but the thermal module only exists in a dev build. Until you have
one, guardrails report `thermal: unknown` and run at half speed. For the full app:

```bash
cd apps/mobile
npx expo prebuild
npx expo run:ios               # or run:android
```

### Run against the coordinator

```bash
cp services/coordinator/.env.example services/coordinator/.env   # edit as needed
npm run coordinator            # http://localhost:8787, seeded with sample tasks
# in apps/mobile/.env:
EXPO_PUBLIC_COORDINATOR_URL=http://<your-LAN-IP>:8787
```

Desktop agent: `COORDINATOR_URL=http://localhost:8787 npm start -w @satscompute/desktop-agent`

## Environment variables

### Coordinator (`services/coordinator/.env`)

| Var | Default | Notes |
|---|---|---|
| `PORT`, `HOST` | `8787`, `0.0.0.0` | |
| `TOKEN_PEPPER` | dev value | **Required in production.** Mixed into stored device-token hashes. |
| `SEED_SAMPLE_TASKS` | `true` | Keeps the queue filled with sample tasks. **Must be `false` in production.** Sample tasks would pay real sats for work nobody bought. |
| `REQUESTER_API_KEYS` | — | Comma-separated keys for `POST /v1/requester/tasks`. |
| `PAYOUT_MIN_SATS` | `250` | Floor on payouts. Can't be set below 250. |
| `LIGHTNING_PROVIDER` | `mock` | `mock` or `lnd`. `mock` is refused when `NODE_ENV=production`. |
| `LND_REST_URL` | — | For example a Voltage node, `https://<node>.m.voltageapp.io:8080`. |
| `LND_MACAROON_HEX` | — | Bake a restricted macaroon (`lncli bakemacaroon offchain:read offchain:write`). Don't use admin.macaroon. |
| `REVENUECAT_WEBHOOK_SECRET` | — | Must match the Authorization header set in the RevenueCat dashboard. |
| `ADMIN_TOKEN` | — | Bearer token for `/v1/admin/metrics` (k-anonymised analytics). |
| `BTC_USD_REFERENCE` | — | Optional. Shows a rough fiat figure, labelled as a reference price. |

### Mobile (`apps/mobile/.env`)

| Var | Notes |
|---|---|
| `EXPO_PUBLIC_COORDINATOR_URL` | Blank means offline demo mode. |
| `EXPO_PUBLIC_REVENUECAT_IOS_KEY` / `_ANDROID_KEY` | Public SDK keys. Blank means the dev mock store, which only works in `__DEV__`. |
| `EXPO_PUBLIC_EARNINGS_IAP_ENABLED` | `false` by default. Hides boosts, fee tiers and premium tasks. Read docs/STORE-COMPLIANCE.md before turning it on. |
| `EXPO_PUBLIC_ANALYTICS_URL` | Defaults to `<coordinator>/v1/analytics`. Only used with user consent. |

`EXPO_PUBLIC_*` values are compiled into the app bundle, so never put a secret in one.

## How a task flows

1. **Guardrails** (`core/guardrails.ts`) evaluate the live `DeviceState` against the user's
   `ContributionPolicy`: charging, battery, low-power mode, thermal state, battery temperature,
   Wi-Fi, quiet hours and whether the user is idle. Close to a limit, the duty cycle is lowered
   gradually (derated) so the device slows down before it has to stop.
2. The engine **leases** a task. The coordinator's scheduler (`core/scheduler.ts`) scores open
   tasks on capability, thermal headroom, battery, network and pay per device-second.
3. The device **re-checks fit** locally (`checkTaskFit`) and refuses anything too long, too big
   or not opted in. The device is the final authority.
4. The **executor** runs in small chunks. At each `checkpoint()` the engine sleeps to honour
   the CPU limit (40% means it rests 1.5× as long as it worked). Every 2 s it re-samples the
   device. If it gets warm or unplugged, the task is aborted and released, and nothing is
   claimed for it.
5. The device submits the output plus a **proof**: sha256 over the canonical
   `(taskId, kind, output)`.
6. The coordinator **verifies** the result:
   - The proof must match the output.
   - Real tasks go to 2 devices. The majority wins, and a disagreement adds a third replica as
     a tie-breaker. Minority results aren't paid and the device loses reputation.
   - Single-replica tasks (the samples) are re-executed by the coordinator ("house verify").
7. The net amount (gross − platform fee) is credited, the result appears in the ledger with
   its hash, and auto-payout runs if enabled.

## Extending the AI task layer

Executors implement one interface (`packages/core/src/tasks/executor.ts`):

```ts
const myExecutor: Executor<MyInput, MyOutput> = {
  kind: 'llm-small',
  version: 'qwen0.5b-q4@1',        // bump whenever outputs could change
  parse(input) { /* validate untrusted input, throw TaskInputError */ },
  async run(input, ctx) {
    for (const chunk of work) {
      doSomeWork(chunk);
      await ctx.checkpoint(progress); // REQUIRED: duty cycle, guardrails, abort
    }
    return output;
  },
};
registry.register(myExecutor);
```

Rules for a new executor:

- **Determinism matters.** Replicas are compared by hash. Quantise float outputs (the
  embedder outputs int8), or add a tolerance comparison in
  `services/coordinator/src/verification.ts`, as embeddings already have (cosine ≥ 0.99).
  Avoid engine-dependent APIs. That is why `tokenize` doesn't use Unicode property regexes or
  `normalize()`.
- **Call `checkpoint()` often**, at least every ~100 ms of work. If you don't, the CPU limit
  and thermal aborts can't take effect.
- **Model-backed executors** (ONNX Runtime, ExecuTorch, llama.rn, or llama.cpp on desktop)
  belong in the app or agent, not in `core`. Register them at runtime in
  `apps/mobile/src/engine/runtime.ts`. Ship models as on-demand downloads over Wi-Fi with a
  checksum, never inside the app binary.
- Add the kind to `TaskKind`, `KIND_LABEL` and `KIND_EXPLAINER` so the dashboard can say in
  plain language what the device is doing.
- Requesters post work with `POST /v1/requester/tasks` (`x-api-key`). The coordinator
  validates the input using the same `parse()`.

## Lightning payouts

- Users bring their own wallet: a Lightning Address (`name@wallet.com`), LNURL-pay, or a
  BOLT11 invoice. The app resolves the address before saving it, so typos fail early.
- The coordinator gets an invoice from the user's wallet (LUD-06/16), checks the amount, then
  pays through `LightningProvider`. The LND REST provider works with Voltage. To use
  Lightspark, implement the same interface with its SDK.
- Before paying, the coordinator holds `amount + routing-fee cap`. Any unused fee is refunded,
  and a failed payment refunds everything. An `Idempotency-Key` header prevents a double pay.
- The preimage is shown to the user as proof of payment.
- **Custody, stated honestly:** we never hold user keys. We do hold the *unpaid earned
  balance* until it reaches the payout threshold (default 250 sats). That is a short-lived
  liability and is labelled as such in the app. Auto-payout keeps it small.

## Production gaps (deliberately not faked)

- **Persistence.** `MemoryStore` stands in for a database. Balances and payouts need Postgres
  with row locks or serializable transactions, and payouts should move to a queue worker
  instead of being paid inside the HTTP request.
- **Requester billing/escrow.** Requesters should pre-fund tasks (for example by paying a
  Lightning invoice) before tasks are leased.
- **Real models.** The built-in embedder is a hashing baseline. Customers who need neural
  embeddings need a model executor.
- **Android long-running work.** A foreground service would allow sessions beyond the screen
  being on, but it needs a native module. Today: a Nightstand session (screen on, near-black),
  plus WorkManager windows via `expo-background-task`.
- **iOS background.** BGTaskScheduler decides if and when the app runs. Expect occasional
  overnight windows, not continuous work.
- **Account linking** (phone + laptop earning into one balance), reputation-weighted
  replication, fraud and Sybil limits, and KYC/AML review for your jurisdiction.
- **Compliance review.** Read docs/STORE-COMPLIANCE.md before submitting to either store.
