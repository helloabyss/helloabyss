# Review and fixes — 2026-10-27

A creative-director agent reviewed `watt-hours-v3.mp4` from 36 decoded frames and
ffmpeg measurements. It found nine blocking defects. This records what it found,
what was verified, and what was done — including the one diagnosis that was wrong.

## Blocking defects, and their fixes

| # | Defect | Verified | Fix |
|---|---|---|---|
| 1 | **Frame 0 was an 82%-white blank reading "0.00 Wh"** — and frame 0 is the feed thumbnail on a Short | Yes, luma 218 | The agent blamed a clipped plate. **That was wrong** — W1 measures luma 105–123 throughout. The real cause was `flash:true` on beat 0: the white impact flash fires at `u < 0.035`, which on the opening beat is t=0. A cut accent needs something to cut *from*. Flash is now suppressed on the first beat. Frame 0 measures luma 66. The count-up also restarted on each of the first three beats, so it never read as one count — the number is static and whole now. |
| 2 | **The thesis read "never one numb" for 53% of its screen time** | Yes — the quote spans beats 26 and 27 and the typewriter was keyed to `u`, progress *within* a beat, so it restarted | Reveal keys off absolute time across a quote *group* via `qt0`/`qt1`, and completes at 26% of the group rather than 50%. |
| 3 | **The bar chart animated the opposite of the narration** | Yes, and worse than described: amber went **482px → 341px** while its value went 0.17 → 0.24. `mx = Math.max(g.a, g.b)` normalised to each beat's own max, pinning white at full width | Fixed scale `g.max = 24` across every beat, so 0.10/0.17/0.24 → 342/582/820px. Both bars are now labelled `TOTAL` and `CHIP ONLY`. |
| 4 | **Sourcing strip vanished at 3.90s** — on screen for 10% of the runtime | Yes | `#card` no longer gated on `t < CARD`. It is what this channel carries *instead of* a disclaimer, so it runs the full 38.48s. |
| 5 | **~2.2s of unreadable hero across five band beats** — near-black type on a 170-luma plate while the amber band wiped in | Yes | Wipe quickened to `u/.16` and the hero waits for it via `heroOpacity`. |
| 6 | **Paraphrase presented as a sourced quotation** | Yes | The worst defect on an accuracy channel, in a video about people misreading a published number. Quote marks, the `"` glyph and the invented `— WHAT THE FOOTNOTE ACTUALLY SAYS` attribution are gone. It is a statement card with an accent rule. |
| 7 | **W4 was 461 kb/s with edge-energy 0.27** — seven times softer than anything else, carrying 23.4% of the runtime | Yes | **Removed from the video entirely.** |
| 8 | 14 of 29 beats visually static; the close was a freeze frame at 0.043 | Yes | Partly fixed: four generated plates carry real motion, and the close is now the chalk line rather than an empty sky. Not fully solved. |
| 9 | 6.26s of digital silence, 16.3% of runtime, no bed | Yes | **Not fixed.** Needs a music/room-tone bed and a decision about it. |

## Also actioned

- **HW1 broke the palette** — full-spectrum iridescence, the most saturated thing
  in the video, on a channel locked to near-black plus one accent. Regraded to
  `hue=s=0.32` rather than regenerated, as the agent advised.
- **`#sub` was invisible** on bright plates at `LOOK.mute`. Now ink with a real shadow.
- **The video now bookends.** It opens on a prompt being typed and closes on the
  chalk line from "the boundary moved" — the same object as the penultimate beat.

## Four generated shots, 40 credits

Native 9:16 at 720x1280, so a 1.5x upscale rather than the 2.7x on the bridged
clips. All four are warm brass and amber, on palette, and each one *is* the
argument rather than a stand-in for it:

| Plate | Shot | Line it serves |
|---|---|---|
| `GB` | brass weights on a balance pan | "Same paper. Same prompt." / "Both numbers are correct." |
| `GF` | cooling fans behind a mesh grille | "adds the host machine, idle capacity, cooling" |
| `GC` | mechanical counter wheels blurring | "never publishes how many prompts it serves" |
| `GL` | a hand drawing a chalk line on asphalt | "the boundary moved" and "ask where they drew the line" |

## Still open

- **Defect 9, the silence.** No bed, LRA 2.50, RMS between words at −65 dBFS.
  Loudness itself is correct at −14.02 LUFS / −3.24 dBTP and should not be touched.
- **Defect 8 only partly fixed.** Some beats are still near-static.
- **"Six layouts" is really three.** `full`, `split` and `card` are the same
  composition — muted label, left-aligned hero, bottom third. 65% of runtime in
  one arrangement. The fix is not a seventh layout; it is to vary where the eye
  goes.
- **Amber is doing eight jobs** and `#hero.red` resolves to amber, so the accent
  marks everything and therefore marks nothing.
- **Ten lines still run on recycled stock.** `SHOTPLAN.md` has the list. The two
  worth the next spend: "Nothing was hidden. Google printed every line" (asks out
  loud for a document) and "It is a median" — the latter is a graphic, not a
  plate, so it costs nothing to build in the engine.

## What the review confirmed was right — do not break these

- Every one of the 16 cut anchors lands exactly on a word onset from the HeyGen
  timestamps. Beat durations vary 1.07–1.95s. Picture never drifts against voice.
- Loudness on target.
- Faceless rule held in all 36 frames checked; no logos, no clickbait close.
- Counter-evidence is 27% of the runtime.
- 38.48s, inside the sub-40s window the channel's own data says works.
