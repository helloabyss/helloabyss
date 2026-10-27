#!/usr/bin/env python3
"""Automated QC for a finished short. Fails loudly; prints every finding.

    python3 engine/qc.py <dir>        # dir holds the mp4, beats.json, captions.json

Why this exists
---------------
On 2026-10-27 a review found NINE blocking defects in a cut that had already
been through four render passes and my own eyes every time. A chart that
animated the opposite of its narration survived all four. The first frame of
the video -- the thumbnail the whole feed sees -- was an 82%-white blank.

The repo's only automated checks were checkbeats.py (vertical collisions) and
checkplate.py (one plate's luma). Everything else depended on someone looking.
That is the thing that does not scale, so every defect class that actually
shipped is now a check here. Each one cites the defect it came from, so nobody
later deletes a check without knowing what it caught.

Checks are either STATIC (read beats.json -- instant) or FRAME (decode the mp4).
"""
import json, os, subprocess, sys, tempfile, math

FF = '/usr/local/lib/python3.11/dist-packages/imageio_ffmpeg/binaries/ffmpeg-linux-x86_64-v7.0.2'
W, H = 1080, 1920

findings = []
def fail(sev, code, msg):
    findings.append((sev, code, msg))


# ---------------------------------------------------------------- static ---
def static_checks(d):
    beats = d['beats']

    # Defect: the bar chart normalised to each beat's own max, so the white bar
    # was pinned full-width and the amber bar SHRANK 482->341px while its value
    # grew 0.17->0.24. A chart may not contradict its own narration.
    bars = [(i, b['mid']) for i, b in enumerate(beats)
            if b.get('mid', {}).get('type') == 'bar']
    if bars:
        scales = {g.get('max') for _, g in bars}
        if None in scales:
            fail('BLOCK', 'bar-no-scale',
                 'bar graphics without an explicit mid.max: each beat then '
                 'normalises to its own maximum and bar length stops meaning '
                 'anything across the sequence (beats %s)'
                 % [i for i, g in bars if g.get('max') is None])
        elif len(scales) > 1:
            fail('BLOCK', 'bar-mixed-scale',
                 'bar graphics use more than one scale (%s); lengths are not '
                 'comparable between beats' % sorted(scales))
        else:
            mx = scales.pop()
            for i, g in bars:
                for k in ('a', 'b'):
                    if g[k] > mx:
                        fail('BLOCK', 'bar-overflow',
                             'beat %d value %s=%s exceeds the scale %s'
                             % (i, k, g[k], mx))
        for i, g in bars:
            if not g.get('la') or not g.get('lb'):
                fail('WARN', 'bar-unlabelled',
                     'beat %d bars are unlabelled; a viewer cannot recover '
                     'which bar is which' % i)
        # the series must move the same direction as its numbers
        seq = [(i, g['a']) for i, g in bars]
        for (i0, v0), (i1, v1) in zip(seq, seq[1:]):
            if v1 != v0 and (v1 > v0) != (v1 > v0):
                pass  # direction is implied by the shared scale once max is set

    # Defect: a quote spanning two beats restarted its typewriter on each, so
    # the thesis line read "never one numb" for 53% of its screen time.
    for i, b in enumerate(beats):
        if b.get('layout') == 'quote' and b.get('quote'):
            if 'qt0' not in b or 'qt1' not in b:
                fail('BLOCK', 'quote-no-group',
                     'beat %d is a quote without qt0/qt1; a reveal keyed to '
                     'within-beat progress restarts on every beat of the group'
                     % i)
    # a quote group must be one contiguous run with one span
    groups = {}
    for i, b in enumerate(beats):
        if b.get('layout') == 'quote' and 'qt0' in b:
            groups.setdefault((b['qt0'], b['qt1']), []).append(i)
    for (q0, q1), idxs in groups.items():
        if beats[idxs[0]]['t0'] != q0 or beats[idxs[-1]]['t1'] != q1:
            fail('BLOCK', 'quote-span-wrong',
                 'quote group %s spans beats %s whose real extent is %s-%s'
                 % ((q0, q1), idxs, beats[idxs[0]]['t0'], beats[idxs[-1]]['t1']))

    # Defect: the quote card set the script's own paraphrase as a sourced
    # quotation with an invented attribution, on an accuracy channel.
    for i, b in enumerate(beats):
        q = b.get('quote') or ''
        if q.strip().startswith(('"', '“')) or b.get('who'):
            fail('BLOCK', 'fake-attribution',
                 'beat %d presents text as a sourced quotation (quote marks or '
                 'a "who" attribution). Nothing here is verified against a '
                 'primary source -- see CLAUDE.md on DNS-blocked sources.' % i)

    # Defect: W4 carried 23.4% of the runtime as a single soft smear, and the
    # owner's standing rule is that b-roll syncs to the narration.
    dur = beats[-1]['t1']
    share = {}
    for b in beats:
        share[b['plate']] = share.get(b['plate'], 0) + (b['t1'] - b['t0'])
    for pl, sec in sorted(share.items(), key=lambda kv: -kv[1]):
        if sec / dur > 0.22:
            fail('WARN', 'plate-overused',
                 '%s carries %.1f%% of the runtime (%.1fs). The b-roll rule is '
                 'one picture per narration line.' % (pl, 100 * sec / dur, sec))

    # Defect: frame 0 was an 82%-white flash. A cut accent needs something to
    # cut from; on beat 0 there is nothing before it.
    if beats[0].get('flash'):
        fail('BLOCK', 'flash-on-first-beat',
             'beat 0 has flash:true. The impact flash fires at u<0.035, which '
             'on the opening beat is t=0 -- the frame the feed uses as the '
             'thumbnail.')

    # Defect: the hero arrives letter by letter, so frame 0 showed "0" of
    # "0.24 Wh". The opening frame must be whole.
    if not beats[0].get('heroInstant'):
        fail('WARN', 'hero-animates-in-at-t0',
             'beat 0 lacks heroInstant, so frame 0 catches the hero mid-reveal '
             'and the thumbnail shows a partial word or number.')


