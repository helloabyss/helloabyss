import re, json, numpy as np, soundfile as sf
from kokoro_onnx import Kokoro

M="/root/.cache/hyperframes/tts/models/kokoro-v1.0.onnx"
V="/root/.cache/hyperframes/tts/voices/voices-v1.0.bin"
k=Kokoro(M,V)
VOICE="am_michael"; SR=24000
GAP_S=0.10   # between sentences inside a beat
GAP_P=0.55   # between beats (scene seam)

paras=[p.strip() for p in open("../../scripts/2026-09-20-vo.txt").read().split("\n\n") if p.strip()]
assert len(paras)==9, len(paras)

audio=[]; t=0.0; scenes=[]; words=[]
for pi,p in enumerate(paras):
    flat=" ".join(p.split())
    sents=[s.strip() for s in re.findall(r'[^.!?]+[.!?]', flat) if s.strip()]
    s_start=t
    for si,s in enumerate(sents):
        samples,_=k.create(s, voice=VOICE, speed=1.0, lang="en-us")
        d=len(samples)/SR
        # word timings: distribute across the sentence by character weight
        ws=s.split(); tot=sum(len(w)+1 for w in ws); acc=0
        for w in ws:
            w0=t+(acc/tot)*d; acc+=len(w)+1; w1=t+(acc/tot)*d
            words.append({"w":w,"s":round(w0,3),"e":round(w1,3)})
        audio.append(samples); t+=d
        gap=GAP_S if si<len(sents)-1 else 0.0
        if gap: audio.append(np.zeros(int(gap*SR),dtype=samples.dtype)); t+=gap
    scenes.append({"i":pi,"start":round(s_start,3),"end":round(t,3),"dur":round(t-s_start,3)})
    if pi<len(paras)-1:
        audio.append(np.zeros(int(GAP_P*SR),dtype=audio[-1].dtype)); t+=GAP_P

full=np.concatenate(audio)
sf.write("vo.wav", full, SR)
json.dump({"total":round(len(full)/SR,3),"scenes":scenes,"words":words}, open("vo_timing.json","w"), indent=1)
print(f"TOTAL {len(full)/SR:.3f}s  ({len(words)} words)")
for s in scenes: print(f"  scene {s['i']+1}: {s['start']:7.3f} -> {s['end']:7.3f}  ({s['dur']:6.3f}s)")
