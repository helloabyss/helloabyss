#!/usr/bin/env python3
"""Word timings for any narration file, keyed to the script's own words.

    python3 align.py vo.wav script.txt words.json
Runs faster-whisper (word timestamps) on the audio, matches its words to the script's
whitespace tokens with difflib, and interpolates any unmatched token between its matched
neighbours. Output has one entry per script token, so phrase cues in scenes.js resolve.
Use this when the voice provider gives no timestamps or the audio was edited/concatenated."""
import json, re, sys, difflib
from faster_whisper import WhisperModel
wav, script, out = sys.argv[1:4]
txt = re.sub(r'^##.*$', '', open(script).read(), flags=re.M)
toks = txt.split()
norm = lambda s: re.sub(r"[^a-z0-9]", "", s.lower())
model = WhisperModel("base.en", device="cpu", compute_type="int8")
segs, info = model.transcribe(wav, word_timestamps=True, vad_filter=False)
ww = [w for s in segs for w in s.words]
# split whisper hyphen/number tokens the same way as the script's (rough), then match on normalized text
A = [norm(t) for t in toks]; B = [norm(w.word) for w in ww]
sm = difflib.SequenceMatcher(a=A, b=B, autojunk=False)
st = [None]*len(toks); en = [None]*len(toks)
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        st[blk.a+k] = ww[blk.b+k].start; en[blk.a+k] = ww[blk.b+k].end
# interpolate gaps
i = 0; dur = info.duration
while i < len(toks):
    if st[i] is None:
        j = i
        while j < len(toks) and st[j] is None: j += 1
        t0 = en[i-1] if i > 0 else 0.0
        t1 = st[j] if j < len(toks) else dur
        n = j - i
        for k in range(n):
            st[i+k] = t0 + (t1-t0)*k/n; en[i+k] = t0 + (t1-t0)*(k+1)/n
        i = j
    else: i += 1
matched = sum(1 for blk in sm.get_matching_blocks() for _ in range(blk.size))
json.dump(dict(dur=round(dur,3), words=[dict(w=t, s=round(s,3), e=round(e,3)) for t,s,e in zip(toks,st,en)]), open(out,'w'))
print(f"{len(toks)} script words, {matched} matched to whisper ({matched/len(toks):.0%}), {dur:.1f}s")
