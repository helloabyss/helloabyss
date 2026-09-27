# Opus 5.5 Short, v3: A/B remake

**Why:** the owner rejected v1/v2 as "horrible": slideshow, no motion, dark, too much text, no
music, flat energy, a script that didn't *show* Opus 5.5 doing anything, and background images
reused from the Grok 4.7 Short. v3 rewrites the script around real work done in this session
(see `2026-09-27-opus55-v3-facts.md`) and makes it two ways for the owner to pick.

Script: `2026-09-27-opus55-v3-vo.txt` (99 words). Both versions use the same verbatim narration
in Alex Wright's voice.

## A: HeyGen Video Agent

| Setting | Value |
|---|---|
| Session | `28e1c068cec740fea92e1d0d076d0a09` (https://app.heygen.com/video-agent/28e1c068cec740fea92e1d0d076d0a09) |
| Style / voice | Economist `e7f9a12679ec426099db7646b70a4639` / Alex Wright `0db3abd83c74452fb2460b0dd113daad` |
| Mode / orientation | chat / portrait |
| Glossary | `c7cb764ee025432caa879e8d76048c7f` |
| Blueprint | Agent timed it at ~42 s to keep the VO verbatim; approved as is |
| Output | video `0ab25010503441d1bb3e707a7e95a9ee`, 40.39 s, 1080×1920 (https://app.heygen.com/videos/0ab25010503441d1bb3e707a7e95a9ee) |

## B: rebuilt engine (`build/opus55v3/`)

| Item | Value |
|---|---|
| Output | Higgsfield media `d131067b-6729-4a73-9e62-a43febf5bfbf`, 43.83 s, 1080×1920, h264/aac |
| Engine | `motion.html`: 9 fully animated scenes, no static slides |
| VO | HeyGen `create_speech`, Alex Wright, 42.92 s; word timestamps → `words.json` (no whisper needed) |
| Captions | Word-by-word, 1–3 word groups (≤15 chars), current word amber with pop, y≈1500 (clear of Shorts UI) |
| Music | HeyGen library track `d3d4fddb…` ("energetic driving electronic"), sidechain-ducked under VO |
| Loudness | −14.6 LUFS integrated, −1.4 dBTP peak; music ≈ −22 dB in VO gaps |
| Imagery | 2 new images only (robot on road, rocket on pad), graded brighter, no reuse from earlier Shorts |
| Render | `render.sh` in the Higgsfield sandbox, code pinned to commit `26cfa0f` |

Changes vs v2, one per complaint:

- **Slideshow / no motion.** Every scene animates: lane race with counters, a scrolling checklist, an
  equation, a strike-through, a stamp with shake, a title slam, bar growth, a price shrink. There are
  whip-in camera moves on each cut.
- **Dark.** Alternates paper-white and near-black scenes, and the photos are graded brighter.
- **Too much text.** One idea per scene. Captions carry the words.
- **No music.** There is now a ducked electronic bed.
- **Didn't show the power of Opus 5.5.** The script now is the receipts: 3 parallel agents,
  17 stories, 2 real catches.
- **Reused images.** Two fresh images; no server corridors, monoliths or coins.

Layout was checked on locally rendered frames before the sandbox render (overlaps fixed:
caption crowding, OPUS/5.5 collision, date pill vs caption).

## Constraints hit

- Higgsfield video models (seedance_2_5, 35 cr / 5 s) need a higher plan tier and were refused.
  Nothing was charged. B uses animated graphics and moving photos instead.
- The CDN is still unreachable from this container. The final MP4 was checked in the sandbox by
  ffprobe, sampled frames and loudness, but has not been watched end to end. **Complete, not
  verified by eye.**

## Spend

| Item | Cost |
|---|---|
| Higgsfield gpt_image_2_5 × 2 | 0.5 credits |
| Higgsfield seedance preflight / refused | 0 |
| **Higgsfield "Seed Audio 1.0" −6.9 at 21:45:37Z** | **Not requested by this session.** No generate_audio call was made. Unexplained, like the five 2.75 charges on Sep 25. Owner to check the Higgsfield history. |
| HeyGen create_speech + Video Agent (A) | 29 premium credits combined (141 → 112) |

Balances after: Higgsfield 505.1 (from 512.5), HeyGen 112 premium (reset 2026-10-06).

## Verification checklist (owner)

- [ ] A and B: VO is word-for-word, in Alex Wright's voice
- [ ] Disclosure card visible in the first 4 s
- [ ] B: captions track the voice word by word; nothing overlaps
- [ ] B: robot and rocket images are clean (no garbled text or logos)
- [ ] Music audible but never over the voice
- [ ] Pick A or B (or elements of both) as the channel's template going forward
