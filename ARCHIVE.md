# ARCHIVE — covered stories and framings

Running log so the series does not repeat itself. **Read in Phase 0 of every `/twim` run;
appended in Phase 9.2.**

The rule: **do not reuse a framing from the last 4 episodes.** If this week's story is last
week's story, the angle must be *what changed* — a new print, a new guide, a reversal — not
the same explainer with new numbers.

---

## TWIM episodes

## 2026-09-25 — "Why A Bond Auction Moved Your Mortgage"
- **Runtime / words:** 101.9s / 259 words (measured 159.9 wpm through Kokoro)
- **Cold-open number:** the US 10-year at **5.12%**, highest since 2007
- **Source:** a Wall Street Trapper Facebook clip supplied by the user. Facebook is blocked by
  the egress proxy; ingested via OpusClip (`P3092504KIRS`, 179s) and transcribed.
- **Beats and framings:**
  | Segment | Story | Framing used | Named |
  |---|---|---|---|
  | The print | 10-year at 5.12% | the level plus the speed — "most of it in one day" | US 10Y |
  | What it is | definition | "the price of government money" | — |
  | The trigger | weak $70bn 5-year auction | **the auction as the cause**, not the Fed | — |
  | Portfolio | risk-free rate competition | "they compete for the same dollar" | US equities |
  | Who hurts | long-duration / AI capex | data centres, chips, power — "all built with borrowed money" | — |
  | Mortgage | 30-yr at 7.03% | "arriving at your kitchen table" | — |
  | **Correction** | Aug 2024 claim | **"it fell"** — 4.28% → 3.73% | — |
  | Close | what to watch | "watch the rate, not the reaction" | US 10Y |
- **Counter-beat / disconfirming data:** the episode's spine. The source clip claims the
  10-year hit 5% in August 2024; it **fell** that month during the yen carry-trade unwind.
  The April 2025 tariff-pause claim is half right — bonds did force it, at ~4.5%, not 5%.
  Framed against "the version going around", never against the creator. No name, no dunk.
- **China channel used:** none — no in-window story passed the scope test.
- **Cut as unresolvable:** Thursday's index closes. Two conflicting sets across outlets
  (−0.51/−0.32/−0.78 vs −0.8/−0.7/−1.1), almost certainly a Sep 23 vs Sep 24 mix-up. No daily
  index percentage appears anywhere in the cut.
- **Cut as too close to a forecast:** market-implied Fed hike odds (~64% Oct, ~48% Dec).
- **Video (HeyGen, locked voice):** `4e87955e22af47b687fcc29026b392e3` — "The Ten-Year Yield",
  99.29s, 9:16, 1080p, **67 credits**. Alex Wright on all 25 scenes, script verbatim, faceless,
  glossary applied, captioned cut available. Palette unverified — CDN blocked.
- **Video (HyperFrames):** `videos/twim-2026-09-25/ten-year-at-5.mp4` — rendered locally, **0 credits**,
  check passed 69/69 WCAG AA, frames inspected and two collisions fixed before final.
- **Notes:** two cuts exist because HeyGen's CDN block prevents lifting the voice stem into
  the HyperFrames picture. The HeyGen cut carries the channel voice; the HyperFrames cut
  carries the exact charts. Both still blocked on the `[OPEN]` primary-sourcing flag:
  Treasury, FRED and Freddie Mac are all unreachable from this environment.

## 2026-09-20 — "The Fed Just Hiked For The First Time Since 2023"
- **Runtime / words:** 112.0s / 280 words (cut to the measured 150 wpm; no audio yet)
- **Cold-open number:** the US 10-year at **5.006%**, above 5%
- **Beats and framings:**
  | Segment | Story | Framing used | Named |
  |---|---|---|---|
  | Cold open | 10-year above 5% | "the number underneath every American stock" | US 10Y |
  | The tape | week split three ways | dispersion, not direction | DJIA, COMP, SPX |
  | Closes | Friday levels | the level itself | SPX, COMP, DJIA |
  | Fed | +25bp to 3.75–4.00%, 12–0 | "first increase since 2023", unanimity as the signal | all US equities |
  | Chair | Warsh replaced Powell in May | new chair, quoted by name | — |
  | Counter-beat | CPI unchanged at 3.4%, in line | **"They hiked anyway"** | — |
  | The split | Nasdaq +2.6% vs Dow −733pts | duration vs cyclicals, same week | COMP, DJIA |
  | Week ahead | Micron fiscal Q4, Sep 30 | calendar, not prediction | MU |
- **Counter-beat:** the Fed tightened although inflation did not accelerate — August CPI
  unchanged from July and in line with forecasts.
- **China channel used:** **none — beat cut.** No in-window story passed the scope test.
- **Cut for no transmission:** all China items (June/July, out of window).
- **Cut as untraceable:** steel guidance (NUE/STLD) and the SEC tokenisation/crypto move —
  single-sourced, dropped under the Grade-A-only posture.
- **Video:** `videos/twim-2026-09-20/twim-2026-09-20.mp4` — rendered locally, **0 credits**,
  `check` passed, frames inspected. Picture only.
- **Notes:** style set as **editorial data-motion** — no photography. First episode where the
  render was actually watched rather than filed "complete, not verified". Blocked on the
  `[OPEN]` primary-sourcing flag and on narration audio (HeyGen credits reset 2026-10-06).

