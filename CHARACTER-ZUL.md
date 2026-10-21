# ZUL — channel host

Zul is the recurring host of PARADOCS10X. He appears in every stickman video.
The point of this file is that he looks and sounds **identical every time** —
treat it the way `STYLE-GUIDE.md` is treated, as locked.

Code: `engine/zul.py`. Model sheet: `engine/zulsheet/01.png`, `02.png`.

---

## The look

| | |
|---|---|
| **Head** | Plain circle, radius 46, white fill, 7pt black line |
| **Beanie** | Three-band knit cap — **red crown, yellow middle, green brim**, in that order top to bottom. Roughly 47 / 21 / 32 of its height. Sits ~12 above the head top |
| **Hair** | Tight black spiral coils, 5 per side, each ~6.5 radius, on an arc just outside the head edge from under the brim down to cheek level |
| **Glasses** | Rectangular frames, rounded corners, **light blue-grey tinted lenses** (`#b9c7d0`). Black dot eyes visible through them |
| **Face** | Dot eyes, single-line mouth. Nothing else — no nose, no brows |
| **Shirt** | White polo: cap sleeves, V-shaped collar band, short placket, two buttons |
| **Limbs** | Plain stick lines. Hands are **three short strokes**, never a filled shape |
| **Legs** | Two lines with a small outward foot |

### Palette

```
black  #000000     beanie red     #d81e28
white  #ffffff     beanie yellow  #f2c200
                   beanie green   #2e9e3e
lens   #b9c7d0
```

The beanie's red is the **same red as the channel accent**, deliberately. Zul's
three beanie colours are the only place the palette widens; everything else in
a frame stays black, white and that one red.

### Proportions — measured, not guessed

Taken off the reference art. Getting these wrong is what makes him look squat
or childish:

- torso (shoulder to hem) = **1.5 head-diameters**
- legs (hem to foot) = **1.6 head-diameters**
- whole figure ≈ **5 head-diameters** tall

---

## Using him

He is positioned by the **centre of his head**, not his feet, so a call site
can line his eyeline up with everything else in the frame.

```python
from zul import zul

zul(960, 400)                                   # bust, front, arms down
zul(960, 300, 1.2, 'up', legs=True)             # full figure, arms raised
zul(300, 400, view='three_quarter', mood='worried')
zul(300, 400, view='back')
```

| arg | values |
|---|---|
| `arms` | `None` · `down` · `table` · `up` · `point` · `shrug` |
| `view` | `front` · `three_quarter` · `back` |
| `mood` | `neutral` · `worried` · `wry` · `talking` · `flat` |
| `glasses` | `True` (default) · `False` |
| `legs` | `False` (default, bust) · `True` |

**Glasses are on by default.** The reference pack showed him with glasses in
three views of four; the bare-eyed close-up is kept as `glasses=False` for the
rare shot that wants it. Pick one per video and stay with it.

**Stand him on the ground.** Pass `legs=True` and put his head centre at
`ground_y - 290*sc`. The 60 scenes in `engine/scenes.py` predate the rig and
float him as a bust — don't copy that pattern into a new video.

---

## Hard rules

- **Never redraw him by hand or in another tool.** He comes out of `zul.py` or
  he does not go in the video. A one-off hand-drawn Zul is how a character
  stops being a character.
- **Never recolour the beanie.** Red over yellow over green, always.
- **Never add facial detail.** No nose, eyebrows, ears, or mouth shapes beyond
  the five moods. The face carries meaning through the mouth alone.
- **Never draw a detailed hand.** Filled mittens, gloves and five-finger hands
  were all tried and all read as a blob at this line weight. Three strokes.
- He is **faceless-channel compatible**: a drawn stick figure is not an
  identifiable person, and no real logos appear on him.

## Known limits

- **Three-quarter view is an approximation** — features shift 9 units toward
  camera and the silhouette narrows. It reads at a glance but will not survive
  a slow push-in. Prefer front or back for hero shots.
- **No walk cycle, no side view.** If a scene needs him moving across frame,
  cut rather than animate it.
- The beanie's band dividers are clipped to the dome. If you edit the dome
  path, keep them inside the clip group or they stick out as tabs at the sides.
