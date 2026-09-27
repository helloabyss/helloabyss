# Opus 5.5 Short, v4

**Owner feedback on v3:** "I like B. I don't understand the script. I love the b roll and the
added background sounds. It's supposed to be about opus 5.5."

v4 keeps B's look (animated graphics, moving B-roll, word-by-word amber captions, ducked music)
and replaces the script. The old one was about the research process; v4 covers what Opus 5.5 is,
how it compares, what it costs, the catch, and what to do next.

| Item | Value |
|---|---|
| Output | Higgsfield media `599c357c-6978-4fca-860e-6bbeea062d49`, 50.03 s, 1080×1920 |
| Link | https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/599c357c-6978-4fca-860e-6bbeea062d49.mp4 |
| Script / facts | `2026-09-27-opus55-v4-vo.txt` (106 words) · `2026-09-27-opus55-v4-facts.md` |
| VO | HeyGen `create_speech`, Alex Wright, 49.11 s, word timestamps in `build/opus55v4/words.json` |
| Engine | `build/opus55v4/motion.html`, render `render.sh` at commit `629052f` |
| B-roll (new) | laptop with code, two equal chess kings (parity with Fable), running track (speed), magnifier over charts (the catch) |
| Graphics | FASTER/CHEAPER punch-ins, title slam, SEP 22 calendar flip, Terminal-Bench bars 66.4 vs 55.8, +30% counter, old→new price strike, "Anthropic's own numbers" stamp, 2-step checklist close |
| Audio | Same music bed as v3 (`d3d4fddb…`, looped, sidechain-ducked), plus a "Fast airy whoosh" SFX (`a4855a82…`) peaking on each of the 8 cuts |
| Loudness | −14.8 LUFS integrated |

Scene cuts (s): 4.01 · 7.15 · 9.53 · 16.69 · 24.24 · 27.84 · 37.46 · 42.98.

## Verification

Layout was checked on locally rendered frames. The final file was checked in the sandbox for
duration, loudness, whooshes at the cuts and B-roll brightness (mean luma 104–175). It has not
been watched end to end here (CDN blocked). **Complete, not verified by eye.**

- [ ] Captions track Alex Wright word by word
- [ ] The four B-roll images contain no garbled text or logos
- [ ] Whooshes feel tight, not cluttered (8 in 50 s)
- [ ] 50 s is acceptable (Shorts max 60 s)

## Spend

| Item | Cost |
|---|---|
| Higgsfield gpt_image_2_5 × 4 | 1.0 credit |
| HeyGen create_speech (106 words) | ~2–3 premium credits |
| Music + SFX (HeyGen library) | 0 |
