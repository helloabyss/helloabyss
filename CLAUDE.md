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
| vidIQ | **41 add-on credits**; renewable pool 0/150, resets 2026-10-03 |

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`). Renders
  cannot be downloaded or watched from here. Always report a render as *complete, not
  verified*, and give the user a verification checklist.
- **HeyGen `create_speech`** failed on the old Creator plan (needs separate `api` credits).
  The account is now Pro — **untested since the upgrade.** Test once before assuming there is
  no detached VO stem.
- **vidIQ cost discipline.** Research calls (`channel_stats`, `channel_videos`,
  `channel_search`, `youtube_search`, `keyword_research`) appear not to draw down the balance.
  Generation does: thumbnail 22, scoring 5. With 41 credits that is **one thumbnail, or eight
  scores — not both.** Spend on research first; HeyGen generates a free thumbnail per session.
- **`vidiq_outliers` ignores its `query` argument** — it returned cat compilations and Kaiju
  gameplay for "investing stock market money". Use `vidiq_channel_search` and
  `vidiq_youtube_search` instead; both respect the query.
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
| `.claude/agents/` | scout · fact-checker · scriptwriter · art-director · packager |

**Unresolved:** the connected YouTube channel is `PARADOCS10X` (AI/tech, 57 subs), not a
finance channel. See `GROWTH-PLAN.md` §1 — this gates publishing automation.
