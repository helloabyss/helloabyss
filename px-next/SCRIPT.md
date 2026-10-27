# PARADOCS10X — "Xbox Series S: $399 to $499"

**89 words · ~32.4s at 165 wpm · 11 VO lines · 1080×1920 · Alex Wright · no host**

Research source: `px-next/FACTS.md` (researched 2026-10-27). Every figure below comes from
that table. No figure outside it appears in the VO.

---

## Hook (reusable as the title)

> **Xbox Series S: four hundred to five hundred dollars, August first.**

Named thing + one hard number, inside two seconds, with no build-up.

---

## Verbatim VO

One sentence per line, exactly as spoken. Numbers are written the way the narrator
should say them.

```
Xbox Series S: four hundred to five hundred dollars, August first.
Third increase since May twenty twenty-five.
This one Microsoft blamed on memory and storage.
The chips A I data centres buy.
Microsoft says those costs are up more than two and a half times.
They could double again by autumn twenty twenty-seven.
But that multiple comes from the company raising the price.
Unaudited. No agreed baseline.
Sony raised too, and never named memory.
A June lawsuit alleges the memory makers coordinated supply. Untested.
Ask who supplied the number.
```

Clean copy for narration: **`px-next/vo.txt`** (VO text only, nothing else in the file).

### Count

