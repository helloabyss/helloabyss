# Production Record — Frontier AI Shorts, 2026-09-22

## FINAL — 5 Shorts, narrated ✅

| # | Title card | Runtime | Link |
|---|---|---:|---|
| 1 | GROK 4.7 IS LIVE | 17.77s | https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/b2f8d3fa-b535-4f03-8e01-a85e67fbba8c.mp4 |
| 2 | SAME PRICE, BIGGER MODEL | 16.87s | https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/dae03f97-e0ce-4f47-af12-9f08ec06d143.mp4 |
| 3 | READ THE BENCHMARK FINE PRINT | 17.17s | https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/c0adf1ec-ba45-4991-a013-3ea8afe01d2c.mp4 |
| 4 | STEP 5 IS CHEAPER THAN GROK | 21.44s | https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/44815045-6ce9-4f82-8335-70ba039509f2.mp4 |
| 5 | WHAT YOU CAN ACTUALLY USE | 17.10s | https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/9afcfb49-7580-4042-8fbd-796996ac6d48.mp4 |

All 1080×1920 · 30fps · H.264 + AAC. Every runtime inside the 15–25s spec.

## Build settings
- **Voice:** Callan `d8061b90-ff25-5882-8384-7a6a28806f30` (seed_audio), **native speed**.
  Pauses capped at 0.28s per `VO_PROFILE.md` §8 — no `atempo`, no pitch shift.
- **Plates:** 7 × `soul_cinematic` @1.5k, graded by `build/plates/norm.py` (all landed
  luminance 33.6–34.0).
- **Palette:** amber `#FFB020` per `STYLE.md`, **not** the cyan in the brief — see below.
- **Assembly:** Playwright + ffmpeg in the Higgsfield sandbox.

## SKIP list compliance — verified in the build, not just intended
- **No product UI or fake screenshots.** All 7 plates are abstract (node networks, data
  streams, server aisle, circuit macro, fibre optics, wireframe mesh, particle field).
  Every prompt carried an explicit "no interface, no screens, no text" clause.
- **No human presenter or faces.** No people in any plate prompt.
- **No tickers or price charts.** The only numeric graphics are token prices and one
  benchmark bar pair — neither is a market chart.
- **No invented demos.** Nothing depicts a product in operation.

## Fact-check corrections carried into the video
From `research/2026-09-22-frontier-ai.md`:
- **Short 3 is built around the correction.** The `xHIGH vs HIGH` box is a full-screen card,
  not a footnote, and `xHIGH vs HIGH` also runs as the persistent corner label.
- Shorts 1, 2, 4, 5 carry a persistent `COMPANY-REPORTED` corner label.
- Short 4 says **text and image** — "video input" dropped (sources conflict).
- All five end on an on-screen `x.ai/news/grok-4-7` source stamp.
- Digit 5 is **not** in any Short — early access H1 2027 fails the "use it today" lane.

## Palette decision
Built in **amber**, as recommended, so this lane reads as the same channel as TWiT and the
finance shorts. The brief specified cyan. Switching is a one-line change (`ACC` in `sr.js`)
plus a re-render at **zero credit cost** — only generation is charged.

## Spend
7 plates × 0.12 = 0.84 · 5 narration × 0.10 = 0.50 · **1.34 credits total.**

## NOT VERIFIED — needs your eyes
The Higgsfield CDN is blocked from the build container, so these were checked by probing the
encoded files (duration, video+audio streams present) and by inspecting rendered frames, but
**not watched**. Before posting, confirm:
1. Captions clear the Shorts UI on a phone (they sit 470px off the bottom).
2. The `xHIGH vs HIGH` card in Short 3 is legible at speed — it is the whole point of that one.
3. No plate reads as a product UI or contains stray generated text.
4. Amber vs cyan is the call you want.

---

## Short 1 — local render (2026-09-23)

`scripts/2026-09-22-grok47-short.mp4` — 17.80s · 1080×1920 · 30fps · H.264 CRF 21 · silent AAC · 19MB.

Built entirely in this container by `build/grok47/`, **0 credits**. This exists because the
Higgsfield CDN (`d2ol7oe51mr4n9.cloudfront.net`) is blocked by the environment's network
policy, so no cloud render can be downloaded and delivered as a file. A local render can.

| File | Role |
|---|---|
| `build/grok47/render.js` | Canvas renderer — `seek(t)` is pure in `t`, so frames are reproducible |
| `build/grok47/cues.json` | Caption cues, timed to the approved Short 1 VO at 152 WPM |
| `build/grok47/short.html` | Host page, 1080×1920 canvas |
| `build/grok47/capture.js` | Playwright frame capture |

Rebuild:
```bash
cd build/grok47 && python3 -m http.server 8941 &
NODE_PATH=/opt/node22/lib/node_modules node capture.js
ffmpeg -framerate 30 -i /tmp/g47/%05d.jpg -f lavfi -i anullsrc=channel_layout=stereo:sample_rate=48000 \
  -shortest -c:v libx264 -preset slow -crf 21 -pix_fmt yuv420p -c:a aac -movflags +faststart out.mp4
```

### Deviations from `STYLE.md`, stated not hidden
- **No narration.** Every neural TTS voice model is hosted on HuggingFace or GitHub releases,
  both unreachable from here, and the HeyGen token is expired. Captions carry the script.
  The VO in `VO_PROFILE.md` is unchanged and still governs — this is a missing layer, not a new setting.
- **Base layer is procedural, not photographic.** `STYLE.md` inherits "imagery first" from the
  finance guide. No plate can be generated or fetched locally, so the base is a drifting
  bokeh/key-light field, graded dark and desaturated, under the motion-graphics and type layers.
  The three-layer stack is preserved; the bottom layer is synthetic. Swap in real plates when
  CDN egress is restored.

