# STYLE.md — This Week in Tech (TWiT), series bible

A weekly **faceless** YouTube Short. 50–60 seconds, vertical, one week of tech news.
No presenter on camera. Every second is voiceover over B-roll, screen recordings, motion
graphics and kinetic text.

Narration settings live in `VO_PROFILE.md` and are locked. This file governs everything
else: what the show sounds like in writing, how it is built, and what it looks like.

---

## 0. Relationship to `STYLE-GUIDE.md` — read this first

This repo already holds `STYLE-GUIDE.md`, the locked visual identity of the **faceless
finance channel** (`pdt-short`, `moat-short`, `paradocs-short-1`). **This Week in Tech is a
separate series with its own look**, decided by the channel owner on 2026-09-20.

Three places TWiT deliberately diverges, and why:

| Rule in `STYLE-GUIDE.md` | TWiT | Why |
|---|---|---|
| Near-black / white / **one red** accent | Near-black / off-white / **one amber** accent | Keeps the two series visually distinct on the same channel surface. Same three-colour discipline, different accent. |
| **No real corporate logos** anywhere | Real logos appear **only inside attributed third-party footage** | A tech news show runs on press-kit clips and screen recordings. A product reveal with the product's branding scrubbed is not reporting. The channel's *own* motion graphics stay logo-free and use plain text name-tags, exactly as the finance channel does. |
| **No identifiable people** at all | No *presenter*; third-party footage **may** contain people, attributed on screen | "Faceless" here means the channel has no host and no avatar. A keynote clip of an executive announcing the thing is the news. |

Everything else carries over unchanged and is **not** open for reinterpretation: imagery
first, dark and desaturated grade, continuous motion, burned-in captions, no clickbait, no
subscribe animations, no emoji, no sparkles, no neon.

`CLAUDE.md`'s compliance card ("Educational only. Not financial advice.") is a
**finance-channel** requirement and does not apply to a tech news Short — **unless** a beat
quotes a valuation, a funding round, a share price or a market move. When it does, carry the
card for that episode. The week of 2026-09-20 dropped its only such story (SoftBank/OpenAI)
at the scoring stage, so no card is needed; re-check every week.

---

## 1. Written voice

Fast, warm, genuinely excited — a smart friend who read everything so you didn't have to.

- **Concrete numbers over adjectives.** Not "a huge field of view" — "fifty-one degrees".
- **No jargon without a five-word explanation.** "AR glasses — screens in the lenses."
- **Short clauses.** 8–14 words per sentence (`VO_PROFILE.md` §4).
- **Say what is true about shipping.** "Announced", "opened pre-orders", "in beta", "ships
  in fall" — never "released" for a thing you cannot buy today. Always give the real
  availability date.
- **Admit the weak part.** Every beat that can carry a caveat, carries it: the subscription
  tier, the beta label, the hardware requirement, the fact that a claimed benchmark is a
  company claim. This is the difference between the show and a press-release reader.

### Banned outright
`game-changer` · `revolutionary` · `insane` · `breaking the internet` · `you won't believe`

Also banned, as house preference: "literally" as intensifier, "quietly" as in "X quietly
launched", rhetorical questions in the body (the *close* gets the only question), and any
sentence beginning "And the best part?"

### No clickbait
No "what they don't want you to know". No subscribe animations. No arrows drawn on faces.
The hook is the wildest **fact**, stated plainly — the fact does the work.

---

## 2. Format

| | |
|---|---|
| Runtime | **50–60 seconds**, hard |
| Word count | **135–142 words**, aim 138 — derived in `VO_PROFILE.md` §3, never guessed |
| Aspect | 9:16 vertical, 1080×1920 |
| Frame rate | 30fps |
| Structure | cold-open hook → 3 beats → wildcard close |

### Beat map

| Segment | Length | Content |
|---|---|---|
| **Hook** | 0:00–0:04 | The single wildest fact of the week. No intro, no "hey guys", no channel name, no logo sting. First frame is already the story. |
| **Beat 1–3** | ~12s each | One story each: **what happened**, then **why it matters**. Date it. Caveat it. |
| **Wildcard** | ~14s | The weird/fun one. Closes on a specific question that earns comments. |

The wildcard is not filler. It is the reason the episode gets watched to the end and the
only place the show is allowed to be delighted rather than precise.

---

## 3. Visual system — define once, reuse weekly

