# SHOTLIST — "82% / 25%" (PARADOCS10X short 5) — REBUILD

Supersedes the shot list in the previous `SCRIPT.md`, which shipped a white-background
typographic slideshow and was rejected. `STYLE-GUIDE.md` §1 bans exactly that: *"text
floating on abstract textures … reads flat and cheap. Imagery is the foundation."*

**20 beats · 84 words · target 28–30s · 9:16 portrait · 24fps**
Average beat 1.5s. **Nothing on screen past 2.0s without a punch-in sub-cut** (marked `»`).

---

## Global rules for this build

| | |
|---|---|
| **Layer stack** | BASE photographic plate (always full-frame, never a texture) → MID motion graphics → TOP hero type + captions. Camera move applies to the **plate**, not only the type. |
| **Grade** | Every plate crushed to near-black. Saturation ≤ 8%. Lifted blacks rolled back down, highlights rolled off. **Red exists only on the MID/TOP layers** — never in the photography. If a plate arrives warm or colourful it is regraded, not used as shot. |
| **Parallax** | Three depth planes move at visibly different speeds in every beat. Foreground element streaks past the lens on every camera move. |
| **Transitions** | **No plain cuts anywhere.** Each beat below names its exit: match-cut / type-as-mask / whip / push-through. |
| **Numbers** | Every figure physically counts up or draws on. Never appears finished. |
| **Type** | Heavy condensed sans. Letters arrive individually with overshoot. 1–2 frame white flash + screen shake on beats 4, 11, 13 only. |
| **Captions** | Burned-in, word-by-word, bottom third, **white with black stroke**, current word in the red accent. Dark scrim behind the band on every plate (all plates here are busy). Caption band y≥1415 stays clear of art — `engine/checkband.py` still gates the build. |
| **Compliance** | `Educational only. Not financial advice.` — a thin white-on-black strip **above** the caption band, held 0.0–4.2s. **Not a full card.** It must not take the frame away from the hook; §"Hook veto" in `PACKAGING.md` is why. |
| **Faces** | None. People are implied by their objects — empty desks, set-down tools, hung coats — never shown, not even in silhouette. |
| **Logos** | None. "UC BERKELEY RDI · SNORKEL AI" is set as plain text name-tags. |

---

## Spine

- **Bookend object: the night desk** (plate A) — matte-black desktop, one open laptop as the
  only light source, a printed stack beside it. Beat 1 pushes *into* that screen. Beat 20
  pulls back *out of* it from the identical angle. The whole video happens inside that push.
- **HERO shot: beat 10** — extreme macro, a red pen nib dragging a wet line across printed
  text. It is the single most tactile frame and it carries the central idea: the agent is
  not marked against a rubric, it is marked against what a human actually handed in.
- **Match-cut chain:** laptop screen → rack LED → full stop → lamp → paper → pen stroke →
  spindle → pie circle → stair well → sky well → laptop screen. The video closes its own loop.

---

## Beat sheet

Hero word = the single TOP-layer word that owns the frame.

### Act 1 — the two numbers (beats 1–5, ~0.0–7.0s)

**B01 · "Eighty-two percent." (2w, ~1.2s)**
- BASE: **A — night desk.** Laptop screen fills frame, pixel grid resolving out of bokeh.
- MID: score readout ticking `00 → 82`, monospaced, white.
- TOP hero: **82%** — arrives letter by letter, overshoot, settles.
- CAMERA: hard dolly in on the screen, foreground paper edge streaking past the lens.
- EXIT: **type-as-mask** — the `8` scales until the camera is inside its counter, and B02 is
  revealed through the hole.

**B02 · "One AI agent. Its coding benchmark." (6w, ~1.7s)** `» punch in on "benchmark"`
- BASE: **B — data-centre aisle,** low angle, rack LEDs receding, near-black.
- MID: plain text name-tag `TERMINAL-BENCH · CODING` + a white `PASS` tag snapping on.
- TOP hero: **PASS**
- CAMERA: whip-pan right down the aisle, directional motion blur.
- EXIT: **whip** carries straight into B03 on the same vector.

