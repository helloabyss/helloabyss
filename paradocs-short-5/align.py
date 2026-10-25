#!/usr/bin/env python3
"""Scene durations from the narration itself, by sentence alignment.

The first attempt allocated by word count and snapped to the nearest pause.
That put the scene-3 cut on a comma, because speaking rate is not uniform and
"nearest pause" cannot tell a comma from a full stop.

This does it structurally instead. The script is 16 sentences in 8 paragraphs,
so the read contains exactly 15 major breaks: 8 sentence-internal and 7 between
paragraphs. Filter silencedetect to the major pauses, require that the count
matches exactly, and the mapping is then 1:1 and ordered -- no estimation at
all. If the counts ever disagree the script stops rather than guessing.
"""
import io, re, json, sys

AUDIO_LEN = float(sys.argv[1])
MAJOR = float(sys.argv[2]) if len(sys.argv) > 2 else 0.55

paras = [p.strip() for p in io.open('VO-FINAL.txt', encoding='utf-8').read().split('\n\n') if p.strip()]
# Sentences per paragraph, by terminal punctuation.
sents = [len(re.findall(r'[.!?](?:\s|$)', p)) for p in paras]
n_breaks = sum(sents) - 1          # every sentence end but the last one
n_para = len(paras) - 1

txt = io.open('pauses.txt', encoding='utf-8').read()
starts = [float(m) for m in re.findall(r'silence_start: ([\d.]+)', txt)]
ends = [float(m) for m in re.findall(r'silence_end: ([\d.]+)', txt)]
allp = [((a + b) / 2.0, b - a) for a, b in zip(starts, ends)]
# Trailing silence is the tail, not a break.
major = [(m, d) for m, d in allp if d >= MAJOR and m < AUDIO_LEN - 1.0]

print('%d paragraphs, %d sentences -> %d expected breaks' % (len(paras), sum(sents), n_breaks))
print('%d pauses detected, %d of them >= %.2fs' % (len(allp), len(major), MAJOR))
if len(major) != n_breaks:
    raise SystemExit('ABORT: %d major pauses for %d sentence breaks. The 1:1 mapping '
                     'does not hold -- retune MAJOR or check the read.' % (len(major), n_breaks))

# Walk the sentence breaks; every time one closes a paragraph, that is a cut.
bounds, k = [], 0
for i, n in enumerate(sents[:-1]):
    k += n                      # index of the break that ends paragraph i
    bounds.append(major[k - 1][0])

assert len(bounds) == n_para, '%d cuts for %d paragraph gaps' % (len(bounds), n_para)
assert bounds == sorted(bounds), 'cuts not monotonic'
cuts = [0.0] + bounds + [AUDIO_LEN]
dur = [round(cuts[i + 1] - cuts[i], 3) for i in range(len(paras))]
assert abs(sum(dur) - AUDIO_LEN) < 0.02, 'durations %.3f != audio %.3f' % (sum(dur), AUDIO_LEN)
assert all(d > 1.5 for d in dur), 'scene too short to read: %s' % dur

json.dump({'durations': dur}, io.open('durations.json', 'w', encoding='utf-8'))
print()
for i, (p, d, c) in enumerate(zip(paras, dur, cuts), 1):
    print('%d  %5.2f s  @%6.2f  %2dw %ds  %.2f s/word  %s'
          % (i, d, c, len(p.split()), sents[i - 1], d / len(p.split()), p[:46]))
print('total %.2f s' % sum(dur))
