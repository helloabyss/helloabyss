#!/bin/bash
# Standard Shorts render (owner-approved 2026-09-27; reference episode build/opus55v4).
# Env: EP (episode dir under build/), SHA (commit to pin), VO_URL, MUSIC_URL, WHOOSH_URL, PUT_URL,
#      IMG_<NAME> for every name in the episode's IMAGES list. Signed URLs are never committed.
set -e; mkdir -p /home/user/ep_$EP && cd /home/user/ep_$EP
R=https://raw.githubusercontent.com/helloabyss/helloabyss/$SHA/build
for f in core.js boot.js short.html cap.js; do curl -sSf -o $f $R/standard/$f; done
for f in scenes.js words.json; do curl -sSf -o $f $R/$EP/$f; done
curl -sSf -o vo.wav "$VO_URL"; curl -sSf -o music.wav "$MUSIC_URL"; curl -sSf -o whoosh.mp3 "$WHOOSH_URL"
for n in $(node -e "eval(require('fs').readFileSync('scenes.js','utf8').split('\n').find(l=>l.startsWith('const IMAGES')).replace('const ','global.'));console.log(IMAGES.join(' '))"); do v=IMG_${n^^}; curl -sSf -o $n.png "${!v}"
  convert $n.png -resize 1080x -modulate 104,92 -sigmoidal-contrast 3,50% -quality 90 $n.jpg; done
(python3 -m http.server 8958 >/dev/null 2>&1 &); sleep 1
NODE_PATH=/usr/local/lib/node_modules node cap.js
D=$(python3 -c "import glob;print(len(glob.glob('fr/*.jpg'))/30)")
# mix: VO untouched in time; looped music ducked under it; a whoosh peak (0.45 s in) on every cut
python3 - "$D" <<'PYF'
import json,sys
D=float(sys.argv[1]);c=json.load(open('cuts.json'));n=len(c)
f=["[0:a]aresample=48000,apad=pad_dur=3,asplit=2[v][sc]",
   f"[1:a]aresample=48000,volume=0.30,afade=t=in:d=0.4,afade=t=out:st={D-1.8:.2f}:d=1.8[m]",
   "[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md]",
   "[2:a]aresample=48000,asplit=%d%s"%(n,''.join(f'[s{i}]' for i in range(n)))]
f+= [f"[s{i}]adelay={max(0,int((t-0.45)*1000))}:all=1,volume=0.55[w{i}]" for i,t in enumerate(c)]
f.append("[v][md]"+''.join(f'[w{i}]' for i in range(n))+f"amix=inputs={n+2}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
open('mix.txt','w').write(';\n'.join(f))
PYF
ffmpeg -v error -y -i vo.wav -stream_loop -1 -i music.wav -i whoosh.mp3 -filter_complex_script mix.txt -map "[a]" -t $D -ar 48000 mix.wav
ffmpeg -v error -y -framerate 30 -i fr/%05d.jpg -i mix.wav -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p \
 -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4
curl -sf -o /dev/null -w "PUT %{http_code}\n" -X PUT -H "Content-Type: video/mp4" --upload-file out.mp4 "$PUT_URL"