### Held to
Amber `#FFB020` accent · near-black `#0B0B0D` · off-white `#F2F2F0` · no logos, plain text
name-tags · on-screen source attribution throughout · the xHigh-vs-High caveat on screen in the
close · burned-in captions · content kept clear of the bottom 300px Shorts UI overlay.

---

## Short 1 v2 — cinematic plates + locked VO (2026-09-23)

`https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/79c37b42-45ba-4029-8461-934cc78e2d02.mp4`
18.834s · 1080×1920 · 30fps · H.264 CRF 20 · AAC 160k · 22MB · media_id `79c37b42-45ba-4029-8461-934cc78e2d02`

**Total spend: 1.55 credits** (5 plates × 0.25 + 1 narration × 0.30). Balance 554.6 → ~553.

### What v2 adds over the local silent cut
| | v1 (local file) | v2 (this) |
|---|---|---|
| Base layer | procedural bokeh | 5 graded photographic plates, Ken Burns |
| Voice | none | Callan, locked profile, native speed |
| Runtime | 17.80s | 18.834s, cut to the actual read |
| Caption sync | estimated at 152 WPM | faster-whisper word timings off the real WAV |

### Assets
| # | Beat | Plate | Job |
|---|---|---|---|
| 1 | Hook | server hall corridor, single amber source | `bee521cb` |
| 2 | Price | gold contact pins macro | `9636c9a5` |
| 3 | What changed | long-exposure light trails | `f90d2356` |
| 4 | Available today | desk, out-of-focus monitor glow | `70cd790d` |
| 5 | Close | dawn shaft across a bare desk | `92807410` |
| — | VO | Callan `d8061b90…`, seed_audio | `34b3b888` |

### Grade (measured, not eyeballed)
`TARGET_LUM=35`, autocontrast → soft-knee highlight rolloff at 0.62 → desaturate → contrast 1.12
→ binary-search gamma. All five land 33.6–33.8 mean luminance, stddev 38–52. Prompted
**well-exposed** and graded down afterwards — prompting for "near-black" returns crushed frames.

### VO timing
Raw 26.88s → trim/loudnorm 26.33s → pause-cap at 0.30s **18.83s**. 30% of raw seed_audio output
is inter-sentence padding. Native speed, **no `atempo`** — per `VO_PROFILE.md` §8 that is what
made the rejected Arthur take sound synthetic.

### Pipeline note — git is the transport
The sandbox pulls `render_v2.js` / `cues_v2.json` / `short_v2.html` from
`raw.githubusercontent.com` on the working branch. Code travels by git; only the finished MP4
is uploaded back. Reusable for every future episode.

### Known limits
- Plates generated at 752×1344 and Lanczos-upscaled to 1080×1920 (~1.44×). Regenerate at higher
  resolution if the upscale ever shows.
- **This cut has not been watched by anyone yet.** The render was verified numerically (frame
  count, duration, stream layout, per-plate luminance) and the layout was validated locally
  against stand-in plates, but the CDN is unreachable from the container so I could not view it.
  Report it as *complete, not verified*.

---

## Frontier AI lane — all five Shorts shipped (2026-09-23)

Every Short narrated by Callan (locked profile, native speed), cinematic plates graded to the
house look, captions aligned to the real audio. Built with the spec-driven engine.

| # | Title | Runtime | URL |
|---|---|---|---|
| 1 | GROK 4.7 IS LIVE | 18.83s | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/79c37b42-45ba-4029-8461-934cc78e2d02.mp4` |
| 2 | SAME PRICE, BIGGER MODEL | 20.66s | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/33f036a0-81f4-4260-89b3-a946a8d7f4bf.mp4` |
| 3 | READ THE BENCHMARK FINE PRINT | 18.94s | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/3ee8f71e-0dd4-4885-a58f-100ec01278d1.mp4` |
| 4 | STEP 5 IS CHEAPER THAN GROK | 20.22s | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/83ff2341-5569-43ce-b735-c3c3c96761ba.mp4` |
| 5 | WHAT YOU CAN ACTUALLY USE | 16.30s | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/be2cf66b-038a-4cf4-a8fb-002f0214ad39.mp4` |

**Credits: 554.6 → 540.05 = 14.55 for the whole lane**, about 2.9 per Short. 21 plates at 0.25,
5 narration tracks at 0.30; the rest was rendering, which is free.

### The system
`engine.js` renders any episode from a JSON spec — primitives are label, big, accent, sub,
rule, para, statpair, rows, stamp, bars, list, vs, caveat, composited over a graded plate with
Ken Burns. `build.py` grades plates, pause-caps the VO, aligns captions to faster-whisper
sentence spans, renders and encodes. **A new episode is a spec file, not new code.**

Code travels to the sandbox by `raw.githubusercontent.com`; only the finished MP4 is uploaded
back. Presigned upload URLs are credentials and are passed directly to the sandbox, never committed.

### Editorial
Every Short carries its caveat on screen, per `STYLE.md`:
- 2 — "COMPANY-REPORTED: these are SpaceXAI's own claims about its own model."
- 3 — the whole Short is the caveat: xHigh vs High is not like-for-like.
- 4 — "CUT FROM THIS SCRIPT: some coverage claims video input. No primary document settles it."
- 5 — "BOTH COMPANY-REPORTED: none of it is independently benchmarked."

### Still true
**None of these have been watched.** Verified numerically — frame counts, durations, stream
layout, per-plate luminance 33.4–33.8 — and the layout was validated locally against stand-in
plates. The CDN is unreachable from the container, so report them *complete, not verified*.
