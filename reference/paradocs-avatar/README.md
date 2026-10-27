# PARADOCS10X channel avatar

Three options, all 800x800, all tested at the sizes YouTube actually renders:
160px (channel page), 68px (search), 48px (beside a video title), 40px
(comments). 40px is the real test and it is where the old one failed.

## What was wrong with the old one

| Problem | Measured |
|---|---|
| **A ring drawn inside YouTube's circular mask** | YouTube already crops avatars to a circle, so the drawn ring is a *second* ring. It eats the outer third: at 40px the X occupies about half the visible disc. |
| **Reads as a close button** | At 40px a plain cyan X on dark is the universal "dismiss / delete / error" glyph. No channel identity, and it now also collides with the X logo. |
| **Neon and glow** | `STYLE-GUIDE.md` is explicit: "No neon, gradients, sparkles." The bloom also softens every edge, which is the one thing you cannot afford at 40px. |
| **Matched nothing** | Cyan appears in no video on this channel. |

## The options

**A — `A-10x-recommended.png`. Recommended.** `10X` with the X in amber.
Carries the public channel name, survives 40px, and nothing else in a
subscription feed looks like it.

**B — `B-px-monogram.png`.** `PX` monogram, the most legible of the three at
40px. The catch: PX is the *internal* shorthand in the build docs. Viewers
have never seen it, so this teaches an abbreviation rather than reinforcing
the name.

**C — `C-x-twotone.png`.** Keeps the X, which is the existing equity, but
fills the frame and splits it two-tone so it stops reading as a close button.
Pick this one to change as little as possible.

An earlier pass cut a notch out of the X to make its silhouette specific. At
small size that read as a rendering artifact, not as design. Dropped.

## Palette

Near-black `#141118` with one amber accent `#e0a008` — the WARM DARK scheme
the owner chose for this channel's videos, so the avatar and the content
finally match.
