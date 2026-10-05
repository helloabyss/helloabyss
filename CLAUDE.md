# helloabyss — faceless finance YouTube Shorts

Repo holds scripts, shot lists and production records for a **faceless YouTube money
channel**. Video is generated with HeyGen; the repo is the durable record.

## Before writing any script

**Verify every factual claim with a web search first.** This channel publishes finance
content people may act on. Never script from memory — regulatory dates, ticker figures and
market-share numbers change. Record each claim in a fact table in `SCRIPT.md` with a
confidence level, and mark analyst estimates as estimates, never as market prices.

Include the disconfirming data. An explainer that admits where the thesis is weak is both
more honest and better content than a promo. Every video carries an on-screen
"Educational only. Not financial advice." card in the first 4 seconds.

## House style — apply to every short

**Read `STYLE-GUIDE.md` and build the brief from its template.** It is the channel's
locked visual identity. Summary of the non-negotiables:

- **The first five seconds decide everything.** The opening sentence must be the most
  surprising true thing in the fact table, and must work as the title. No build-up, no title
  card, no question. The compliance line renders as a thin bottom-edge strip, never a
  full-frame card that eats the hook. Then: new information or a reversal every 10–15s, the
  counter-evidence turn signposted out loud, and a close that loops back to the opening.
  **`STYLE-GUIDE.md` §5A is the standard and `retention-editor` has veto over it.**
- **Imagery-first, three-layer stack.** Cinematic photographic imagery is the BASE layer,
  motion graphics over it, type and captions on top. Never typography on abstract
  backgrounds — that was tried and rejected.
- **Faceless.** No avatars, no presenters, no identifiable people, ever.
- **No real corporate logos or badges.** Use plain text name-tags.
- **Three-colour editorial palette** — near-black, white, one red accent. Imagery graded
  dark and desaturated. No neon, gradients, sparkles or emoji.
- **Dramatic motion**, but from camera and animation, not decoration.
- **No clickbait.** No subscribe animations, no "what they don't want you to know" CTAs.
  Close on something the viewer can act on.

## Fixed production settings

| Setting | Value |
|---|---|
| HeyGen style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| HeyGen voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` (revisable — send follow-ups into the session) |
| Orientation | `portrait` (9:16) |

Keep style and voice constant across videos so the channel reads as one series.

## Known environment constraints

**Credit figures measured 2026-10-05. Re-check with `vidiq_balance`, `higgsfield balance` and
`heygen get_current_user` at the top of each session — this block has been wrong before in
both directions. In September it understated what was available and the channel avoided tools
it could afford; by 2026-10-05 the same block overstated two balances by three orders of
magnitude, which is the more expensive failure because it plans spends that cannot clear.**

| Resource | Status 2026-10-05 | Was claimed |
|---|---|---|
| HeyGen | **0 premium credits.** Pro plan; resets **2026-10-06 12:57 UTC** | 372 |
| Higgsfield | **0.35 credits**, starter — B-roll is **NOT** available | 564.84 |
| vidIQ | **121** = 120 renewable (of 150) + 1 add-on. Next reset **2026-11-03** | 1, blocked to 10-03 |

All three read directly from `vidiq_balance`, `higgsfield balance` and `heygen
get_current_user` on 2026-10-05 — observed, not inferred.

**Consequences, which invert three task-board rows:** no HeyGen render can run until the
2026-10-06 reset; Higgsfield hero plates (T5) are unaffordable, not merely unapproved; and
vidIQ research (T4) is unblocked with ~24 calls of headroom at the pessimistic 5/call.
`GROWTH-PLAN.md` §4 still describes Higgsfield as "564 credits … idle" and §6 budgets against
372 HeyGen credits; both are stale and the figures there should not be spent against.

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`). Renders
  cannot be downloaded or watched from here. Always report a render as *complete, not
  verified*, and give the user a verification checklist.
- **HeyGen `create_speech`** failed on the old Creator plan (needs separate `api` credits).
  The account is now Pro — **untested since the upgrade.** Test once before assuming there is
  no detached VO stem.