**B03 · "Berkeley gave it real professional work." (6w, ~1.7s)** `» punch in on "real"`
- BASE: **C — empty brutalist lecture hall / concrete stairwell at night.** No people.
- MID: plain text name-tags `UC BERKELEY RDI` and `SNORKEL AI`, set as two small rules.
- TOP hero: **REAL WORK**
- CAMERA: slow crane down between the seat rows, hard parallax on the concrete fins.
- EXIT: **match-cut** — a lit window rectangle becomes the card B04 drops into.

**B04 · "Twenty-five." (1w, ~1.0s)**
- BASE: **A — night desk, overhead,** screen now dark.
- MID: the 82 counter **structurally fails** — the bar cracks, shards drop out of frame, the
  readout falls `82 → 25`. The number is red for the first time in the video.
- TOP hero: **25%**
- CAMERA: snap zoom out. **1-frame white flash + screen shake.**
- EXIT: a **red line wipe** travels left-to-right and takes B05 with it.

**B05 · "Same agent." (2w, ~1.0s)**
- BASE: **B — macro of a single rack status LED,** everything else fallen out of focus.
- MID: `82%` and `25%` side by side under one bracket reading `SAME CONFIGURATION`.
- TOP hero: **SAME**
- CAMERA: rack-focus from a foreground cable to the LED.
- EXIT: **match-cut** — the LED dot becomes the full stop in the B06 title.

### Act 2 — what the test actually is (beats 6–11, ~7.0–16.0s)

**B06 · "Agents' Last Exam." (3w, ~1.3s)**
- BASE: **D — dense printed pages / archive shelving,** single hard raking light.
- MID: title plate drawn as two rules closing on the words.
- TOP hero: **AGENTS' LAST EXAM**
- CAMERA: push **through** the gap between two paper stacks.
- EXIT: **type-as-mask** — `EXAM` wipes off and B07 is revealed through its counters.

**B07 · "Fourteen hundred real tasks." (4w, ~1.5s)**
- BASE: **D — archive aisle, deep one-point perspective.**
- MID: a grid of small squares draws itself across the shelving; counter ticks `0 → 1,400+`.
- TOP hero: **1,400+**
- ⚠ **On screen it reads `1,400+`. Never `1,490`.** The spoken figure is "fourteen hundred";
  `FACTS.md` has the precise count but the card must not out-precise the read.
- CAMERA: dolly down the aisle, shelf uprights streaking past.
- EXIT: **whip left.**

**B08 · "From three hundred working professionals." (5w, ~1.6s)**
- BASE: **D/E — a wall of switched-off desk lamps, or coats on hooks, in near-dark.**
  People are implied by their objects. Nobody is in frame.
- MID: counter `0 → 300`, tag `300+ PRACTITIONERS`.
- CAMERA: lateral truck, three depth planes at visibly different speeds.
- TOP hero: **300**
- EXIT: **match-cut** — one lamp head becomes the lit lamp of B09.

**B09 · "Their own finished work." (4w, ~1.4s)**
- BASE: **E — workbench, finished deliverable:** a bound report squared up, instruments set
  down beside it, one lamp.
- MID: a `DELIVERED` stamp arrives with overshoot.
- TOP hero: **THEIR WORK**
- CAMERA: push in with a slight roll.
- EXIT: the push **continues straight into the paper surface** → the hero macro.

**B10 · "Graded against what the human delivered." (6w, ~1.9s) — ★ HERO SHOT** `» punch on "delivered"`
- BASE: **F — extreme macro: a red pen nib dragging a wet red line across a line of printed
  text.** Shallow DOF, single raking light, paper fibre visible. This is the one frame the
  video is built around. *This is the plate to spend the Higgsfield credit on if a generated
  plate is ever approved; otherwise macro stock.*
- MID: a ghosted second document slides into register over the first; mismatched lines light red.
- TOP hero: **GRADED**
- CAMERA: macro track along the pen stroke, **slow-mo**.
- EXIT: **speed ramp snaps to full** on the cut into B11.

