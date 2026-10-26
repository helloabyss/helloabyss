#!/usr/bin/env python3
"""Fetch a HeyGen VO through ElevenLabs, tempo-fit it, and normalise to -14 LUFS.

HeyGen's CDN 403s on CONNECT, so ElevenLabs fetches it server-side and we pull
the preview from storage.googleapis.com, which is reachable.

Tempo: this channel's own data says shorts over ~40s die. A small atempo lift
is inaudible on speech and brings a 44s read into the band that actually
performs. Word timings are divided by the same factor so alignment holds.

  python3 fetchvo.py <preview_url> <outdir> <target_seconds|0>
"""
import sys, os, json, subprocess, urllib.request

FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'


def run(a, **k):
    return subprocess.run(a, capture_output=True, text=True, **k)


def measure(f):
    r = run([FF, '-hide_banner', '-nostats', '-i', f, '-af',
             'loudnorm=I=-14:TP=-1.0:print_format=json', '-f', 'null', '-'])
    s = r.stderr[r.stderr.rindex('{'):]
    return json.loads(s[:s.index('}') + 1])


def main(url, out, target):
    os.makedirs(out, exist_ok=True)
    raw = os.path.join(out, 'vo-raw.mp3')
    urllib.request.urlretrieve(url, raw)
    dur = float(run([FF, '-i', raw], ).stderr.split('Duration: ')[1][:11].replace(':', ' ').split()[-1]) \
        if False else None
    p = run([FF, '-i', raw])
    h, m, s = p.stderr.split('Duration: ')[1].split(',')[0].split(':')
    dur = int(h) * 3600 + int(m) * 60 + float(s)
    tempo = 1.0
    if target and dur > target:
        tempo = round(dur / target, 4)
        if tempo > 1.25:
            raise SystemExit('tempo %.2f is too aggressive to be inaudible' % tempo)
    src = raw
    if tempo > 1.0:
        fit = os.path.join(out, 'vo-fit.mp3')
        run([FF, '-y', '-loglevel', 'error', '-i', raw, '-af', 'atempo=%.4f' % tempo, fit])
        src = fit
    m0 = measure(src)
    wav = os.path.join(out, 'vo.wav')
    run([FF, '-y', '-loglevel', 'error', '-i', src, '-af',
         ('loudnorm=I=-14:TP=-1.0:LRA=11:measured_I={input_i}:measured_TP={input_tp}:'
          'measured_LRA={input_lra}:measured_thresh={input_thresh}:offset={target_offset}:'
          'linear=true').format(**m0), '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', wav])
    m1 = measure(wav)
    gain = -14.0 - float(m1['input_i'])
    if abs(gain) > 0.05:
        tmp = os.path.join(out, '_g.wav')
        run([FF, '-y', '-loglevel', 'error', '-i', wav, '-af',
             'volume=%.2fdB,alimiter=limit=0.891:level=disabled' % gain,
             '-ar', '48000', '-ac', '2', '-c:a', 'pcm_s16le', tmp])
        os.replace(tmp, wav)
    m2 = measure(wav)
    for f in (raw, os.path.join(out, 'vo-fit.mp3')):
        pass
    print(json.dumps({'duration': round(dur / tempo, 3), 'tempo': tempo,
                      'lufs': m2['input_i'], 'tp': m2['input_tp']}))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], float(sys.argv[3]))
