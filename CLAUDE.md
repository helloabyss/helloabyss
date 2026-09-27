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

**`STANDARD.md` is the approved Short (owner sign-off 2026-09-27, reference: Opus 5.5 v4).**
Build every Short to it with the engine in `build/standard/`. Where it disagrees with
`STYLE-GUIDE.md`, `STANDARD.md` wins. `STYLE-GUIDE.md` still holds the HeyGen Video Agent brief
template and the identity rules below. Summary of the non-negotiables:

- **Imagery-first, three-layer stack.** Cinematic photographic imagery is the BASE layer,
  motion graphics over it, type and captions on top. Never typography on abstract
  backgrounds — that was tried and rejected.
- **Faceless.** No avatars, no presenters, no identifiable people, ever.
- **No real corporate logos or badges.** Use plain text name-tags.
- **Three-colour editorial palette.** Near-black, white and one accent (amber for tech,
  red for finance). Imagery is graded **bright** per `STANDARD.md`; the owner rejected the dark,
  desaturated grade on 2026-09-27. No neon, gradients, sparkles or emoji.
- **Music bed and a whoosh on every cut** (`STANDARD.md` §6), with fresh B-roll every video, never reused.
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

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`). Renders
  cannot be downloaded or watched from here. Always report a render as *complete, not
  verified*, and give the user a verification checklist.
- **HeyGen `create_speech` needs separate `api` credits**, which the Creator plan lacks.
  No detached VO stem is available; narration is baked into the render.
- **Higgsfield: 0 credits.** Unusable for B-roll unless topped up.
- **vidIQ: ~1 credit.** Thumbnail generation costs 22, scoring 5. Needs a top-up.
- vidIQ thumbnail scores penalise low saturation and reward vibrancy. That conflicts with
  this channel's editorial palette. **Do not chase the score** at the cost of the identity.

## Repo layout

One directory per video: `SCRIPT.md` (VO, fact table, shot list, packaging) and
`PRODUCTION.md` (session IDs, settings, verification checklist, constraints hit).
Engine-built Shorts: `build/<ep>/` (`scenes.js`, `words.json`) on top of `build/standard/`
(`core.js`, `render.sh`, `preview.js`, `words.py`), with records in `scripts/<date>-<slug>-*`.
