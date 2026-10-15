# Thumbnail kit

Thumbnails are built here as HTML and screenshotted with the Chromium that ships in this
environment. No credits, no generative model, fully reproducible and diffable — which matters
because vidIQ thumbnail generation costs 22 credits (balance: 1) and Higgsfield is at 0.

## Build

```sh
SHELL_BIN=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
"$SHELL_BIN" --no-sandbox --disable-gpu --hide-scrollbars \
  --force-device-scale-factor=1 --window-size=720,1280 --virtual-time-budget=2000 \
  --screenshot=out.png "file://$PWD/<name>.html"
```

**720x1280**, matching `pdt-short/thumbnail-pdt.png`. Copy the PNG into the video's directory
as `thumbnail-<slug>.png`.

### Use `headless_shell`, NOT `chrome --headless`

This cost three rounds of silently broken output, so it is worth stating plainly.

`chromium-1194/chrome-linux/chrome --headless --window-size=720,1280` produces a **1280px-tall
PNG from a 1193px-tall viewport**. Chromium reserves ~87px of window chrome even in headless
mode, so everything below y=1193 is simply never painted — while the file still comes out at
the right dimensions. The footer vanished off three thumbnails this way and the PNGs looked
plausible enough that it read as a CSS bug. It was not; the CSS was correct throughout.

Measured behaviour on this image:

| Binary | `--window-size=720,1280` gives | Screenshot |
|---|---|---|
| `chrome --headless` | viewport **1193** | 1280 tall, bottom 87px blank |
| `chrome --headless=new` | viewport **1193** | same |
| `chromium_headless_shell` | viewport **1280** | 1280 tall, correct |

`headless_shell` maps viewport 1:1 to window size. Use it. If you ever must use `chrome`,
pass `--window-size=720,1367` (1280 + 87) and crop, but there is no reason to.

**How to catch this class of bug:** put something deliberately at the very bottom of the frame
and confirm it survives. Or measure in-page —
`document.querySelector('.foot').getBoundingClientRect()` against `window.innerHeight` — which
is what finally identified it.

## The template

`thumbnail.css` is shared and holds the locked palette and the type scale. Each video gets one
HTML file that pulls it in and adds only its own graphic. Keep the structure identical across
videos — the channel should read as one series in a thumbnail grid, the same way the videos do.

Fixed anatomy, top to bottom:

| Slot | Rule |
|---|---|
| Red rule + kicker | The frame for the video. Never the hook. |
| Hero, two lines | Line one white, line two red. Short — under ~10 characters each. |
| Sub | One line, must not wrap. The arithmetic or the thesis. |
| Graphic | The video's own data visual, not decoration. |
| Footer | "Educational only" left, the channel name right, in red. Absolutely positioned at `bottom:56px` so it cannot be pushed out of frame by a tall middle band. |

## Series mark

All thumbnails carry **THE METICULOUS INVESTOR** in the footer right. That is what makes a
grid of them read as one channel. Paradocs 10X is a separate series with its own sign-off —
do not mix the two marks.

## House style notes

- Palette is `STYLE-GUIDE.md` §3: near-black `#0a0b0c`, white, one red `#E3120B`. Nothing else.
- **No condensed font is installed.** Liberation Sans Bold is compressed with
  `transform:scaleX(.74)` to read as condensed. If a real condensed face is ever installed,
  drop the transform rather than stacking them.
- Hero lines use `white-space:nowrap` deliberately — a wrapped hero means the copy is too long.
  Shorten the words, do not shrink the type.
- The layout is flex with a `flex:1` middle band, so the footer cannot be pushed out of frame.
  Both earlier drafts clipped their footers before this was fixed; keep the structure.
- **Always look at the rendered PNG before committing.** Every defect found in these two —
  clipped labels, a footer off the bottom edge, a label detached from its arrow — was invisible
  in the markup and obvious in the image.

## Deliberately not chasing the vidIQ score

`CLAUDE.md` notes vidIQ's thumbnail scoring rewards saturation and vibrancy, which is the
opposite of this channel's palette. These are built to the identity, not the score.
