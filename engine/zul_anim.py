# -*- coding: utf-8 -*-
"""Zul, moving.

The reference short the owner supplied keeps Zul as a small corner host who is
re-posed every shot — pointing, gesturing, hands clasped — over live footage.
`zul.py` only had five fixed poses, so he could be placed but not animated.
This drives him from a continuous clock: poses blend, he breathes, his head
tilts into a gesture, he blinks, and his mouth flaps against the narration.

Nothing here redraws him by hand. Every stroke still comes out of `zul.py`,
which is the locked model sheet.
"""
import math
from zul import zul, _ARMS

# Extra poses beyond the five in the model sheet, in the same coordinate space:
# ((left shoulder x, y, left hand x, y), (right shoulder x, y, right hand x, y))
POSES = dict(_ARMS)
POSES.update({
    'present':  ((-57, 152, -96, 176), (57, 150, 112, 150)),   # open palm to the data
    'count':    ((-57, 152, -62, 214), (56, 148, 96, 92)),     # one hand up, listing
    'clasp':    ((-57, 152, -16, 206), (57, 152, 16, 206)),    # hands together, settled
    'weigh_l':  ((-57, 150, -112, 128), (57, 152, 60, 206)),   # one side of the argument
    'weigh_r':  ((-57, 152, -60, 206), (57, 150, 112, 128)),   # the other side
})


def _ease(u):
    u = max(0.0, min(1.0, u))
    return u * u * (3 - 2 * u)          # smoothstep: no snap at either end


def blend(a, b, u):
    """Interpolate two poses. Arms are four points, so this is a straight lerp."""
    A, B = POSES[a], POSES[b]
    e = _ease(u)
    return tuple(tuple(p + (q - p) * e for p, q in zip(sa, sb))
                 for sa, sb in zip(A, B))


def pose_at(t, keys):
    """keys = [(time, pose), ...] in order. Holds the last pose past the end."""
    keys = sorted(keys)
    if t <= keys[0][0]:
        return POSES[keys[0][1]]
    for i in range(len(keys) - 1):
        (t0, p0), (t1, p1) = keys[i], keys[i + 1]
        if t0 <= t < t1:
            # Move over 0.45s, then hold — a gesture that eases the whole way
            # between beats reads as drifting rather than as a decision.
            return blend(p0, p1, (t - t0) / 0.45) if t1 - t0 > 0 else POSES[p1]
    return POSES[keys[-1][1]]


def mouth_at(t, words, closed=0.0):
    """Lip-flap from real word timings, not a loop.

    Openness follows a fast attack and slower release inside each word, with a
    wobble so repeated words do not look identical. Silence closes the mouth.
    """
    for w in words:
        if w['t0'] <= t < w['t1']:
            u = (t - w['t0']) / max(0.08, w['t1'] - w['t0'])
            env = math.sin(math.pi * min(1.0, u)) ** 0.6
            wob = 0.72 + 0.28 * abs(math.sin(t * 27.0))
            return max(closed, env * wob)
    return closed


def zul_frame(x, y, sc, t, keys, words=None, view='front', mood='neutral',
              legs=False, breathe=True):
    """Zul at absolute time t. Drop the string straight into a frame."""
    arms = pose_at(t, keys)
    # Breathing: the torso rises ~1.5px and the head leads it slightly. Small
    # enough to read as alive, not as a bounce.
    bob = (math.sin(t * 2.0) * 1.5 + math.sin(t * 3.7) * 0.6) if breathe else 0.0
    # Head tilts into whichever hand is higher — the gesture leads the head.
    lift = (arms[0][3] - arms[1][3]) / 120.0
    tilt = max(-5.0, min(5.0, lift * 4.0)) + (math.sin(t * 1.3) * 0.7 if breathe else 0)
    # Blink: a closed lid is two frames, roughly every 4s, offset so two Zuls
    # on screen never blink together.
    blink = (t % 4.1) < 0.09
    m = mouth_at(t, words) if words else None
    return zul(round(x, 1), round(y + bob, 1), sc,
               view=view, mood=mood, legs=legs,
               arm_xy=arms, mouth=(0.0 if blink and m is None else m), tilt=tilt)
