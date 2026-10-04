# Production: Dots vs Grok Bot (PARADOCS10X pipeline #11)

## Status, 2026-10-04
| Item | State |
|---|---|
| Long-form script | `vo-long.txt`, ~1,190 words (~7–8 min). Cold open is the verified OpenAI / Hugging Face sandbox escape |
| Short script | `vo-short.txt`, ~140 words (~45–50 s) |
| Facts | `FACTS.md`. Every claim has a source; company claims are labelled on screen |
| Visuals | 72 long-form scenes (`build/dots-long/scenes.js`), 15 Short scenes (`build/dots-short/scenes.js`) |
| B-roll | 24 images (`images.json`) and 15 Kling 3.0 motion clips (`clips.json`); every graphic scene sits on a moving plate |
| Preview | Cold open + chapter 1, no voice or captions: https://d2ol7oe51mr4n9.cloudfront.net/user_3IyooMrH11AlVriZuDqzIr96yrM/a4cc6506-f67b-4c2b-b840-f9028715a415.mp4 (2:00, 1920×1080; motion verified at every sample point) |
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