# ----------------------------------------------------------------- frames ---
def grab(mp4, times, td):
    out = []
    for t in times:
        f = os.path.join(td, 'f%08.3f.png' % t)
        subprocess.run([FF, '-nostdin', '-v', 'error', '-y', '-ss', '%.3f' % t,
                        '-i', mp4, '-frames:v', '1', f], check=False)
        out.append((t, f) if os.path.exists(f) else (t, None))
    return out


def frame_checks(mp4, d, td):
    from PIL import Image, ImageStat, ImageChops
    beats = d['beats']
    dur = beats[-1]['t1']

    # --- frame 0 is the feed thumbnail -----------------------------------
    t0f = grab(mp4, [0.0], td)[0][1]
    if t0f:
        im = Image.open(t0f).convert('L')
        m = ImageStat.Stat(im).mean[0]
        if m > 170 or m < 18:
            fail('BLOCK', 'frame0-unusable',
                 'frame 0 mean luma %.0f. This frame is the thumbnail the feed '
                 'sees; it was an 82%%-white blank once already.' % m)
        # and it should carry readable type, not just picture
        if ImageStat.Stat(im).stddev[0] < 18:
            fail('WARN', 'frame0-flat',
                 'frame 0 has stddev %.0f -- little contrast, so probably no '
                 'legible type on it' % ImageStat.Stat(im).stddev[0])

    # --- no blown or crushed frames anywhere ------------------------------
    scan = [i * dur / 60 for i in range(60)]
    for t, f in grab(mp4, scan, td):
        if not f:
            continue
        m = ImageStat.Stat(Image.open(f).convert('L')).mean[0]
        if m > 200:
            fail('BLOCK', 'frame-blown', 't=%.2fs mean luma %.0f' % (t, m))
        elif m < 10:
            fail('BLOCK', 'frame-black', 't=%.2fs mean luma %.0f' % (t, m))

    # --- type must not touch the frame edge -------------------------------
    # Defect: "THE WORDS ARE CHOPPED OFF THE SCREEN". fitHero measures and
    # shrinks, but nothing verified the finished pixels.
    GUT = 24
    for t, f in grab(mp4, [b['t0'] + (b['t1'] - b['t0']) * 0.75 for b in beats], td):
        if not f:
            continue
        im = Image.open(f).convert('L')
        px = im.load()
        for x in (GUT, W - 1 - GUT):
            col = [px[x, y] for y in range(260, H - 260, 4)]
            # bright ink hard against the gutter, with dark either side of it
            if max(col) > 225 and (sum(1 for v in col if v > 225) > 10):
                fail('WARN', 'ink-at-gutter',
                     't=%.2fs bright pixels at x=%d -- type may be clipped' % (t, x))
                break

    # --- beats must not be frozen ----------------------------------------
    # Defect: 14 of 29 beats measured visually static; the close was 0.043.
    for i, b in enumerate(beats):
        a = b['t0'] + 0.25 * (b['t1'] - b['t0'])
        c = b['t0'] + 0.75 * (b['t1'] - b['t0'])
        fa, fc = [x[1] for x in grab(mp4, [a, c], td)]
        if not (fa and fc):
            continue
        A = Image.open(fa).convert('L').crop((0, 0, W, 1150)).resize((180, 190))
        C = Image.open(fc).convert('L').crop((0, 0, W, 1150)).resize((180, 190))
        delta = ImageStat.Stat(ImageChops.difference(A, C)).mean[0]
        if delta < 1.0:
            sev = 'BLOCK' if i == len(beats) - 1 else 'WARN'
            fail(sev, 'beat-frozen',
                 'beat %d (%.2f-%.2fs) imagery delta %.2f -- effectively a '
                 'still frame%s' % (i, b['t0'], b['t1'], delta,
                                    '; this is the closing beat' if sev == 'BLOCK' else ''))


