# Long-form guide

The shorts rules in `CLAUDE.md` and `STYLE-GUIDE.md` all still apply. This file covers
only what changes when a video runs minutes instead of seconds.

## Timing

**Aaron reads at 158.7 wpm, measured.** 1,400 words of `ai-picks-longform/SCRIPT.md` came
back as 529.40s of audio. Earlier drafts assumed 166 wpm and under-ran the estimate by
about 30 seconds across a nine-minute cut.

| Use | Value | Basis |
|---|---|---|
| Script length planning | **158.7 wpm** | measured, Aaron, `eleven_multilingual_v2` |
| Alex Wright (HeyGen) | **unmeasured** | measure on the first HeyGen long-form and record it here |

Never pin picture to a *predicted* duration. Generate the VO, measure the file, then
distribute scene durations against the measured total. `engine/anim_aip.py` does this:
weights each beat, turn cards at 0.42, and scales so the sum equals the measured seconds.

## Picture must be aligned to the words, not to visual weight

**This is the one that produced the worst-looking defect in the first two cuts.** Beat
durations were distributed by *weight* — turn cards 0.42, everything else 1.0 — scaled to
the measured voiceover length. Every ordinary beat therefore ran exactly **13.1s**,
whether its narration took eight seconds or twenty. The picture drifted against the words
for nine minutes.

`engine/align_aip.py` is the fix and the contract:

- Every beat declares, in `SRC`, the **script paragraphs it illustrates**. Beats sharing
  a paragraph split it by word count. The list is asserted to be monotonic and to cover
  every paragraph, so a beat added or reordered without updating `SRC` fails the build.
- Duration follows **word position** at the measured speaking rate, not visual weight.
- Every boundary is **snapped to a real pause** found by
  `silencedetect=noise=-30dB:d=0.28` (208 of them in this narration), so cuts land between
  sentences rather than mid-word.
- `anim_aip.py` refuses to build if the duration count and the beat count disagree.

There is **no ASR here** — `huggingface.co` is egress-blocked, so no Whisper weights and
no true forced alignment. Word position at a constant rate is the available approximation
and it is a good one, but it is an approximation: confirm on the watch-through.

**Dense narration needs more beats, not longer ones.** Aligning the first 42-beat cut
produced a card held for **51.7 seconds**, which breaks the 10–15s rule in `CLAUDE.md`.
The answer is to add beats where the script is dense, not to let one card sit there. After
rebuilding to 58 beats: median 9.8s, longest 17.5s, nothing over 18s.

**The closing card holds past the last word.** `OUTRO` seconds of picture run after the
narration ends, so the render must not pass `-shortest` — that would cut the outro off.

## Structure

- A **turn card** at the end of each section — hard cut to near-black, the section's
  counter-evidence headline, the ticker beneath. These are the spine: they tell the viewer
  a reversal is coming and they are where the counter-evidence rule is discharged.
- **New information or a reversal every 10–15s** holds for long-form too. At ~13s a beat,
  that means every beat earns its place or it is cut.
- The close loops back to the opening and gives the viewer something to do.

## Motion

A long-form cut cannot be a slideshow. The first `ai-picks-longform` render was stills
pushed uniformly and it read as dead; it was rebuilt. The standard now:

- Numbers **count up**; they do not appear.
- Bars, rules and arcs **grow or wipe**; their length is always proportional to the figure.
- Type **rises in line by line**, staggered.
- Zul **cuts between drawn poses** mid-beat. He is never tweened, bent or warped
  (`CHARACTER-ZUL.md`) — animation is cutting between the supplied artwork.
- A **ticker rail** scrolls continuously along the bottom so no frame is fully static. It
  hides on turn cards.

## Layout — Zul and type never overlap

This was shipped broken once: Zul's figure sat on top of the words and made them
unreadable. The separation is now enforced by arithmetic, not by eye.

