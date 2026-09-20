# Production Record — This Week in Tech, 2026-09-20

## v2 — FULL CUT WITH CINEMATIC PLATES ✅ (2026-09-20)

**Watch / download:**
https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/759185cd-6001-499c-aa9a-56221ea31326.mp4

54.367s · 1080×1920 · 30fps · H.264 · 12.1MB · **total cost 1.56 Higgsfield credits**

Every placeholder plate is gone. The 12 photographic shots now carry real cinematic
imagery, generated on Higgsfield and graded to the house look; the 8 motion-graphic shots
are the same builds as v1. Captions, lower-thirds, the amber wipe and all timings are
unchanged, so the runtime still matches `VO_PROFILE.md` exactly.

| | |
|---|---|
| Imagery | 9 plates, `soul_cinematic` @1.5k, 9:16 — `build/plates/PROMPTS.md` |
| Grade | `build/plates/norm.py` — per-plate normalised to luminance 35 |
| Motion | Ken Burns per shot (zoom + pan), vignette, bottom gradient for caption legibility |
| Assembly | Playwright + ffmpeg **inside the Higgsfield sandbox** (the CDN is blocked here) |

### Cost discipline
`get_cost: true` preflights before spending anything:
`soul_cinematic` @1.5k **0.12** · `z_image` 0.15 · `nano_banana` 1 · `cinematic_studio_2_5` 2
· **`generate_video` (seedance_2_5, 5s) 35.**

Stills + the free local compositor is ~290× cheaper than generated video, and it keeps
exact control of the 2–3s shot grid. Generated clips cannot be timed to it.
**998.44 credits remain.**

### Still no fabricated products
No real product or UI was generated — no Google Home app, no Snap Specs, no iOS screens.
Plates are generic, unbadged objects, following the finance channel's existing practice.
The specifics stay in type: counters, stamps, lower-thirds and captions.

### What is still missing
**Narration.** Unchanged — HeyGen premium credits are 0 until 2026-10-06 and the locked
series voice exists only there. The cut is silent; captions carry it.
**Shot 17's aperiodic tiling patch** is still the single hat tile rather than a true
tiling patch, for the reason below.

### Verified
Frames extracted from the finished MP4 at 1s, 12s, 19s, 30s, 42s and 53s and checked:
plates, lower-thirds, captions and the hat tile all present and correctly placed.
**Not verified by eye** — the Higgsfield CDN is blocked from this container, so the plates
and the final file could not be viewed directly. Composition was QA'd as ASCII luminance
maps and the grade numerically. Watch it before publishing.

---

## v1 — animatic (superseded, kept for the record)

## What was rendered

**`scripts/2026-09-20-animatic.mp4`** — 54.37s · 1080×1920 · 30fps · H.264 · 12MB

A complete timed **animatic (previz)** of the episode. Every one of the 20 shots is in
place at its exact timecode, with burned-in captions, lower-thirds, the amber wipe and the
full house visual system from `STYLE.md`.

Built locally with Chromium + Playwright frame capture + ffmpeg. **No render credits were
used or required.** Source lives in `build/animatic/` and regenerates the file
deterministically.

| Rendered for real | Marked as a placeholder plate |
|---|---|
| Amber wipe between all four beats | 11 shots needing licensed or owner-recorded footage |
| Lower-thirds with source + date | Each plate carries its shot number, description, **exact source** and **licence status** |
| Burned-in word-by-word captions, current word amber | |
| `$20` and `250+` counters | |
| `$2,195` counter → `NOT SHIPPED` stamp + flash | |
| `BETA` stamp with screen shake | |
| Three-tier silicon graphic | |
| `US ONLY` amber fill sweep | |
| **The hat monotile** — geometry verified, see below | |
| Chiral pinwheel diffraction (labelled illustrative) | |
| Closing question card | |

### The hat tile geometry is verified, not approximated
The closing beat's subject had to be the real shape. It was confirmed three independent ways:

1. **Edge signature** — 13 edges as drawn: 6 long (√3), 6 short (1), 1 double-short (2).
   Matches the published description of the hat exactly.
2. **Area** = 13.856406 = **8√3** — exactly 8 kites, as required for an octakite.
3. **Independent derivation** — an exhaustive enumeration of 37,398 connected 8-kite
   subsets of a hexagonal kite grid yielded 46 distinct shapes with the right boundary
   signature; the published coordinates match candidate #39 of that set.

