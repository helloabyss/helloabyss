# TOOLS_USED: tmi-fed-calendar

| Stage | Tool | Credits | Note |
|---|---|---|---|
| Fact lock | WebSearch x2 | 0 | Two independent passes; the second specifically to corroborate the surprising claims (new Chair, calendar change) before scripting |
| Narration + word timings | HeyGen `create_speech`, Alex Wright | 1 generation | 32.65s, word-level timestamps. Pre-narration gate run first: zero digits in the TTS input, no risky pronunciations, no banned finance phrasing |
| CDN bridge | ElevenLabs `creative_attach_reference_file` | 0 | HeyGen's CDN 403s here |
| Loudness + room tone | `engine/bed.sh` (ffmpeg) | 0 | |
| Plates | regraded from `tmi-cash-sweep` + reused from `paradocs-watt-hours` | **0** | No new generation. The three TMI plates were from the rejected dark look and were lifted and warmed |
| Render + gate | `engine/build.sh` | 0 | 980 frames, ~18 fps, 4 workers |
| Thumbnail | `engine/layouts.py` + Playwright | 0 | |

**Deliberately not used:** Higgsfield 0, Adobe Stock 0, Canva 0, vidIQ 0,
OpusClip 0. New b-roll was not generated — existing plates covered the topic
and the spend was not authorised.

**Total new credits: 1 HeyGen speech generation.**
