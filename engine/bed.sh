#!/bin/bash
# Lay a room-tone bed under a narration stem.
#
# QC measured 6.26s of silence below -50dB across 16 gaps -- 16% of a 38s
# short, every one of them at a sentence boundary. Digital silence is a hole,
# and holes are where people swipe. This is NOT music: it is filtered noise at
# roughly -44 dBFS, felt rather than heard, so the gaps stop being dead.
# A real music bed is a separate decision; this removes the defect.
set -euo pipefail
IN=$1; OUT=$2
FF=$(/usr/local/bin/python3 -c "import imageio_ffmpeg;print(imageio_ffmpeg.get_ffmpeg_exe())")
DUR=$("$FF" -nostdin -v error -i "$IN" -f null - 2>&1 >/dev/null; \
      /usr/local/bin/python3 -c "
import subprocess,sys
r=subprocess.run(['$FF','-nostdin','-i','$IN'],capture_output=True,text=True).stderr
for ln in r.splitlines():
    if 'Duration' in ln:
        h,m,s=ln.split('Duration:')[1].split(',')[0].strip().split(':')
        print(float(h)*3600+float(m)*60+float(s)); break")
"$FF" -nostdin -v error -y -i "$IN" \
  -f lavfi -t "$DUR" -i "anoisesrc=color=brown:amplitude=0.30:sample_rate=48000" \
  -filter_complex "[1:a]lowpass=f=320,highpass=f=40,volume=-30dB,aformat=channel_layouts=stereo[bed];
                   [0:a][bed]amix=inputs=2:duration=first:weights=1 0.9:normalize=0[mix];
                   [mix]loudnorm=I=-14:TP=-1.0:LRA=11[out]" \
  -map "[out]" -ar 48000 -ac 2 -c:a pcm_s16le "$OUT"
echo "bed laid: $OUT"
