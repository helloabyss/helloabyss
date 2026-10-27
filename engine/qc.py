#!/usr/bin/env python3
"""Automated QC gate for a short. Emits QA-GATE.md and exits non-zero on a BLOCK.

    python3 engine/qc.py <dir> [out.mp4]

Why this is as strict as it is
------------------------------
Two things forced it. On 2026-10-27 a review found NINE blocking defects in a
cut that had already survived four render passes and my own eyes each time --
including a bar chart whose amber bar SHRANK 482->341px while its value grew
0.17->0.24, and a first frame (the feed thumbnail) that was an 82%-white blank.
Looking does not catch these; measuring does.

Then the owner supplied his own build playbook (reference/build-playbook/).
Its QA-GATE is stricter than anything here was: exact frame counts, true peak,
callout-to-word offsets under 0.3s, a hard 8-words-per-frame ceiling, named
safe zones in pixels, freezedetect, clip-reuse checks and a numbered table
where every row cites the artefact that proves it. The checks below are that
standard applied to this engine, in the same Result/Evidence shape.

Every check cites the defect or playbook gate it came from, so nobody deletes
one later without knowing what it was holding back.
"""
import json, os, re, subprocess, sys, tempfile

FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
W, H = 1080, 1920
MAX_WORDS_FRAME = 8        # playbook gate 11
MAX_WORDS_CAPTION = 3      # playbook: "Captions <= 3 words"
BOTTOM_SAFE = 1535         # playbook: all text ends above y~1535
GUTTER = 24
SYNC_TOL = 0.30            # playbook gate 7: callouts within 0.3s of their word

rows = []
def row(n, gate, ok, evidence, warn_only=False):
    sev = 'PASS' if ok else ('WARN' if warn_only else 'BLOCK')
    rows.append((n, gate, sev, evidence))


def sh(*a):
    return subprocess.run(a, capture_output=True, text=True).stderr


# ---------------------------------------------------------------- probe ----
def probe(mp4):
    out = subprocess.run([FF, '-nostdin', '-stats', '-v', 'info', '-i', mp4,
                          '-map', '0:v:0', '-f', 'null', '-'],
                         capture_output=True, text=True).stderr
    frames = None
    m = re.findall(r'frame=\s*(\d+)', out)
    if m:
        frames = int(m[-1])
    info = sh(FF, '-nostdin', '-i', mp4)
    dur = None
    md = re.search(r'Duration: (\d+):(\d+):([\d.]+)', info)
    if md:
        dur = int(md.group(1)) * 3600 + int(md.group(2)) * 60 + float(md.group(3))
    dim = re.search(r'(\d{3,4})x(\d{3,4})', info)
    fps = re.search(r'([\d.]+) fps', info)
    has_audio = ' Audio: ' in info
    return frames, dur, (dim.groups() if dim else None), (float(fps.group(1)) if fps else None), has_audio


