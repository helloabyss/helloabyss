# Still-frame engine — one command per video

```sh
sh make.sh out          # 60 scenes -> out/01.png … 60.png + manifest.json + timing.srt
```

**Measured: 6.6 seconds for 60 frames at 1920×1080.** Google Flow was 60 manual generations.

## What it produces

| File | Use |
|---|---|
| `01.png … 60.png` | The stills, numbered, import-ordered |
| `timing.srt` | Subtitle file at 8s/scene — **drop into CapCut and your VO lines up without eyeballing** |
| `manifest.json` | Scene number, filename, VO line, duration — for any other tool |

## The three files you edit

- **`prims.py`** — the drawing kit. `zul()`, `fig()`, `shop()`, `axes()`, `pile()`, `box()`,
  `card()`, `t()`. Palette constants at the top: change `R` once and every red in every frame
  changes.
- **`scenes.py`** — 60 entries of `(number, voiceover, svg)`. Each scene is a few lines.
- **`build.py` / `shoot.js`** — the runner. You should never need to touch these.

## Making the next video

1. Copy `scenes.py` to `scenes-<name>.py`.
2. Replace the 60 entries — each is `A((n, "the narration line", composition))`.
3. `sh make.sh out-<name>`

The primitives carry over, so video two is faster than video one. Add a new primitive to
`prims.py` once and every future video can use it.

## Why this beats prompting an image model for this style

Your spec is flat line art, bold black outlines, flat fills, no gradients or shadows, white
background. That is a description of vector graphics, so SVG renders it exactly rather than
approximately — and you get for free the things image models fight you on:

- **@Zul is the same code every frame.** Not "consistent enough" across 60 generations.
- **Exact colours and exact text.** No drifting reds, no mangled AI lettering on numbers.
- **Exact repeats.** Scenes 01, 50, 56 and 60 are one street at four moments — same camera,
  only the lit windows change. One function call, four arguments.
- **Free iteration.** Re-render all 60 in under seven seconds, as many times as you like.

## Honest state of the art direction

The pipeline is finished. The **composition is not uniformly good yet.**

**Reading well (~40 scenes):** 01, 05, 07, 11, 13, 15, 18, 21, 23, 24, 26, 30, 33–36, 39,
41, 43, 44, 46, 48–50, 52–58, 60.

**Needing a pass (~20 scenes):** 02, 03, 04, 06, 09, 10, 12, 14, 16, 17, 19, 22, 25, 27, 28,
29, 31, 32, 45, 47.

Two faults account for nearly all of them:

1. **Figures float disconnected from their props** — the stickman stands beside the counter
   rather than reaching to it (06, 12, 14, 28, 31).
2. **Close-ups sit too small in a 1920×1080 frame**, leaving dead white space (19, 22, 25,
   29, 32).

Both are composition fixes of a few lines each, and re-rendering costs seconds. That is the
point of building it this way: the expensive part is done once, and art direction became cheap.
