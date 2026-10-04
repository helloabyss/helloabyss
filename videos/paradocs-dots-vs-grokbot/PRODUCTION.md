# Production: Dots vs Grok Bot (PARADOCS10X pipeline #11)

## Status, 2026-10-04
| Item | State |
|---|---|
| Long-form script | `vo-long.txt`, ~1,190 words (~7–8 min). Cold open is the verified OpenAI / Hugging Face sandbox escape |
| Short script | `vo-short.txt`, ~140 words (~45–50 s) |
| Facts | `FACTS.md`. Every claim has a source; company claims are labelled on screen |
| Visuals | 72 long-form scenes (`build/dots-long/scenes.js`), 15 Short scenes (`build/dots-short/scenes.js`) |
| B-roll | 24 images (`images.json`) and 15 Kling 3.0 motion clips (`clips.json`); every graphic scene sits on a moving plate |
| Long-form (final, stock voice) | Higgsfield Seed Audio preset **Callan**, 8 chapters voiced separately, pauses capped at 0.4 s, 1 s between chapters; script trimmed ~740 chars to fit the 40.35-credit balance; captions on, 15 Kling clips: https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/3ac1f250-4512-4e89-a350-97ed78825aa7.mp4 (6:26, 1920x1080, 7.1 Mb/s, -15.2 LUFS, -1.3 dBTP; 94% of script words aligned). Voice cost ~39.6 credits. Complete; sample frames checked, not watched end to end. |
| Short (final, stock voice) | Higgsfield Seed Audio preset voice **Callan** (owner chose a stock voice on 2026-10-04 while HeyGen credits are 0), pauses capped at 0.4 s (`VO_CAPGAP`), captions on, 15 Kling clips: https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/e151c879-5fe9-4c17-b65c-bd736996d290.mp4 (49.7 s, 1080x1920, 16 Mb/s). Voice cost 5.2 Higgsfield credits. Complete, not verified by eye. |
| Preview v5 | Cold open + chapter 1, footage-first, de-pixelated (clip VP9 crf 15 instead of crf 33 realtime, push 1.03-1.09x, x264 crf 16 at 14 Mb/s), no voice or captions: https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/6f72a3c8-975c-4cee-b49c-9b6ae8ab299d.mp4 (2:00, 1920x1080). |
| **Voice** | **Blocked.** The owner chose their own HeyGen voice, "Sheldon" (`a32f980daef743d49caae9e269d14346`, ElevenLabs engine via HeyGen; tested OK on 2026-10-03). HeyGen premium credits are 0 until **2026-10-06 12:57 UTC**. The full set needs ~33 credits (long ~30, Short ~3) |
| Thumbnail | `build/thumb/versus.html`: DOTS vs GROK BOT, `$100 vs $20` tag, standoff plate |
| Publish copy | `PUBLISH.md` |

## Voice log (owner's instructions)
- 2026-10-03: "Use Sheldon's voice from heygen. Just the voice not the avatar." This overrides VO_PROFILE's Alex Wright for this video.
- Callan (Higgsfield) and the ElevenLabs library voice "Sheldon Calm Voice (2025)" were both tried and abandoned at the owner's direction. The ElevenLabs free tier was then disabled ("unusual activity").
- Timbre check: HeyGen Sheldon voices 1 and 2 match (distance 0.23). The ElevenLabs "Sheldon Calm" did not (0.58); the owner says it is theirs.

## To finish (when HeyGen credits exist)
1. `create_speech`, voice `a32f980daef743d49caae9e269d14346`, `language:"en"` (no locale), in two parts (≤5,000 chars each): chapters 0–3 and 4–7. Concatenate with 0.35 s of silence. Then the Short.
2. Store the audio on Higgsfield (`media_upload`, PUT with `If-None-Match: *`).
3. Refresh the music and whoosh URLs with `search_audio_sounds` (ids `bc09667f…` music, `a4855a82…` whoosh); the signed URLs expire after 7 days.
4. `build/standard/render2.sh` with `EP=dots-long PAGE=long.html SCRIPT=…/vo-long.txt CLIPMAP=…/clips.json`. Alignment, 6-worker capture and mix are automatic.
5. The Short: `EP=dots-short PAGE=shortk.html SCRIPT=…/vo-short.txt`.
6. Render thumbnails from `versus.html` with the real standoff image.

## Spend (this video)
| Item | Credits |
|---|---|
| Higgsfield gpt_image_2_5 × 25 | ~6.25 |
| Higgsfield Kling 3.0 × 15 clips (5 s, std, no sound) | 112.5 |
| Higgsfield Seed Audio (Callan, before the owner switched voice) | ~30 |
| ElevenLabs (Sheldon Calm, part A + Short; not used in final) | 3,719 chars |
| HeyGen create_speech test line | 1 premium |
| vidIQ (outliers + 1 transcript) | ~10 |
| **Not this session:** Seed Audio spends of ~100 credits on 2026-10-04 01:18–01:55 UTC | — |

Higgsfield balance after: 80.75.

## 2026-10-04 notes

- Higgsfield upload URLs carry a short-lived STS token: request `media_upload` right before the PUT (a URL issued ~15 min before the PUT returned 400).
- Seed Audio leaves 4-11 s gaps at paragraph breaks; `VO_CAPGAP=0.4` (sox) took the Short from 82.7 s to 48.8 s.
- Long-form stock voice would cost ~45 Higgsfield credits (balance 40.35 after the Short). Long-form waits for the HeyGen Sheldon voice (credits reset 2026-10-06 12:57 UTC) unless the owner tops up.
- Unexplained Seed Audio spend on the account, not from this session: ~100 credits 01:18-01:55 UTC and ~35 credits 02:01-02:14 UTC on 2026-10-04.
- Long-form render: Higgsfield upload returns 413 for very large files (crf 16 veryfast ~700 MB+); `MAXRATE=7M X264_PRESET=faster` gave 342 MB and uploaded. Seed Audio allows one job at a time on this account (parallel jobs fail and are refunded).
- 2026-10-04: owner approved the Callan versions ("Ok with callan"). The Oct 6 Sheldon re-voice routine was cancelled; no HeyGen credits will be spent on this video.
- Thumbnail (hero): one amber hero robot vs a blue crew (gpt_image_2_5, 0.25 credits; a second variant was dropped because it resembled a trademarked character), composited with `build/thumb/hero.html` (DOTS vs GROK BOT, $100 vs $20): https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/2fce7dfa-4e77-40c9-af16-4833575fe488.jpg (1280x720). Higgsfield balance after: ~0.35.
- Thumbnail v2 (owner: "bigger bolder fonts"): stacked DOTS / vs GROK BOT at ~2x size, heavier outline, $100 vs $20 pill on the floor: https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/8543a720-1f5a-488a-8cbe-fbbb0281280b.jpg (render: hero.html?tx=0.37&tagy=0.87). No credits spent.
