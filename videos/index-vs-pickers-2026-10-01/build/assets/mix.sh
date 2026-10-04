#!/usr/bin/env bash
# Mix the narration with a low music bed: music about 15 dB under the voice, ducked further by sidechain
# compression while Brian speaks, 1.5 s fade-in (the track fades itself out as the narration ends); loudness normalised to -14 LUFS. Output: assets/vo-mix.m4a
set -euo pipefail
cd "$(dirname "$0")"
TOTAL=${1:-62.05}
ffmpeg -v error -y -i vo-brian.mp3 -i music-bed.mp3 -filter_complex "
 [0:a]aresample=48000,aformat=channel_layouts=stereo,apad=whole_dur=${TOTAL},asplit=2[vo][sc];
 [1:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:${TOTAL},volume=0.14,afade=t=in:d=1.5[mus];
 [mus][sc]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=350[duck];
 [vo][duck]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000[out]" \
 -map "[out]" -c:a aac -b:a 192k vo-mix.m4a
ffprobe -v error -show_entries format=duration -of compact vo-mix.m4a
