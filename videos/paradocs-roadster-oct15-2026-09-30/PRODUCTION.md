# Production — PARADOCS10X Roadster "another date" Short (2026-09-30)

**Status: COMPLETE, NOT VERIFIED** (submitted and completed 2026-09-30; CDN blocked, so not watched)

| | |
|---|---|
| Session | `a6e9cc3b5dc14df4ada077135620e8f6` · https://app.heygen.com/video-agent/a6e9cc3b5dc14df4ada077135620e8f6 |
| video_id | `ab86416b92974d2497ae541086bb6689` |
| Mode | `generate`, portrait, Economist style `e7f9a126…`, glossary `c9064148…` |
| Voice | **Sheldon - Voice** `f925838e942b4f43838bafa25abac051` (private clone, status complete, default engine elevenlabs_v3), per owner instruction 2026-09-30. Not Alex Wright. |
| Visuals | Motion graphics only, no B-roll: the budget allowed ~22 credits, and B-roll bills ~60 cr/min |
| Budget | ~22 credits est. against a 28 balance (41 on 9/28; 13 were spent outside this session) |

The full brief is in the session's first message (same text as the `create_video_agent` call). It mirrors `SCRIPT.md`.

## Verification checklist (CDN blocked, so the render will be *complete, not verified*)
- [ ] `get_video_scenes`: Sheldon voice on every scene, script verbatim, zero avatar elements, 9:16
- [ ] Watch in HeyGen: no Tesla logo, no car imagery, no faces; the palette stays near-black, white and red
- [ ] "OCT 1" struck → "OCT 15"; "82%" labelled as a forecast; the quote card attributed to Tesla, Sep 28
- [ ] "Educational only. Not financial advice." within 4 s
- [ ] Publish the `captioned_video_url` cut (generate mode disables inline captions)
- [ ] Post by Sun 10/4, never on or after Oct 15

## Owner-supplied clips → CapCut inserts (2026-09-30, 0 credits)

The owner supplied three clips. Two are AI-generated Roadster shots, made into inserts here. They can't go into the HeyGen render:
it can't be downloaded from here, and a re-render has no credits. So they go on over the render in CapCut.

| File (`inserts/`) | Source | Treatment |
|---|---|---|
| `roadster-thrusters-ai-illustration-9x16.mp4` / `-band.mp4` | AI clip, car lifting on thrusters (1280×720, 6.0 s) | Tesla "T" badge tracked (OpenCV template match, all 145 frames) and blurred; graded dark and desaturated; label "AI ILLUSTRATION · NOT REAL FOOTAGE"; muted |
| `roadster-coast-ai-illustration-9x16.mp4` / `-band.mp4` | AI clip, coastal road at sunset (736×400, 6.0 s) | Same |

- `-9x16` is full frame (1080×1920, blurred fill). `-band` is only the picture plus label (1080×~700), so the burned-in captions in the
  bottom third stay visible. **Use the band versions over the captioned cut.**
- Placement (estimated at 150 wpm; confirm against the render's timing):
  - thrusters on "The reveal was set for October 1st, outdoors near Waco" (~0:04–0:08, **after** the 4 s compliance card);
  - coast on "The Roadster was unveiled in 2017, with production promised for 2020" (~0:15–0:20). Trim each to 3–4 s.
- Keep the label on screen, and turn on YouTube's altered/synthetic content disclosure. The thruster shot shows something Tesla
  has not demonstrated.
- The third clip (`PARADOCS10X_short1_oct1_reveal.mp4`, 12 s) is **not used**. Its "Oct 1 is a reveal" line is now out of date.

## Result — completed 2026-09-30

**"Tesla Roadster: Another Date"** · `ab86416b92974d2497ae541086bb6689` · **41.12 s** · 9:16 · 1080p · 10 scenes ·
watch: https://app.heygen.com/videos/ab86416b92974d2497ae541086bb6689

| Check (`get_video_scenes`) | Result |
|---|---|
| Voice `f925838e…` (Sheldon - Voice) on all 10 scenes, ElevenLabs engine, speed 1.1 | **PASS** |
| Script verbatim: 435 chars, exact match to `scripts/2026-09-30-paradocs-roadster-oct15-vo.txt` | **PASS** |
| Faceless: 10 `motion_graphics` elements, **zero** avatar elements | **PASS** |
| 9:16, 1080p | **PASS** |
| `caption.enabled` false; `captioned_video_url` **populated** | Publish the captioned cut |

**Cost: 24 credits (28 → 4) = 35.0 cr/min.** This is below the ~40 cr/min estimate for motion graphics. The runtime came out
~8 s longer than the 30 s planned, even at speed 1.1, so HeyGen appears to add holds and a closing beat.

**UNKNOWN — needs eyes:**
- **Palette.** Every scene's background is set to `#ffffff`. The full-frame motion-graphics plates probably cover it,
  but `get_video_scenes` can't show the plate content. Check that it reads near-black, white and red, not white.
- No logo or car imagery, compliance card within 4 s, and the "82%" labelled as a forecast.
