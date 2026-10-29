# Production record — "82% / 25%" (PARADOCS10X short 5)

| | |
|---|---|
| Channel | **PARADOCS10X** — AI/tech lane. **No host, no stickman** |
| Runtime | **39.07s**, 20 VO beats cut into **30 shots**, 0.98–1.96s each |
| Format | **1080×1920 (9:16)**, 30 fps, H.264 + AAC |
| Narrator | **Alex Wright – Informative** `0db3abd83c74452fb2460b0dd113daad` (HeyGen) |
| Picture | 7 licensed Adobe Stock **video** plates, graded on ingest; `engine/reel.js` |
| Cost | **7 Adobe Stock licences** + HeyGen `create_speech`. Zero Higgsfield, zero ElevenLabs generation |

## The version this replaces

The first attempt was a white-background typographic slideshow built on the money
channel's stickman engine. It was rejected, correctly. Against `STYLE-GUIDE.md` it broke
the first rule in the document — imagery is the BASE layer, never typography on flat
ground — plus shot length (3.35–6.32s against "no shot past 2s"), continuous motion,
counting numbers, no-plain-cuts, caption styling and the dark grade. It also put **Zul**
on PARADOCS10X; Zul belongs to the money channel. `CHARACTER-ZUL.md` said otherwise and
has been corrected.

## Narration

Alex Wright via HeyGen `create_speech`, which returns **word-level timestamps**. That is
true forced alignment — every cut in this video sits on a measured word boundary, with no
estimation anywhere. The previous method (map sentences 1:1 onto `silencedetect` pauses)
would have failed on this script: 23 sentences across 20 paragraphs of 1–7 words, and the
detector does not reliably fire between "Not low." and "Zero."

`resource2.heygen.ai` is blocked (403 on CONNECT), so the audio came back through the
recorded workaround: `creative_attach_reference_file` → `creative_get_available_assets` →
download the `preview_url` from `storage.googleapis.com`. Verified again today.

Loudness: raw **−16.42 LUFS**, two-pass `loudnorm` landed **−14.66**, a +0.66 dB gain pass
brought it to target. **Final −13.97 LUFS, true peak −3.10 dBTP, measured by decoding the
finished MP4.**

## Plates

Seven Adobe Stock **video** clips, not stills. Stills with a CSS zoom is Ken Burns, which
is what made the first version a slide deck. `getplate.sh` licenses, downloads, crops to
1080×1920, grades dark and desaturated, and **deletes the master**: Stock ships ProRes and
one 15s clip is ~1 GB, so ten would exhaust the session's disk.

`checkplate.py` gates every plate on mean luma. It earned itself immediately — the first
bookend plate graded to **mean luma 0.0, pure black**, and would have shipped as an
invisible layer. Brightness is now per-plate, because an already-dark source needs lifting
where a bright one needs pulling down.

Plates are **gitignored**: the licence covers use in a work, not redistribution, and this
repo may be public. Asset IDs and search strings are in `SHOTLIST.md` so the set can be
re-sourced.

## Two environment findings worth keeping

- **This Chromium has no H.264 decoder.** `canPlayType('video/mp4; codecs="avc1…")`
  returns empty; VP9 returns "probably". Plates must be **VP9 WebM** for the compositor to
  see them. The first render with video plates produced a perfectly valid, perfectly black
  MP4 because `<img>` cannot display an mp4 and nothing errored.
- **Subagents get balance-reader tools only.** Every Adobe, ElevenLabs and Higgsfield
  generation tool is main-session only. Sourcing and generation cannot be delegated.

## Verification

```
1080x1920 · h264 · 30 fps · 9:16 · 39.07s
aac 48000 Hz stereo 191 kb/s
−13.97 LUFS integrated, true peak −3.10 dBTP   (decoded from ale-reel.mp4)
30/30 shots carry visible footage; luma spread 7.4–86.5 across the cut
beats validated by engine/checkbeats.py: shot length, plate presence, layout collisions
```

**Complete, not verified.** Nobody has watched it end to end, and that is still the one
thing that cannot be delegated.

## Upload checklist (human)

1. Watch all 39s with sound on a phone.
2. Confirm the compliance strip is readable inside the first 4 seconds.
3. Confirm captions clear YouTube's own Shorts UI.
4. Title, description and hashtags from `PACKAGING.md`; disclaimer verbatim.
5. Upload `thumbnail.png`.
6. **Positions line** — fresh answer for this upload; never copied forward.