Episodes must look like siblings. These values do not change week to week.

### Palette
| Role | Hex | Use |
|---|---|---|
| Base | `#0B0B0D` | Background, letterbox, scrims |
| Type | `#F2F2F0` | Captions, body type |
| **Accent** | `#FFB020` | Lower-third rule, highlight word, counters, the transition wipe |
| Caution | `#8A8A86` | Source attributions, footnotes, de-emphasised type |

One accent. Amber is the show's signature — it is never joined by a second accent colour,
and it is never used on footage, only on graphics and type.

### Type
- **Captions & hero type:** Inter Tight ExtraBold.
- **Lower-thirds & attribution:** Inter Tight Medium.
- All-caps for hero words and lower-third titles. Sentence case for captions.

### Captions (burned in)
- Word-by-word, **current word highlighted in `#FFB020`**.
- Bottom third, safe area: **≥ 420px from the bottom** of a 1920px frame — clear of the
  YouTube Shorts UI, which eats the lower ~15%.
- `#F2F2F0` fill, 4px `#0B0B0D` stroke, plus a 60%-opacity `#0B0B0D` scrim wherever the
  plate underneath is busy.
- Max 4 words visible at once. Assume muted viewing.
- **SRT sidecar** cues follow the same text, but allow up to 5 words with a **0.6s minimum
  cue duration** — a sub-half-second caption flashes and cannot be read.

### Lower-third (every story beat)
Appears on the first frame of each beat, holds ~2s, wipes out:
```
┌────────────────────────────────
│ ███ 2px amber rule
│ STORY TITLE            ← Inter Tight ExtraBold, all caps, #F2F2F0
│ Source · Sept 16       ← Inter Tight Medium, #8A8A86
└────────────────────────────────
```
Left-aligned, 80px from frame left, sitting above the caption band.

### The recurring transition
**The amber wipe.** Between every beat, without exception:
1. A 6px `#FFB020` vertical rule enters from frame right and sweeps left across the frame.
2. The outgoing shot travels left with it; the incoming shot is revealed behind it.
3. 2-frame `#0B0B0D` flash on the handover.
4. Total: 8 frames.

This is the show's punctuation. Viewers should be able to identify the series from the
transition alone with the sound off.

### On-screen source attribution
Any third-party footage carries its source in `#8A8A86`, bottom-left, for as long as the
footage is on screen. Non-negotiable — it is both the licence condition and the credibility.

### Motion
- **No static image longer than 2.5 seconds.** Ever. If a shot has to hold, it gets a slow
  push, a parallax drift or a counter running over it.
- Cut or punch in every 1.2–2.0s.
- Camera moves on the **imagery**, not only the type.
- Numbers count up. They never simply appear.
- Screen recordings: cursor visible and moving, 1.4× scale so UI reads at phone size.

### Banned visually
Neon glows · rainbow gradients · sparkles · lens flare · emoji · countdown timers ·
subscribe animations · clickbait arrows · stock "hacker in a hoodie" · spinning globes ·
any AI-generated footage presented as real product footage.

---

## 4. Rules

1. **Every factual claim traces to a linked primary source.** Unsourced means cut. Not
   softened — cut.
2. **"Announced" ≠ "released."** If it has not shipped, say so, and give the real
   availability date.
3. **On-screen source attribution** for any third-party footage.
4. **Never repeat an `ARCHIVE.md` story.** Check before scoring, not after writing.
5. **Licensing is checked before a clip enters the manifest.** Anything unclear gets
   replaced, not risked.
6. **The narration file and the timecoded script must match verbatim.** Any drift is a bug.
7. **Company claims are labelled as company claims.** "Huawei says", "Nvidia's CEO
   forecasts" — never stated as measured fact.
8. **Runtime is fixed by cutting words, never by changing voice speed** (`VO_PROFILE.md` §2).

---

## 5. Weekly deliverables

| File | Contents |
|---|---|
| `research/YYYY-MM-DD.md` | 12–20 scored candidates, each with date, link, source type |
| `scripts/YYYY-MM-DD.md` | Script + shot list + asset manifest + packaging |
| `scripts/YYYY-MM-DD-vo.txt` | Narration only, generator-ready |
| `scripts/YYYY-MM-DD.srt` | Caption file |
| `ARCHIVE.md` | Updated with every story covered |

Run with `/twit`.
