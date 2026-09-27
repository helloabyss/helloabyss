# STANDARD.md — the approved Short

**Owner sign-off, 2026-09-27: "This is the standard."** Every Short is built to this spec.
Where another doc disagrees with it (for example the dark grade in `STYLE-GUIDE.md` §3 or the cut
rate in §2), this file wins for engine-built Shorts.

**Reference episode:** Claude Opus 5.5, v4 (50 s)
https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/599c357c-6978-4fca-860e-6bbeea062d49.mp4
Files: `build/opus55v4/` (`scenes.js`, `words.json`; `motion.html` is the frozen original) ·
`scripts/2026-09-27-opus55-v4-*` (script, fact table, production record).

## What the owner asked for, and against

| Approved (v4) | Rejected (v1–v3) |
|---|---|
| "I like B", which is the engine build rather than the HeyGen Video Agent | Slideshow of stills, no motion |
| "I love the B-roll and the added background sounds" | Dark, too much on-screen text, flat energy |
| A script that is about the subject: "It's supposed to be about Opus 5.5" | No music; a script about our own process (v3) that viewers couldn't follow |
| | Background images reused across videos ("sloppy") |

---

## 1. Script

- **About the subject, every sentence.** No meta story about how the video was made. That
  goes in a small disclosure card, not the narration.
