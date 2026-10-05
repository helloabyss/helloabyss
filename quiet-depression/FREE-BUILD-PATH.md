# Building this video for £0

## The route

| Stage | Tool | Cost | Who |
|---|---|---|---|
| **60 stills** | SVG → PNG, rendered here with Chromium + Playwright | **£0** | Me |
| **Voiceover** | Digital Maker free tier | **£0** | You |
| **Assembly** | CapCut free | **£0** | You |

No Flow credits, no HeyGen, no Higgsfield, no Nano Banana.

## Why SVG beats AI image generation *for this specific style*

Your style spec is: flat 2D line art, bold black outlines, flat colour fills, no gradients, no
shadows, pure white background, 16:9.

**That is a description of vector graphics.** SVG renders it exactly. An image model renders it
approximately, and has to be argued with for 60 frames.

What you get free that AI generation struggles with:

- **Perfect character consistency.** @Zul is literally the same code every frame. Not "close
  enough across 60 images" — identical. This is the hardest problem in AI character work and
  here it costs nothing.
- **Exact colours.** `#d81e28` red every time, never drifting.
- **Exact text.** Numbers and labels render as typed. No mangled AI lettering.
- **Exact repeats.** Scenes 01, 50, 56 and 60 are the same street at four moments — same camera
  position, only the lit windows change. Trivial in code, nearly impossible to get right from a
  prompt four separate times.
- **Free revisions.** Change a colour across all 60 frames in one line.

## The honest trade-off

AI-generated frames have more texture and incidental detail. SVG frames are cleaner and more
diagrammatic. For a stickman explainer channel, cleaner is arguably correct — but it is a
different look, and worth deciding deliberately rather than by budget.

Three samples are in `samples/` so you can judge before committing to all sixty.

## What the samples show

- **`scene-01.png`** — the street. Dark vs lit shops reads instantly; compliance card present.
- **`scene-07.png`** — wages flat vs prices climbing. Labelled axes from a zero baseline, the
  gap shaded. Infographics are where this approach is strongest.
- **`scene-21.png`** — @Zul at the kitchen table. Character is accurate to your reference
  sheet: beanie stripes, glasses, curly hair, polo.

**Known issues in the samples, all fixable:** Zul needs arms reaching to the table (currently
floating), scene 01's caption text overflows its box, and scene 01 has dead space up top. These
are composition fixes, not limits of the method.

## Effort, stated plainly

Sixty hand-composed scenes is real work — roughly a day of my time, in batches. It is not
"press go." The infographic frames (04, 07, 13, 15, 42, 58) are fast; the character and
environment scenes each need composing.

Suggested order so you can bail cheaply if you dislike the look:
1. Scenes 01–10 first. Review.
2. If approved, 11–40.
3. Then 41–60.

## Your side

1. **Record the VO** from `VO-SCRIPT.md` in Digital Maker. It is clean — no `@Zul`, no camera
   directions.
2. **Export the stills** I produce.
3. **In CapCut:** import all 60, set each to 8 seconds, drop the VO on the audio track.
   The VO line printed above each scene in `FLOW-PACKAGE.md` tells you exactly where each
   image lands.
4. Export 1920×1080.

## If you would rather keep the Flow route

`FLOW-PACKAGE.md` is corrected and ready to paste. It costs Flow credits but gives richer
frames. The two approaches are not exclusive — a sensible hybrid is SVG for the infographic
and repeat-street frames (where exactness matters most) and Flow for the atmospheric ones.
