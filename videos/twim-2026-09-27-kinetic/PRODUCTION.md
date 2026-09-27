# Production — The Meticulous Investor · kinetic weekly, 2026-09-27

**69.5s · 9:16 · 1080×1920 · 30fps · silent · 0 credits**
Research: `research/2026-09-27.md` · Build: `videos/twim-2026-09-27-kinetic/`

---

## Brief

> "Kinetic motion graphics short… most interesting headlines on Wall Street this week… the
> viewer should be intrigued and have a plan… Don't use external tools."

Read as: **local HyperFrames only.** No HeyGen, no Higgsfield, no vidIQ, no OpusClip. Web
search was still used, because `CLAUDE.md` forbids scripting finance content from memory —
that is a research requirement, not a production tool.

## Why it is silent

No voiceover, and that is a decision rather than a limitation.

1. The locked channel voice (Alex Wright) is only reachable through HeyGen, which the brief
   rules out. A Kokoro placeholder would break series continuity — `VO_PROFILE.md` exists
   precisely to stop that.
2. **Shorts are watched muted.** A kinetic piece that carries its whole argument in type is
   *stronger* silent than a narrated piece watched with the sound off.
3. It makes the type do the work, which is what "kinetic motion graphics" actually means.

A music bed can be added later without touching the build — drop an `<audio>` element with
`data-start`/`data-duration` into the root and re-render. Nothing else changes.

## Structure — 8 scenes on a 0.5s beat grid

Silent means there is no narration to sync to, so pacing is a hand-placed **beat grid**
(`B = 0.5s`, `b(n)` in `gen.py`). Every reveal lands on a beat; the piece has a pulse even
with no audio.

| # | Scene | Beats | The move |
|---|---|---|---|
| 01 | The hook | 0.0–6.5 | "THE MARKET WENT UP." → slam "ALMOST NOTHING IN IT DID." |
| 02 | The tape | 6.5–15.0 | **Bar race** — Nasdaq +2.1% / S&P +1.2% / Dow +0.3%, then "seven times the Dow's week" |
| 03 | Meanwhile | 15.0–22.5 | Number wheel rolls to **5.18%**, slam "HIGHEST SINCE 2007" |
| 04 | The part that doesn't fit | 22.5–29.5 | The thesis: a higher risk-free rate should compress multiples — "THIS WEEK IT DIDN'T" |
| 05 | What actually changed | 29.5–37.5 | Two wheels side by side: **42% → 58%** October hike odds |
| 06 | The week ahead | 37.5–50.5 | Calendar strip builds row by row — five prints |
| 07 | How to be ready | 50.5–60.0 | Three **if → then** scenarios, then "WRITE THEM DOWN BEFORE MONDAY" |
| 08 | Close | 60.0–65.0 | "PREPARED BEATS REACTIVE." |
| — | Disclaimer | 65.0–69.5 | Full card |

## The motion vocabulary

Four composable helpers in the template, used everywhere:

- **`slam`** — scale 1.34 → 1 with `power4.out`. The signature move; carries every punchline.
- **`wordsIn`** — per-word `yPercent` stagger. The kinetic backbone for sentences.
- **`rise`** — quiet lift for supporting lines, so it never competes with a slam.
- **`bar` / `wipe`** — horizontal reveals for the race and the rules.

Restraint is the point: one loud move per scene, everything else supports it. A short where
everything slams reads as noise.

## Editorial

The hook is the **contradiction**, not the headline. "Yields hit a cycle high" is what every
channel will run. "Every index closed green while the 10-year hit its highest since 2007, and
the advance was seven-to-one Nasdaq over Dow" is the same week, read properly.

The "plan" in scene 07 is deliberately **scenarios, not instructions** — `COMPLIANCE.md`
forbids recommendations. "Decide what each print means before it lands" is preparation, which
is what the brief asked for, and it is education rather than advice.

## Compliance

- ✅ "Educational only. Not financial advice." on screen from **0.55s**, inside the 4s rule
- ✅ Full disclaimer card, 4.5s
- ✅ Attribution stamp on every scene
- ✅ Every week-ahead number labelled **estimate / consensus**, never a price
- ✅ Hike odds labelled **"Market pricing — not a forecast"** on screen
- ✅ No clickbait, no CTA, no subscribe animation
- ✅ Closes on preparation, not a position
- ⚠️ `[OPEN]` all figures convergence-graded — primary sources blocked. **Blocks publish.**

## Validation

```
Lint      0 errors, 10 warnings   (inline-scene advisories, same as every project here)
Runtime   0 errors, 0 warnings
Layout    0 errors, 0 warnings, 19 infos  (number-wheel strip overflow — intentional)
Motion    0 errors, 0 warnings
Contrast  56/56 text checks pass WCAG AA
```

