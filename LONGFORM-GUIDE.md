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
python3 anim_aip.py                               # build + run the layout guard
NODE_PATH=/opt/node22/lib/node_modules node render_anim.js stills   # sample frames, LOOK AT THEM
NODE_PATH=/opt/node22/lib/node_modules node render_anim.js 20       # full render -> aip-silent.webm
```

Local ffmpeg is Playwright's build: **webm out only**, no audio codecs, no MP4 muxer. The
mux to H.264/AAC MP4 happens on the ElevenLabs composition node, which costs **0 credits**.
Each audio source there starts its own track at 0 — tracks are parallel, not sequential —
so concatenate audio *before* uploading, not in the composition.

## Verification

Renders cannot be watched from the agent environment; the HeyGen and Higgsfield CDNs are
egress-blocked. Report every render as **complete, not verified**, and hand the user the
checklist in `DISCLAIMER.md`. A human watches it end to end before upload.