**B11 · "Match it or fail." (4w, ~1.4s)**
- BASE: **F continued** — the stroke closes into a hard red X on the page.
- MID: a PASS/FAIL toggle snaps to `FAIL`.
- TOP hero: **FAIL**
- CAMERA: two-step punch in. **1-frame white flash + shake.**
- EXIT: the **X wipes** the frame diagonally into B12.

### Act 3 — zero, and why (beats 12–16, ~16.0–23.5s)

**B12 · "Hardest tier: the leaders scored zero." (6w, ~1.8s)** `» punch on "zero"`
- BASE: **G — looking straight down a dark stairwell or lift shaft,** vanishing into black.
- MID: three tier labels descending into the dark — `NEAR-TERM` / `FULL-SPECTRUM` /
  `LAST EXAM` — the last one unreadable in the black.
- TOP hero: **HARDEST TIER**
- CAMERA: vertical plunge down the shaft, rails streaking.
- EXIT: the fall **continues unbroken** into B13 (the only through-move in the video).

**B13 · "Not low. Zero." (3w, ~1.4s)**
- BASE: **G — the bottom of the shaft.** Almost pure near-black with one edge of light.
- MID: the counter tries to count up and flatlines at `0.0%`. Small qualifier rule under it:
  `top configurations · hardest tier` — the honesty line that stops the 10x misread.
- TOP hero: **0.0%** in red, scaling past the frame edges until the camera is inside the `0`.
- CAMERA: inside the letterform. **1-frame white flash + shake.**
- EXIT: **type-as-mask** out through the `0` into B14.

**B14 · "The tools worked." (3w, ~1.2s)**
- BASE: **H — macro of a precision machine running perfectly:** oiled gear train, CNC spindle,
  or a robot-arm joint rotating. Dark metal, one specular highlight.
- MID: white check-tag `TOOL EXECUTION: OK`. No green — palette is absolute.
- TOP hero: **TOOLS: OK**
- CAMERA: tight orbit around the rotating part.
- EXIT: **match-cut** — the spindle circle becomes the ring of the B15 split graphic.

**B15 · "Three quarters of failures: missing domain knowledge." (7w, ~2.0s)** `» punch on "knowledge"`
- BASE: **I — a technical schematic on dark paper, out of focus,** raking light.
- MID: a split bar draws itself — ~75% red `DIDN'T KNOW THE JOB` against white `TOOLS`.
  Footnote rule: `single-source analysis` — this claim is graded Medium in `FACTS.md` and is
  load-bearing, so the frame says so.
- TOP hero: **3/4**
- CAMERA: push in until the bar fills the frame.
- EXIT: the **red segment wipes** right and becomes the void in B16.

**B16 · "The agent didn't know the job." (6w, ~1.8s)** `» punch on "job"`
- BASE: **I — the same schematic, now sharp, with a whole region blank.** A hole in the drawing.
- MID: a dotted outline around the void, labelled `DOMAIN KNOWLEDGE`.
- TOP hero: **DIDN'T KNOW THE JOB**
- CAMERA: push **through the hole** into black.
- EXIT: **push-through** lands in B17.

### Act 4 — the counter-evidence (beats 17–20, ~23.5–30.0s · 5 of 20 beats = 25% of runtime)

> This act is mandatory and is not a coda. It gets the same weight of frame as the thesis:
> same hero-type scale, same camera energy, and the climb is shown as a real climb.

**B17 · "Now the other side." (4w, ~1.4s)**
- BASE: **J — low angle on a steel staircase or escalator ascending into dark.**
- MID: a thin red line ignites on the bottom tread.
- TOP hero: **THE OTHER SIDE**
- CAMERA: fast tilt up the structure.
- EXIT: **whip up.**

**B18 · "June: twenty-four percent." (3w, ~1.3s)**
- BASE: **J — stair treads in steep perspective.**
- MID: a line chart draws itself along the treads; counter `0 → 24.0%`; tag `JUN`.
- TOP hero: **24%**
- CAMERA: dolly up the stairs, handrail streaking in foreground.
- EXIT: the **climb continues** — no cut, a speed-ramped match on the rising line.