- **vidIQ cost discipline — CORRECTED 2026-09-21, then corrected again. Read before any call.**
  An earlier version of this file said research calls were free. **That was wrong and it cost
  the channel 40 of its 41 credits in one session.**

  **What is directly confirmed:** `vidiq_youtube_search` costs **5 credits** — the API said so
  in an error message. That is the only per-call price actually observed.

  **What is inferred, not measured:** 10 successful vidIQ calls consumed 40 credits. If the
  charged ones cost 5 each, 8 were charged and 2 were free — most likely `vidiq_user_channels`
  and `vidiq_trend_categories`, which are metadata lookups rather than searches. **This is
  arithmetic, not per-call verification. Do not treat the split as established.**

  | Call | Cost | Basis |
  |---|---|---|
  | `vidiq_balance` | free | observed — called 3× with no drawdown |
  | `vidiq_youtube_search` | **5** | **confirmed by API error message** |
  | `channel_stats`, `channel_videos`, `channel_search`, `outliers` | assume **5** | inferred from arithmetic |
  | `keyword_research`, `video_stats` | assume **5** | never called — assumed by analogy |
  | `user_channels`, `trend_categories` | possibly free | inferred; do not rely on it |
  | `score_thumbnail` / `score_title` | 5 | from the tool's own docs, not observed |
  | `generate_thumbnail` | 22 | from the tool's own docs, not observed |

  **Operating rule: assume every vidIQ call costs 5 unless it is `vidiq_balance`.** Budget on
  the pessimistic number. The renewable pool of 150/month is then ~30 calls, about 7 a week.
  Call `vidiq_balance` before and after a batch to measure the real cost and correct this table
  with observed values.

  **Never** call `vidiq_outliers`. Observed once: given "investing stock market money" it
  returned cat compilations, Kaiju gameplay and a Hindi TV promo, and charged for it. Whether
  it ignores the `query` argument or does something else is **not known** — only that the
  output was unusable. Either way it is not worth 5 credits.
- **`vidiq_outliers` returned unusable results** (see above). Use `vidiq_channel_search` and
  `vidiq_youtube_search`, which did respect the query when tested.
- **vidIQ cannot find The Meticulous Investor** (`@meticulousmoney`) — channels this small are
  not indexed. Two `channel_search` attempts cost 10 credits and returned nothing. **Do not
  search for it again**, and do not try to resolve its `UC…` ID: `www.youtube.com` is
  egress-blocked here, and nothing in the pipeline needs the ID anyway.
- vidIQ thumbnail scores penalise low saturation and reward vibrancy. That conflicts with
  this channel's editorial palette. **Do not chase the score** at the cost of the identity.

## Repo layout

One directory per video: `SCRIPT.md` (VO, fact table, shot list, packaging) and
`PRODUCTION.md` (session IDs, settings, verification checklist, constraints hit).

Channel-level documents:

| File | Purpose |
|---|---|
| `STYLE-GUIDE.md` | Locked visual identity. Read in full before every brief. |
| `GROWTH-PLAN.md` | Channel strategy, tool stack, pipeline interconnection, metrics. |
| `WEEKLY-RUNBOOK.md` | The weekly production cycle and how to run the agent team. |
| `AGENTS.md` | **Agent registry** — the six agents, their roles, authority and handoffs. |
| `TASKS.md` | **Assignment board** — the open queue per agent, with blockers. Check this first in a new session. |
| `PROVENANCE.md` | **What is verified vs asserted.** Read this before trusting any claim in the repo. Unchecked claims must be labelled in the sentence that states them. |
| `SERIES-ONE-NUMBER.md` | **Prepared series brief, awaiting a decision (T8).** Zero-credit stickman format aimed at the §2 cadence constraint. §6 states the case against it as well as for it. |
| `CHARACTER-ZUL.md` | **Zul**, the host that series would use. Locked design, built by `engine/zul.py`, never drawn by hand. Transferred from the parked PARADOCS10X channel — a deliberate reuse, not continuity. |
| `engine/` | Zero-credit deterministic still renderer (SVG → PNG via headless Chromium). Composed for 1920×1080; `engine/portrait/proof.png` shows it reframing to 9:16. |
| `.claude/agents/` | scout · fact-checker · scriptwriter · **retention-editor** · art-director · packager |

## Which channel this repo serves

**The Meticulous Investor** — `@meticulousmoney`, faceless finance, 6 subscribers, cold start.
The `UC…` ID is unknown and **is not needed** — publishing runs on an OAuth connection, not an
ID. Do not spend calls hunting for it. Every script,
render and packaging decision in this repo targets that channel.

`PARADOCS10X` (`UCX2_NXOHIgXUQFsBOub65HQ`, AI/tech, 57 subs) is a **separate, parked** channel.
Its OpusClip / AgentOpus publishing connection (`6797cd6d213f56bd20026a41`) is **reserved for
the tech channel and must not be repointed** at the finance channel.

Consequences to work around until The Meticulous Investor is connected:

- **vidIQ cannot see it.** Channels this small aren't indexed, so `channel_stats`,
  `channel_videos` and competitor baselines are unavailable for it. Research the *niche*, not
  the channel.
- **`vidiq_user_channels` returns PARADOCS10X** (auth is `paradocs10x@gmail.com`). Do not read
  its numbers as this channel's performance.
- **No publishing automation.** Uploads are manual. The X account (@troybillion) is
  channel-agnostic and usable today.
- **Topical discipline is the whole strategy at 6 subs.** No off-lane videos for 90 days — one
  is a meaningful fraction of the classification evidence.

See `GROWTH-PLAN.md` §1 and §7.
