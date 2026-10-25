# ZUL — host of The Meticulous Investor

**Zul belongs to the money channel (The Meticulous Investor). He is NOT a PARADOCS10X
host.** Corrected 2026-10-25 by the channel owner; this file previously said the opposite
and that error put him into a PARADOCS10X short.

PARADOCS10X has no on-screen host. It is imagery-first per `STYLE-GUIDE.md` — a line-art
stickman on that channel is an off-brand import, not a style.
The point of this file is that he looks and sounds **identical every time** —
treat it the way `STYLE-GUIDE.md` is treated, as locked.

Code: `engine/zul.py`.

**Authoritative model sheets — supplied by the owner, locked 2026-10-06:**
`engine/zulsheet/bust-kit-2026-10-06.jpg` (nine bust poses),
`body-profile-2026-10-06.jpg` (turnaround, cut views, full poses),
`no-beanie-2026-10-06.jpg` (the off-duty variant).
Earlier `01.png` / `02.png` are superseded.

**When the code and a sheet disagree, the sheet is right.** Checked 2026-10-25 and the
code had drifted in four ways: tinted lenses instead of clear, too few curls, a single
collar band instead of two flaps, and a torso wide enough to read squat — the exact
failure the proportions note below warns about. All four corrected.

Still not built: the **no-beanie variant** (full afro, same glasses, curls and polo).

### Minimum legible scale — measured 2026-10-25

**Do not draw him below `sc=0.8`.** Below that the glasses, curls and mouth merge into a
dark blob on a dark plate — the same failure already recorded for hands. `zul.py` raises
below 0.6 rather than letting it ship.

He was placed at `0.62` in a first composite and read as a smudge. The error was size, not
detail: measured against the reference, the corner host occupies about **22% of frame
height**, which in this coordinate space is **`sc≈1.2`** on a 1080×1920 frame — roughly
double what looks right in a layout sketch. Curl count also thins automatically below 0.75.

---

## The look

| | |
|---|---|
| **Head** | Plain circle, radius 46, white fill, 7pt black line |
| **Beanie** | Three-band knit cap — **red crown, yellow middle, green brim**, in that order top to bottom. Roughly 47 / 21 / 32 of its height. Sits ~12 above the head top |
| **Hair** | Tight black spiral coils, 5 per side, each ~6.5 radius, on an arc just outside the head edge from under the brim down to cheek level |
| **Glasses** | **Meta Ray-Ban smart glasses — black Wayfarer.** Heavy black frames, rounded corners, **clear lenses, not tinted**. Black dot eyes read plainly through them. *Corrected 2026-10-25 from the locked 2026-10-06 sheet: the code and this file both carried a blue-grey tint (`#b9c7d0`) that made them read as safety goggles.* |
| **Face** | Dot eyes, single-line mouth. Nothing else — no nose, no brows |
| **Shirt** | White polo: cap sleeves, **two folded collar flaps** forming the V, short placket, two buttons centred on it. *The code drew the collar as a single V band for thumbnail legibility; the sheet shows two flaps and the sheet wins.* |
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
