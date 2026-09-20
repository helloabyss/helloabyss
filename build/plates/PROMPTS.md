# Plate prompts — 2026-09-20

**Model:** `soul_cinematic` (Soul Cinema) · **quality:** `1.5k` · **aspect:** `9:16`
**Cost:** 0.12 credits per image. 13 generated (11 kept, 2 discarded), **1.56 credits total**.

## Why this model and this shape

| Option | Cost | Verdict |
|---|---:|---|
| `generate_video` (seedance_2_5, 5s) | **35.00** | 11 clips ≈ 385 credits, and generated clips can't be timed to a 2–3s shot grid |
| `cinematic_studio_2_5` image | 2.00 | |
| `nano_banana` image | 1.00 | |
| `z_image` image | 0.15 | budget, but stylised rather than cinematic |
| **`soul_cinematic` @1.5k** | **0.12** | **cheapest AND the cinematic/concept-art model** |

Stills + local motion is ~290× cheaper than generated video, and the camera moves,
captions, lower-thirds, graphics and wipes are all done for free in `build/animatic/`.
Costs were confirmed with `get_cost: true` preflights before anything was spent.

## Two rules the prompts follow

1. **Always prompt for a well-exposed image.** Asking for "near-black / deep shadow"
   returns a near-empty frame — measured at 99% of pixels below luminance 40 on the first
   two attempts. The house look is applied afterwards by `norm.py`.
2. **Generic, unbadged objects only.** No real product or UI is ever generated: no Google
   Home app, no Snap Specs, no iOS screens. That would be fabricating product footage.
   This follows the finance channel's existing practice ("the autonomous pod is generic and
   unbadged"). Every prompt ends with the no-people / no-text / no-logos clause.

## The plates

| # | Used in shots | Subject |
|---|---|---|
| p1 | 1, 6 | Matte black electronic deadbolt on a wooden door, macro |
| p2 | 2 | Unbranded phone face-up on a dark walnut desk, screen glow across the grain |
| p3 | 3 | Modern living room at dusk, standby indicator lights, empty room |
| p4 | 4 | Generic cylindrical fabric smart speaker, warm light ring |
| p5 | 5 | Unbranded indoor security camera lens, macro |
| p6 | 8, 9 | Generic thick-rimmed smart glasses on dark slate, rim light |
| p7 | 10 | Single convex optical lens element, edge highlight, caustic |
| p8 | 12, 13, 14 | Unbranded phone at an angle on concrete, screen OFF, mirror-dark |
| p9 | 18 | Laser beam through a diffraction grating on an optical bench |

Shared suffix on every prompt:

> Strong contrast, shallow depth of field, anamorphic lens, fine film grain,
> editorial photography, well exposed, muted palette. No people, no hands, no faces,
> no text, no logos, no branding.

## Two plates were regenerated after QA

Composition was checked by rendering each graded plate as a luminance map (the
Higgsfield CDN is blocked from the build container, so images can't be viewed directly).

- **p7** first read as flat horizontal bands rather than optics → reprompted for a single
  convex element with an edge highlight and a caustic.
- **p8** first came back as a **featureless glowing rectangle** — "blank glowing screen"
  was rendered literally, 32% blown pixels → reprompted with the screen **off**, acting as
  a dark mirror, lit by raking side light.

## Verification

Every plate is checked numerically after grading: mean luminance, % below 40, % blown,
mean saturation. Final set: all plates at luminance 33.7–45.0, blown ≤ 7%.
Consistency across plates is what the grade is for — don't skip it.
