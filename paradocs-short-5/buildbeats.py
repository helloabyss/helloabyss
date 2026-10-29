#!/usr/bin/env python3
"""Beat sheet from HeyGen's word-level timestamps.

No estimation anywhere: each VO paragraph's first word gives the cut, straight
off the measured read. STYLE-GUIDE allows no shot past 2.0s, so any beat longer
than 1.8s is split into punch-in sub-shots on the same plate -- a reframe is a
cut, which is how a 39s read still cuts every 1.2-1.8s.
"""
import io, json, math

W = json.load(open('words-aw.json')); DUR = W['duration']; words = W['words']
paras = [p.strip() for p in io.open('VO-FINAL.txt', encoding='utf-8').read().split('\n\n') if p.strip()]

# Walk the words in order, handing each paragraph its own slice.
starts, k = [], 0
for p in paras:
    n = len(p.split())
    assert k < len(words), 'ran out of words at paragraph %r' % p[:30]
    starts.append(words[k]['start'])
    k += n
assert k == len(words), '%d words consumed of %d' % (k, len(words))
starts[0] = 0.0
cuts = starts + [DUR]

# Design table, one row per VO beat, following SHOTLIST.md onto the plates
# actually licensed. plate / sub / hero / count / mid / red / flash / move / trans
D = [
 dict(plate='A',    sub='TERMINAL-BENCH', count=dict(from_=0, to=82, suf='%'), size=300, move='push',   trans='whip',   flash=True),
 dict(plate='B',    sub='ONE AGENT',      hero='PASS',        size=210, move='driftL', trans='whip'),
 dict(plate='D',    sub='REAL WORK',      hero='BERKELEY',    size=150, move='push',   trans='whipUp'),
 dict(plate='BLED', sub='SAME AGENT',     count=dict(from_=82, to=25, suf='%'), size=300, move='pull', red=True, flash=True, trans='whip',
      mid=dict(type='bar', y=1060, a=82, b=25)),
 dict(plate='BLED', sub='NOT A NEW MODEL',hero='SAME',        size=230, move='push',   trans='whip'),
 dict(plate='D',    sub="BERKELEY RDI · SNORKEL AI", hero='LAST EXAM', size=135, move='driftR', trans='whip'),
 dict(plate='D',    sub='REAL TASKS',     count=dict(from_=0, to=1400, pre='', suf='+'), size=210, move='push', trans='whip',
      mid=dict(type='grid', y=950)),
 dict(plate='D',    sub='WORKING PROFESSIONALS', count=dict(from_=0, to=300), size=250, move='driftL', trans='whipUp'),
 dict(plate='I',    sub='THEIR OWN WORK', hero='DELIVERED',   size=150, move='push',   trans='whip'),
 dict(plate='I',    sub='GRADED AGAINST THE HUMAN', hero='GRADED', size=190, move='push', trans='whip',
      note="deterministic · no partial credit"),
 dict(plate='BLED', sub='MATCH IT OR',    hero='FAIL',        size=280, move='pull', red=True, flash=True, trans='whipUp'),
 dict(plate='G',    sub='THE HARDEST TIER', hero='TIER 3',    size=200, move='down',   trans='whip'),
 dict(plate='G',    sub='TOP CONFIGURATIONS', count=dict(from_=0, to=0, suf='.0%'), size=320, move='push', red=True, flash=True, trans='whip',
      note='hardest tier · not the overall score'),
 dict(plate='H',    sub='TOOL EXECUTION', hero='OK',          size=260, move='driftR', trans='whip'),
 dict(plate='I',    sub='WHY THEY FAIL',  hero='75%',         size=250, move='push',   trans='whip',
      mid=dict(type='bar', y=1080, a=75, b=25), note='single-source analysis'),
 dict(plate='I',    sub='MISSING',        hero='DOMAIN',      size=200, move='pull',   trans='whipUp',
      note="it didn't know the job"),
 dict(plate='G',    sub='BUT',            hero='THE OTHER',   size=170, move='up',     trans='whip'),
 dict(plate='A',    sub='JUNE',           count=dict(from_=0, to=24, suf='%'), size=280, move='push', trans='whip'),
 dict(plate='A',    sub='OCTOBER',        count=dict(from_=24, to=59, suf='%'), size=300, move='push', red=True, flash=True, trans='whip',
      note='different boards · not like-for-like'),
 dict(plate='A',    sub='THE GAP IS REAL',hero='CLOSING',     size=200, move='pull',   trans='none'),
]
assert len(D) == len(paras), '%d designs for %d beats' % (len(D), len(paras))

# The hard rule is "no shot past 2s"; 1.2-1.8s is the target. Splitting a 1.9s
# beat in two would make both halves under a second, which is worse than one
# shot inside the limit -- so only beats that actually breach 2.0s get split.
HARD, TARGET = 2.0, 1.8
# Seven plates cover twenty beats, so a plate is reused. Each reuse starts at
# a different in-point, otherwise the same two seconds of footage repeats and
# the viewer notices immediately.
used = {}
beats = []
for i, d in enumerate(D):
    t0, t1 = cuts[i], cuts[i + 1]
    dur = t1 - t0
    n = math.ceil(dur / TARGET) if dur > HARD else 1
    step = dur / n
    for j in range(n):
        b = dict(t0=round(t0 + j * step, 3), t1=round(t0 + (j + 1) * step, 3),
                 plate=d['plate'], heroY=470, heroSize=d['size'],
                 move=d['move'] if j == 0 else ('push' if d['move'] != 'push' else 'pull'),
                 trans=d['trans'] if j == n - 1 else 'whip')
        if 'sub' in d: b['sub'] = d['sub']
        if 'hero' in d: b['hero'] = d['hero']
        if 'note' in d: b['note'] = d['note']
        if d.get('red'): b['red'] = True
        if d.get('flash') and j == 0: b['flash'] = True
        if 'mid' in d: b['mid'] = d['mid']
        k = d['plate']
        b['pt0'] = round((used.get(k, 0) * 1.7) % 4.0, 2)
        used[k] = used.get(k, 0) + 1
        if 'count' in d:
            c = d['count']
            b['count'] = {'from': c['from_'], 'to': c['to'], 'suf': c.get('suf', ''), 'pre': c.get('pre', '')}
        beats.append(b)

# PARADOCS10X carries no financial disclaimer: this video names no ticker,
# values no company and implies no trade. It carries what actually earns trust
# here -- what the figures are and how good they are. See CLAUDE.md.
NOTICE = 'SECONDARY REPORTING \u00b7 SOURCES IN DESCRIPTION'
json.dump({'notice': NOTICE, 'beats': beats}, open('beats.json', 'w'), indent=1)
ds = [b['t1'] - b['t0'] for b in beats]
print('%d VO beats -> %d shots, %.2fs' % (len(D), len(beats), beats[-1]['t1']))
print('shot length %.2f-%.2fs, mean %.2f' % (min(ds), max(ds), sum(ds) / len(ds)))
