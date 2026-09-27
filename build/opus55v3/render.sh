#!/bin/bash
# Opus 5.5 v3 render. Env: SHA, VO_URL, MUSIC_URL, ROBOT_URL, ROCKET_URL, PUT_URL (never committed).
set -e; mkdir -p /home/user/v3 && cd /home/user/v3
R=https://raw.githubusercontent.com/helloabyss/helloabyss/$SHA/build/opus55v3
for f in motion.html words.json cap.js; do curl -sSf -o $f $R/$f; done
curl -sSf -o vo.wav "$VO_URL"; curl -sSf -o music.wav "$MUSIC_URL"
curl -sSf -o r.png "$ROBOT_URL"; curl -sSf -o k.png "$ROCKET_URL"
# brighter grade, gentle contrast (user feedback: previous cuts were too dark)
convert r.png -resize 1080x -modulate 104,92 -sigmoidal-contrast 3,50% -quality 90 robot.jpg
convert k.png -resize 1080x -modulate 104,92 -sigmoidal-contrast 3,50% -quality 90 rocket.jpg
(python3 -m http.server 8958 >/dev/null 2>&1 &); sleep 1
NODE_PATH=/usr/local/lib/node_modules node cap.js
D=$(python3 -c "import glob;print(len(glob.glob('fr/*.jpg'))/30)")
# VO untouched in time (captions are keyed to its timestamps); music ducked under it
ffmpeg -v error -y -i vo.wav -i music.wav -filter_complex \
 "[0:a]aresample=48000,apad=pad_dur=2,asplit=2[v][sc];[1:a]aresample=48000,volume=0.30,afade=t=in:d=0.4,afade=t=out:st=$(python3 -c "print($D-1.8)"):d=1.8[m];\
[m][sc]sidechaincompress=threshold=0.03:ratio=6:attack=15:release=350[md];[v][md]amix=inputs=2:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[a]" \
 -map "[a]" -t $D -ar 48000 mix.wav
ffmpeg -v error -y -framerate 30 -i fr/%05d.jpg -i mix.wav -c:v libx264 -preset medium -crf 19 -pix_fmt yuv420p \
 -c:a aac -b:a 192k -shortest -movflags +faststart out.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 out.mp4
curl -sf -o /dev/null -w "PUT %{http_code}\n" -X PUT -H "Content-Type: video/mp4" --upload-file out.mp4 "$PUT_URL"
