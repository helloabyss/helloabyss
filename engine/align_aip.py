# -*- coding: utf-8 -*-
"""Align the picture to the narration.

The first cut distributed beat durations by *weight* -- turn cards 0.42, everything
else 1.0 -- scaled to the measured voiceover length. Every ordinary beat therefore ran
exactly 13.1s whether its narration took eight seconds or twenty, and the picture drifted
against the words. That is the defect this file fixes.

There is no ASR here: huggingface.co is egress-blocked, so no Whisper weights. But the
script text is known exactly and Aaron reads at a near-constant 158.7 wpm, so word
position is a good clock. Each beat declares which script paragraphs it illustrates;
duration follows from word count, and every boundary is then snapped to a real pause
detected in the audio so cuts land between sentences rather than mid-word.

    python3 align_aip.py      # writes aip-durations.json
"""
import io, json, re

VO_TXT   = '../ai-picks-longform/vo.txt'
PAUSES   = 'pauses.json'       # midpoints from: silencedetect=noise=-30dB:d=0.28
SPEECH   = 529.40              # measured length of vo-full.mp3 / vo-master.wav
OUTRO    = 6.0                 # closing card holds past the last word
SNAP_WIN = 1.60                # snap a boundary to a pause within this many seconds
MIN_BEAT = 3.0                 # never cut faster than this

# Which script paragraph(s) each beat illustrates. Beats sharing a paragraph split it by
# word count. This list is the contract between the script and the picture -- if a beat is
# added, reordered or removed, its entry moves with it. Indices must be non-decreasing:
# the picture cannot illustrate a paragraph the narration has not reached.
SRC = [
    [0], [0],              # 0-1   the hook: burned $14bn / worth $2 trillion
    [1], [1],              # 2-3   both numbers, same filing
    [2],                   # 4     Micron margin doubled
    [3], [4], [5],         # 5-7   three companies / three numbers / the bull case then the line
    [6], [6],              # 8-9   SPCX listing, valuation at the close
    [7], [7], [7],         # 10-12 rocket company / the filing disagrees / revenue split
    [8], [8],              # 13-14 reusability, the jet left in Paris
    [9], [9],              # 15-16 subscriber series, Starlink operating income
    [10, 11],              # 17    TURN CARD, SPCX
    [12], [12],            # 18-19 subs up vs ARPU down, then ARPU $99 -> $66
    [13],                  # 20    the cash bridge
    [14], [14],            # 21-22 satellites are replaced / a subscription it pays
    [15],                  # 23    BE joins the S&P 500
    [16], [16],            # 24-25 the grid queue / Bloom sells the box
    [17], [17],            # 26-27 quarterly revenue / guidance raised
    [18, 19],              # 28    TURN CARD, BE
    [20],                  # 29    the backlog
    [21], [21],            # 30-31 not a bank balance / intent, cancellable
    [22],                  # 32    MU card
    [23], [23],            # 33-34 FY25 vs FY26 revenue, then +256%
    [24],                  # 35    net income, EPS, margin
    [25], [25],            # 36-37 high-bandwidth memory
    [26, 27],              # 38    TURN CARD, MU
    [28], [28],            # 39-40 the dial, then net margin (calculated)
    [29],                  # 41    the comparison that should make you careful
    [30], [30],            # 42-43 Nvidia quarter vs Micron year, then both full years
    [31], [31],            # 44-45 out-earning the chips / everyone is adding capacity
    [32], [32], [32],      # 46-48 memory is cyclical / not a new normal / top of a cycle
    [33],                  # 49    next-quarter guidance
    [34],                  # 50    deficit, clause, cycle
    [35], [35],            # 51-52 not bad businesses / same document, one side told
    [36], [36], [36],      # 53-55 counterweights are filed / ten minutes / go and look
    [37],                  # 56    if it is not there
]                          # 57    outro card -- holds OUTRO seconds past the last word


def paragraphs():
    t = io.open(VO_TXT, encoding='utf-8').read()
    return [p.strip() for p in re.split(r'\n\s*\n', t) if p.strip()]


def build():
    paras = paragraphs()
    words = [len(p.split()) for p in paras]
    total_words = sum(words)

    covered = sorted({i for s in SRC for i in s})
    if covered != list(range(len(paras))):
        missing = set(range(len(paras))) - set(covered)
        raise SystemExit('script paragraphs not covered by any beat: %s' % sorted(missing))
    flat = [i for s in SRC for i in s]
    if flat != sorted(flat):
        raise SystemExit('SRC is not monotonic -- the picture would run ahead of the words')

    # how many beats share each paragraph, so a shared one splits by word count
    share = {}
    for s in SRC:
        for i in s:
            share[i] = share.get(i, 0) + 1

    # cumulative word position at the END of each beat
    cum, acc = [], 0.0
    for s in SRC:
        for i in s:
            acc += words[i] / float(share[i])
        cum.append(acc)

    pauses = json.load(open(PAUSES))

    def snap(t):
        near = [p for p in pauses if abs(p - t) <= SNAP_WIN]
        return min(near, key=lambda p: abs(p - t)) if near else t

    # word position -> time, then snap to a real pause
    bounds, prev = [], 0.0
    for k, c in enumerate(cum):
        raw = SPEECH * c / total_words
        t = SPEECH if k == len(cum) - 1 else snap(raw)
        if t - prev < MIN_BEAT:
            t = prev + MIN_BEAT
        bounds.append(t)
        prev = t

    durs = [bounds[0]] + [bounds[i] - bounds[i-1] for i in range(1, len(bounds))]
    durs.append(OUTRO)                      # beat 41, the closing card
    json.dump({'durations': [round(d, 3) for d in durs],
               'total': round(sum(durs), 3),
               'speech': SPEECH, 'outro': OUTRO,
               'method': 'word-position alignment, snapped to silencedetect pauses'},
              open('aip-durations.json', 'w'), indent=1)
    return durs, bounds, cum, total_words


if __name__ == '__main__':
    durs, bounds, cum, tw = build()
    print('%d beats  total %.2fs  (speech %.2f + outro %.1f)' % (len(durs), sum(durs), SPEECH, OUTRO))
    print('shortest %.1fs   longest %.1fs   (was a flat 13.1s for every non-turn beat)'
          % (min(durs), max(durs)))
    for i, (d, b) in enumerate(zip(durs, bounds + [None])):
        if b is None: break
        print('  beat %2d  %5.1fs  ends %3d:%04.1f  paras %s'
              % (i, d, int(b // 60), b % 60, SRC[i]))
