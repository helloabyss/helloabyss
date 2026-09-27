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

def _tok(s):
    import re
    return [t for t in re.split(r"[\s\-]+", s) if re.sub(r"[^A-Za-z0-9']", "", t)]

def _norm(t):
    import re
    return re.sub(r"[^a-z0-9']", "", t.lower())

def align(wav, src, dur):
    """Word-level alignment. Each script token is matched to a whisper token with
    difflib; unmatched tokens (e.g. 'twenty' vs '20') are interpolated between the
    nearest matched neighbours. Returns per-sentence and per-phrase (start, end)."""
    import difflib
    from faster_whisper import WhisperModel
    m = WhisperModel("base.en", device="cpu", compute_type="int8")
    segs, _ = m.transcribe(wav, word_timestamps=True)
    wt = []
    for sg in segs:
        for w in sg.words:
            parts = _tok(w.word) or [w.word]
            step = (w.end - w.start) / len(parts)
            for k, pt in enumerate(parts):
                wt.append((_norm(pt), w.start + k * step, w.start + (k + 1) * step))
    mine, where = [], []
    for si, ph in enumerate(src["phrases"]):
        for pi, p in enumerate(ph):
            for t in _tok(p):
                mine.append(_norm(t)); where.append((si, pi))
    sm = difflib.SequenceMatcher(None, mine, [x[0] for x in wt], autojunk=False)
    times = [None] * len(mine)
    for blk in sm.get_matching_blocks():
        for k in range(blk.size):
            times[blk.a + k] = (wt[blk.b + k][1], wt[blk.b + k][2])
    matched = sum(1 for t in times if t)
    print(f"  aligned {matched}/{len(mine)} tokens directly", flush=True)
    t_first = wt[0][1] if wt else 0.0
    t_last = wt[-1][2] if wt else dur
    idx = [i for i, t in enumerate(times) if t]
    for i in range(len(times)):
        if times[i]: continue
        lo = max([j for j in idx if j < i], default=None)
        hi = min([j for j in idx if j > i], default=None)
        ta = times[lo][1] if lo is not None else t_first
        tb = times[hi][0] if hi is not None else t_last
        la = lo if lo is not None else -1
        hb = hi if hi is not None else len(times)
        f0 = (i - la) / (hb - la); f1 = (i + 1 - la) / (hb - la)
        times[i] = (ta + (tb - ta) * f0 - 0.0, ta + (tb - ta) * f1)
    ph_span, se_span = {}, {}
    for (si, pi), (t0, t1) in zip(where, times):
        a, b = ph_span.get((si, pi), (t0, t1)); ph_span[(si, pi)] = (min(a, t0), max(b, t1))
        a, b = se_span.get(si, (t0, t1)); se_span[si] = (min(a, t0), max(b, t1))
    return se_span, ph_span

def build_spec(src, se_span, ph_span, dur):
    beats, cues = [], []
    starts = [se_span[b["sent"][0]][0] for b in src["beats"]]
    for i, b in enumerate(src["beats"]):
        a = 0.0 if i == 0 else max(0.0, starts[i] - 0.18)
        z = dur if i == len(src["beats"]) - 1 else max(a + 0.4, starts[i + 1] - 0.18)
        beats.append({"a": round(a, 3), "b": round(z, 3), "plate": b.get("plate", 0),
                      "plates": b.get("plates"), "source": b.get("source"),
                      "mv": b.get("mv", {}), "blocks": b["blocks"]})
    for si, ph in enumerate(src["phrases"]):
        for pi, p in enumerate(ph):
            t0, t1 = ph_span[(si, pi)]
            cues.append({"a": round(t0, 3), "b": round(min(max(t1, t0 + 0.6), dur), 3), "t": p})
    # a cue never overlaps the next one
    for k in range(len(cues) - 1):
        cues[k]["b"] = min(cues[k]["b"], cues[k + 1]["a"])
    # no cue shorter than MIN_CUE: borrow time from the following cue (STYLE.md captions)
    MIN_CUE = 0.55
    for k in range(len(cues) - 1):
        short = MIN_CUE - (cues[k]["b"] - cues[k]["a"])
        if short > 0:
            nxt = cues[k + 1]
            room = max(0.0, (nxt["b"] - nxt["a"]) - MIN_CUE)
            shift = min(short, room)
            cues[k]["b"] = round(cues[k]["b"] + shift, 3)
            nxt["a"] = round(nxt["a"] + shift, 3)
    return {"dur": round(dur, 3), "eyebrow": src["eyebrow"], "date": src["date"],
            "source": src["source"], "plates": src["plates"], "beats": beats, "cues": cues}

def main():
    man = json.load(open(os.environ.get("MANIFEST", "manifest.json")))
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
        se, ph = align(f"vo{i}.wav", src, dur)
        spec = build_spec(src, se, ph, dur)
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