A body pose at `h=760` puts its **ink** at x 268–492 (the panel is larger than the ink;
the manifest records both). The type column therefore starts at **x=620**. `anim_aip.py`
asserts this at build time and refuses to emit the page if any text in a scene containing
Zul starts left of it. Do not relax the guard to fit a line — shorten the line.

## Rendering

```
cd engine
python3 anim_aip.py                                                  # build + run both guards
NODE_PATH=/opt/node22/lib/node_modules node render_anim.js stills    # sample frames, LOOK AT THEM
NODE_PATH=/opt/node22/lib/node_modules node render_anim.js 20        # -> ai-picks-longform.mp4
```

The render writes the **finished deliverable in one pass**: frames out of headless
Chromium into ffmpeg over `image2pipe`, narration muxed in the same command, H.264 +
AAC in an MP4 with `+faststart`. About 21 minutes for 10,587 frames at 20fps.

**Use imageio-ffmpeg's binary, not Playwright's.** Playwright bundles a cut-down ffmpeg
that can write only VP8 webm and has **no audio codecs at all** — it cannot mux a
soundtrack, so for a while the only route to a finished file was an external service.
It is not needed:

```
pip install imageio-ffmpeg
python3 -c 'import imageio_ffmpeg; print(imageio_ffmpeg.get_ffmpeg_exe())'
```

gives a full static ffmpeg 7.0.2 with `libx264`, `aac` and an mp3 decoder. PyPI is
reachable directly here (it is in the proxy's `noProxy` list), so this works offline of
every connector. `render_anim.js` resolves the path itself.

**Do not route the mux through ElevenLabs.** The composition node did work once and
costs 0 credits, but as of 2026-10-08 the MCP bridge returns a schema-validation error
for `creative_create_asset_upload`, so the video cannot be put on a flow in the first
place. More importantly it is an unnecessary dependency: the mux is a local operation
and should stay one.

## Audio loudness — check this on every cut

**Normalise the narration before it goes anywhere.** ElevenLabs returns audio at whatever
level it happens to return; on `ai-picks-longform` that was **−24.66 LUFS**, about 10.7 dB
under the −14 LUFS a published video wants. The cut shipped and was reported as having no
voiceover at all, because at that level on a phone speaker it may as well not have.

```
ffmpeg -i <file> -af loudnorm=I=-14:TP=-1.5:print_format=json -f null -   # measure
```

Target **−14 LUFS integrated**, true peak at or under **−1.0 dBTP**, **stereo**. More than
~1.5 dB off and it needs a two-pass `loudnorm` (see `ai-picks-longform/PRODUCTION.md` for
the exact invocation). Normalising the stem and remuxing with `-c:v copy` takes under a
minute, so this never justifies a re-render.

**"The audio stream exists" is not this check.** Verifying presence answers a different
question from verifying level, and only the second one tells you whether a viewer will
hear it.

## Waiting on a long render — do not let pgrep match itself

A render takes ~21 minutes, so it gets backgrounded and waited on. `pgrep -f` matches
against **full command lines, including the waiting shell's own**, so this never exits:

```
while pgrep -f "node render_anim.js" >/dev/null; do sleep 20; done   # WRONG: waits on itself
```

The same bug makes `pkill -f render_anim.js` kill the shell that runs it, losing whatever
came after in that command. Both happened here. Match on something the waiter's own
command line does not contain, or check the output instead:

```
while pgrep -f "[n]ode render_anim" >/dev/null; do sleep 20; done    # bracket breaks self-match
until [ -s out.mp4 ] && ! pgrep -f "[n]ode render_anim" >/dev/null; do sleep 20; done
```

A stuck waiter is harmless — it expires — but it reports nothing, so the render looks
unfinished long after it is done. Check the output file's size and `ffmpeg -i` on it
before believing a waiter that has gone quiet.

## Verification

Renders cannot be watched from the agent environment; the HeyGen and Higgsfield CDNs are
egress-blocked. Report every render as **complete, not verified**, and hand the user the
checklist in `DISCLAIMER.md`. A human watches it end to end before upload.
