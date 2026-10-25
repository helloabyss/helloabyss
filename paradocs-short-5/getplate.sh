#!/bin/sh
# License -> download -> graded 1080x1920 proxy -> delete the master.
# Adobe Stock ships ProRes; one 15s clip is ~1GB and ten would exhaust the
# session's disk allowance, so the master never survives this script.
set -e
NAME=$1; URL=$2; TRIM=${3:-6}
# Brightness is per-plate: a bright office clip needs pulling down, an
# already-near-black source needs leaving alone or lifting.
BRI=${4:--0.13}
FF=/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2
D=$(dirname "$0")/plates
curl -sS -L -o "$D/_raw.mov" "$URL"
"$FF" -y -hide_banner -loglevel error -i "$D/_raw.mov" -t "$TRIM" \
  -vf "scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,eq=saturation=0.28:contrast=1.22:brightness=$BRI,format=yuv420p" \
  -r 30 -c:v libx264 -crf 21 -preset veryfast -an "$D/$NAME.mp4"
rm -f "$D/_raw.mov"
# The grade crushed one plate to pure black (mean luma 0.0) and it would have
# shipped unnoticed. Every plate is measured before it is accepted.
python3 "$(dirname "$0")/checkplate.py" "$D/$NAME.mp4"
echo "$NAME.mp4  $(du -h "$D/$NAME.mp4" | cut -f1)"
