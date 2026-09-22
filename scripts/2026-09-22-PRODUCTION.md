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
