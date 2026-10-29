# paradocs-watt-hours — plates

Licensed Adobe Stock footage is gitignored: the licence covers use in a work,
not redistribution, and this repo may be public. These are the IDs and the
search strings, so the set can be re-sourced.

## The brief, rewritten 2026-10-26

The first cut of this short was plated with server racks and fibre-optic
abstracts graded to `brightness 0.72, saturation 0.62`. The owner rejected the
whole look ("Hate the dark Vader with a splash of red theme ughh … makes me
sick") and asked for vox-pop style. A machine room is the opposite of vox pop.

So the plates are now human-scale and warm: hands, feet, daylight, a sky. The
channel rule that there are **no identifiable people** still holds — every shot
is hands, feet, or a figure from behind, and the two that show a face were not
licensed. That satisfies both the faceless rule and the vox-pop energy.

| Plate | Stock ID | What it is | Search string |
|---|---|---|---|
| `W1` | 619849758 | Vertical. Hands typing on a phone, indoors, night. The query being made. | `close up hands typing on smartphone screen warm indoor light no face` |
| `W2` | 518397775 | Vertical. Power lines over the Utah desert at sunset. Where the energy comes from. | `electricity power lines pylon sunset golden hour warm sky` |
| `W3` | 568507442 | Feet of four unrecognizable people, business district, hard sun. | `handheld street interview golden hour city people walking warm candid back of head faceless` |
| `W4` | 303759063 | Hands on a phone beside a window, daylight. | `close up hands typing on smartphone screen warm indoor light no face` |
| `W5` | 225263680 | High-voltage lines close up at sunset. | `electricity power lines pylon sunset golden hour warm sky` |

## Grade

`engine/getwarm.sh`, not `engine/getplate.sh`. Lifted and warmed rather than
crushed:

    eq=brightness=0.04:saturation=0.98:contrast=1.06,
    colorbalance=rm=0.08:gm=0.01:bm=-0.06:rh=0.06:bh=-0.05

Mean luma lands 115–178, where the old plates sat near 40. `engine/checkplate.py`
now passes that range and prints a note above 120: a bright plate means type has
to sit on chrome (a card, a panel, a band) or inside the foot scrim, never bare
over the picture. Every layout here obeys that.

## Composition

Six layouts across 29 beats — `full`, `split`, `card`, `quote`, `versus`,
`band` — rather than one layout repeated. The `quote` beats are the vox-pop
caption cards.
