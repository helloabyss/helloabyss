# App Store / Google Play compliance notes

> These notes reflect the guidelines as we understood them while building. Store policies
> change. **Re-read the current text before every submission.** This is engineering
> guidance, not legal advice.

## The big risk: background compute

- **Apple App Review Guideline 2.4.2** (performance/power) says apps may not "run unrelated
  background processes, such as cryptocurrency mining." SatsCompute doesn't mine, but a
  reviewer may still class distributed compute as an unrelated background process.
- **Apple Guideline 3.1.5** (cryptocurrencies) allows mining only when the processing happens
  off-device. We don't mine. The listing and review notes should say so plainly, and describe
  the workload.
- **Google Play** prohibits apps that mine cryptocurrency on the device. The same reasoning
  applies.

### What the app does to stay inside the lines

1. Contribution is the app's stated core purpose, not a hidden side job. It is opt-in and off
   by default, and the work shown is explained as it happens.
2. On iOS, the main mode is a **foreground** Nightstand session. Background work uses only
   OS-granted `BGTaskScheduler` windows, with a 25 s budget and the expiration handler
   honoured. The app never uses audio, location or VoIP tricks to stay alive.
3. It only runs while charging (by default), at a capped duty cycle, and stops when warm.
4. The app says "not mining" on onboarding, the dashboard, Bitcoin mode and Settings.

### Review notes template

> SatsCompute lets users opt in to run small AI text-processing jobs (search embeddings,
> classification, dataset de-duplication) on their device while it is charging. Users are
> paid in bitcoin over the Lightning Network for completed jobs. The app does not mine
> cryptocurrency. Work runs in a foreground "Nightstand" screen, or in system-scheduled
> background processing windows while charging. Demo account and coordinator: …

## In-app purchases that affect earnings

Boosts, lower-fee tiers and premium task access mean "pay money to earn more crypto." A
store may treat that as investment-like or as a payout-related mechanic. They sit behind
`EXPO_PUBLIC_EARNINGS_IAP_ENABLED` (off by default). Cosmetics, analytics and the setup pack
don't affect earnings and are always available.

If you turn them on:
- Product copy must not promise returns. The current copy states that a boost can't create
  demand, and Pro shows its break-even point.
- Use digital IAP (StoreKit / Play Billing) for all of these. Never accept sats for an IAP
  product. That would break 3.1.1 (Apple) and Play's payments policy.

## Payments / money transmission

Paying users in bitcoin may count as money transmission in some jurisdictions. Holding unpaid
balances (even briefly) may too. Get legal review for each launch market. Apple 3.1.5(i)
requires crypto wallet functionality to be offered by developers enrolled as an organization.
SatsCompute is not a wallet, but you should expect the question in review.

## Privacy labels

- Data linked to user: payout destination (Lightning address), purchase history (through
  RevenueCat).
- Data not linked: diagnostics (opt-in, bucketed).
- No tracking, no ads SDKs, no location. The location permissions are explicitly blocked in
  `app.json`.
