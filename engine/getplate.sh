#!/bin/sh
# License -> download -> graded 1080x1920 proxy (+ VP9 for the compositor) -> delete master.
#
#   sh engine/getplate.sh <outdir> <NAME> <signed-url> [trim_s] [brightness] [saturation]
#
# Adobe Stock ships ProRes: one 15s clip is ~1GB and a set of ten would
# exhaust the session's disk, so the master never survives this script.
# Chromium here has no H.264 decoder, so a VP9 copy is written for reel.js.
set -e
D=$1; NAME=$2; URL=$3; TRIM=${4:-6}; BRI=${5:--0.13}; SAT=${6:-0.22}
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
HERE=$(dirname "$0")
mkdir -p "$D"
curl -sS -L -o "$D/_raw.mov" "$URL"
"$FF" -y -hide_banner -loglevel error -i "$D/_raw.mov" -t "$TRIM" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=saturation=$SAT:contrast=1.22:brightness=$BRI,format=yuv420p" \
  -r 30 -c:v libx264 -crf 21 -preset veryfast -an "$D/$NAME.mp4"
rm -f "$D/_raw.mov"
python3 "$HERE/checkplate.py" "$D/$NAME.mp4"
"$FF" -y -hide_banner -loglevel error -i "$D/$NAME.mp4" \
  -c:v libvpx-vp9 -b:v 2M -deadline realtime -cpu-used 5 -row-mt 1 -an "$D/$NAME.webm"
echo "$NAME  $(du -h "$D/$NAME.mp4" | cut -f1)"
