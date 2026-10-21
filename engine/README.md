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

## State of the art direction

**Composition pass complete.** All 60 frames rebuilt and reviewed; the two systemic faults are
fixed:

1. **Figures now sit behind their props.** The trick is draw order — the figure is emitted
   first and the counter painted over it, so the torso disappears behind the surface instead of
   floating beside it. Pass `legs=False` on any figure at a counter or table (03, 06, 12, 14,
   25, 28, 31).
2. **Close-ups now fill the frame.** Objects scaled up two to three times (19, 22, 29, 32, 43,
   47). The cup, the key, the seed and the piggy bank all read at a glance now.

New primitives added along the way: `counter()`, `piggy()`, `hand()`.

### Two things worth knowing

**Hands do not work at this line weight.** Four attempts — separated fingers read as a glove,
merged silhouettes read as a mitten, ruled palms read as a sliced ball. `hand()` survives and is
usable *small and gripping something* (scene 47), but never as the subject of a close-up.

**Scene 25 is the one deliberate deviation from its narration.** The line is "Just hands,
folded, waiting their turn," and after the hand attempts failed it is now four figures seated
still on a bench. It carries the same beat — stillness, patience, waiting — and reads instantly,
which a mitten did not. Change it back only if a better hand turns up.