- **~100–110 words, about 50 s** at Alex Wright's native pace. Short declarative sentences, one idea each.
- **Beat order:** hook (what happened and why you should care, ≤4 s) → name it (by 6 s) → what
  it is, with the vendor's headline claim labelled as a claim → 2–3 concrete numbers, one per sentence →
  **the catch** (mandatory: who says so, what isn't proven) → **one action** the viewer can take.
- Numbers are spelled as spoken. Every figure goes in `scripts/<date>-<slug>-facts.md` with a source and a confidence level.
  Verify with a web search first (`CLAUDE.md`).

## 2. Scenes

- **8–10 scenes**, cut on sentence starts, **0.12–0.15 s before the first word** (`CUTS` in `scenes.js`).
- **Alternate B-roll scenes and graphic scenes.** Never two B-roll scenes back to back.
- **Everything moves, always.** B-roll uses `cover()` (push 1.12→1.34 plus a pan). Graphic scenes enter
  with `camera()` (whip-in scale, slide and tilt) and keep a slow drift. A B-roll scene longer than
  about 6 s gets a hard punch-in reframe mid-scene (v4 scene 3).
- **Things land on the spoken word.** Every pop, stamp, counter and strike is keyed with `at('word')`.
- **One idea per scene, ≤6 words of graphic text** besides numbers. The captions carry the sentence.
- **Vendor claims are labelled on screen**, for example `ANTHROPIC'S CLAIM` or `Anthropic's estimate`.

**Scene vocabulary** (all in `build/opus55v4/scenes.js`; copy and adapt):

| Scene type | Use for | v4 example |
|---|---|---|
| B-roll + word punch-ins | Hook | laptop + FASTER / CHEAPER pills |
| Title slam | Naming the subject | CLAUDE / OPUS / 5.5 on paper |
| Calendar flip | Dates | SEP 22 |
| B-roll + comparison label | Parity or versus claims | chess kings + OPUS 5.5 ≈ FABLE 5.1 |
| Racing bars with counters | Benchmarks, head-to-head numbers | 66.4% vs 55.8% |
| B-roll + big counter + radial streaks | Speed, growth | running track + "+30%" |
| Old price struck → new price rolls | Price changes | $5/$25 → $4/$20 |
| B-roll + stamp | The catch | magnifier + ANTHROPIC'S OWN NUMBERS |
| Numbered checklist | Action close | rerun one job / compare the bill |

## 3. B-roll

- **3–5 fresh images per video.** `gpt_image_2_5`, 9:16, 0.25 credits each. **Never reuse an
  image from another video.**
- **One concrete visual metaphor per beat.** v4 used equal chess kings for parity, a running track for speed and
  a magnifier over charts for the catch.
- Prompt pattern: `Photograph: <subject>, <angle>, bright <light>, crisp, cinematic 35mm. No people, no text, no logos.`
- Grade in the render: `-modulate 104,92 -sigmoidal-contrast 3,50%`. The result is **bright**, not dark.
- Higgsfield video models are refused on the current plan. Motion comes from the engine.

## 4. Look

| Token | Value |
|---|---|
| Ink / paper | `#0B0B0D` / `#F4F3EF`, alternating by scene |
| Accent | `#FFB020` amber (tech series). The finance series swaps in its red. |
| Negative | `#FF4A3D`, only for strikes, stamps and "NOT" |
| Type | Montserrat 800–900, fallback Liberation Sans |
| Chrome | Accent progress bar at the top edge, light film grain, scrims only at the top and bottom of B-roll |

## 5. Captions

Word by word, in groups of 1–3 words (≤15 characters, broken at punctuation and pauses over 0.35 s).
The current word is in the accent colour with a small pop, spoken words are white and upcoming
words are dim. Captions sit at **y = 1500**, clear of the Shorts UI. Groups wider than 900 px shrink
to fit. Timing comes from `create_speech` `word_timestamps` (`build/standard/words.py`). No whisper is needed.

## 6. Audio

| Layer | Setting |
|---|---|
| VO | Alex Wright via HeyGen `create_speech` (`VO_PROFILE.md` §7), timing untouched so the captions stay locked |
| Music | HeyGen library `d3d4fddb25da4d95aee88f496e90242a` ("energetic driving electronic"), looped, volume 0.30, sidechain-ducked under the VO (threshold 0.03, ratio 6) |
| SFX | HeyGen `a4855a82116cd4cc` "Fast airy whoosh", its 0.45 s peak placed on **every cut**, volume 0.55 |
| Master | `loudnorm I=-14 TP=-1.5 LRA=11` |

The library URLs are signed for 7 days. Refresh them with `search_audio_sounds` (the ids stay the
same) and never commit them.

## 7. Required on screen

- First 4 s: `EDUCATIONAL ONLY. NOT FINANCIAL ADVICE.`, plus `MADE WITH CLAUDE OPUS 5.5` when the
  video is about an Anthropic model (disclosure).
- End card: `Sources in the description`.

## 8. Build pipeline

1. Research, then the script and fact table (§1).
2. Check HeyGen credits, then `create_speech` → save the JSON → `python3 build/standard/words.py speech.json build/<ep>/words.json`.
3. Generate the images (§3) with `generate_image_batch`.
4. Write `build/<ep>/scenes.js` (`IMAGES`, `CUTS`, `SC`), starting from `build/opus55v4/scenes.js`.
5. **Local layout check:** copy `core.js`, `boot.js` and `short.html` into a scratch dir with the
   episode files and placeholder jpgs, then run `build/standard/preview.js` at a timestamp inside every
   scene. Look at the contact sheet and fix overlaps before spending anything else.
6. Commit and push. Pin the render to that commit SHA, because raw.githubusercontent branch paths are cached.
7. `media_upload` gives the PUT URL. In the Higgsfield sandbox, write the env file (`EP`, `SHA`,
   `VO_URL`, `MUSIC_URL`, `WHOOSH_URL`, `IMG_<NAME>`, `PUT_URL`) and run
   `build/standard/render.sh` in the background. It takes about 3 min for 50 s.
8. After `PUT 200`, run `media_confirm`. Then check in the sandbox: duration, −14 ±1 LUFS, and
   B-roll mean luma ≥ 100.
9. Report the render as **complete, not verified by eye**, with the viewing checklist from the production record.

## 9. Cost per Short

About **1 Higgsfield credit** (4 images) + **about 3 HeyGen premium credits** (VO). Music, SFX and
rendering are free. Anything more needs the owner's go-ahead ("DON'T WASTE MY CREDITS").

## 10. Open question for the owner

`VO_PROFILE.md` §7 says to trim, loudnorm and **cap internal pauses at 0.30 s** before building.
v4 **kept `create_speech`'s natural pauses** (up to about 0.9 s) so the word timestamps drive the
captions and cuts directly, and that is the version the owner approved. `VO_PROFILE.md` changes only
on the owner's explicit words, so it is unchanged. Until the owner rules, follow v4 (natural pauses)
and log it as a known difference.
