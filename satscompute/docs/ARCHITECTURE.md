# Architecture

```
┌──────────────── device (phone / desktop agent) ────────────────┐
│ DeviceSensor ──► Guardrails ──► ContributionEngine ──► Executors │
│ (battery, thermal,   (policy,      (lease, duty cycle,  (embed,   │
│  network, idle)       derating)     re-check, abort)     classify,│
│                                         │                filter,  │
│        Ledger (local, offline) ◄────────┤                verify)  │
└─────────────────────────────────────────┼────────────────────────┘
                                          │ HTTPS, per-device bearer token
┌──────────────── coordinator ────────────▼────────────────────────┐
│ Scheduler (selectTask) · Lease sweeper · Verification (replicas / │
│ house) · Ledger + balances · Payouts ─► LightningProvider (LND)   │
│ RevenueCat webhook ─► Entitlements · Anonymous analytics (k≥50)   │
│ Requester API (marketplace v0) · Leaderboard (opt-in, rounded)    │
└───────────────────────────────────────────────────────────────────┘
```

## Why the engine lives in `packages/core`

Phone, desktop agent and coordinator all import the same guardrails, scheduler, executors and
proof code. A new platform supplies one thing: a `DeviceSensor`. On the coordinator, the
executors used for house verification are byte-for-byte the code devices run, so a
verification mismatch means a real disagreement in output, not a difference between two
implementations.

## Safety model

- **Off by default.** Turning sharing on requires an explicit toggle plus a confirmation
  dialog.
- **Policy limits are clamped** (`sanitizePolicy`) on every save and every rehydrate, so a
  corrupted store can't raise them.
- **Guardrails run before every lease and every ~2 s during a task.** Any breach aborts the
  task and releases the lease.
- **Unknown sensor means conservative behaviour:** `thermal: unknown` halves the duty cycle,
  and an unreadable battery level is treated as 0%.
- **Phones only take short tasks** (≤ 60 s locally, ≤ 45 s scheduled, halved when warm). They
  never take GPU work, and never use more than a quarter of device memory.

## Privacy model

- Task inputs are processed on the device. The device sends back only its output and proof.
- The coordinator knows a random device id, a coarse profile (class, platform, memory,
  benchmark) and the payout destination.
- Analytics are opt-in and bucketed. They carry no identifiers, are aggregated per ISO week,
  and are only exposed for weeks with at least 50 reports.
- The leaderboard is opt-in, uses a self-chosen handle, and rounds weekly sats to the nearest
  100.
- RevenueCat's `appUserID` is the opaque account id. The coordinator never sees store
  receipts.

## Data model (target Postgres schema)

`accounts(id, available_msat, pending_msat, lifetime_msat, fee_tier, boost_until, …)`,
`devices(id, account_id, token_hash, profile jsonb, last_seen_at)`,
`tasks(id, kind, requester_id, input jsonb, reward_msat, replication, lease_expires_at)`,
`assignments(task_id, device_id, leased_at, expires_at, result jsonb, output_hash, outcome)`,
`ledger(id, account_id, kind, amount_msat, fee_msat, status, ref, at)` (append-only),
`payouts(id, account_id, amount_sats, fee_sats, destination, status, preimage, idem_key unique)`.

Every balance change and its ledger insert must happen in the same transaction.

## Economics knobs (all config)

| Knob | Default | Where |
|---|---|---|
| Platform fee | 20 / 15 / 10 % (standard / plus / pro) | `core/fees.ts` |
| Payout minimum | 250 sats | `PAYOUT.minSats`, `PAYOUT_MIN_SATS` |
| Routing fee cap | 0.5 %, minimum 2 sats | `PAYOUT.routingFeeLimitBps` |
| Sample price | 2 msat per work unit | `core/tasks/samples.ts`, `/v1/market` |

Earnings estimates are always shown as a range (p10–p90 utilisation), with the reminder that
there is no work without demand.
