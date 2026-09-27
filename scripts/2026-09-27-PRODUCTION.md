# Production — This Week in Tech, 2026-09-27

## Deliverables
| Asset | URL |
|---|---|
| **Video** — 50.40s · 1080×1920 · 30fps · H.264 CRF 20 · AAC 160k · 57.4MB | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/f7f6cc0d-59a1-4bec-840f-5fd5ddcd7a2c.mp4` |
| Thumbnail 1280×720 | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/3f26f652-5739-42e4-a8f9-eff8313dd174.jpg` |
| Thumbnail 1080×1920 | `https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/1a9b62ed-b07d-4863-9a03-0a537860956a.jpg` |

## Spend — reconciled against the transaction log
| Item | Qty | Each | Total |
|---|---:|---:|---:|
| GPT Image 2.5 plates (13 × 9:16, 1 × 16:9) | 14 | 0.25 | 3.50 |
| Seed Audio narration, 142 words | 1 | **5.70** | 5.70 |
| **Episode** | | | **9.20** |

Balance 526.30 → 517.10. Rendering, grading, alignment and thumbnails ran in the sandbox at no credit cost.
Rate-limited (429) submissions were not charged.

**Correction to earlier notes:** Seed Audio is priced by length, not flat. The `get_cost` preflight
used a one-line test prompt, which returned 0.30. Real narration costs roughly 1.8–5.7 depending on
length. Earlier per-item breakdowns that assumed 0.30 per narration were wrong; the lane *totals*
were right, because they came from balance differences.

**Not ours:** five GPT Image charges of 2.75 each (13.75 total) on 2026-09-25 01:33–01:37 UTC.
No session work ran then. Someone else is using this Higgsfield account, or these are manual generations.

## Voice
Callan `d8061b90-ff25-5882-8384-7a6a28806f30`, seed_audio, native speed, internal pauses capped at 0.30s.
Raw read → 50.39s after the pause cap. **Measured 169 WPM** (142 words / 50.39s). That is faster than the
152 WPM HeyGen planning rate in `VO_PROFILE.md` §3, because the cap removes padding. It lands inside
50–60s, but only just. **Suggestion for the channel owner, not applied:** add a Callan row to §3's
measurement table. `VO_PROFILE.md` is unchanged.

## Pipeline notes
- **Captions:** word-level difflib alignment against faster-whisper. 129/149 tokens matched directly;
  the 20 that whisper wrote differently (for example "20" for "twenty") are interpolated. Minimum 0.55s
  burned-in, 0.6s in the SRT.
- **raw.githubusercontent.com caches branch paths.** One render pulled a stale `build.py`. Always pin
  sandbox pulls to a **commit SHA**. This render used `b7a9e036…`.
- `pkill -f <pattern>` kills the sandbox's own shell when the pattern appears in the command. Filter by PID.

## Verification checklist
- [x] 142 words, inside the 135–142 band. **Measured 50.40s**, inside 50–60s
- [x] Hook payoff lands at **3.98s** ("The capital of France."). Headline text is on screen from frame 1
- [x] Longest sentence 13 words. No comma list of 4+ items
- [x] No banned words, no SSML, no bare numerals
- [x] `-vo.txt` == spec sentences == audio prompt == SRT text (mechanical diff, all verbatim)
- [x] Every claim sourced in the description. Company claims labelled on screen
- [x] Announced vs available correct: Gen 3 "on sale now"; VR Glasses "next spring"; RAIBO2 "published this week", race dated 2024 on screen
- [x] Nothing from `ARCHIVE.md` reused
- [x] Compliance card: **not needed.** No valuation, funding round or market move quoted
- [~] Pronunciation: the HeyGen `brandGlossaryId` does not apply to Higgsfield seed_audio. The terms at risk were DNS, VR, AI, Ray-Ban, Qualcomm and gigahertz. Whisper transcribed them back cleanly, which is strong evidence but not a listen
- [ ] **Watched by a human.** Verified numerically and against local stand-in-plate QA frames. The CDN is unreachable from here: *complete, not verified*
