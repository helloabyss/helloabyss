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

**Credit figures verified 2026-09-21. Re-check with `vidiq_balance`, `higgsfield balance` and
`heygen get_current_user` at the top of each session — this block has been wrong before, and
being wrong made the channel avoid tools it could afford.**

| Resource | Status |
|---|---|
| HeyGen | **Pro plan, 372 premium credits** (resets 2026-10-06) |
| Higgsfield | **564.84 credits**, starter plan — B-roll IS available |
| vidIQ | **1 credit** — exhausted 2026-09-21. Renewable pool 0/150, **resets 2026-10-03**. No vidIQ research until then unless topped up. |

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`). Renders
  cannot be downloaded or watched from here. Always report a render as *complete, not
  verified*, and give the user a verification checklist.
- **HeyGen `create_speech`** failed on the old Creator plan (needs separate `api` credits).
  The account is now Pro — **untested since the upgrade.** Test once before assuming there is
  no detached VO stem.
- **vidIQ cost discipline — CORRECTED 2026-09-21. Read this before any vidIQ call.**
  An earlier version of this file said research calls were free. **That was wrong and it cost
  the channel 40 of its 41 credits in a single session.**

  | Call | Cost |
  |---|---|
  | `vidiq_balance` | free |
  | **Every other research call** — `channel_stats`, `channel_videos`, `channel_search`, `youtube_search`, `keyword_research`, `video_stats`, `outliers`, `trend_categories` | **5 credits each** |
  | `score_thumbnail` / `score_title` | 5 |
  | `generate_thumbnail` | 22 |

  The renewable pool is **150/month** = **30 research calls a month**, about **7 a week**.
  That is the real budget. Plan queries before making them; a vidIQ call is a purchase.

  **Never** call `vidiq_outliers` — it ignores its `query` argument and returns unrelated
  results, so it is 5 credits for nothing. It is the single worst spend in the tool.
- **`vidiq_outliers` ignores its `query` argument** — it returned cat compilations and Kaiju
  gameplay for "investing stock market money", and charged 5 credits to do it. Use
  `vidiq_channel_search` and `vidiq_youtube_search`, which respect the query.
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
| `PROVENANCE.md` | **What is verified vs asserted.** Read this before trusting any claim in the repo. Unchecked claims must be labelled in the sentence that states them. |
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
