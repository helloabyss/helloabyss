# Animating and encoding the video, here

```sh
python3 player_det.py player.html          # one page, all 60 scenes, deterministic
NODE_PATH=/opt/node22/lib/node_modules \
  node render_video.js player.html quiet-depression.webm 60 12 8
```

Output: **1920×1080, 12 fps, VP8/WebM, exactly 8.000s per scene, 8m00s total.**

## How it works

Chromium renders each frame, the JPEG buffer is piped straight into ffmpeg's stdin, and ffmpeg
encodes VP8. **Nothing touches disk between the two** — 5,760 frames would otherwise be ~500 MB
of intermediates.

```
player.html --(Playwright screenshot, JPEG buffer)--> ffmpeg image2pipe --> .webm
```

Animation per scene: a fast entry pop (3.5% scale-up over the first 4% of the hold) then a slow
linear push to +5.5%. Hard cuts between scenes, which matches the "sudden pop-ins and hard cuts"
rhythm in the original spec.

## Why this build of ffmpeg forced the design

The bundled Playwright ffmpeg is stripped. Discovered the hard way:

| Wanted | Available | Consequence |
|---|---|---|
| libx264 / MP4 | **libvpx only**, webm muxer only | Output is **WebM**, not MP4 |
| `concat` demuxer | absent | Cannot stitch a file list |
| `image2` demuxer | **absent** — only `image2pipe` | Cannot read `%02d.png` off disk |
| PNG decoder | **absent** — but **mjpeg decoder present** | Frames must be **JPEG**, not PNG |
| `-preset`, `-safe` | absent | x264-style flags all fail |

The unlock was `-f image2pipe -c:v mjpeg -i pipe:0`. **The explicit `-c:v mjpeg` before the
input is required** — without it ffmpeg opens the pipe but decodes no stream and dies with
"Output file does not contain any stream".

## Why not Playwright's own recordVideo

It works and is far simpler, but it records in **real time** and the renderer cannot keep up:
measured **~15% stretch**, so 8-second scenes landed at ~9.2s and drifted further with each
cut. That breaks sync against a voiceover and against `timing.srt`.

Driving frames deterministically — `setFrame(scene, progress)`, screenshot, next — removes wall
clock from the loop entirely. Measured output: **24.00s for three 8s scenes.** Zero drift.

## WebM, not MP4

Nothing here can produce H.264. WebM is fine for YouTube (it accepts VP8/VP9 directly) and
CapCut imports it. If you need MP4, convert once locally:

```sh
ffmpeg -i quiet-depression.webm -c:v libx264 -crf 18 -preset slow quiet-depression.mp4
```

## Cost and speed

~0.085s per frame; **5,760 frames ≈ 8 minutes of wall time** for 8 minutes of video. Zero
credits, zero API calls.

To go faster, drop `fps` from 12 to 10 (the push is slow enough to survive it) or shorten
`hold`. Both are arguments to `render_video.js`.