Two collisions were caught by the layout checker and fixed before render: the scene-06 title
ran into the first calendar row, and the scene-07 title wrapped onto the red line beneath it.

## Packaging

**Titles** (no clickbait):
1. `Every Index Rose. Almost Nothing In It Did.`
2. `The Week Bonds Broke And Stocks Didn't Care`
3. `Five Prints That Decide Next Week`

Recommend **1** — it is the actual finding, it creates the question the video answers, and it
promises nothing it doesn't deliver.

**Description:**
```
Every major index closed the week higher. The 10-year Treasury hit 5.18%, its highest
since 2007. Those two things are not supposed to happen together.

The advance was narrow: Nasdaq +2.1% against the Dow's +0.3% — seven to one.

Five prints decide next week: JOLTS (Tue), Core PCE and Micron (Wed), ISM (Thu),
payrolls (Fri). Decide what each one means before it lands.

Figures as of 2026-09-25. Estimates are consensus, not predictions.
Educational only. Not financial advice.
```

## Bug found by frame inspection, not by the checker

The first render produced **three empty bar tracks** in scene 02 — no fill at all, which
silently killed the "seven to one" argument the scene exists to make.

Cause: `.barFill` was absolutely positioned with `left:0` and a height, but **no `width`**.
An absolutely positioned element with no width and no right anchor collapses to zero, and
`scaleX(0.84)` of zero is still zero. Fix: `width:790px` on `.barFill`, matching `.barTrack`.

`check` passed cleanly both before and after — **a zero-width element is not an error, it is
just invisible.** Contrast, motion, layout and lint all reported green on a scene that was
rendering nothing. This is the standing argument for pulling real frames out of the MP4 on
every build, not trusting the validator.

---

## Voiced cut — Alex Wright + B-roll (HeyGen)

User direction, 2026-09-27: **"I want videos that are produced with the Alex Wright VO. Add
b-roll with fitting pictures too."** This is now the default for the channel.

The locked voice is only reachable through HeyGen's video agent, and HeyGen's CDN is blocked
here, so the voiced version is a **HeyGen render**, not this HyperFrames build with a new audio
track. B-roll suits that path: `CLAUDE.md` already specifies cinematic photography as the base
layer with motion graphics over it.

- VO: `scripts/2026-09-27-vo.txt` — 157 words, facts from `research/2026-09-27.md`, rewritten
  for the ear (the hook uses the index ratio rather than "almost nothing in it did", which leaned
  on single-sourced sector data)
- `session_id` `d89984c8f1c242ce9d8ebaf9195d0e3c` · `video_id` `692226063fb54a55a502206ad478ac53`
- generate mode, portrait, Economist style, Alex Wright `0db3abd8…`, glossary `c9064148…`
- B-roll brief per beat: financial-district skyline, blurred trading screens, stone columns and
  bond paper, empty boardroom, desk calendar, wafer and server racks, empty factory floor, empty
  office, sunrise. No faces, logos, seals or signage; graded dark and desaturated
- Budget: ~45 credits against a 110 balance

The balance was 110, not the 168 left after the 2026-09-25 render: a 40s video titled
"Claude Opus 5.5: The Fact-Check" was created on the account outside this session.

### Result — completed

**"The Meticulous Investor — Seven to One"** · `692226063fb54a55a502206ad478ac53` · **69.30s** · 9:16 ·
1080p · 15 scenes · watch: https://app.heygen.com/videos/692226063fb54a55a502206ad478ac53

| Check (`get_video_scenes`) | Result |
|---|---|
| Alex Wright `0db3abd8…` on all 15 scenes | **PASS** |
| Script verbatim — 930 chars, exact match to `scripts/2026-09-27-vo.txt` | **PASS** |
| Faceless — 15 `motion_graphics` elements (ids prefixed `b_roll_`), **zero** avatar elements | **PASS** |
| 9:16, 1080p, glossary `c9064148…` | **PASS** |
| Closing card — final scene is a 3.0s silent break | **PASS** |
| `caption.enabled` false; `captioned_video_url` **populated** | Publish the captioned cut |

**Cost: 69 credits (110 → 41) = 59.7 cr/min.** Confirmed no other video was created during the
render. That is ~50% above the 40.3–40.5 cr/min of the two plain motion-graphics renders, so the
**B-roll photo layers carry a real premium**. Budget B-roll shorts at **~60 cr/min**.

**UNKNOWN — needs eyes.** The B-roll is baked inside opaque `motion_graphics` plates, so which
photos were used, whether any show faces or logos, and whether the grade stayed dark and
desaturated cannot be checked from here. CDN egress is blocked. Watch before publishing.

Took ~58 minutes from submit to completion, with no progress messages for the last ~40. Same
pattern as 2026-09-25: slow, not stuck.
