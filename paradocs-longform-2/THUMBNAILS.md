# Thumbnails

Built locally with headless Chromium + Playwright — **no credits used**. vidIQ's generator
costs 22 and the balance is 1; Higgsfield is 0. Source files are in `thumb-src/`, re-render
with `NODE_PATH=/opt/node22/lib/node_modules node thumb-src/shoot.js`.

Per `CLAUDE.md`, these are deliberately dark and desaturated. vidIQ's thumbnail scorer
penalises exactly that — **do not chase the score at the cost of the identity.**

| File | Size | For |
|---|---|---|
| `thumb-longform-A.png` | 1280×720 | Long-form — **"The promise that expired"** |
| `thumb-longform-B.png` | 1280×720 | Long-form — **"$30,000 for one wafer"** |
| `../paradocs-short-3/thumbnail.png` | 1080×1920 | Short 3 |
| `../paradocs-short-4/thumbnail.png` | 1080×1920 | Short 4 |

## Choosing between the long-form variants
- **A — "The promise that expired."** Editorial and curiosity-led. The cost curve falls for
  fifty years then turns red. Carries `$30,000` as a secondary callout, so it does both jobs.
  **Recommended** — it matches the video's actual thesis rather than one statistic.
- **B — "$30,000 for one wafer."** Concrete and arresting; the number does the work. Likely
  the higher click-through of the two, but it front-loads the least-audited number in the
  video, which sets up a "that figure is wrong" comment thread.

Pick A if the video should be judged on its argument, B if on its hook.

## Design rules applied
- Three-colour palette only: near-black `#0B0B0C`, white, one red `#E11D22`
- Heavy uppercase sans, horizontally condensed (`scaleX(.88–.9)`) — no condensed face is
  installed, so it is synthesised
- No faces, no logos, no device that resembles a real product; the wafer and the cost curve
  are drawn as vector, not photographed
- No emoji, arrows, glows, gradients or exclamation marks
- `PARADOCS 10X` wordmark bottom-left on all four, for series consistency

## Two rendering gotchas, recorded so they are not rediscovered
1. **Chromium's `--screenshot` silently stops painting below ~600px** with
   `--window-size=1280,720` — content near the bottom vanishes with no error, and the PNG is
   still emitted at the full requested size. Use **Playwright** (`page.screenshot`), which sets
   the viewport correctly. Installed globally at `/opt/node22/lib/node_modules`.
2. **`position:absolute` with `bottom:` does not resolve** under that same headless path. The
   layout here uses flexbox `space-between` instead.