<!-- Append newest first, using this schema:

## DATE — "<title used>"
- **Runtime / words:** 118s / 295 words (measured WPM: 150.0)
- **Cold-open number:** <the figure that opened the episode>
- **Beats and framings:**
  | Segment | Story | Framing used | Tickers named |
  |---|---|---|---|
  | Fed | <what> | <the angle — this is what must not repeat> | <tickers> |
- **Counter-beat:** <the disconfirming data point used>
- **China channel used:** <which row of STYLE.md §1 — rotate these>
- **Cut for no transmission:** <stories dropped by the scope test>
- **Cut as untraceable:** <claims dropped under COMPLIANCE §6>
- **Video:** <heygen video_id / URL, or "not rendered — credits">
- **Notes:** <what to do differently next week>

-->

## Framing-reuse watch

**The US 10-year is now spent twice.** 2026-09-20 opened on it at 5.006% as "the number
underneath every American stock"; 2026-09-25 made it the whole subject at 5.12%. A third
episode needs a genuinely new development on the instrument — a new level, a new transmission,
or a new counterparty — not another restatement of the mechanism. Both "the number underneath"
and "the rate underneath" are burned.

Track angles that are getting worn so they can be rested:

| Framing | Last used | Times in last 4 |
|---|---|---|
| "First X since Y" (rarity framing) | 2026-09-20 | 1 |
| Dispersion / "same week, two directions" | 2026-09-20 | 1 |
| Counter-beat: policy vs the print | 2026-09-20 | 1 |

**China channel rotation** — vary which transmission channel leads, so the China beat does
not become the same story weekly:

| Channel | Last used |
|---|---|
| PBOC / policy | — |
| Export controls & tariffs | — |
| Rare earths & supply chain | — |
| Chinese demand → US revenue | — |
| Semis & chip restrictions | — |
| Listings & delisting risk | — |
| Yuan → multinational repricing | — |

---

## Prior channel videos — not TWIM, but their framings are spent

These predate the series. Their angles should not be recycled into a TWIM beat without a
genuinely new development.

| Video | Subject | Framing used | Tickers |
|---|---|---|---|
| `pdt-short` | FINRA Pattern Day Trader rule elimination (eff. 2026-06-04) | "The gate is open, the floor isn't" — deregulation with a hidden risk transfer | — (retail brokers) |
| `moat-short` | Tesla's competitive moat | "The moat isn't the cars, it's the plug" — NACS standard adoption as objective moat evidence; includes EV-share erosion counter-beat | TSLA |
| `paradocs-short-1` | 1890s horse-manure crisis → Cybercab | "The solution was never a better horse" — displacement rather than incremental improvement | TSLA |

**Live caveats carried from those videos** (if any TWIM beat touches them, honour these):
- The `$100B` Supercharger figure is a **Morgan Stanley estimate**, not a market price.
  A more conservative case put it near `$42B`. Always framed as a range, always attributed.
- The "1894 London newspaper" quote is **unsourced** — The Times refuted the attribution in
  2018. Never repeat it as fact.

---

## The Meticulous Investor — kinetic weekly format

A second format alongside TWIM: **silent kinetic motion graphics**, type-led, built entirely
in local HyperFrames at zero credits. Same locked palette and faceless rule; different motion
language (slam / wordsIn / bar race / calendar build on a 0.5s beat grid).

### 2026-09-27 — "Every Index Rose. Almost Nothing In It Did."
- **Runtime:** 69.5s · silent · 9:16 · **0 credits**
- **Cold-open number:** Nasdaq **+2.1%** against the Dow's **+0.3%**
- **The find:** every index closed green while the 10-year hit **5.18%**, its highest since
  2007 — a rising risk-free rate that did not compress multiples, on a seven-to-one advance
- **Beats:** hook → bar race → 5.18% → the contradiction → 42%→58% hike odds → five-print
  calendar → three if/then scenarios → "prepared beats reactive"
- **The payload:** the week-ahead calendar and three scenarios, so the viewer goes into Monday
  with a decision already made rather than a reaction to have
- **Cut for scope:** Alibaba's AI chip (no stateable US-equity transmission inside the window)
- **Cut as untraceable:** the "Nvidia rose on a SpaceX chip surprise" line — single weak source,
  and the SpaceX/Nvidia tie-up is from August
- **Cut as single-sourced:** sector percentages; breadth is carried by the index ratio instead
- **Correction logged:** the 2026-09-25 episode used 5.12% for the 10-year (Thursday's reported
  figure, correct as published). The week's high was 5.18%. Different reference points, not a
  contradiction — see `research/2026-09-27.md` §3
- **Video:** `videos/twim-2026-09-27-kinetic/meticulous-week-ahead.mp4`
- **Notes:** silent is a decision, not a gap — Shorts are watched muted, and the locked voice
  is only reachable through HeyGen, which the brief excluded. A music bed can be added without
  rebuilding. Still blocked on the `[OPEN]` primary-sourcing flag.

## 2026-09-28 — Can the Market Crash 20% in One Day? (Short, scripted)
- `videos/crash-20-2026-09-28/` · VO `scripts/2026-09-28-crash20-vo.txt` (159 words)
- Framing: circuit breakers and slow crashes. Deliberately **not** a 10-year-yield episode (framing-reuse watch).
- Render held: ~65–72 credits needed, 41 available until 2026-10-06.