**B19 · "October: fifty-nine." (2w, ~1.2s)**
- BASE: **J — higher up, the structure opening to a bright sky-well** (still desaturated).
- MID: the line continues to `59.3%`; tag `OCT`; qualifier rule
  `different boards · not like-for-like`. Required — `FACTS.md` #9 is directional, not
  like-for-like, and the frame must not imply a clean series.
- TOP hero: **59%**
- CAMERA: continue up, speed ramp into the opening.
- EXIT: **match-cut** — the sky-well rectangle becomes the laptop screen of B20.

**B20 · "The gap is real. It's closing fast." (7w, ~2.0s) — BOOKEND**
- BASE: **A — the night desk, identical angle to B01,** pulling back out of the screen.
- MID: `82` and `25` placed side by side with a red bracket measuring the gap between them;
  the bracket narrows as the camera retreats, and **does not close.**
- TOP hero: **THE GAP IS CLOSING**
- CAMERA: the only shot allowed to breathe. Slow pull-back; motion never fully stops.
- FINAL FRAME: the desk, laptop now closed. One actionable line, held 0.8s:
  **`Run an agent on your own last finished deliverable.`**
- **No subscribe animation, no CTA arrow, no follow-bait.** `STYLE-GUIDE.md` §3.

---

## Plate families (10 plates cover 20 beats)

| ID | Plate | Used on | Adobe Stock search query to run |
|---|---|---|---|
| **A** | Night desk, laptop the only light, printed stack, matte-black surface | B01, B04, B20 | `dark desk at night laptop screen glow documents low key moody` |
| **B** | Data-centre aisle, rack LEDs, low angle + a macro of one status LED | B02, B05 | `dark server room aisle rack lights low key` / `macro server status led dark` |
| **C** | Empty brutalist lecture hall or concrete stairwell, night, no people | B03 | `empty lecture hall night dark concrete no people` |
| **D** | Dense printed pages / archive shelving, raking light | B06, B07, B08 | `archive shelving dark documents raking light` / `stack of printed paper macro dark` |
| **E** | Workbench with a finished bound report, instruments set down, one lamp | B09 | `dark desk bound report drafting instruments single lamp overhead` |
| **F** | ★ **HERO** — macro, red pen nib dragging a wet line across printed text | B10, B11 | `macro red pen marking printed document shallow depth of field dark` |
| **G** | Looking straight down a dark stairwell / lift shaft into black | B12, B13 | `looking down dark stairwell spiral vanishing into black` |
| **H** | Precision machine running — gear train, CNC spindle, robot joint | B14 | `macro industrial gears dark oiled metal` / `cnc spindle close up dark` |
| **I** | Technical schematic on dark paper, raking light | B15, B16 | `technical blueprint schematic dark paper close up` |
| **J** | Steel staircase / escalator ascending into dark, steep perspective | B17, B18, B19 | `steel staircase ascending low angle dark industrial` |

Reject any candidate that contains a face, a readable logo, visible branding, neon, a lens
flare, or colour that survives the grade. Portrait crops preferred; landscape plates are
acceptable where the camera move is a push or a vertical plunge, since the crop is covered
by the move.

## Hero plate note

Beat 10 is the one plate worth generating rather than sourcing, because stock "red pen on
paper" is overwhelmingly bright, white-paper, office-stock-reel imagery that fights the
grade. Prompt, if generation is ever approved:

> Extreme macro photograph, red pen nib dragging a wet red ink line across a line of dense
> printed text on off-white paper. Single hard raking light from camera left, everything
> else falling to near-black. Shallow depth of field, visible paper fibre, desaturated
> except the red ink. 9:16 vertical. No hands, no people, no logos.

## Hand-off note to video-editor

`align.py`'s 1:1 sentence↔pause mapping **will not survive this script.** It is 23 sentences
across 20 paragraphs of 1–7 words, and `silencedetect ≥0.55s` will not reliably fire between
"Not low." and "Zero." Align on **paragraph (beat) boundaries using word-level timestamps**
from the narration instead, and let the sub-cuts marked `»` be placed inside a beat by frame
count, not by pause detection.
