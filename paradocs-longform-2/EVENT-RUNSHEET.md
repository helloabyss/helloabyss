# EVENT RUN-SHEET — Apple "Surprise and Shine", 2026-09-09, 10:00 PT

Live capture sheet. Every item maps to a `[[SLOT]]` in `SCRIPT.md`.
**Write timestamps as you go** — they are worth more than notes, because they let you find the
frame again later.

---

## ⚠️ READ FIRST — about "actual clips from the event"

Two separate problems, and the second is the one that matters more.

**1. I cannot fetch them.** YouTube egress is 403 at this environment's proxy; vidIQ has 1
credit against a 5-credit transcript; Higgsfield has 0. There is no route from here to the
stream. And until the keynote ends there is nothing to clip regardless.

**2. Apple keynote footage breaks this channel's own locked style guide.** `STYLE-GUIDE.md`,
section 4, hard constraints:

> **No human faces or identifiable people.** … **No real corporate logos or badges.**

An Apple keynote is wall-to-wall identifiable executives and Apple logos. Cutting it in would
break the channel's visual identity on its most-watched video, on top of the obvious copyright
exposure on a monetised channel.

**Recommendation:** don't use raw keynote footage as the base layer. Do what
`paradocs-longform-1` did and the style guide already prescribes — **rebuild the idea of the
shot** in house style: unbadged device silhouettes, wafers, fab interiors, an empty stage.
The scripts are already written to that imagery plan and need no keynote footage to work.

**If you want event footage anyway**, the defensible version is short, clearly-attributed
excerpts used as commentary — kept brief, captioned as Apple's own claims, and never as the
video's visual backbone. That's your call to make, not mine; I've written the scripts so they
don't depend on it either way.

**What is genuinely worth capturing live: the numbers, the quotes and the timestamps below.**
Those are what the scripts actually need.

---

## CAPTURE LIST — in keynote order

### A. Opening / leadership `[[SLOT — beat 1]]`
- [ ] Who opens the keynote? Confirm **John Ternus as CEO** (reported to have taken over 1 Sept 2026)
- [ ] Is Tim Cook present / referenced? In what role?
- [ ] Timestamp: ______

### B. Products announced `[[SLOT — beat 14]]`
- [ ] iPhone 18 Pro — confirmed? Screen sizes?
- [ ] iPhone 18 Pro Max — confirmed?
- [ ] **The foldable — what is it actually called?** (pre-event guesses: iPhone Ultra / Duo / Fold)
- [ ] Foldable display sizes (outer / unfolded)
- [ ] Apple Watch (Ultra 4?), any other hardware
- [ ] Timestamp: ______

### C. The chip — **most important section** `[[SLOT — beat 14]]`
- [ ] Chip name (A20 Pro?)
- [ ] **Does Apple say "2-nanometre" on stage, or bury it in the spec sheet?** ← this is a
      story beat either way. Note which.
- [ ] Apple's own performance claim: ____% faster than ______
- [ ] Apple's own efficiency claim: ____% more efficient
- [ ] GPU core count / CPU config if stated
- [ ] **C2 modem** — mentioned? Apple's own silicon?
- [ ] Any mention of TSMC by name (rare, but note it)
- [ ] Timestamp: ______

> ⚠️ **Use Apple's stage numbers only.** The pre-event leak (18% faster, 30% more efficient,
> 7-core GPU) is marked LOW confidence in the fact table and **must not be scripted**.

### D. Prices — decides the FORK `[[SLOT — beat 15]]`
- [ ] iPhone 18 Pro base price + storage tier: ______
- [ ] iPhone 18 Pro Max base price + tier: ______
- [ ] Foldable price: ______
- [ ] **Compare to last year.** ⚠️ Resolve the conflict first: iPhone 17 Pro Max started at
      **$1,199 or $1,249** — reports disagree. Check Apple's own site before writing the delta.

**→ Then pick the fork in `SCRIPT.md` beat 15:**
- **FORK A** — prices rose → cost passed to the customer
- **FORK B** — prices held → cost absorbed; the story moves to the gross margin line

### E. The launch cycle `[[SLOT — beat 20]]`
- [ ] **Is the standard iPhone 18 absent from this event?** Beat 20 leans on this
- [ ] Any stated spring 2027 timing?
- [ ] Ship / pre-order dates for what was announced
- [ ] Timestamp: ______

### F. Quotes worth keeping verbatim
Anything about cost, manufacturing, silicon, or "most advanced chip we've ever built."

| Quote | Speaker | Timestamp |
|---|---|---|
| | | |

---

## IMMEDIATELY AFTER THE KEYNOTE

1. **Fill the slots** in `paradocs-longform-2/SCRIPT.md` and `paradocs-short-3/SCRIPT.md`.
2. **Pick the fork** (beat 15) and delete the unused one.
3. **Re-verify the two LOW-confidence rows** in the fact table — last year's price, and
   anything the leak got wrong.
4. **Check the Ternus/CEO line** in beat 1 against what actually happened on stage.
5. Render. Order below.

---

## RENDER ORDER

`paradocs-short-4` has **no slots** — nothing in it depends on the keynote. It can render now,
in parallel with the event.

| # | Piece | Blocked on event? | Settings |
|---|---|---|---|
| 1 | **`paradocs-short-4`** — "Moore's Law Was Never About Speed" | ❌ **No — render now** | portrait 9:16 |
| 2 | `paradocs-short-3` — "The $30,000 Wafer" | ⚠️ One slot (the close) | portrait 9:16 |
| 3 | `paradocs-longform-2` — the long-form | ✅ Yes | **landscape 16:9** |

**All three:** `mode: chat` · style `e7f9a12679ec426099db7646b70a4639` ·
voice `0db3abd83c74452fb2460b0dd113daad`

**Credits:** HeyGen showed **129 premium** (resets 2026-10-06) as of this morning. The 11-minute
long-form is affordable, but re-check `get_current_user` before firing the long-form — render it
**last**, so a failed short doesn't eat the budget for the main piece.

**On every render:**
- Restate the constraints at blueprint approval (chat mode pauses for it) — grade, bookend,
  hero shot, and **make every number count up**. That restatement is what makes them survive
  generation.
- Expect `caption.enabled: false` — it has happened on all four renders so far. **Publish the
  `captioned_video_url` cut, not the bare one.**
- Verify the **"Educational only. Not financial advice."** card exists in the first 4 seconds.
  `paradocs-longform-1` appears to be missing it.

---

## PUBLISHING ORDER

Long-form first, then the shorts as feeders pointing at it — `LONGFORM-GUIDE.md` §5. Short 4
is the strongest factually (it rests on a published 1965 document rather than on leaked wafer
prices), so it is the safest one to lead with if you want something out during the news cycle.