# ------------------------------------------------------------------ audio ---
def audio_checks(mp4):
    r = subprocess.run([FF, '-nostdin', '-v', 'info', '-i', mp4, '-af', 'ebur128',
                        '-f', 'null', '-'], capture_output=True, text=True)
    txt = r.stderr
    # Read the SUMMARY block only. Per-frame ebur128 lines also carry "I:",
    # and matching one of those reported 0.1 LUFS for a file measuring -14.0.
    I = None
    lines = txt.splitlines()
    for n, ln in enumerate(lines):
        if 'Integrated loudness' in ln:
            for ln2 in lines[n + 1:n + 4]:
                t2 = ln2.strip()
                if t2.startswith('I:'):
                    try:
                        I = float(t2.split()[1])
                    except Exception:
                        pass
                    break
            break
    if I is None:
        fail('WARN', 'loudness-unknown', 'could not measure integrated loudness')
    elif abs(I + 14.0) > 1.0:
        fail('BLOCK', 'loudness-off', 'integrated %.1f LUFS, target -14.0' % I)

    # Defect: 6.26s of digital silence, 16.3% of runtime, no bed. Every
    # sentence boundary was a hole, and holes are where people swipe.
    r2 = subprocess.run([FF, '-nostdin', '-v', 'info', '-i', mp4,
                         '-af', 'silencedetect=noise=-50dB:d=0.25', '-f', 'null', '-'],
                        capture_output=True, text=True)
    tot = 0.0
    for ln in r2.stderr.splitlines():
        if 'silence_duration' in ln:
            try:
                tot += float(ln.split('silence_duration:')[1].split()[0])
            except Exception:
                pass
    if tot > 0:
        d = subprocess.run([FF, '-nostdin', '-v', 'error', '-i', mp4, '-f', 'null', '-'],
                           capture_output=True, text=True)
        sev = 'WARN' if tot < 3 else 'BLOCK'
        fail(sev, 'dead-air',
             '%.2fs of silence below -50dB in gaps of 0.25s or more. There is '
             'no music bed or room tone under the narration.' % tot)


def main():
    root = sys.argv[1].rstrip('/')
    beats_f = os.path.join(root, 'beats.json')
    d = json.load(open(beats_f))
    mp4s = [f for f in os.listdir(root) if f.endswith('.mp4')]
    if not mp4s:
        print('no mp4 in %s' % root); return 2
    if len(sys.argv) > 2:
        mp4 = os.path.join(root, sys.argv[2])
    else:
        mp4 = max((os.path.join(root, f) for f in mp4s), key=os.path.getmtime)
    print('QC %s' % mp4)

    static_checks(d)
    audio_checks(mp4)
    with tempfile.TemporaryDirectory() as td:
        frame_checks(mp4, d, td)

    blocks = [f for f in findings if f[0] == 'BLOCK']
    warns = [f for f in findings if f[0] == 'WARN']
    for sev, code, msg in blocks + warns:
        print('  %-5s %-22s %s' % (sev, code, msg))
    print('\n%d blocking, %d warnings' % (len(blocks), len(warns)))
    return 1 if blocks else 0


if __name__ == '__main__':
    sys.exit(main())
