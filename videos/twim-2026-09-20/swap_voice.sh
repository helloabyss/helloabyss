#!/usr/bin/env bash
# Swap in the locked Alex Wright stem and rebuild the episode. Zero credits.
#   ./swap_voice.sh alexwright.wav              (one file)
#   ./swap_voice.sh beat1.wav ... beat9.wav     (nine files - exact sync)
set -e
export FFMPEG_PATH=/usr/bin/ffmpeg FFPROBE_PATH=/usr/bin/ffprobe
python3 align_stem.py "$@"
python3 gen.py
npx --yes hyperframes@0.8.55 check
npx --yes hyperframes@0.8.55 render --quality delivery --output twim-2026-09-20.mp4
ffprobe -v error -show_entries format=duration -show_entries stream=codec_type -of default=noprint_wrappers=1 twim-2026-09-20.mp4
