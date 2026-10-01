# Production — "93% of Pros Lost to the S&P 500" (2026-10-01)

**Status: RENDERED WITH NARRATION, B-ROLL PENDING.** `93-percent-lost-to-the-sp500.mp4` · 62.0 s (57.5 s VO + 4.5 s disclaimer) · 1080×1920 · 30 fps · H.264 + AAC.
MP4s are gitignored (repo convention), so regenerate with `cd build && python3 gen.py && npx --yes hyperframes@0.8.55 render -o ../93-percent-lost-to-the-sp500.mp4 -f 30`.

## Why silent
The owner asked for the video that night. The house voice (Sheldon - Voice, HeyGen) costs about 35–40 credits for this length,
and the balance was 4 (resets 2026-10-06). So this cut is built **VO-paced**: each of the 18 beats is timed to its spoken line,
and a caption rail carries every line word for word, so it plays complete with the sound off. To add the voice later:
- **Sheldon's own recording** (free): put it in `build/assets/vo.wav` and add
  `<audio id="vo" class="clip" src="assets/vo.wav" data-start="0" data-duration="52.8" data-track-index="3"></audio>` to the root,
  then nudge the `BEATS` durations in `gen.py` to the recording and re-render.
- **HeyGen render** after the reset: submit the VO in `SCRIPT.md` with voice `f925838e…`. HeyGen redraws its own visuals, so that is a
  separate video, not this one with audio added.

## Build
`build/gen.py` generates `build/index.html` from `tpl.tplsrc` (cloned from `twim-2026-09-27-kinetic`). Six scenes over 18 beats:
93% roll-up and 20-year line race · pros stack and 79/100 dot grid · "winners don't stay" strike · top-quartile leaderboard draining to 0.46% ·
"to be fair" 67/100 grid with the crash line · fee columns and mock fund page with the expense ratio highlighted · disclaimer card.
Palette #0B0B0C / #F5F5F3 / #D42A2A; no logos, no faces, no tickers.

## QA
- `hyperframes check`: 0 errors. Remaining warnings are the known number-wheel overflow, sub-composition suggestions and
  two-sample overlaps during cross-fades.
- Frames checked by eye at every beat. Three bugs were caught and fixed: charts and dot grids visible before their beats
  (`immediateRender:false` on the reveal), a duplicate `#fK` id (kicker vs headline), and stray line caps/axes before the draw.
- **Deviation from the style guide:** motion graphics only, no photographic base layer (no image source at 0 credits). This is the same
  trade-off as `twim-2026-09-27-kinetic`.

## Before posting
- [ ] `[OPEN]` Confirm the 93% (20-yr) against the SPIVA YE2025 PDF; if it differs, change beat 1 and re-render
- [ ] Description disclaimer and sources from `SCRIPT.md`
- [ ] YouTube altered/synthetic setting: not needed (no realistic synthetic footage)

## B-roll (owner request 2026-10-01): stills generated, waiting on download
- 10 AI stills generated on Higgsfield (`gpt_image_2_5`, 9:16, 752×1344): **2.5 credits** (327.25 → 324.75). The prompts ask for no
  people, no logos and no readable text, graded dark. Shot list: trading floor · tower looking up · screen wall · lobby · trophy ·
  boardroom · dawn skyline · storm · coins · laptop.
- **Blocked:** the network policy of this cloud environment denies Higgsfield's file host `d8j0ntlcm91z4.cloudfront.net`, so the files can't be
  pulled here. Once the host is allowed (or the files are uploaded by hand into `build/assets/broll/` under the names in `fetch.sh`):
  `cd build && assets/broll/fetch.sh && python3 gen.py && npx --yes hyperframes@0.8.55 render -o ../93-percent-lost-to-the-sp500.mp4 -f 30`
- The plate layer is already in `gen.py` (track 1, behind all graphics): slow push-in, grayscale .7 / brightness .78 grade, top and bottom
  scrim, and the trophy plate falls with "STAY." It was tested end to end with placeholder images (check: 0 errors). Grade and opacity
  still need tuning against the real photos.

## Narration (owner: "go with a fitting voice or use ElevenLabs", 2026-10-01)
- **ElevenLabs "Brian - Deep, Resonant and Comforting"** (`nPczCjzI2devNBz1zQrb`, premade, American, middle-aged), `eleven_multilingual_v2`,
  script verbatim, **860 ElevenLabs credits (~$0.09)**. Flow: https://elevenlabs.io/app/flows/D7InKIOKdcGugwgqCcgf
- The first pick, library voice "BlueAshby", is refused on the current ElevenLabs tier (creator tier needed).
- **This is a one-off exception to the house voice** (Sheldon - Voice) on the owner's say-so. `CLAUDE.md` is unchanged.
- File: `build/assets/vo-brian.mp3` (57.52 s). The download host (storage.googleapis.com) is reachable here, unlike Higgsfield's.
- Sync: local transcription can't fetch its model (HTTP 403), so beat edges come from the pauses (silencedetect −38 dB / 0.18 s),
  mapped to sentences by hand (`LINE_END_GAP` in `gen.py`). The automatic mapping got 4 of 18 lines wrong, so it isn't used.
  Pauses in the rendered MP4 land at the same times as the source (1.28 / 5.68 / 7.13 / 9.96 s …).
- Loudness of the render: mean −25.1 dB, peak −3.8 dB. No music bed yet.

## Music bed (owner: "I would love a low background track", 2026-10-01)
- ElevenLabs Music v2.5, instrumental, 63 s: a minimal dark underscore (low synth bass pulse ~90 BPM, muted clock ticks, warm pad, no melody,
  no vocals). **945 ElevenLabs credits (~$0.09).** It's on the same flow as the narration.
- Mix (`build/assets/mix.sh`): music at 0.14 gain, sidechain-ducked under the voice (6:1), 1.5 s fade-in; the track fades out by itself
  as the narration ends. Master loudness **-14.3 LUFS / -1.3 dBFS peak** (YouTube's reference level). Music in the narration pauses sits
  ~-25 dB, so it stays in the background.
- `build/assets/vo-mix.m4a` is the single audio track in the render. The narration and music stems sit next to it.
