# ZUL — channel host

Zul is the recurring host. He appears in every stickman video. The point of
this file is that he looks **identical every time**.

## The artwork is the character

**The supplied sheets in `engine/art/` are canonical.** Everything generated —
the vector rig in `engine/zul.py`, any cut-out parts — is **secondary and must
match them, never the other way round.**

Locked **2026-10-06**. ID: R/Y/G beanie · **Meta Ray-Ban smart glasses (black
Wayfarer)** · curls · white polo.

| Sheet | Contents |
|---|---|
| `art/zul-body.jpg` | Official turnaround + 11 full-figure views and poses |
| `art/zul-bust-glasses.jpg` | 9 bust poses, with glasses |
| `art/zul-bust-plain.jpg` | 9 bust poses, no glasses |
| `art/zul-turnaround.jpg` | Front / three-quarter / back |
| `art/zul-face.jpg` | Close-up, no glasses |

### The pose library

`extract_poses.js` cuts all 30 named poses off the sheets into `art/poses/`,
keyed to transparency, and writes `art/poses/manifest.json`.

| Set | Poses |
|---|---|
| `glasses` | official · idle-deadpan · point-right · point-left · present-palm · shock · skeptical · thumbs-up · thinking |
| `plain` | the same nine, without glasses |
| `body` | body-front · body-3q-right · body-3q-left · body-back · full-point-right · full-point-left · full-present-palm · full-shock · full-skeptical · full-thumbs-up · full-shrug · turnaround |

```python
from art import zul_pose, POSES
svg += zul_pose('body', 'full-point-right', x=120, y=80, h=900)
svg += zul_pose('glasses', 'skeptical', x=18, y=58, h=600)
```

### Three rules the extraction depends on

- **Panels keep their full uniform size. Never trim a pose to its ink.** The
  sheets are drawn at one crop and scale, so the poses are registered to each
  other; trimming destroys that and makes a pose swap jump on screen.
- **The background comes off by flood fill, not a luminance key.** The polo is
  white on a white page — a key deletes the shirt along with the page.
- **Seed the fill only from edges the figure does not cross.** A bust is
  cropped at the chest, so the shirt's interior touches the bottom edge; seed
  there and the fill leaks straight into the polo. This one shipped broken
  once and was caught by rendering the poses onto a dark plate.

### Animate by cutting between poses

The poses are **drawn**, so animation cuts between them and adds only a float
and a settle — limited animation, done the way it is actually done. See
`engine/pose_anim.py`.

**Do not bend the limbs of a drawn pose.** An earlier rig synthesised poses
from generated parts and the result was not Zul; a later one cut a head off
the official art and could only nod, because the arms overlap the torso and
separating them punches holes in the supplied drawing. The pose library makes
both obsolete. If a pose is needed that is not in the 30, it gets **drawn** —
that is what `PROCREATE-PIPELINE.md` is for.

### Do not

- Redraw, recolour, restyle or "improve" the sheets.
- Let anything generated drift from them. If the two disagree, the art wins.
- Mix the glasses and no-glasses sets inside one video.

## The look

| | |
|---|---|
| **Head** | Plain circle, radius 46, white fill, 7pt black line |
| **Beanie** | Three-band knit cap — **red crown, yellow middle, green brim**, in that order top to bottom. Roughly 47 / 21 / 32 of its height. Sits ~12 above the head top |
| **Hair** | Tight black spiral coils, 5 per side, each ~6.5 radius, on an arc just outside the head edge from under the brim down to cheek level |
| **Glasses** | Rectangular frames, rounded corners, **light blue-grey tinted lenses** (`#b9c7d0`). Black dot eyes visible through them |
| **Face** | Dot eyes, single-line mouth. Nothing else — no nose, no brows, no beard |
| **Head** | A plain circle |
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
| `beanie` | `True` (default) · `False` — full head of curls instead |
| `beard` · `brows` · `jaw` | all default **`False`** — see below |
| `legs` | `False` (default, bust) · `True` |

### Bare-headed variant — `beanie=False, glasses=False`

No cap, no glasses: the crown is drawn as a hairline arc plus an inner ring of
coils, and the face is just eyes and mouth. Sheets in `engine/zulbare/`.

This variant is **pure black and white** — the beanie was the only colour on
him. That makes it a closer fit to the three-colour editorial palette than the
cap version, which is worth knowing when picking a host look for a channel.

Three things had to be solved for the bare head, so don't re-litigate them:

- **The crown needs both rings.** The outer hairline arc alone leaves a bald
  patch inside a halo.
- **The back of the head is a perimeter ring, crown left white.** A filled grid
  of coils packs tighter than the 5pt stroke and collapses into a solid black
  disc, which is off-style for flat line art. Scattered interior coils read as
  a colander. The ring matches how the hairline works in front view.
- Coil radius stays ~7. Larger and they merge; smaller and they read as dots.

**Glasses are on by default in the cap version.** The reference pack showed him with glasses in
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
- **Never add facial detail** beyond what is listed: no nose, no ears, no mouth
  shapes outside the five moods.
- **Never draw a detailed hand.** Filled mittens, gloves and five-finger hands
  were all tried and all read as a blob at this line weight. Three strokes.
- He is **faceless-channel compatible**: a drawn stick figure is not an
  identifiable person, and no real logos appear on him.

### The masculine variant — available, and OFF by default

`beard=True, brows=True, jaw=True` reads noticeably more masculine. **It does
not match the canonical artwork**, which has a round head, no brow bar and no
beard, so it is off by default and should not be mixed with the originals
inside one video. It is kept because it works, and because the problems below
were expensive to find:

1. **The beard.** A filled jaw-line shape. The strongest cue the style allows.
   It must follow the jaw and stop at the cheek — an earlier version climbed to
   eye level and ringed the face in black, closing it in.
2. **The brow bar.** Two straight low strokes. Worth checking it is actually
   visible: the first attempt was drawn correctly and completely hidden behind
   the inner ring of crown curls.
3. **The jaw.** Replacing the plain circle with straight temples and a flat
   wide chin. Subtle alone, decisive combined with the brow.
4. **Shoulders out to ±46 and a straighter torso**, which `jaw=True` also
   switches on. The neck went with it — but 11pt read as a pillar at thumbnail
   scale, so the broad build uses 7 like the canonical one.

**The beanie hides the brow bar**, because the brim sits lower than the brow.
That is what a beanie pulled down does, and it is left alone rather than
fought — but it means the cap version reads slightly softer than the bare one.

## Known limits

- **Three-quarter view is an approximation** — features shift 9 units toward
  camera and the silhouette narrows. It reads at a glance but will not survive
  a slow push-in. Prefer front or back for hero shots.
- **No walk cycle, no side view.** If a scene needs him moving across frame,
  cut rather than animate it.
- The beanie's band dividers are clipped to the dome. If you edit the dome
  path, keep them inside the clip group or they stick out as tabs at the sides.
