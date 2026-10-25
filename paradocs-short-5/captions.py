#!/usr/bin/env python3
"""Word timings for burned-in captions.

Words are spread evenly inside each SENTENCE, not inside each scene. The
sentence ends are real measured pauses, so drift is reset 16 times across the
video instead of 8 and can never accumulate past one sentence.
"""
import io, re, json, sys

AUDIO_LEN = float(sys.argv[1]); MAJOR = 0.55
paras = [p.strip() for p in io.open('VO-FINAL.txt', encoding='utf-8').read().split('\n\n') if p.strip()]
txt = io.open('pauses.txt', encoding='utf-8').read()
starts = [float(m) for m in re.findall(r'silence_start: ([\d.]+)', txt)]
ends = [float(m) for m in re.findall(r'silence_end: ([\d.]+)', txt)]
allp = [(a, b, b - a) for a, b in zip(starts, ends)]
major = [(a, b) for a, b, d in allp if d >= MAJOR and (a + b) / 2 < AUDIO_LEN - 1.0]

# Sentence spans: speech runs from the end of one major pause to the start of the next.
sent_txt, sent_para = [], []
for pi, p in enumerate(paras):
    for s in re.findall(r'[^.!?]+[.!?]', p):
        sent_txt.append(s.strip()); sent_para.append(pi)
assert len(sent_txt) == len(major) + 1, '%d sentences vs %d pauses' % (len(sent_txt), len(major))

spans, t = [], 0.0
for i in range(len(sent_txt)):
    end = major[i][0] if i < len(major) else AUDIO_LEN
    spans.append((t, end))
    t = major[i][1] if i < len(major) else AUDIO_LEN

words = []
for i, (s, (a, b)) in enumerate(zip(sent_txt, spans)):
    w = s.split()
    step = (b - a) / len(w)
    for j, tok in enumerate(w):
        words.append({'w': tok, 't0': round(a + j * step, 3),
                      't1': round(a + (j + 1) * step, 3), 'p': sent_para[i]})

json.dump({'words': words}, io.open('captions.json', 'w', encoding='utf-8'))
print('%d sentences, %d words timed' % (len(sent_txt), len(words)))
for x in words[:6] + words[-3:]:
    print('  %6.2f-%6.2f  p%d  %s' % (x['t0'], x['t1'], x['p'], x['w']))
