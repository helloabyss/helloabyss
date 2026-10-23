# Production — TWIM 2026-09-25 · The ten-year at 5%

**Runtime** 101.9s · **9:16** 1080×1920 · **30fps** · **0 credits**
**Script** `scripts/2026-09-25.md` · **Research** `research/2026-09-25.md`

---

## Source ingestion — how a blocked link got read

The brief was "watch this Facebook video and make a short from it". Facebook is **blocked by
the egress proxy** (`connect_rejected`, gateway 403 on `www.facebook.com:443`), so the clip
could not be opened, fetched or watched from this environment at all.

**What worked:** OpusClip accepts Facebook URLs and ingests server-side, outside this
environment's egress policy. Project `P3092504KIRS` → 179s source → full transcript with
per-word timings, pulled via `opusclip_get_transcript` and archived to
`research/2026-09-25-source-transcript.txt`.

**What to know next time:**
- **Each submit bills ~1 hour of the OpusClip monthly API cap**, success or failure. Two
  submissions took the cap 52 → 53 of 60 hours. Do not resubmit speculatively.
- The job sat at `QUEUED` with a frozen `updated_at` for **~20 minutes** before completing.
  That is not a failure signal — it is just slow. A retry submitted during the wait was pure
  waste (project `P3092504NgZ3`, still queued, discard it).
- vidIQ's `watch_shortform_content` is the obvious alternative and was **unusable**: it costs
  10 credits, the account has 1, and it does not accept Facebook URLs anyway.
- `opusclip_get_transcript` returns ~89k characters for a 3-minute video because of per-word
  timing arrays. It **exceeds the tool output limit** — read it off disk with `jq`/`python`
  rather than into context.

## Build

Same pipeline as `videos/mstr-btc-2026-09-23`, which is the reference implementation.
`gen.py` + `tpl.tplsrc` → `index.html`. Kokoro `am_michael` for the local voice track.

- 8 paragraphs in `vo.txt` → 8 scenes, one per paragraph, cut at narration midpoints
- 259 words → **97.2s at 159.9 wpm** through Kokoro
- 59 caption groups, word-level highlight timing derived from the synthesis itself
- Number wheels in scenes 1, 3 and 6 (`5.12`, `70`, `7.03`)
- Two mirrored line charts: scene 6 rises (mortgage 6.71 → 7.03), scene 7 falls
  (10-year 4.28 → 3.73). The rhyme is the argument

### Validation
```
0 error(s), 0 warning(s), 15 info(s)
Motion     0 errors, 0 warnings
Contrast   69/69 text checks pass WCAG AA
Check passed
```
The 15 infos are all `hf-number-wheel-strip` overflow — the rolling digits are *supposed* to
sit outside the clip window. Same as the MSTR build. Not a defect.

## Known pitfalls this build avoided

Carried forward from the MSTR post-mortem:
- **Caption ID collision.** MSTR lost most of a scene when scene ids `#g1`–`#g7` collided with
  caption ids `#g0`–`#g71`. This build namespaces captions as `#cg{n}` / `#cw{n}_{m}` and uses
  no `g`-prefixed scene ids.
- **`tl.set()` is not seek-safe.** Zero-duration tweens do not re-evaluate under the renderer's
  per-frame seek and stack caption lines on screen. All caption reveals are tiny-duration
  `.to()` on `autoAlpha`.
- **`immediateRender:false`** on the wheel tweens, so entrance state is not clobbered on seek.
- **Brace escaping** — `tpl.tplsrc` is not named `.html`, or the CLI treats it as a second root
  composition. `{{`→`{` runs last in `gen.py`.

## Local frame QA

Screenshotting the composition needs `window.__timelines = {}` stubbed via `addInitScript`
before load — standalone `file://` has no HyperFrames runtime, so the composition's
`window.__timelines["main"] = tl` throws and the timeline never registers.

Playwright lives at `/opt/node22/lib/node_modules/playwright`; Chromium at
`/opt/pw-browsers/chromium`. **Kill stray browsers between runs** — leftover Chromium
processes from an aborted capture starved the next one and it hung with zero frames written.

## Voice — Alex Wright cut

User directive: **"Only Alex Wright."** Approved spending credits on the locked voice.

