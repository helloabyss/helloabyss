#!/bin/bash
# Standard render v2: any length, 16:9 or 9:16, parallel frame capture, word timings by alignment.
# Env (signed URLs are never committed):
#   EP        episode dir under build/ (scenes.js lives there)        PAGE   long.html | shortk.html
#   SHA       commit to pin                                          SCRIPT repo path of the narration text
#   IMGMAP    repo path of images.json ({name: url})                 VO_URL narration audio (wav/mp3)
#   MUSIC_URL, WHOOSH_URL, PUT_URL                                   WORKERS (default 6)
#   CLIPMAP   optional repo path of clips.json ({name: mp4 url}); each clip becomes <name>.webm, the moving plate
set -e; WD=/home/user/ep_$EP; mkdir -p $WD && cd $WD
R=https://raw.githubusercontent.com/helloabyss/helloabyss/$SHA
for f in core.js kinds.js boot.js $PAGE cap.js align.py; do curl -sSf -o $f $R/build/standard/$f; done
curl -sSf -o scenes.js $R/build/$EP/scenes.js; curl -sSf -o script.txt $R/$SCRIPT; curl -sSf -o images.json $R/$IMGMAP
curl -sSfL -o vo.src "$VO_URL"; ffmpeg -v error -y -i vo.src -ar 44100 -ac 1 vo.wav; ffmpeg -v error -y -i vo.wav -ar 16000 vo16.wav
python3 align.py vo16.wav script.txt words.json
curl -sSfL -o music.wav "$MUSIC_URL"; curl -sSfL -o whoosh.mp3 "$WHOOSH_URL"
LAND=$([[ $PAGE == long* ]] && echo 1 || echo 0)
for n in $(node -e "eval(require('fs').readFileSync('scenes.js','utf8').split('\n').find(l=>l.startsWith('const IMAGES')).replace('const ','global.'));console.log(IMAGES.join(' '))"); do
  u=$(python3 -c "import json;print(json.load(open('images.json')).get('$n',''))"); [ -z "$u" ] && { echo "WARN no image for $n"; continue; }; curl -sSfL -o $n.png "$u"
  convert $n.png -resize $([ $LAND = 1 ] && echo 1920x || echo 1080x) -modulate 104,92 -sigmoidal-contrast 3,50% -quality 90 $n.jpg; done
if [ -n "$CLIPMAP" ]; then curl -sSf -o clips.json $R/$CLIPMAP
  python3 -c "import json;[print(k,v) for k,v in json.load(open('clips.json')).items()]" | while read n u; do
    curl -sSfL -o $n.mp4 "$u" && ffmpeg -v error -y -i $n.mp4 -an -vf "scale=$([ $LAND = 1 ] && echo 1920:-2 || echo -2:1920),eq=saturation=1.08:brightness=0.02" \
      -c:v libvpx-vp9 -b:v 0 -crf 33 -g 6 -deadline realtime -cpu-used 8 -row-mt 1 $n.webm && echo "clip $n ok" &
  done; wait; fi
(python3 -m http.server 8958 >/dev/null 2>&1 &); sleep 1
N=$(python3 -c "import json,math;print(math.ceil((json.load(open('words.json'))['dur']+0.9)*30))"); K=${WORKERS:-6}; C=$(( (N+K-1)/K ))
echo "frames $N, $K workers x $C"
for i in $(seq 0 $((K-1))); do F0=$((i*C)) F1=$(( (i+1)*C )) PAGE=$PAGE NODE_PATH=/usr/local/lib/node_modules node cap.js > cap$i.log 2>&1 & done; wait
grep -h "ERRORS" cap*.log || true; ls fr | wc -l
D=$(python3 -c "print($N/30)")
python3 - "$D" <<'PYF'
import json,sys
D=float(sys.argv[1]);c=json.load(open('cuts.json'));n=len(c)
f=["[0:a]aresample=48000,apad=pad_dur=3,asplit=2[v][sc]",
   f"[1:a]aresample=48000,volume=0.26,afade=t=in:d=0.4,afade=t=out:st={D-2.5:.2f}:d=2.5[m]",
   "[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md]",
   "[2:a]aresample=48000,asplit=%d%s"%(n,''.join(f'[s{i}]' for i in range(n)))]
f+=[f"[s{i}]adelay={max(0,int((t-0.45)*1000))}:all=1,volume=0.45[w{i}]" for i,t in enumerate(c)]
f.append("[v][md]"+''.join(f'[w{i}]' for i in range(n))+f"amix=inputs={n+2}:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]")
open('mix.txt','w').write(';\n'.join(f))
PYF
ffmpeg -v error -y -i vo.wav -stream_loop -1 -i music.wav -i whoosh.mp3 -filter_complex_script mix.txt -map "[a]" -t $D -ar 48000 mix.wav
ffmpeg -v error -y -framerate 30 -i fr/%05d.jpg -i mix.wav -c:v libx264 -preset veryfast -crf 20 -pix_fmt yuv420p \
  -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
ffprobe -v error -show_entries format=duration,size -of csv=p=0 out.mp4
curl -sf -o /dev/null -w "PUT %{http_code}\n" -X PUT -H "Content-Type: video/mp4" -H "If-None-Match: *" --upload-file out.mp4 "$PUT_URL"
