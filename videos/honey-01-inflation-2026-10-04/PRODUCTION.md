# Production — Explained with Honey No.1: Inflation (2026-10-04)

**Final:** `inflation-explained-with-honey.mp4` (62.7 s, 1080×1920, 30 fps, -14.5 LUFS) and `-mobile.mp4` (7.2 MB, same content, phone-friendly).
MP4s are gitignored. Rebuild: `cd build && python3 gen.py && npx --yes hyperframes@0.8.55 render -o ../inflation-explained-with-honey.mp4 -f 30`.

## Assets and cost
| Item | Source | Cost |
|---|---|---|
| Narration | ElevenLabs "Brian" (`nPczCjzI2devNBz1zQrb`), eleven_multilingual_v2 | 811 cr · **$0.30** |
| Music | ElevenLabs Music v2.5, playful pizzicato/marimba, 64 s instrumental | 960 cr · **$0.35** |
| Transcript | ElevenLabs Scribe (came back as text only, no timestamps) | free |
| Visuals | Hand-built SVG/GSAP in HyperFrames | free |
| Research | vidIQ: 2 channel lists + 2 transcripts | 20 vidIQ credits |

⚠️ **ElevenLabs is now billing at the paid rate:** ~$0.036 per 100 credits, against ~$0.01 on 2026-10-01. The free allowance looks spent.
Flow: https://elevenlabs.io/app/flows/nE500nSMpFskFFfYY9oM

## Sync
Beats are pinned to the narration's 28 speech segments (silencedetect -38 dB / 0.18 s, 27 internal pauses), mapped by hand to the
26 sentences. Three pauses are comma pauses inside a sentence ("richer, so", "tokens, less", "hive, prices"). `gen.py` asserts 27 pauses,
so a re-voiced narration fails loudly instead of drifting.

## QA
- `hyperframes check`: 0 errors. Warnings are track density and a two-sample cross-fade on the 100→60 counter.
- Frames checked for every scene. Fixed after the draft: the bee head disappeared on black (now gold-outlined), the wings were hidden
  behind the body (now on top), "PRICE CLIMBS AGAIN" overflowed its tag, and the "YOUR SAVINGS" label sat on its line.
