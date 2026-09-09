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

## Long-form

`STYLE-GUIDE.md` is written for Shorts and its pacing rules break at length.
**For anything over ~2 minutes, read `LONGFORM-GUIDE.md`** — 16:9, a 16-beat spine,
~166 wpm, ~66 words per scene, and its own brief template. The hard rules (faceless, palette,
no logos, compliance card, mandatory counter-evidence) are unchanged at any runtime.

## Fixed production settings

| Setting | Value |
|---|---|
| HeyGen style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| HeyGen voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` (revisable — send follow-ups into the session) |
| Orientation | `portrait` (9:16) |

Keep style and voice constant across videos so the channel reads as one series.

## Known environment constraints

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`, and also
  `static.heygen.ai`, which holds scene background images). Renders and stills cannot be
  downloaded or watched from here. Always report a render as *complete, not verified*, and
  give the user a verification checklist.
- **YouTube egress is blocked** (`www.youtube.com`, `googleapis.com`) — verified 2026-09-09.
  Source videos cannot be fetched, watched or transcribed directly. The only server-side
  routes are vidIQ (`vidiq_video_transcript`, 5 credits) and Higgsfield
  (`video_analysis_create`, accepts a YouTube URL) — both need credits.
- **HeyGen `create_speech` needs separate `api` credits**, which the Creator plan lacks.
  No detached VO stem is available; narration is baked into the render.
- **Higgsfield: 0 credits** (plan `starter`). Unusable for B-roll or video analysis.
- **vidIQ: 1 credit** as of 2026-09-09 (0 renewable + 1 add-on); resets to 150 on 2026-10-03.
  Transcript costs 5, video-watch 25, thumbnail 22, scoring 5 — **all currently unaffordable**.
- **HeyGen: 54 premium credits** as of 2026-09-09 (down from 129), resets 2026-10-06.
  ⚠️ **A long-form render appears to cost ~45 credits and can fail with no error message,
  consuming them anyway** — see `paradocs-longform-2/PRODUCTION.md`. At this balance there is
  roughly **one** long-form attempt left. Shorts are cheap by comparison.
- **`create_video_agent` prompt cap is 10,000 characters**, which limits a single-call verbatim
  long-form to ~1,350 words (~8 min). See `LONGFORM-GUIDE.md`.
- **A ~1,350-word / ~8-minute landscape generate-mode render FAILED** on 2026-09-09 with
  `failure_code: null` and `failure_message: null`, minutes after two ~150-word portrait renders
  succeeded. Long scripts through this API path are **not proven**. Do not promise a long-form
  runtime without testing at a small size first.
- **HeyGen chat mode is currently unusable** — verified 2026-09-09. Sessions are accepted and
  appear in `list_video_agent_sessions`, but `get_video_agent_session` returns 404 for **every**
  session, new and old alike, so the blueprint-approval step cannot be reached. Credits are not
  the cause. **Fall back to `mode: generate`**, which returns a real `video_id` immediately and
  is trackable via `get_video`. Note `bulk_video_statuses` reports `not_found` for a freshly
  created video while `get_video` correctly reports `pending` — trust `get_video`.
  Generate mode skips blueprint approval, so **harden the prompt before firing**: state the
  caption requirement on its own line, ban typography over flat colour explicitly, and make the
  palette absolute.
- vidIQ thumbnail scores penalise low saturation and reward vibrancy. That conflicts with
  this channel's editorial palette. **Do not chase the score** at the cost of the identity.

## Repo layout

One directory per video: `SCRIPT.md` (VO, fact table, shot list, packaging) and
`PRODUCTION.md` (session IDs, settings, verification checklist, constraints hit).

Shorts: `moat-short`, `pdt-short`, `paradocs-short-1`, `paradocs-short-3` ("The $30,000
Wafer"), `paradocs-short-4` ("Moore's Law Was Never About Speed").
Long-form: `paradocs-longform-1` (the 11m07s Cybercab video — format precedent, with its
defects listed), `paradocs-longform-2` (Apple/2nm; scripted and fact-checked, **not rendered** —
blocked on confirming what the keynote actually announced; see `EVENT-RUNSHEET.md` for the
fill-in list and `EDIT-SHEET.md` for the CapCut assembly plan).
