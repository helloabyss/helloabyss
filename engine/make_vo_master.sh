#!/bin/sh
# Rebuild the loudness-normalised narration stem the renderer muxes.
#
# vo-full.mp3 is the raw ElevenLabs output and measures -24.66 LUFS -- about 11 dB under
# what a published video wants. A cut built straight from it sounds like it has no
# narration. This produces vo-master.wav at -14 LUFS, stereo, which render_anim.js
# requires. The .wav is gitignored (97MB), so run this after a fresh clone.
set -e
FF=$(python3 -c 'import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())')
SRC=../ai-picks-longform/vo-full.mp3
OUT=../ai-picks-longform/vo-master.wav

echo "measuring $SRC ..."
"$FF" -hide_banner -i "$SRC" -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json \
      -f null - 2>&1 | sed -n '/^{/,/^}/p'

# Pass 2 uses the measurements printed above. They are pinned here because this stem is
# fixed; re-measure and update if the narration is ever regenerated.
"$FF" -hide_banner -loglevel error -i "$SRC" \
  -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=-24.66:measured_TP=-2.36:measured_LRA=3.90:measured_thresh=-35.72:offset=2.62:linear=true,volume=1.97dB,aformat=channel_layouts=stereo" \
  -ar 48000 -c:a pcm_s16le "$OUT" -y

echo "verifying $OUT ..."
"$FF" -hide_banner -i "$OUT" -af loudnorm=I=-14:TP=-1.5:print_format=json -f null - 2>&1 \
  | grep -E '"input_i"|"input_tp"'
echo "done -- input_i should read about -14.0"