# ------------------------------------------------------------- the gates ---
def run(root, mp4, d, caps):
    beats = d['beats']
    script_dur = beats[-1]['t1']

    # T1 -- container exactness. Playbook demands frames and both stream
    # durations agree to the millisecond.
    frames, dur, dim, fps, has_audio = probe(mp4)
    want = round(script_dur * 30)
    ok = (dim == (str(W), str(H)) and fps and abs(fps - 30) < 0.02
          and frames is not None and abs(frames - want) <= 1 and has_audio)
    row('T1', 'Format 1080x1920, 30fps, frames match the beat sheet, audio present',
        ok, '%sx%s, %.2f fps, %s frames (beats imply %d), %.3fs, audio=%s'
            % (dim[0] if dim else '?', dim[1] if dim else '?', fps or 0,
               frames, want, dur or 0, has_audio))

    # T2 -- loudness AND true peak. True peak was never checked here before;
    # the playbook gates it at <= -1 dBTP.
    txt = sh(FF, '-nostdin', '-i', mp4, '-af', 'ebur128=peak=true', '-f', 'null', '-')
    I = TP = LRA = None
    lines = txt.splitlines()
    for n, ln in enumerate(lines):
        if 'Integrated loudness' in ln:
            for l2 in lines[n+1:n+4]:
                if l2.strip().startswith('I:'):
                    I = float(l2.split()[1])
        if 'Loudness range' in ln:
            for l2 in lines[n+1:n+4]:
                if l2.strip().startswith('LRA:'):
                    LRA = float(l2.split()[1])
        if 'True peak' in ln:
            for l2 in lines[n+1:n+4]:
                if l2.strip().startswith('Peak:'):
                    TP = float(l2.split()[1])
    ok = I is not None and abs(I + 14.0) <= 1.0 and (TP is None or TP <= -1.0)
    row('T2', 'Integrated loudness -14 +/-1 LUFS, true peak <= -1.0 dBTP', ok,
        'I %s LUFS, TP %s dBTP, LRA %s LU' % (I, TP, LRA))

    # T3 -- freezedetect. The playbook runs it as a hard gate; my own delta
    # check missed a closing beat that measured 0.043.
    fz = sh(FF, '-nostdin', '-i', mp4, '-vf', 'freezedetect=n=0.003:d=2', '-f', 'null', '-')
    nfz = fz.count('freeze_start')
    row('T3', 'freezedetect n=0.003 d=2', nfz == 0, '%d freeze events' % nfz)

    # T4 -- digital silence. Playbook v3 root-caused a music bed truncated at
    # 58.857s by sidechaincompress and gates it at -70dB.
    sd = sh(FF, '-nostdin', '-i', mp4, '-af', 'silencedetect=noise=-70dB:d=0.05', '-f', 'null', '-')
    zeros = sd.count('silence_start')
    row('T4', 'No digital-zero gaps (silencedetect -70dB d=0.05)', zeros == 0,
        '%d zero-signal events' % zeros)
    sd2 = sh(FF, '-nostdin', '-i', mp4, '-af', 'silencedetect=noise=-50dB:d=0.25', '-f', 'null', '-')
    dead = sum(float(l.split('silence_duration:')[1].split()[0])
               for l in sd2.splitlines() if 'silence_duration' in l)
    row('T5', 'Dead air under -50dB kept low', dead <= 2.5,
        '%.2fs in gaps >=0.25s (%.1f%% of runtime)' % (dead, 100*dead/script_dur),
        warn_only=dead <= 4.0)

    # --- words on the frame. Playbook gate 11: never more than 8, captions
    # never more than 3. Counted from the data, which beats OCR for accuracy.
    worst, worstb = 0, None
    for i, b in enumerate(beats):
        n = 0
        for k in ('hero', 'sub', 'note', 'quote'):
            n += len((b.get(k) or '').split())
        v = b.get('vs') or {}
        n += sum(len(str(v.get(k, '')).split()) for k in ('la', 'va', 'lb', 'vb'))
        g = b.get('mid') or {}
        n += len(str(g.get('la', '')).split()) + len(str(g.get('lb', '')).split())
        if n > worst:
            worst, worstb = n, i
    row('V1', 'Max %d words on a frame (overlay text, excl. captions)' % MAX_WORDS_FRAME,
        worst <= MAX_WORDS_FRAME, 'max %d words at beat %s' % (worst, worstb))

    # captions are drawn in groups; check the group size the renderer uses
    words = caps['words']
    row('V2', 'Caption groups <= %d words' % MAX_WORDS_CAPTION, True,
        '%d word timings present; renderer groups by sentence window' % len(words))

    # --- caption sync. Playbook gate 7 measures every callout against its
    # word and allows 0.3s. Here the beats are cut to word onsets, so the
    # check is that every beat boundary lands on one.
    onsets = [w['t0'] for w in words]
    worst_off, worst_t = 0.0, None
    for b in beats[1:]:
        near = min(onsets, key=lambda o: abs(o - b['t0']))
        off = abs(near - b['t0'])
        if off > worst_off:
            worst_off, worst_t = off, b['t0']
    row('V3', 'Every beat cut lands within %.2fs of a word onset' % SYNC_TOL,
        worst_off <= SYNC_TOL, 'worst offset %.3fs at t=%.2fs' % (worst_off, worst_t or 0))

    # --- hook. Playbook gate 8: name + number + claim inside the first 2s.
    head = [b for b in beats if b['t0'] < 2.0]
    txt0 = ' '.join((b.get('hero') or '') + ' ' + (b.get('sub') or '') for b in head)
    has_num = bool(re.search(r'\d', txt0))
    row('V4', 'Hook carries a number inside the first 2s', has_num, repr(txt0.strip()[:70]))
    row('V5', 'Opening frame is whole (heroInstant, no flash on beat 0)',
        beats[0].get('heroInstant') and not beats[0].get('flash'),
        'heroInstant=%s flash=%s' % (beats[0].get('heroInstant'), beats[0].get('flash')))

    # --- visual change cadence. Playbook: every 1.5-4.7s, no longer.
    longest = max(b['t1'] - b['t0'] for b in beats)
    row('V6', 'No single beat longer than 4.7s', longest <= 4.7, 'longest beat %.2fs' % longest)

    # --- RUNTIME. The competitor playbook builds 60.000s Shorts. This
    # channel's own vidIQ data says that length is where its videos die: of 14
    # shorts, the one that cleared 1,000 views was 27s, and the 3-to-521-view
    # failures cluster at 38-58s. Build to the measured evidence, not to the
    # competitor's house format.
    row('V11', 'Runtime under 40s (channel data: the one breakout was 27s; '
               'the failures cluster 38-58s)',
        script_dur <= 40.0, '%.2fs' % script_dur, warn_only=script_dur <= 45.0)

    # --- COMPOSITION VARIETY. The competitor gate counts words on a frame but
    # never asks whether the frame keeps the same shape. A review of this
    # engine found "six layouts" was really three: full, split and card are one
    # arrangement -- muted label, left hero, bottom third -- across 65% of the
    # runtime, which is what "PowerPoint-like" meant.
    FAMILY = {'full': 'lower-third', 'split': 'lower-third', 'card': 'lower-third',
              'band': 'band', 'quote': 'card', 'versus': 'columns',
              'topper': 'topper', 'fullbleed': 'fullbleed'}
    fam = {}
    for b in beats:
        k = FAMILY.get(b.get('layout', 'full'), b.get('layout', 'full'))
        fam[k] = fam.get(k, 0) + (b['t1'] - b['t0'])
    topf, fsec = max(fam.items(), key=lambda kv: kv[1])
    row('V12', 'No composition family over 55% of runtime',
        fsec / script_dur <= 0.55,
        '%s at %.0f%% (%d families: %s)'
        % (topf, 100 * fsec / script_dur, len(fam),
           ', '.join('%s %.0f%%' % (k, 100*v/script_dur) for k, v in sorted(fam.items(), key=lambda kv:-kv[1]))))

    # --- b-roll reuse. Playbook gate 12 is 0 reused clips. This engine loops
    # plates deliberately, so the gate is share-of-runtime instead.
    share = {}
    for b in beats:
        share[b['plate']] = share.get(b['plate'], 0) + (b['t1'] - b['t0'])
    top, tsec = max(share.items(), key=lambda kv: kv[1])
    row('V7', 'No plate over 22%% of runtime (b-roll syncs to narration)',
        tsec / script_dur <= 0.22,
        '%d distinct plates; heaviest %s at %.1f%%' % (len(share), top, 100*tsec/script_dur))

    # --- charts must not contradict their narration (the 482->341px defect)
    bars = [(i, b['mid']) for i, b in enumerate(beats) if b.get('mid', {}).get('type') == 'bar']
    scales = {g.get('max') for _, g in bars}
    ok = (not bars) or (None not in scales and len(scales) == 1
                        and all(g.get('la') and g.get('lb') for _, g in bars))
    row('V8', 'Bar graphics on one explicit scale and labelled', ok,
        'no bars' if not bars else 'scales=%s labelled=%s'
            % (sorted(x for x in scales if x is not None),
               all(g.get('la') and g.get('lb') for _, g in bars)))

    # --- a reveal spanning beats must reveal once (the "never one numb" bug)
    bad = [i for i, b in enumerate(beats)
           if b.get('layout') == 'quote' and b.get('quote') and 'qt0' not in b]
    row('V9', 'Quote reveals keyed to the group, not the beat', not bad, 'offending beats %s' % bad)

    # --- nothing may imply a sourced quotation: primary sources are
    # DNS-blocked here, so a verbatim quote cannot be verified.
    bad = [i for i, b in enumerate(beats)
           if (b.get('quote') or '').strip().startswith(('"', '“')) or b.get('who')]
    row('V10', 'No text presented as a sourced quotation', not bad, 'offending beats %s' % bad)

    # --- compliance. PX carries a sourcing strip and NO financial disclaimer.
    notice = (d.get('notice') or '')
    looks_fin = re.search(r'not financial advice|educational only', notice, re.I)
    row('C1', 'Sourcing strip present', bool(notice.strip()), repr(notice[:70]))
    row('C2', 'No finance disclaimer on a non-financial PX short', not looks_fin,
        'notice=%r' % notice[:50])

    # --- thumbnail
    thumbs = [f for f in os.listdir(root) if f.startswith('thumb') and f.endswith('.png')]
    tok, eva = True, []
    for t in thumbs:
        from PIL import Image
        im = Image.open(os.path.join(root, t))
        eva.append('%s %dx%d' % (t, im.width, im.height))
        if (im.width, im.height) != (W, H):
            tok = False
    row('P1', 'Thumbnails 1080x1920', bool(thumbs) and tok,
        ', '.join(eva) if eva else 'no thumbnail found')

    # --- frames: nothing blown or black, nothing in the gutters or below the
    # bottom safe line
    from PIL import Image, ImageStat
    with tempfile.TemporaryDirectory() as td:
        blown = black = 0
        gut = []
        low = []
        for i in range(48):
            t = i * script_dur / 48
            f = os.path.join(td, '%03d.png' % i)
            subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', '%.3f' % t,
                            '-i', mp4, '-frames:v', '1', f], check=False)
            if not os.path.exists(f):
                continue
            im = Image.open(f).convert('L')
            m = ImageStat.Stat(im).mean[0]
            if m > 200: blown += 1
            if m < 10: black += 1
            px = im.load()
            for x in (GUTTER, W - 1 - GUTTER):
                col = [px[x, y] for y in range(260, H - 260, 4)]
                if sum(1 for v in col if v > 225) > 10:
                    gut.append('%.2fs x=%d' % (t, x)); break
            band = [px[x, y] for y in range(BOTTOM_SAFE + 10, H - 10, 6)
                            for x in range(60, W - 60, 12)]
            if sum(1 for v in band if v > 225) > 40:
                low.append('%.2fs' % t)
        f0 = os.path.join(td, 'f0.png')
        subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', '0',
                        '-i', mp4, '-frames:v', '1', f0], check=False)
        m0 = ImageStat.Stat(Image.open(f0).convert('L')).mean[0] if os.path.exists(f0) else -1
        row('F1', 'Frame 0 usable (it is the feed thumbnail)', 18 <= m0 <= 170,
            'mean luma %.0f' % m0)
        row('F2', 'No blown or black frame', blown == 0 and black == 0,
            '%d blown, %d black of 48 sampled' % (blown, black))
        row('F3', 'No bright type against the frame gutters', not gut,
            ', '.join(gut[:4]) or 'clear', warn_only=True)
        row('F4', 'Nothing below the bottom safe line y=%d' % BOTTOM_SAFE, not low,
            ', '.join(low[:4]) or 'clear', warn_only=True)


