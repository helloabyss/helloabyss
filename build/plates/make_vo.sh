#!/bin/bash
# Narration assembly — This Week in Tech
#
# The rule this encodes: NEVER use atempo to hit runtime. seed_audio pads every
# sentence boundary, and the house script style is punctuation-dense, so ~31% of
# raw TTS output is silence. Capping internal pauses removes dead air without
# touching the speech, which is what keeps the read sounding natural.
#
# Usage: generate one wav per beat (s1..s5), then run this.
set -e
CAP=${CAP:-0.30}      # max internal pause, seconds
GAP=${GAP:-0.20}      # silence between beats, seconds

for i in 1 2 3 4 5; do
  # 1. trim lead/tail silence, 2. normalise loudness
  ffmpeg -hide_banner -loglevel error -y -i s$i.wav \
    -af "silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB,\
areverse,silenceremove=start_periods=1:start_silence=0.05:start_threshold=-45dB,areverse,\
loudnorm=I=-16:TP=-1.5:LRA=11" -ar 48000 -ac 1 f$i.wav
  # 3. cap internal pauses — this is what buys the runtime
  ffmpeg -hide_banner -loglevel error -y -i f$i.wav \
    -af "silenceremove=stop_periods=-1:stop_duration=$CAP:stop_threshold=-38dB:detection=rms" \
    -ar 48000 -ac 1 g$i.wav
done

ffmpeg -hide_banner -loglevel error -y -f lavfi -t $GAP -i anullsrc=r=48000:cl=mono -c:a pcm_s16le gap.wav
ffmpeg -hide_banner -loglevel error -y \
  -i g1.wav -i gap.wav -i g2.wav -i gap.wav -i g3.wav -i gap.wav -i g4.wav -i gap.wav -i g5.wav \
  -filter_complex "[0][1][2][3][4][5][6][7][8]concat=n=9:v=0:a=1" -ar 48000 -ac 2 vo_master.wav

python3 - <<'PY'
import subprocess, json
d=lambda p: float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration',
    '-of','csv=p=0',p],capture_output=True,text=True).stdout.strip())
GAP=0.20; segs=[d(f'g{i}.wav') for i in range(1,6)]
t=0.0; beats=[]
for i,s in enumerate(segs):
    beats.append({'i':i,'start':round(t,3),'end':round(t+s,3)}); t+=s+(GAP if i<4 else 0)
tot=d('vo_master.wav')
print(f"VO MASTER {tot:.3f}s  {139/tot*60:.1f} WPM  in 50-60: {50<=tot<=60}")
json.dump({'beats':beats,'total':tot}, open('timeline.json','w'))
PY
