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

## A video is four things, not one — NON-NEGOTIABLE

**Nothing counts as delivered until all four exist.** Asked for "a video", produce all
four without being asked again; this standing instruction was given 2026-10-08 and does
not expire.

| | Where it goes | Built by |
|---|---|---|
| **Video** | the render | `engine/render_anim.js` (or the house path) |
| **Thumbnail** | `engine/thumb.png`, 1280×720 | `engine/make_thumb.py` — zero credits, deterministic |
| **Title** | `<dir>/PACKAGING.md` | the hook, verbatim from the VO's opening line |
| **Description** | `<dir>/PACKAGING.md` | disclaimer first, then chapters, then sources |

Rules that bind all four together:

- The **title is the hook**. It is the voiceover's opening sentence, which is the most
  surprising true thing in the fact table. Not a separate piece of writing, and never
  clickbait (§ house style).
- The **thumbnail carries a claim from the fact table**, not a tease. Both halves of a
  contradiction must be CONFIRMED rows. No arrows, no circles, no shock faces.
- The **description leads with the compliance paragraph** and the positions line, per
  `DISCLAIMER.md`. Everything else goes below them.
- **Check the thumbnail downscaled to ~320px** before calling it done. If the numbers
  stop reading at sidebar size it has failed, whatever it looks like full-bleed.
- Chapter timings read off the built timeline are where the *picture* cuts, not where
  the *narration* breaks. Say so, and have them confirmed on the watch-through.
- **Measure the audio loudness of every cut before delivering it.** Target **−14 LUFS**
  integrated, true peak at or under −1.0 dBTP, stereo:
  `ffmpeg -i <file> -af loudnorm=I=-14:TP=-1.5:print_format=json -f null -`
  ElevenLabs output is **not** normalised — `ai-picks-longform` came back at −24.66 LUFS,
  10.7 dB under target, and was delivered sounding like it had no voiceover at all.
  Confirming an audio stream *exists* is a different check and will not catch this.

## Fixed production settings

| Setting | Value |
|---|---|
| HeyGen style | Economist — `e7f9a12679ec426099db7646b70a4639` |
| HeyGen voice | Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad` |
| Mode | `chat` (revisable — send follow-ups into the session) |
| Orientation | `portrait` (9:16) |

Keep style and voice constant across videos so the channel reads as one series.

**The voice is Alex Wright. It has one recorded exception.** `ai-picks-longform` ships
narrated by **Aaron** (`ESDuPqgyZIDDVZTlIrH7`, ElevenLabs) because HeyGen was on the free
plan when it was produced. That was a forced *platform* substitution; reaching for Aaron,
the parked tech channel's voice, was not forced, and calling it "the locked channel voice"
in `ai-picks-longform/PRODUCTION.md` was false. The user's call on 2026-10-08 was to keep
that cut and fix the record. **Alex Wright is still the channel voice**; a second episode
in Aaron would be a channel-voice change and needs an explicit decision. If HeyGen stays
unavailable, audition an ElevenLabs match for Alex Wright rather than defaulting to Aaron
again.

## Known environment constraints

**Credit figures measured 2026-10-05. Re-check with `vidiq_balance`, `higgsfield balance` and
`heygen get_current_user` at the top of each session — this block has been wrong before in
both directions. In September it understated what was available and the channel avoided tools
it could afford; by 2026-10-05 the same block overstated two balances by three orders of
magnitude, which is the more expensive failure because it plans spends that cannot clear.**

| Resource | Status **2026-10-08** | On 2026-10-05 |
|---|---|---|
| HeyGen | ⚠️ **Plan is now `free`; premium credits `null`.** The Pro plan and its 10-06 reset are gone. Treat the house render path as unavailable until resolved | Pro, 0 credits, reset due 10-06 |
| Higgsfield | **242.35 credits**, starter — **B-roll IS available** | 0.35 — unusable |
| vidIQ | **116** = 115 renewable (of 150) + 1 add-on. Resets **2026-11-03** | 121 |

All three read directly from `vidiq_balance`, `higgsfield balance` and `heygen
get_current_user` on 2026-10-08 — observed, not inferred. **In three days HeyGen
went Pro → free and Higgsfield went 0.35 → 242.** This block goes stale faster
than anything else in the file; the session-start re-check is not optional.

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
  | `vidiq_video_transcript` | **5** | **observed 2026-10-08** — balance 121 → 116 on one call |
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
- **B-roll sourcing — established 2026-10-08. Read before spending on imagery.**
  **Higgsfield output cannot be retrieved from this environment.** Its CDN
  (`d8j0ntlcm91z4.cloudfront.net`) returns **403 on CONNECT** at the agent proxy — a policy
  denial, not a transient failure, and `curl -sS "$HTTPS_PROXY/__agentproxy/status"` logs it
  as `connect_rejected`. Three usable plates generated on 2026-10-08 are stranded in the
  account. Routing the URL through ElevenLabs' server-side fetch
  (`creative_attach_reference_file`) was tried twice and added no node. **Generating b-roll
  on Higgsfield is money for files you cannot download. Do not do it** until the host is
  allowed.
  **ElevenLabs creative generation is broken through the MCP bridge**, which returns a
  schema-validation error (`missing required resultType`) for `creative_generate_image`,
  `creative_attach_reference_file`, `creative_get_model_guide` and
  `creative_get_available_assets`. `creative_list_voices` and `creative_get_flow` return
  normally, so the bridge is up and the fault is tool-specific. A call that errors this way
  may still have run server-side, so **do not retry these in a loop** — each attempt can
  spend without returning anything retrievable.
  **What does work: Adobe Stock's free collection.** `adobe_mandatory_init` → `asset_search`
  with `entityScope: "StockAsset"` → `asset_license_and_download_stock` → download the
  presigned URL. Assets marked `"pricing":"free"` license at **no cost** and the file lands
  locally. The free collection is uneven — "rocket launch" returned an Iron Dome battery and
  an aircraft carrier — so read each result's name and reject anything off-subject; industrial
  and technology subjects (data centres, substations, wafers, dish arrays) are well covered.
  See `engine/broll/MANIFEST.md`. **Plate files are gitignored**: an Adobe Stock licence
  covers use in a work, not redistribution, and this repository may be public.
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
| `engine/art/` | **CANONICAL Zul artwork — the supplied originals.** These are the character; the vector rig and cut-out parts are secondary and must match them. Place figures with `art.zul_art()`. |
| `CHARACTER-ZUL.md` | **Zul**, the host that series would use. Locked design, built by `engine/zul.py`, never drawn by hand. Transferred from the parked PARADOCS10X channel — a deliberate reuse, not continuity. |
| `PROCREATE-PIPELINE.md` | **How hand-drawn iPad art gets in and how it animates.** Canvas sizes and pivots are a contract, not a convention. Proven end to end. |
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
