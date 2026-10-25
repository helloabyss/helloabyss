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

**Every video description carries the full disclaimer from `DISCLAIMER.md`, pasted verbatim.**
The 4-second on-screen card and the written disclaimer are both required — neither replaces
the other. `DISCLAIMER.md` also holds the extra lines to add for options, crypto and
videos naming a real person.

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

**The narrator is the same person in every video, whatever the format.**

| Setting | Value |
|---|---|
| **PARADOCS10X narrator** | **Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`** (HeyGen). Confirmed by the channel owner 2026-10-25 |
| **TMI narrator** | **Alex Wright**, or **Sheldon** — a HeyGen voice. Sheldon does not surface through `list_voices` (the `search`/`voice_type` filters are ignored and it returns the public list); get the id from the HeyGen app |
| **Aaron** | `ESDuPqgyZIDDVZTlIrH7` (ElevenLabs). **Not the channel voice.** Used on the stickman long-form; superseded |
| **Channel host** | **Zul** — see `CHARACTER-ZUL.md`. Code in `engine/zul.py`; never drawn by hand |
| HeyGen style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| Mode | `chat` (revisable — send follow-ups into the session) |
| Orientation | `portrait` (9:16) for shorts · `landscape` (16:9) for long-form |

✅ **Narrator settled 2026-10-25 by the channel owner: Alex Wright for PARADOCS10X.**
This file previously recorded Aaron as the locked narrator and called a second voice "a
defect, not a choice." That was wrong and it caused a real misbuild — a short was narrated
in Aaron on the strength of this line. **Alex Wright is the PARADOCS10X voice.** Use HeyGen
`create_speech`, which also returns **word-level timestamps** — true forced alignment, which
is what the Shorts cutting rhythm (a cut every 1.2–1.8s) needs.

Keep style, voice and host constant across videos so the channel reads as one series.

## Known environment constraints

- **HeyGen CDN egress is blocked** (`files2.heygen.ai`, `resource2.heygen.ai`, and also
  `static.heygen.ai`, which holds scene background images). Renders and stills cannot be
  downloaded or watched from here. Always report a render as *complete, not verified*, and
  give the user a verification checklist.
- **Primary sources are DNS-blocked, not just 403.** Verified 2026-10-25: `WebFetch` returns
  `getaddrinfo ENOTFOUND` for arxiv.org, metr.org, dailycal.org and others. Only server-side
  web search works, so nothing can be graded CONFIRMED. Corroborate across independent
  outlets and record the conflicts — a single search's headline number was wrong by 10x on
  2026-10-25 and re-checking is what caught it.
- **YouTube egress is blocked** (`www.youtube.com`, `googleapis.com`) — verified 2026-09-09.
  Source videos cannot be fetched, watched or transcribed directly. The only server-side
  routes are vidIQ (`vidiq_video_transcript`, 5 credits) and Higgsfield
  (`video_analysis_create`, accepts a YouTube URL) — both need credits.
- ~~**HeyGen `create_speech` needs separate `api` credits**~~ — **CORRECTED 2026-10-21. It
  works.** Called on the `creator` plan today and it returned audio **plus word-level
  timestamps**. A detached VO stem IS available. The word timestamps are the valuable part:
  they give true forced alignment of picture to narration, which no other route here does.
  (Narrator policy is unchanged — Aaron is the channel voice. Alex Wright is the shorts
  strand and adding it to a long-form would deepen the two-narrator defect, not fix it.)
- **The blocked HeyGen CDN can be routed around.** `resource2.heygen.ai` still 403s on
  CONNECT, but ElevenLabs will fetch it server-side: `creative_attach_reference_file`
  with the HeyGen URL → `creative_get_available_assets` → download the `preview_url` from
  `storage.googleapis.com`, which **is** reachable. Verified end to end 2026-10-21.
- **Higgsfield: 0 credits** (plan `starter`). Unusable for B-roll or video analysis.
- **ElevenLabs can mux audio onto video, in-session and free.** A `composition` node takes a
  video input plus audio inputs and returns a single **H.264 + AAC MP4** — verified 2026-10-05 on
  an 8-minute 1080p render, **0 credits**, ~7 min for a 92 MB WebM source. Upload with
  `creative_create_asset_upload` → HTTP PUT → `creative_finalize_asset_upload` (200 MB cap);
  WebM in, MP4 out. **This removes the need for CapCut as a mux step.** Two caveats: each audio
  source gets **its own track starting at 0** (so sequential VO parts must be concatenated into
  one file first — no `set_clip_property` is exposed to offset them), and the signed download
  URLs expire after 2 hours.
- ~~**Anything involving audio must go server-side**~~ — **CORRECTED 2026-10-21.** Playwright's
  bundled ffmpeg is indeed crippled (two muxers, no audio codecs), but it is not the only one:
  `pip install imageio-ffmpeg` puts a full static **ffmpeg 7.0.2** on the box with `libx264`,
  `aac` and an mp3 decoder. PyPI is in the proxy's `noProxy` list so it installs directly.
  Audio mux, loudness normalisation and H.264 MP4 output are all local now, in one pass.
  **Note:** two interpreters exist here — install with `/usr/local/bin/python3 -m pip` so the
  default `python3` can find it.
- **vidIQ: 101 credits** measured 2026-10-25 (100 renewable of 150 + 1 add-on; resets 2026-11-03).
  Affordable again. **Observed costs today:** `vidiq_channel_analytics` **5**,
  `vidiq_channel_videos` **5**, `vidiq_user_channels` **0** (the tool's own docs say 0 — this
  repo previously listed it as unverified), `vidiq_balance` **0**.
- **HeyGen: 1,573 premium credits**, plan `creator`, measured 2026-10-25 (resets 2026-11-15).
  Was listed as 600 on 2026-10-21; measure, do not trust this line.
  Was 54 on 2026-09-09. **Higgsfield: 350.57**, plan `starter` — the "0 credits, unusable"
  line below is stale; B-roll generation is affordable again, though note its CDN
  (`d8j0ntlcm91z4.cloudfront.net`) 403s on CONNECT, so generated plates cannot be
  downloaded here. The old figure:
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
- **What works on this channel's SHORTS**, measured 2026-10-25 (`vidiq_channel_videos`,
  format=short). Of 14 shorts since September, exactly one cleared 1,000 views: *Tesla
  Roadster: 0-60 Under 0.9s, Half the Range* — **27s, 2,960 views, breakout 23.4**.
  Everything else ran 3–521. The winner is the only title carrying **a named thing, one
  hard number, and the cost that number hides**, and it is also the shortest; the dead
  ones cluster at 38–58s behind vague category titles ("Compute Maxing" 10 views, "THE SI
  AGENT RACE" 3). Same shape as the long-form breakout DOTS VS GROK BOT. **Build shorts to
  that shape and keep them under ~40s.**
- vidIQ thumbnail scores penalise low saturation and reward vibrancy. That conflicts with
  this channel's editorial palette. **Do not chase the score** at the cost of the identity.

## The host

Every stickman video is hosted by **Zul**. Read **`CHARACTER-ZUL.md`** before
drawing him or writing a scene he appears in — he is locked the same way the
palette is. He is built by `engine/zul.py` and positioned by the centre of his
head; the model sheet is `engine/zulsheet/`.

## Repo layout

One directory per video: `SCRIPT.md` (VO, fact table, shot list, packaging) and
`PRODUCTION.md` (session IDs, settings, verification checklist, constraints hit).

Shorts: `moat-short`, `pdt-short`, `paradocs-short-1`, `paradocs-short-3` ("The $30,000
Wafer"), `paradocs-short-4` ("Moore's Law Was Never About Speed"), `paradocs-short-5`
("82% / 25%" — Agents' Last Exam; **first portrait short built on the local engine**, with
burned-in captions, sentence-aligned cuts and a measured layout guard).
Long-form: `paradocs-longform-1` (the 11m07s Cybercab video — format precedent, with its
defects listed), `paradocs-longform-2` (Apple/2nm; **scripted, fact-checked against confirmed
post-keynote reporting, thumbnails built — but the API render FAILED**. Build it in the HeyGen
app: see **`HEYGEN-APP-BUILD.md`** and paste `app-prompt.txt`. `EDIT-SHEET.md` covers CapCut
assembly if event clips are cut in).

**Lesson recorded:** the API's `generate` mode cannot reach blueprint approval, so constraints
get one shot and a failure costs ~45 credits with no error message. For long-form, prefer the
HeyGen app — the blueprint step lets you approve before it spends, and captions are a toggle
there rather than a defect on every render.
