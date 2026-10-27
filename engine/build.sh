#!/bin/bash
# Render a short AND gate it. One command, so QC cannot be forgotten.
#
#   engine/build.sh <dir> <out.mp4> [fps]
#
# Nine blocking defects once shipped from a cut that had been through four
# render passes and a human's eyes every time. Rendering and checking are the
# same step now, and a blocking finding is a non-zero exit.
set -euo pipefail
DIR=${1:?usage: build.sh <dir> <out.mp4> [fps]}
OUT=${2:?usage: build.sh <dir> <out.mp4> [fps]}
FPS=${3:-30}
ROOT=$(cd "$(dirname "$0")/.." && pwd)

AUDIO="$DIR/vo.wav"
[ -f "$DIR/vo-bed.wav" ] && AUDIO="$DIR/vo-bed.wav"
echo "narration: $AUDIO"

( cd "$DIR" && node "$ROOT/engine/reel.js" beats.json plates \
    "$(basename "$AUDIO")" captions.json "$OUT" "$FPS" )

echo
python3 "$ROOT/engine/qc.py" "$DIR" "$OUT" || {
  echo
  echo "QC FAILED -- fix the blocking findings, or record a deliberate waiver"
  echo "in $DIR/PRODUCTION.md saying which and why."
  exit 1
}