**The constraint that decides the shape of this cut:** HeyGen's CDN (`files2.heygen.ai`,
`resource2.heygen.ai`) is blocked from this environment, so a HeyGen audio stem **cannot be
downloaded** and therefore cannot be swapped into the HyperFrames picture via
`swap_voice.sh`. The only way to get the locked voice onto a finished video from here is to
let HeyGen render the whole thing — which means **HeyGen's picture, not the charts in this
project**. Two separate cuts, not one merged one.

**Submitted** with the `PRODUCTION.md` recipe from `videos/mstr-btc-2026-09-23`:
- `session_id` `b863363d9f284d7daa975741e2dd23b7` ·
  watch: https://app.heygen.com/video-agent/b863363d9f284d7daa975741e2dd23b7
- `video_id` `3f8e1bd9b43142c8af83c26b9efb1d11`
- `mode: generate`, portrait, style `e7f9a126…` (Economist),
  voice `0db3abd8…` (Alex Wright – Informative), glossary `c9064148…`
- Full prompt carried the verbatim script plus every palette, faceless, no-logo, chart and
  compliance constraint, because generate mode has no blueprint approval step

**RESULT: completed.** Attempt 1 (`b863363d…`) looped on a caption prerequisite and was
stopped manually → `failed`, **zero credits**. Attempt 2 (`5f0b6160…`, video
`4e87955e22af47b687fcc29026b392e3`) cleared the blocker and completed.

- **99.29s · 9:16 · 1080p · 25 scenes · 67 credits (235 → 168) = 40.5 cr/min**, matching the
  40.3 cr/min baseline in `RENDERING.md`
- Title auto-set to **"The Ten-Year Yield"** — good enough to keep
- Watch: https://app.heygen.com/videos/4e87955e22af47b687fcc29026b392e3

### Verified from `get_video_scenes`
| Check | Result |
|---|---|
| Voice `0db3abd8…` on all 25 scenes | **PASS** |
| Script verbatim — 1,442 chars, character-exact against `vo.txt` | **PASS** |
| Faceless — 25 `motion_graphics` elements, **zero** avatar elements | **PASS** |
| 9:16, 1080p | **PASS** |
| Brand glossary `c9064148…` | **PASS** |
| Closing disclaimer card — final scene is `<break time="4.0s"/>` held in silence | **PASS** |
| `caption.enabled` | **false** — but `captioned_video_url` **is** populated |

**Captions are available this time.** The MSTR run had no captioned cut; here the caption
style that blocked the render twice is exactly what produced one. Publish
`caption_4e87955e22af47b687fcc29026b392e3.mp4` from the video page — no re-render needed.

**UNKNOWN — needs eyes.** Every scene reports `background:#ffffff` with a single opaque
`motion_graphics` element. A full-frame dark plate is invisible to this API, so **whether the
three-colour palette, the mirrored rising/falling charts and the opening compliance card
actually landed cannot be resolved from here.** CDN egress is blocked. Watch it on the video
page before publishing.

## Voice — local placeholder cut

Also rendered with the **local Kokoro placeholder**, not the channel voice. `VO_PROFILE.md`
requires Alex Wright (`0db3abd83c74452fb2460b0dd113daad`) for series cohesion.

**Swap path:** `videos/twim-2026-09-20/swap_voice.sh` aligns an exported HeyGen stem to the
existing scene cuts and re-renders — no rebuild needed.

**Cost of the voiced cut:** ~102s at the measured 40.3 cr/min ≈ **~69 credits**, against a
**235-credit balance** (resets 2026-10-06). Not spent — see `RENDERING.md` for why the cheap
Avatar III carrier path was tested and rejected. **Ask before spending.**

## Status

**Complete, not verified for publish.** The cut renders and passes every automated gate. It
is blocked from publishing by the `[OPEN]` flags in `research/2026-09-25.md` §3 — no primary
source was reachable, so every figure is convergence-graded across independent outlets.

Before upload, confirm from an unblocked machine:
- [ ] 10-year yield 5.11–5.12% on 2026-09-24 — `home.treasury.gov` daily yield curve
- [ ] "Highest since 2007" framing
- [ ] 30-yr mortgage 7.03%, week of 2026-09-24 — Freddie Mac PMMS
- [ ] 10-year path 4.28% (2024-07-24) → 3.73% (2024-08-05) — FRED `DGS10`
- [ ] Prior 5% print October 2023
