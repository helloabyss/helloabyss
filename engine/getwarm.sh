#!/bin/bash
# Fetch a licensed Adobe Stock master, crop it to portrait, grade it WARM, and
# write a VP9 WebM plate. The master is ProRes and runs to ~1GB, so it is
# deleted the moment the transcode lands -- disk here is a fixed allowance.
#
# The grade is the point. The old pipeline ran brightness=0.72 saturation=0.62,
# which is what made every frame read near-black; here the plate is LIFTED and
# warmed instead, so the aubergine/amber palette has something to sit on.
set -euo pipefail
OUT=$1; NAME=$2; URL=$3; TRIM=${4:-0}; DUR=${5:-8}
FF=$(/usr/local/bin/python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
mkdir -p "$OUT"
M="$OUT/.master-$NAME.mov"
curl -sL --fail -o "$M" "$URL"
GRADE="eq=brightness=0.04:saturation=0.98:contrast=1.06,colorbalance=rm=0.08:gm=0.01:bm=-0.06:rh=0.06:bh=-0.05"
CROP="crop='min(iw,ih*9/16)':'min(ih,iw*16/9)',scale=1080:1920:flags=lanczos"
"$FF" -nostdin -v error -y -ss "$TRIM" -t "$DUR" -i "$M" \
  -vf "$CROP,$GRADE" -an \
  -c:v libvpx-vp9 -b:v 0 -crf 32 -row-mt 1 -speed 2 -pix_fmt yuv420p \
  "$OUT/$NAME.webm"
"$FF" -nostdin -v error -y -i "$OUT/$NAME.webm" -c:v libx264 -crf 20 -pix_fmt yuv420p -an "$OUT/$NAME.mp4"
rm -f "$M"
echo "$NAME done: $(du -h "$OUT/$NAME.webm" | cut -f1)"
