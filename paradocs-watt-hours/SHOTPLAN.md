# Shot plan — one picture per narration line

The rule the owner set on 2026-10-26: **b-roll is synced to the narration, as a
rule of thumb, on every video.** The shipped cut breaks it — 5 plates cycled
across 29 beats, so when the VO says "idle capacity, cooling" the screen shows
a pylon.

HeyGen `create_speech` already gives word-level timestamps, so the alignment
is exact and free. What was missing is a shot per line. Higgsfield can
generate those now that the CDN block is solved (see CLAUDE.md).

Source column: **STOCK** = Adobe, already licensed · **GEN** = Higgsfield,
10 credits per 5s 9:16 clip · **HAVE** = already generated and paid for,
bridgeable at no cost.

| # | Narration | What must be on screen | Source | Shot |
|---|---|---|---|---|
| 1 | "Google says one Gemini prompt costs 0.24 watt-hours" | a prompt being typed | STOCK `W1` | hands typing on a phone — real hands, generation gets these wrong |
| 2 | "Same paper. Same prompt. 0.10." | the paper itself | GEN | a bound research paper under a desk lamp, slow push onto a dense table of figures, warm tungsten |
| 3 | "Both numbers are correct." | two things, both true | GEN | two identical brass weights balanced level on a scale, warm key light, slow orbit |
| 4 | "Ten counts the chip doing the thinking." | the chip | HAVE `1b251ea4` | silicon wafer macro, robotic arm, amber cleanroom — already paid for |
| 5 | "Seventeen adds the host machine, idle capacity, cooling." | cooling | GEN | rows of data-centre cooling fans spinning behind a mesh grille, condensation on chilled pipes, amber light |
| 6 | "Twenty-four averages it across the whole fleet." | scale | HAVE `78054207` | tracking shot down an endless data-centre aisle — already paid for |
| 7 | "Two point four times apart. One prompt." | the gap | STOCK `W3` | feet on hard sun — neutral bed for the versus columns |
| 8 | "Nothing was hidden. Google printed every line." | the printing | GEN | macro tracking across a printed page of dense figures, warm lamp, paper fibre visible |
| 9 | "The number moved because the boundary moved." | a boundary moving | GEN | a white chalk line being drawn across dark asphalt, close on the chalk, dust lifting |
| 10 | "Now what it is not." | turn | STOCK `W4` | hands at a window — breath before the reversal |
| 11 | "It is a median. Text only." | the middle of many | GEN | a long row of identical glass bottles, the centre one lit warm, the rest falling dark |
| 12 | "No voice. No images." | what is excluded | GEN | an unplugged microphone and a lens cap on a dark desk, single warm source, slow drift |
| 13 | "Google never publishes how many prompts it serves." | uncounted volume | GEN | a mechanical counter wheel spinning too fast to read, macro, warm light |
| 14 | "So nobody outside can total it." | shut out | GEN | a roller shutter coming down over a lit doorway, warm spill narrowing to a line |
| 15 | "One number is never one number." | the thesis | HAVE `d94d2cec` | city plaza, people passing in soft focus, golden light — the vox-pop card sits on this |
| 16 | "Ask where they drew the line." | back to the line | GEN | the chalk line again, wider, a foot stepping over it |

## Cost

- **GEN:** 9 clips x 10 credits = **90 credits** of 350.57.
- **HAVE:** 3 clips, 0 credits — already generated, bridged free through ElevenLabs.
- **STOCK:** 3 plates, already licensed.

Leaves ~260 Higgsfield credits.

## Why generate rather than search stock

Shots 3, 9, 11, 12, 13, 14 and 16 are **arguments, not objects**. A balance, a
line being drawn, the one lit bottle in a row — stock libraries index by
subject, so there is nothing to search for. Those shots are the reason the cut
currently falls back on pylons: the picture the sentence needs did not exist to
be licensed.

## Pipeline

1. **HeyGen** `create_speech` — narration + word-level timestamps (the spine)
2. **Higgsfield** `generate_video` — the 9 argument shots, 9:16, 5s
3. **ElevenLabs** — bridge Higgsfield's blocked CDN; also the free mux
4. **Adobe Stock** — the 3 shots where real hands and real crowds matter
5. **HyperFrames / `engine/reel.js`** — assembly, captions, layouts
