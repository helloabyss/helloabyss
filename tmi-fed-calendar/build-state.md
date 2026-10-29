# build-state: tmi-fed-calendar

**v1 CURRENT** — 2026-10-29. `fed-calendar.mp4`, 32.67s, QA-GATE 25/25 PASS.

Event was Wed 28 Oct 2026; the reserve-rate change took effect 29 Oct.

## What the gate caught that I did not

1. **No number in the first two seconds.** The hook opened "THE FED HELD /
   YESTERDAY". The shape that works on this channel is a named thing plus a
   hard number, and frame 0 is the feed thumbnail. Lead is now `3.75% - 4%`.
2. **Nine words on a frame** against a ceiling of eight.
3. **No thumbnail.**
4. **The host sat below y=1535**, inside the strip the Shorts UI covers. Zul
   was at y1905 with a 430px height — almost entirely under the title row and
   buttons.

## What my eye caught that the gate did not

The host overlapped the hero, the cards, the band and the versus columns in
most frames. Every gate passed. Nothing measured text against the **host** —
only against the frame. Fixed in `reel.js` (`clearW` clamps every layout box
to the host column) and gated as **V13**.

V13 took three attempts and the two failures are recorded in `qc.py`:
- sniffing bright pixels in the host column counted Zul's white polo as type;
- "reel.js clamps, therefore PASS" is a tautology, which is the same
  "PASS with caveat" pattern this repo criticised in the competitor playbook.
It now detects **amber** in the host column — the host is locked black and
white, so any accent there is overlay. Falsification-tested: moving the host
column over the amber band makes it fail on the same file that passes.
Known limit, stated rather than hidden: cream type behind the host is not
detectable this way.

## Not done
- No new b-roll was generated; plates are regraded and reused.
- Runtime 32.67s. Inside the sub-40s gate, above the 27s that the one breakout
  short ran to.

## Status
**Not posted.** Complete and gated, **not verified** — nothing here can watch
a video with sound. A human must do that first.