Coordinates cross-checked against `christianp/aperiodic-monotile` (**CC0**). The artwork is
redrawn from the coordinates, not lifted from the SVG.

## What is NOT in this file, and why

| Missing | Reason |
|---|---|
| **Narration** | HeyGen premium credits are **0 until 2026-10-06**. The locked series voice is HeyGen `Alex Wright - Informative`; no other provider reproduces it. |
| **Licensed footage** | Press-kit and stock clips cannot be downloaded — the egress proxy blocks those domains. |
| **Screen recordings** | Must be captured on the owner's own devices (Google Home app, iOS 27 Siri). These are the safest assets in the episode: real, free, unambiguously licensed. |
| **Hat tiling patch** (shot 17) | A valid aperiodic patch needs the H/T/P/F metatile substitution. Left as a labelled build task rather than faked — a wrong tiling is exactly what a top comment would catch. |

The animatic is silent. It is a cutting guide and a timing proof, not a publishable cut.

## Render paths, checked 2026-09-20

| Provider | State | Verdict |
|---|---|---|
| **HeyGen** | 0 premium credits, resets 2026-10-06 | Correct voice. **Blocked until top-up or reset.** |
| AgentOpus | 385 recurring credits | Available, but a **different voice** — breaks `VO_PROFILE.md`. Not used. |
| Higgsfield | 0 credits, starter plan | Unusable. |

**Voice cloning was not attempted.** `Alex Wright - Informative` is a licensed HeyGen
library voice; cloning it onto another platform would be a licensing problem, and the
preview audio sits behind blocked CDN egress in any case.

## To finish the episode

1. **Narration** — add HeyGen `api` credits, then `create_speech` with
   `voiceId 0db3abd83c74452fb2460b0dd113daad`, `speed 1.0 / pitch 0 / volume 1.0`,
   `brandGlossaryId c7cb764ee025432caa879e8d76048c7f`, script = `scripts/2026-09-20-vo.txt`.
   Or wait for the 2026-10-06 reset.
2. **Record the two screen captures** (Google Home app; Siri on iOS 27).
3. **Download the Snap press kit** (A5, A7). **Do not use the launch-event clip (A6)** —
   build shot 9 from press-kit stills as the manifest specifies.
4. **Licence the three stock plates** (A1/A4/A10) or substitute.
5. **Build the tiling patch** for shot 17 from the CC0 repo.
6. Cut to the animatic's timings, burn captions per `STYLE.md`, export 1080×1920.

## Verification checklist — needs your eyes

1. **Runtime** lands 50–60s once real VO replaces the estimate (currently 54.4s estimated).
2. **Captions clear the Shorts UI** — they sit 470px off the bottom; confirm on a phone.
3. **Amber wipe** reads as deliberate at all four beat boundaries, not as a glitch.
4. **No caption flashes** — shortest cue is 0.79s by construction.
5. **Pre-publish fact check** — the four-item list in `scripts/2026-09-20.md`. No source
   was opened directly; the egress proxy blocked every news and primary-source domain.
6. **Font substitution** — the animatic uses Liberation Sans; `STYLE.md` specifies
   **Inter Tight ExtraBold**. Swap it for the final.

## Constraints hit
- HeyGen CDN egress blocked (`files2.heygen.ai`, `resource2.heygen.ai`) — unchanged.
- `WebFetch` and `curl` blocked for all news/primary-source domains; only `WebSearch` works.
- Playwright's bundled ffmpeg is VP8-only; `imageio-ffmpeg` supplied an H.264 build.
- No system Inter Tight; container has 59 fonts, none condensed.

## Regenerating the animatic
```bash
cd build/animatic && python3 -m http.server 8931 &
NODE_PATH=/opt/node22/lib/node_modules node capture.js     # 1631 frames, ~55s
ffmpeg -framerate 30 -i /tmp/fr/%05d.jpg -c:v libx264 -preset slow -crf 19 \
       -pix_fmt yuv420p -movflags +faststart scripts/2026-09-20-animatic.mp4
```
Edit `shots.json` to change shot content, timing, sources or licence status. `cues.json` is
generated from the SRT, so captions can never drift from the narration.
