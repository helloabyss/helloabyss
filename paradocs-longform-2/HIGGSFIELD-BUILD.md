# Higgsfield explainer — `higgsfield-prompt.txt` (4,998 chars)

A 5,000-character version of the explainer, rewritten to Higgsfield's own conventions rather
than relabelled from the HeyGen brief.

⚠️ **Higgsfield is at 0 credits** (plan `starter`), re-checked today. I can't generate there —
this is a paste-ready prompt for the Higgsfield UI, the same arrangement as the HeyGen app path.

## What the character budget cost

The HeyGen script is 1,348 words / 8,189 characters. **The script alone is 64% over a
5,000-character budget**, so a shorter video was unavoidable.

| | HeyGen version | Higgsfield version |
|---|---|---|
| Narration | 1,348 words | **473 words** |
| Runtime | ~8 min | **~2.9 min** |
| Beats | all 16 | 11 |

**Every figure survived** — $30,000, $25–27,000, 10–20%, $725M, $15–20B, $1,199, $1,299, +$100,
the $200–300 analyst range, the feared 50%, and 1965. Trimming came out of connective prose, not
evidence.

**The mandatory counter-evidence beat survived intact** — the unaudited-figure caveat, "a wafer
is one input among many", "below the fear", and the premiumisation counter-argument are all
still there. `CLAUDE.md` makes that beat non-negotiable and it was never a candidate for cuts.

**Beats dropped:** the Ford/railway-style historical parallels, the second-order city effects,
the "what it means for you" trio, and the full recap. The argument still lands; the payoff is
thinner.

## What changed for Higgsfield specifically

Read from the platform's own `faceless-video` workflow (v2.4):

- **Blocks, not scenes.** Higgsfield builds one 10-second block at a time, each containing
  **five hard-cut shots of ~2s**, no shot over 2.5s. The prompt asks for ~18 blocks and states
  that structure explicitly — HeyGen's "20–30s scenes" instruction would fight the engine.
- **"Never an object on a blank background"** is one of its own golden rules, and it happens to
  match this channel's imagery-first rule exactly. Stated in the prompt in its language.
- **No real brand names in visual prompts** — also a platform rule (its rule 10), and it lines
  up with the house no-logos rule. Apple is named **once in narration only**; every visual
  instruction is brand-free and asks for generic forms.
- **Aspect ratio must be explicit** — it does not inherit. `16:9` is stated in the first line.
- **No lip-sync, external narrator** — matches the faceless format already.

## Still enforced
Near-black/white/one-red palette · dark desaturated grade · no faces or identifiable people ·
no logos or badges · no device resembling a real product · no neon, gradients, sparkles, flare
or emoji · **"Educational only. Not financial advice." in the first 4 seconds** · the on-screen
wafer-price footnote · hero wafer shot · stage bookend.

## Verify before publishing
Same checklist as `HEYGEN-APP-BUILD.md`, plus two Higgsfield-specific ones:
1. **Count the cuts.** The workflow warns its own model under-delivers — asking for 5 cuts per
   block can return ~4s frames, which reads as a slideshow. If shots hang, regenerate that block
   with the cuts spelled out shot by shot.
2. **Check no logo crept into a frame.** The narration names Apple, which raises the odds of the
   image model volunteering a mark the prompt forbids.

## Which platform to use
**HeyGen app remains the recommendation** for the flagship: it has credits (54), it carries the
full 8-minute script, and its blueprint step lets you approve before spending. This Higgsfield
version is the better option if you want a **tighter 3-minute cut** — as a second edit of the
same story, or if Higgsfield gets topped up and HeyGen's balance is needed elsewhere.

The two are not redundant. A 3-minute cut and an 8-minute cut of the same thesis are different
products, and the shorter one travels further.