| | |
|---|---|
| Words | **89** (counted with `wc -w`, not estimated) |
| Runtime at 165 wpm | **32.4s** |
| Runtime at 158.7 wpm (the repo's other measurement) | 33.6s |
| Target band | 25–35s · 70–95 words |

Estimate only until the audio is measured. If the measured stem lands over 35s, cut
line 6 (*"They could double again by autumn twenty twenty-seven."*) first — it is the
only line whose removal costs no accuracy guard.

---

## Beats

| # | Line | Beat | Function |
|---|---|---|---|
| 1 | Xbox Series S: four hundred to five hundred… | **Hook** | Named thing, hard number, date. Works as the title and as a silent first frame. |
| 2 | Third increase since May twenty twenty-five. | Escalation | Establishes a pattern without printing a month count (sources conflict). |
| 3 | This one Microsoft blamed on memory and storage. | **Turn 1** | *"This one"* is the accuracy guard: it separates the August leg from the two tariff-era hikes. |
| 4 | The chips A I data centres buy. | Define | The one line that makes it an A I story. States what the chips are, not what caused the price. |
| 5 | Microsoft says those costs are up more than two and a half times. | Case | Attribution sits **inside** the sentence, as in the watt-hours short. |
| 6 | They could double again by autumn twenty twenty-seven. | Case | Company forecast. Labelled as the company's by line 5 carrying over. |
| 7 | But that multiple comes from the company raising the price. | **Counter-evidence, signposted** | The mandatory counterweight. *"But"* is the audible turn. |
| 8 | Unaudited. No agreed baseline. | Counter | Two beats of the same point, in the house's clipped register. |
| 9 | Sony raised too, and never named memory. | Counter | Kills the "both console makers blamed A I" reading before a viewer can form it. |
| 10 | A June lawsuit alleges the memory makers coordinated supply. Untested. | Counter | The reason not to narrate the A I explanation as settled. *"Untested"* is not optional. |
| 11 | Ask who supplied the number. | Close | Loops to the 2.5x and gives the viewer a check to run, not a feeling. |

New information or a reversal lands every one to two lines; the counter-evidence block
runs from line 7 to line 10 — four of eleven lines, 36% of the script.

---

## Fact table — only the claims this script makes

Grades carried from `FACTS.md`. **CONFIRMED is unavailable in this environment:** no
primary source was opened. Xbox Wire, the court docket, Bloomberg and the TrendForce
and Deloitte reports were all read through secondary coverage only.

| Line | Claim as spoken | FACTS row | Grade |
|---|---|---|---|
| 1 | Xbox Series S 512GB US list went **$399.99 → $499.99**, announced effective **1 Aug 2026** | F1 | **HIGH** (4 independent outlets; one stale pre-launch $449 report set aside) |
| 1 | The rise on 512GB models is **+$100** | F5 | **HIGH** |
| 2 | **Third** Xbox increase, the first since **May 2025** | F9 | **HIGH on "third"** · window DISPUTED (15 vs 13 months) — **no month count is spoken or printed** |
| 3 | Microsoft named **memory and storage** as the reason for this increase | F6 | **HIGH that Microsoft said it** |
| 3 | The **May 2025** hike was tariff-linked, not memory — hence *"this one"* | F10, §4.3 | MEDIUM — handled by scoping the script to the August leg, never asserted on screen |
| 4 | A I data centres are buyers of the same memory/storage supply (HBM crowd-out) | F18, F19 | **MEDIUM** — spoken as *what the chips are*, not as a measured cause |
| 5 | Microsoft says those costs are up **more than 2.5x** | F6 | **HIGH that Microsoft said it** · the number itself is **company-supplied and unaudited**, baseline date disputed |
| 6 | Microsoft says they **could roughly double again by autumn 2027** | F6 | **HIGH that Microsoft said it** · company forecast |
| 7–8 | The 2.5x originates with Microsoft, is unaudited, and has no agreed baseline | F6, §4.2 | **HIGH** (this is an observation about the sourcing, not a competing figure) |
| 9 | Sony raised PS5 prices (Apr 2026) and gave **economic pressures**, never naming memory | F12, F13 | **HIGH** |
| 10 | A proposed US class action filed **June 2026** alleges the three DRAM makers coordinated supply; **untested** | F20 | **MEDIUM on the filing** · claims are **untested allegations**, no company response or ruling found |

### Rows deliberately not used

`F2`–`F4`, `F8`, `F11` (other SKUs, 2TB sunset, worldwide scope) — cut for runtime, all
usable on frame if a price panel is wanted. `F14`/`F15` (Circana −33% / avg price paid),
`F16`/`F17` (DRAM quarterly percentages) and `F21` (PC and phone forecasts) are **barred
by the brief** and by `FACTS.md` §5.

### Dropped on re-check — do not reinstate

| Dropped | Why |
|---|---|
| "Memory up 700%" | Two different origins, conflicts head-on with Microsoft's 2.5x, scope and baseline unknown. The 10x-wrong trap the repo logged on 2026-10-25. |
| "Microsoft loses ~$150 per Xbox" | Single anonymous-sourced insider origin; also names a real person for no benefit. |
| Any Q3/Q4 2026 DRAM percentage | Forecasts disagree violently; F17 is **DISPUTED** on scope. |
| The lawsuit case number and plaintiff count | Single-source via aggregator-citing-aggregator; docket unreachable. |
| UK £500 → £670 | Single source. |
| Xbox US unit sales **−33%** | Confounded by structural decline and Microsoft's multiplatform strategy; no source separates the price effect. |
| "Today's price" framing | No source confirms current retail. On frame the figures read **announced 1 Aug 2026**. |
| A fourth Xbox increase | Searched, none found. "I found none" is not "none exists." |
| Any verbatim quotation of Xbox Wire or Sony | Primary pages unreachable; `engine/qc.py` blocks text set as a sourced quotation. Everything above is paraphrase. |
| Any ticker, valuation or share price | Out of scope by choice — keeps the video clear of the money-channel disclaimer rules. |

---

## SAY-LIST — pronunciation, read before generating narration

Run this against the stem on first listen. Fixing it after generation costs a second
render.

| Written in `vo.txt` | Say it as | Note |
|---|---|---|
| `A I` | **"ay eye"** — two letters | Written spaced so the engine does not voice it as the word *"ai"*. Never collapse to "AI" in the VO file. |
| `Xbox` | **"EKS-box"** | Not "ex-boks" slurred to one syllable. |
| `Series S` | **"series ESS"** | The S is a letter name, not a hiss. |
| `twenty twenty-five` | **"twenty twenty-five"** | The year. Not "2025" and not "two thousand twenty-five" — the digits are deliberately absent from the file. |
| `twenty twenty-seven` | **"twenty twenty-seven"** | Same. |
| `autumn` | **"AW-tum"** | Silent N. Some engines voice it. |
| `Unaudited` | **"un-AW-dit-id"** | Four syllables, stress on AW. The most likely mangle in the script. |
| `coordinated` | **"koh-OR-din-ay-tid"** | Not "coord-nated". |
| `two and a half times` | **"two and a half times"** | Spelled out on purpose — never render as "2.5x", which engines read as "two point five ex". |
| `four hundred` / `five hundred` | **"four hundred" / "five hundred"** | No "dollars" after the first; the single "dollars" sits after "five hundred". |
| `Sony` | **"SOH-nee"** | |

No stage directions, speaker labels or bracketed notes exist in `vo.txt`. It is read
literally. The whole script is **~530 characters**, far inside the 5,000-character
generation cap, so no split is needed.

---

## Title options

Proven shape: named thing + one hard number + the cost that number hides. All three
keep the 2.5x attributed, because the unattributed version is a claim the script
does not make.

1. **`Xbox Series S: $399 to $499. Microsoft Blames the RAM.`** *(54 chars) — recommended.*
   Named thing, one price delta, and the hidden cause, attributed in the title itself.
   Silent-frame safe: `$399 → $499` is a picture.
2. **`Xbox Went Up $100. Microsoft Says Memory Costs 2.5x.`** *(52 chars)*
   Leads on the component multiple. Stronger number, weaker named-thing recognition.
3. **`Xbox Series S Hit $499. Nobody Audited The Reason.`** *(49 chars)*
   The counter-evidence version — the hidden cost is the sourcing of the explanation.
   Hardest hook of the three, and the most honest.

Rejected: any title asserting *"Because AI Bought the RAM"* as fact. The script does not
assert it and the title must not either.

---

## On-frame sourcing strip

PARADOCS10X names Microsoft and Sony but quotes **no ticker, no valuation, no share
price, and implies no buy / sell / hold**. Per `CLAUDE.md` it therefore carries
**no financial disclaimer at all**. It carries sourcing instead.

**Primary strip — persistent, lower frame:**

```
SECONDARY REPORTING · COMPANY STATEMENTS · SOURCES IN DESCRIPTION
```

**Price-panel label — must appear wherever a dollar figure is on frame:**

```
LIST PRICES AS ANNOUNCED 1 AUG 2026
```

**Attribution tag — must appear on the 2.5x frame, not only in narration:**

```
MICROSOFT'S OWN FIGURE · UNAUDITED
```

**Allegation tag — must appear on the lawsuit frame:**

```
UNTESTED ALLEGATION · NO RULING
```

Set as plain text name-tags. No logos, no badges, no quotation marks anywhere —
`engine/qc.py` blocks text presented as a sourced quotation, and no primary source
was reachable to support one.
