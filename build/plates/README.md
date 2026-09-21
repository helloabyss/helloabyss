# Plate pipeline

Generates the photographic base layer for an episode, then grades it to the house look.

Higgsfield's CDN and all news domains are blocked from this container, so the whole
pipeline runs in the **Higgsfield sandbox** (`sandbox_exec`), which has ffmpeg, Playwright,
Chromium and Pillow, and can reach the CDN.

```
1. generate_image_batch   model soul_cinematic, quality 1.5k, 9:16   (see PROMPTS.md)
2. jobs_wait              collect result_url for each job
3. sandbox: curl each result_url -> pN.png
4. sandbox: norm.py       pN.png -> gN.png   (house grade, per-plate normalised)
5. sandbox: Playwright    render 1631 frames from the plate renderer
6. sandbox: ffmpeg        frames -> H.264 MP4
7. media_upload + PUT + media_confirm        export the finished file
```

**Preflight every model with `get_cost: true` before spending.** Video is ~290× the cost
of a still; the moving-camera look comes from the local compositor, not from the model.

**QA without eyes.** The build container cannot download the generated images. Composition
is verified by rendering each plate as an ASCII luminance map in the sandbox, and the grade
is verified numerically. Both caught real defects — see PROMPTS.md.

## Narration

`make_vo.sh` assembles the VO from five per-beat TTS clips and writes `timeline.json`,
whose beat boundaries drive the shot timings so picture and voice cannot drift.

**Voice selection must score timbre, not pitch.** Picking on median F0 alone produced a
voice the channel owner rejected. Score MFCC timbre against the reference sample across the
whole preset list — see `VO_PROFILE.md` §8 for the method and the 40-voice table.

**Never use `atempo` to hit runtime.** Speeding a voice is what makes TTS sound synthetic.
Runtime comes from capping internal pauses (`CAP`, default 0.30s); raw seed_audio output is
~31% silence on a punctuation-dense script. That alone took 69.4s → 54.9s at natural speed.
