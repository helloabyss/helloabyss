#!/usr/bin/env python3
"""Sandbox-side episode builder: assets -> graded plates -> timed spec -> frames -> mp4."""
import json, os, subprocess, sys, math
from PIL import Image, ImageOps, ImageEnhance, ImageStat

TARGET_LUM = 35.0

def sh(*a, **k):
    return subprocess.run(a, check=True, capture_output=True, text=True, **k).stdout

def grade(src, dst):
    im = Image.open(src).convert("RGB").resize((1080, 1920), Image.LANCZOS)
    im = ImageOps.autocontrast(im, cutoff=(1, 1))
    lut = []
    for v in range(256):
        f = v / 255.0
        f = f if f < 0.62 else 0.62 + (f - 0.62) * 0.42
        lut.append(int(max(0, min(255, f * 255))))
    im = im.point(lut * 3)
    im = ImageEnhance.Color(im).enhance(0.34)
    im = ImageEnhance.Contrast(im).enhance(1.12)
    lo, hi = 0.35, 3.2
    for _ in range(18):
        g = (lo + hi) / 2
        t = im.point([int(255 * ((v / 255.0) ** g)) for v in range(256)] * 3)
        if ImageStat.Stat(t.convert("L")).mean[0] > TARGET_LUM: lo = g
        else: hi = g
    im = im.point([int(255 * ((v / 255.0) ** ((lo + hi) / 2))) for v in range(256)] * 3)
    r, g, b = im.split()
    b = b.point(lambda v: int(v * 0.90)); g = g.point(lambda v: int(v * 0.975))
    im = Image.merge("RGB", (r, g, b))
    im.save(dst, "JPEG", quality=92)
    return ImageStat.Stat(im.convert("L")).mean[0]

def make_vo(src, dst):
    """Trim, normalise, then cap internal pauses at 0.30s. Never atempo."""
    sh("ffmpeg","-v","error","-y","-i",src,"-af",
       "silenceremove=start_periods=1:start_duration=0:start_threshold=-45dB,"
       "areverse,silenceremove=start_periods=1:start_duration=0:start_threshold=-45dB,"
       "areverse,loudnorm=I=-16:TP=-1.5:LRA=11","_t.wav")
    sh("ffmpeg","-v","error","-y","-i","_t.wav","-af",
       "silenceremove=stop_periods=-1:stop_duration=0.30:stop_threshold=-38dB:detection=rms",dst)
    return float(sh("ffprobe","-v","error","-show_entries","format=duration",
                    "-of","default=nw=1:nk=1",dst).strip())

def sent_spans(wav, sents, dur):
    from faster_whisper import WhisperModel
    m = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav)
    S = [(s.start, s.end) for s in segs]
    if len(S) == len(sents):
        return S
    t0 = S[0][0] if S else 0.0
    t1 = S[-1][1] if S else dur
    tot = sum(len(x) for x in sents) or 1
    out, acc = [], t0
    for x in sents:
        d = (t1 - t0) * len(x) / tot
        out.append((acc, acc + d)); acc += d
    return out

def build_spec(src, spans, dur):
    beats, cues = [], []
    starts = [spans[b["sent"][0]][0] for b in src["beats"]]
    for i, b in enumerate(src["beats"]):
        a = 0.0 if i == 0 else max(0.0, starts[i] - 0.18)
        z = dur if i == len(src["beats"]) - 1 else max(a + 0.4, starts[i + 1] - 0.18)
        beats.append({"a": round(a, 3), "b": round(z, 3), "plate": b["plate"],
                      "mv": b.get("mv", {}), "blocks": b["blocks"]})
    for i, ph in enumerate(src["phrases"]):
        s0, s1 = spans[i]
        tot = sum(len(p) for p in ph) or 1
        acc = s0
        for p in ph:
            d = (s1 - s0) * len(p) / tot
            cues.append({"a": round(acc, 3), "b": round(min(acc + d, dur), 3), "t": p})
            acc += d
    return {"dur": round(dur, 3), "eyebrow": src["eyebrow"], "date": src["date"],
            "source": src["source"], "plates": src["plates"], "beats": beats, "cues": cues}

def main():
    man = json.load(open("manifest.json"))
    ups = json.load(open("uploads.json"))
    for ep in man["episodes"]:
        i = ep["id"]
        print(f"=== short {i} ===", flush=True)
        src = json.load(open(f"src{i}.json"))
        for n, url in enumerate(ep["plates"], 1):
            sh("curl","-sSf","-o",f"_p{i}_{n}.png",url)
            lum = grade(f"_p{i}_{n}.png", f"s{i}_{n}.jpg")
            print(f"  plate {n} graded lum={lum:.1f}", flush=True)
        sh("curl","-sSf","-o",f"_vo{i}.wav",ep["vo"])
        dur = make_vo(f"_vo{i}.wav", f"vo{i}.wav")
        print(f"  vo {dur:.2f}s", flush=True)
        spans = sent_spans(f"vo{i}.wav", src["sents"], dur)
        spec = build_spec(src, spans, dur)
        json.dump(spec, open(f"spec{i}.json", "w"))
        print(f"  {len(spec['beats'])} beats, {len(spec['cues'])} cues", flush=True)
        n = int(round(dur * 30))
        env = dict(os.environ, SHORT=str(i), NFRAMES=str(n))
        subprocess.run(["node", "cap.js"], check=True, env=env)
        sh("ffmpeg","-v","error","-y","-framerate","30","-i",f"fr{i}/%05d.jpg",
           "-i",f"vo{i}.wav","-c:v","libx264","-preset","slow","-crf","20",
           "-pix_fmt","yuv420p","-profile:v","high","-level","4.2",
           "-c:a","aac","-b:a","160k","-shortest","-movflags","+faststart",f"out{i}.mp4")
        sz = os.path.getsize(f"out{i}.mp4")
        print(f"  encoded out{i}.mp4 {sz/1e6:.1f}MB", flush=True)
        subprocess.run(["curl","-f","-X","PUT","-H","Content-Type: video/mp4",
                        "--upload-file",f"out{i}.mp4",ups[str(i)]], check=True,
                       capture_output=True)
        print(f"  uploaded short {i}", flush=True)
    print("ALLDONE", flush=True)

main()
