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

## WebM, not MP4 — and how to get MP4 anyway

Nothing here can produce H.264. The bundled ffmpeg is Playwright's
(`/opt/pw-browsers/ffmpeg-1011/ffmpeg-linux`) and carries exactly **two muxers** (`webm`,
`image2`) and **two demuxers** (`image2pipe`, `matroska,webm`). No audio codecs, no MP3
demuxer, no MP4 muxer — so a local `ffmpeg -c:v libx264 ...` will not work here, and neither
will a stream-copy mux, because there is nothing that can read an MP3.

WebM is fine for YouTube (it accepts VP8/VP9 directly) and CapCut imports it.

## Adding the voiceover

Use an **ElevenLabs `composition` node**, which also converts to MP4 as a side effect. Free,
and it ran in ~7 minutes for a 92 MB source:

1. `creative_create_asset_upload` (name, mime type, **exact** byte size) for the WebM and for
   the audio — 200 MB cap each.
2. HTTP `PUT` the bytes to the returned `upload_url` with a matching `Content-Type`.
3. `creative_finalize_asset_upload` with the `asset_id` and `flow_id` → a `node_id`.
4. `creative_add_flow_node` with `node_type: composition`, `model_id: eleven_composition`, and
   `connect_from: [video_node, audio_node]`. The ports resolve automatically.
5. `creative_run_flow_nodes` with `generations_count: 1`, then poll.

Output is **1920×1080 H.264 + AAC**, fragmented MP4, with a `preview_content.mp4` alongside the
master that is ~13× smaller and still full length — a good viewing copy.

**Give it one audio file, not several.** Each audio source lands on its own track starting at
zero, so two VO parts would play over each other, and no clip-offset tool is exposed.

### Verifying the result without a decoder

This ffmpeg cannot open an MP4, so check the container by parsing its atoms: confirm a `vide`
track (`avc1`) and a `soun` track (`mp4a`), then sum the `trun` sample durations per track
across the `moof` fragments — `mdhd.duration` reads 0 in a fragmented MP4 and will mislead you.
Both tracks should come out at the full runtime. The last mux measured:

```
track 1 vide avc1  5816 samples  484.690s   (= 12.0 fps exactly)
track 2 soun mp4a 20873 samples  484.648s
```

## Cost and speed

~0.085s per frame; **5,760 frames ≈ 8 minutes of wall time** for 8 minutes of video. Zero
credits, zero API calls.

To go faster, drop `fps` from 12 to 10 (the push is slow enough to survive it) or shorten
`hold`. Both are arguments to `render_video.js`.
