#!/usr/bin/env python3
"""Align a supplied Alex Wright VO stem to the 9 script beats, then rebuild timings.
Usage: python3 align_stem.py <stem.wav|mp3>            # one continuous file (silence-split)
       python3 align_stem.py beat1.wav ... beat9.wav   # nine files, one per beat (exact)
Writes vo.wav + vo_timing.json, then gen.py re-emits index.html."""
import sys, json, subprocess, numpy as np, soundfile as sf, re, os

SR=24000; GAP_P=0.55
script=[p.strip() for p in open("../../scripts/2026-09-20-vo.txt").read().split("\n\n") if p.strip()]

def load(p):
    w=p if p.lower().endswith(".wav") else "/tmp/_c.wav"
    if w!=p: subprocess.run(["ffmpeg","-v","error","-i",p,"-ar",str(SR),"-ac","1","-y",w],check=True)
    a,sr=sf.read(w)
    if a.ndim>1: a=a[:,0]
    if sr!=SR:
        subprocess.run(["ffmpeg","-v","error","-i",w,"-ar",str(SR),"-ac","1","-y","/tmp/_r.wav"],check=True)
        a,sr=sf.read("/tmp/_r.wav")
    return a.astype(np.float32)

args=sys.argv[1:]
if len(args)==9:
    beats=[load(a) for a in args]
elif len(args)==1:
    a=load(args[0])
    # split on the 8 longest silences -> 9 beats
    win=int(0.02*SR); env=np.array([np.abs(a[i:i+win]).max() for i in range(0,len(a)-win,win)])
    thr=max(env.max()*0.035, 1e-4); quiet=env<thr
    runs=[];s=None
    for i,q in enumerate(quiet):
        if q and s is None: s=i
        elif not q and s is not None:
            if (i-s)*0.02>0.22: runs.append(((i-s)*0.02, s, i))
            s=None
    runs.sort(reverse=True); cuts=sorted([int((r[1]+r[2])/2*win) for r in runs[:8]])
    if len(cuts)!=8: sys.exit(f"found {len(cuts)} pauses, need 8 — supply 9 files instead")
    bounds=[0]+cuts+[len(a)]; beats=[a[bounds[i]:bounds[i+1]] for i in range(9)]
else:
    sys.exit(__doc__)

out=[];t=0.0;scenes=[];words=[]
for i,(b,p) in enumerate(zip(beats,script)):
    d=len(b)/SR; s0=t
    flat=" ".join(p.split())
    sents=[s.strip() for s in re.findall(r'[^.!?]+[.!?]',flat) if s.strip()]
    tot_c=sum(len(s) for s in sents); acc=0
    for s in sents:  # split the beat across sentences by character weight
        s_d=d*len(s)/tot_c; s_t=t+d*acc/tot_c; acc+=len(s)
        ws=s.split(); tc=sum(len(w)+1 for w in ws); a2=0
        for w in ws:
            w0=s_t+(a2/tc)*s_d; a2+=len(w)+1
            words.append({"w":w,"s":round(w0,3),"e":round(s_t+(a2/tc)*s_d,3)})
    out.append(b); t+=d
    scenes.append({"i":i,"start":round(s0,3),"end":round(t,3),"dur":round(d,3)})
    if i<8: out.append(np.zeros(int(GAP_P*SR),dtype=np.float32)); t+=GAP_P

full=np.concatenate(out); sf.write("vo.wav",full,SR)
json.dump({"total":round(len(full)/SR,3),"scenes":scenes,"words":words},open("vo_timing.json","w"),indent=1)
print(f"aligned {len(full)/SR:.2f}s across 9 beats -> vo.wav + vo_timing.json")
