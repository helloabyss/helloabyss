# Production record — "82% / 25%" (PARADOCS10X short 5)

| | |
|---|---|
| Channel | **PARADOCS10X** — AI/tech lane |
| Runtime | **39.00s**, 8 scenes, 3.35–6.32s each |
| Format | **1080x1920 portrait (9:16)**, 24 fps, H.264 + AAC |
| Narrator | **Aaron** `ESDuPqgyZIDDVZTlIrH7`, `eleven_multilingual_v2` — the locked channel voice |
| Host | Zul, from `engine/zul.py` |
| Picture | `engine/scenes-ale.py` on the house `prims.py` kit |
| Cost | **$0.21** ElevenLabs (571 credits) + **5 vidIQ credits** for the shorts pull. Zero HeyGen, zero Higgsfield |

## Balances measured at the start of this cycle (2026-10-25)

`CLAUDE.md` was wrong again, in both directions:

| | file said | measured |
|---|---|---|
| HeyGen | 600 premium | **1,573** (resets 2026-11-15) |
| vidIQ | 106 | **101** (100 renewable + 1 add-on; 96 after the shorts pull) |
| Higgsfield | 350.57 | 350.57 ✓ |

`CLAUDE.md` corrected in the same commit.

## Narration

Single generation, 89 words, 38.96s — comfortably inside the 5,000-character limit that
forced the long-form into two parts.

Loudness: raw output measured **−23.10 LUFS**. Two-pass `loudnorm` landed at −15.63, which
is 1.6 LU short of target, so a `volume=1.63dB` pass with a limiter followed.
**Final: −14.02 LUFS integrated, true peak −2.21 dBTP, measured by decoding the finished
MP4** — not the intermediate stem. A fix measured on the stem instead of the delivered
file is how the loudness regression happened last time.

## Timing — sentence alignment, not word allocation

The first attempt allocated scene durations by word count and snapped to the nearest
pause. It put the scene-3 cut on a comma, because speaking rate is not uniform and
"nearest pause" cannot tell a comma from a full stop.

`align.py` does it structurally instead. The script is **16 sentences in 8 paragraphs**, so
the read must contain exactly **15 major breaks**. Filtering `silencedetect` to pauses
≥0.55s returned **exactly 15**. The mapping is then 1:1 and ordered, with no estimation at
all, and the script aborts rather than guessing if the counts ever disagree.

`captions.py` times words inside each *sentence* rather than each scene, so caption drift
resets 16 times across the video and cannot accumulate past one sentence.

## Layout guard

Zul's extent was computed by hand from the proportions in `CHARACTER-ZUL.md` and the answer
was wrong by about 200px, which put a caption straight across his legs — the collision this
channel has already rejected once. `engine/checkband.py` now measures the actual ink in
each rendered frame and fails the build if anything enters the caption band (y≥1415). Four
scenes were caught and fixed this way.

Two further collisions were found by looking at decoded frames, not by the guard: the
series card drawn over Zul's legs, and a rule through his eyeline, both in scene 8. The
guard only checks the caption band; it does not detect type over art elsewhere in frame.
**Looking at every scene is still required.**

## Verification

```
1080x1920 · h264 · 24 fps · 9:16 · 39.00s
aac 48000 Hz stereo 191 kb/s
−14.02 LUFS integrated, true peak −2.21 dBTP   (decoded from ale-short.mp4)
0 silences longer than 1.5s                    (no dead tail)
8/8 scenes clear of the caption band
compliance card present in the decoded frame at t=1s
caption sync spot-checked: at t=2.0s the highlighted word is "on", timed 1.90–2.22s
```

**Complete, not verified.** Stream metadata, decoded stills and measured loudness are all
checkable here. Playback is not. Nobody has watched this end to end, and that is the one
thing that cannot be delegated: picture/voice sync across the full 39s, and whether Aaron's
read lands the way the cuts assume, need a human pass before upload.

## Constraints hit

- **Every primary source was DNS-blocked.** `WebFetch` returned `getaddrinfo ENOTFOUND`
  for arxiv.org, metr.org, agents-last-exam.org and dailycal.org. This is a harder block
  than the 403-on-CONNECT the repo had recorded — only server-side web search works.
  Nothing in `FACTS.md` is graded CONFIRMED and none of it can be from here.
- **The first-pass headline number was wrong.** See `FACTS.md`; re-checking caught a 10x
  error before it was scripted.
- **`build.py` and `shoot.js` hardcoded 1920x1080** and silently cropped the portrait
  build. Both now read a canvas from `canvas.json`, which `build.py` writes; landscape
  remains the default so the long-form pipeline is unchanged.

## Upload checklist (human)

1. Watch all 39s with sound. Confirm picture changes land on the sentence they belong to.
2. Confirm the compliance card is readable in the first 4 seconds.
3. Confirm the captions do not collide with Shorts' own UI on a real phone.
4. Title, description and hashtags from `PACKAGING.md`; disclaimer pasted verbatim.
5. Upload `thumbnail.png` as the cover.
6. **Positions line** — needs a fresh answer for this upload; never copied forward.
