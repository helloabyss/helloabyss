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
    a=load(args[0]); dur=len(a)/SR
    # Detect every candidate pause, then SNAP to where each beat boundary is expected
    # from the script's word distribution. Picking the globally longest silences is wrong:
    # a sentence pause inside a beat can exceed a beat gap. (Verified failure, 2026-09-21.)
    win=int(0.02*SR); env=np.array([np.abs(a[i:i+win]).max() for i in range(0,len(a)-win,win)])
    thr=max(env.max()*0.040, 1e-4); quiet=env<thr
    def pauses(minlen):
        out=[];st=None
        for i,q in enumerate(quiet):
            if q and st is None: st=i
            elif not q and st is not None:
                if (i-st)*0.02>=minlen: out.append(((st+i)/2*0.02,(i-st)*0.02))
                st=None
        if st is not None and (len(quiet)-st)*0.02>=minlen:
            out.append(((st+len(quiet))/2*0.02,(len(quiet)-st)*0.02))
        return out
    # sentence-end pauses are longer than comma pauses: sweep the minimum pause
    # length to isolate exactly one pause per sentence break.
    _sp=[len([x for x in re.findall(r"[^.!?]+[.!?]", " ".join(pp.split())) if x.strip()])
         for pp in script]
    _want=sum(_sp)-1
    cands=pauses(0.16)
    for ml in [x/100 for x in range(16,101,2)]:
        c=pauses(ml)
        if len(c)==_want: cands=c; print(f"  pause threshold {ml:.2f}s isolates {len(c)} sentence breaks"); break
        if len(c)<_want: break
    # characters + a per-sentence penalty predicts speech time far better than word count
    # (spelled-out numbers are long to say but few words). Measured 2026-09-21.
    wc=[len(re.sub(r"[^A-Za-z0-9]","",p))+2.2*len(re.findall(r"[.!?]",p)) for p in script]
    tot=sum(wc)
    expect=[dur*sum(wc[:i+1])/tot for i in range(8)]          # expected boundary times
    # BEST PATH: we know the script, so we know how many sentences each beat holds.
    # If pause detection finds exactly one pause per sentence break, the beat
    # boundaries are simply the pauses at the cumulative sentence indices — exact,
    # no duration model involved.
    wc=[len(re.sub(r"[^A-Za-z0-9]","",pp))+2.2*len(re.findall(r"[.!?]",pp)) for pp in script]
    expect=[dur*sum(wc[:i+1])/sum(wc) for i in range(8)]
    sents_per=[len([x for x in re.findall(r"[^.!?]+[.!?]", " ".join(p.split())) if x.strip()])
               for p in script]
    want=sum(sents_per)-1
    idx=[sum(sents_per[:i+1])-1 for i in range(8)]
    # A matching pause count is NOT proof the right pauses were found — a comma pause can
    # stand in for a missed sentence break and the count still matches, which measured
    # WORSE than snapping (3.71s vs 2.11s). So validate against the duration model and
    # only accept when every beat agrees. Verified 2026-09-21.
    ok=False
    if len(cands)==want:
        c2=[cands[i][0] for i in idx]
        d2=[b-a2 for a2,b in zip([0.0]+c2, c2+[dur])]
        pred=[dur*x/sum(wc) for x in wc]
        dev=max(abs(x-y) for x,y in zip(d2,pred))
        if dev<=1.5:
            cuts=c2; ok=True
            print(f"  sentence-index alignment accepted (max deviation {dev:.2f}s)")
        else:
            print(f"  sentence-index alignment rejected (max deviation {dev:.2f}s) — snapping instead")
    if ok:
        bounds=[0]+[int(c*SR) for c in cuts]+[len(a)]
        beats=[a[bounds[i]:bounds[i+1]] for i in range(9)]
        cands=None
    if cands is None: pass
    else:
     used=set(); cuts=[]; prev=0.0
     for e in expect:
        best=None
        for j,(mid,ln) in enumerate(cands):
            if j in used or mid<=prev+0.8: continue
            cost=abs(mid-e)-min(ln,1.2)*0.5
            if best is None or cost<best[0]: best=(cost,j,mid)
        if best is None or abs(best[2]-e)>6.0:
            cuts.append(e); prev=e
        else:
            used.add(best[1]); cuts.append(best[2]); prev=best[2]
     bounds=[0]+[int(c*SR) for c in cuts]+[len(a)]
     beats=[a[bounds[i]:bounds[i+1]] for i in range(9)]
     print(f"  WARNING approximate: {len(cands)} pauses found, expected {want}. "
           "Captions may drift ~2-3s. Supply 9 per-beat files for exact sync.")
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
