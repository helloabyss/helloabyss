# Production record — Robinhood agentic trading (PARADOCS10X)

| | |
|---|---|
| Channel | **PARADOCS10X** — AI/tech lane, same as DOTS VS GROK BOT |
| Runtime | **7:17** (437.23s), 20 scenes, 17.6–26.4s each |
| Format | 1920×1080 landscape, 12 fps, H.264 + AAC MP4 |
| Narrator | **Aaron** `ESDuPqgyZIDDVZTlIrH7`, `eleven_multilingual_v2` — the locked channel narrator |
| Host | Zul, from `engine/zul.py` |
| Picture | `engine/scenes-robinhood.py` on the house `prims.py` kit |
| Cost | **$2.42** of ElevenLabs narration. Zero HeyGen, zero Higgsfield, zero vidIQ |

## Why this channel and this format

PARADOCS10X is the only channel with usable data, and the data is unambiguous. Measured
2026-10-21 over 1 Apr – 20 Oct: long-form is **299 views against 4,517 for shorts**, but
**175 of 835 watch-minutes** — 6% of views, 21% of watch time, and a **84s average view
duration against 18s**. Within that, one video stands out: **DOTS VS GROK BOT** (4 Oct,
6:26) took **124 views, a 13.05 breakout score, 128s average view duration and 3 of the
channel's 5 lifetime comments**. Everything posted since — Tesla Roadster, Optimus, This
Week In Tech — sits at **2 to 6 views**.

One format works here: a named thing, examined, with a trust question attached. This is
that format, in the same AI-agents lane.

## Narration

**Aaron, not Alex Wright.** `CLAUDE.md` records two narrators as "a defect, not a choice"
and names Aaron as the one to keep. An earlier pass in this session began generating this
script in Alex Wright via HeyGen; that call timed out, which was lucky, because finishing
it would have deepened the defect rather than fixed it.

Generated in two parts because `creative_generate_speech` rejects prompts over 5,000
characters (the full script is 6,653). Split at the scene-10 boundary: 210.05s + 227.18s.
**Concatenated locally** — the repo previously recorded that audio work had to go
server-side, which is no longer true.

Loudness: raw output measured **−24.47 LUFS**, normalised to **−14.43 LUFS, true peak
−1.49 dBTP**. Un-normalised ElevenLabs output has shipped sounding like silence before;
every cut gets this check now.

## Timing

Scene durations are **not** the house flat 8s. They are allocated by word count within
each generated part and snapped to pauses from `silencedetect`, with the part boundary at
210.05s used as an exact anchor. `build.py` now takes a scenes module and a
`durations.json`; its old defaults are unchanged.

## Verification

```
Duration 00:07:17.23 · 1920x1080 · h264 · 12 fps · aac 48000 Hz stereo
Narration −14.43 LUFS integrated, true peak −1.49 dBTP
```

**Complete, not verified.** Stream metadata and decoded stills are checkable here;
playback is not. Picture/voice sync across the full 7:17, and whether the scene cuts land
on the sentences they belong to, need a human pass.

## Constraints hit

- **No primary source was reachable.** The proxy returns `connect_rejected` (403 on
  CONNECT) for every external host, including `robinhood.com` and `sec.gov`, both of
  which appeared in search results. Everything in `FACTS.md` is corroborated secondary
  reporting; nothing is marked CONFIRMED.
- **No screen recording was possible or wanted.** No network path to Robinhood, no
  account to film, and a live brokerage UI would expose real balances. Interfaces are
  drawn and tagged RECREATION on screen.