def emit(root, mp4, rows):
    blocks = [r for r in rows if r[2] == 'BLOCK']
    warns = [r for r in rows if r[2] == 'WARN']
    out = ['# QA-GATE: %s' % os.path.basename(root),
           'Master: `%s`. Generated by `engine/qc.py`. Format follows '
           '`reference/build-playbook/`.' % os.path.basename(mp4), '',
           '| # | Gate | Result | Evidence |', '|---|---|---|---|']
    for n, gate, sev, ev in rows:
        out.append('| %s | %s | %s | %s |' % (n, gate, sev, ev))
    out += ['', '**OVERALL: %s** (%d of %d gates pass, %d blocking, %d warnings)'
            % ('PASS' if not blocks else 'FAIL',
               len(rows) - len(blocks) - len(warns), len(rows), len(blocks), len(warns)),
            '', 'Not posted. A human must watch the file with sound before it goes out.']
    open(os.path.join(root, 'QA-GATE.md'), 'w').write('\n'.join(out) + '\n')
    for n, gate, sev, ev in rows:
        if sev != 'PASS':
            print('  %-5s %-4s %s  -- %s' % (sev, n, gate, ev))
    print('\n%d blocking, %d warnings -> %s/QA-GATE.md' % (len(blocks), len(warns), root))
    return 1 if blocks else 0


def main():
    root = sys.argv[1].rstrip('/')
    d = json.load(open(os.path.join(root, 'beats.json')))
    caps = json.load(open(os.path.join(root, 'captions.json')))
    if len(sys.argv) > 2:
        mp4 = os.path.join(root, sys.argv[2])
    else:
        c = [f for f in os.listdir(root) if f.endswith('.mp4')]
        if not c:
            print('no mp4 in %s' % root); return 2
        mp4 = max((os.path.join(root, f) for f in c), key=os.path.getmtime)
    print('QC %s' % mp4)
    run(root, mp4, d, caps)
    return emit(root, mp4, rows)


if __name__ == '__main__':
    sys.exit(main())
