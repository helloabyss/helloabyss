# Thumbnail mockups — free, before any video

Renders thumbnail concepts to PNG with the local Chromium. **No credits.** The user picks a
concept from the mockups. Only the chosen one is turned into a real image, one paid
generation at most.

```
node tools/thumbnail-mockup/render.mjs <video-dir>
```

Reads `<video-dir>/thumbnails.json`, writes `<video-dir>/mockups/<id>.png` (1080×1920) and
`mockups/sheet.png`. The sheet shows each concept at review size **and at real Shorts-feed
size**, because feed size is where the click is won or lost.

## Spec
```json
{ "concepts": [ {
  "id": "A", "label": "Name + strike",
  "tag": "PARADOCS 10X",              // small grey top line, optional
  "subject": "vr-glasses",            // preset from subjects.mjs, or "none"
  "subjectSvg": "<svg …>",            // optional custom drawing instead of a preset
  "textPosition": "top",              // or "bottom"
  "lines": [ { "text": "META", "size": 300, "color": "white|red", "strike": false, "box": "red" } ],
  "finalImage": "prompt brief for the one paid generation if this concept is chosen"
} ] }
```
Lines that would overflow are shrunk automatically, so text never clips. Fonts: Anton and
Oswald (SIL OFL, in `fonts/`). Palette is fixed: near-black, white, one red.

## Subject presets (`subjects.mjs`)
`vr-glasses`, `headset`, `headset-vs-glasses`, `glasses-on-scale`, `chart-drop`, `none`.
They are stand-in drawings that show composition and scale, not the final photo. Add a preset
when a new topic needs one.

## Workflow
1. Write `thumbnails.json` with 3 concepts that differ in their **hook** (name, number,
   old-vs-new), not just in the wording.
2. Render, send `mockups/sheet.png` to the user, and get a pick **before making the video**.
3. After the pick: one generation (Higgsfield `gpt_image_2_5`, 9:16, 2K, count 1, ~1.4 credits)
   from that concept's `finalImage` plus its text lines. Check it for free with Adobe
   `asset_inline_preview`.
4. Nothing else gets generated without the user's OK.
