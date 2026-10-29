# EIC SIGN-OFF v2: PX iPhone Duo Short
Reviewed Mon Oct 26, 2026, about 7:55-8:25 PM AZ (America/Phoenix). Master: video.mp4 (mtime 7:53 PM AZ); QA-GATE.md v2 (7:55 PM). This report is newer than both.
Method (all mine, not the builder's logs): ffprobe, ffmpeg ebur128 + loudnorm, frames every 0.5 s and every 0.1 s (720 frames) with tesseract --psm 11 at conf >= 60, frame-exact checks by frame number for the end plate, price overlay and callouts, faster-whisper float32 word timestamps (small.en and medium.en), 20 ms energy envelope.

## VERDICT: HOLD for 2 free fixes (one re-render, no ElevenLabs/Higgsfield/HeyGen credits). Nothing dropped or cut. Everything else PASSES. Window is fine: fix and post before Tue Oct 27 10:00 AM AZ.

## The 2 fixes (exact)
1. END PLATE, 58.367 to 58.733 s (frames 1751 to 1762, 0.40 s): "DROP A COMMENT" appears at 58.367 while the first plate lines "WILL THE DUO BEAT" are still on screen until 58.767. Whole frame there = WILL THE DUO BEAT SAMSUNG'S 200,000 FOLDS? + DROP A COMMENT = 10 words (gate is 8). The staging is set to replace at 58.35 but the old lines are only removed at 58.767. Fix: end "WILL THE DUO" and "BEAT" at 58.35 (same frame the green button starts), leaving SAMSUNG'S 200,000 FOLDS? + DROP A COMMENT = 6. Re-check frames 1745 to 1775.
2. MUSIC TAIL: the music stops hard at 58.87 s while still at about -19 dBFS, then 1.1 s of digital silence to 60.0 (audible cut, dead last frame of the loop). Fix: extend/loop the music bed to 60.0 s and apply a 0.8 s fade-out ending at 60.000 (keep VO/loudness untouched; re-run ebur128 and keep peak <= -1 dBTP; keep 60.000 s on both streams).

## Gate table (your list)
| Gate | Result | My evidence |
|---|---|---|
| Exactly 60.000 s, video+audio | PASS | ffprobe video 60.000000 s, 1800 frames, 30 fps; audio 60.000000 s (2810 AAC frames); container 60.000000. |
| Peak <= -1 dBTP | PASS | True peak -1.5 dBTP (ebur128), loudnorm input_tp -1.53; integrated -13.9 LUFS. |
| VO end ~56.9 s | PASS | whisper small.en and medium.en: "counter." ends 56.94 s. |
| No dead tail, visual change every 3 to 5 s | PASS (see fix 2 for audio) | 49.5-53.1 CNET shot with staged captions; 53.1-57.0 own progress bar with captions CNET STREAM RETURNS / TUESDAY 1PM ET / WATCH THE COUNTER and punches at 54.0 and 55.5; 57-60 plate with pull-out and the 58.37 staging change. Longest unchanged span 3.9 s. |
| Hook 0-2 s 'iPHONE DUO · $1,999' | PASS | Tag visible from frame 0 to about 1.9 s (APPLE LISTS / NO FOLD RATING above it); OCR reads "iPHONE DUO $1,999" at 1.0 and 1.5 s. |
| Captions <= 3 words | PASS | Seen: A DAY / DAY AND NIGHT, NO FOLD RATING, AND SAMSUNG, ISN'T DONE, ITS NEW AD, WORLD'S LIGHTEST FOLD, TUESDAY 1PM ET, OVER 138,000, FOLDS TO GO, ABOUT A WEEK. |
| Whole-frame overlay words <= 8 | FAIL only at fix 1 | 720-frame OCR max is 8 for overlay text; frames reading 9 to 11 words at 5.5-6.9 s and 32.2-33.0 s are footage text (Apple status bar 9:41/8:30AM, Samsung ad "Beautiful Moments") plus OCR noise tokens, acceptable. Count at 31.0 and 31.5 s is exactly 8 (61,227 200,000 OVER 138,000 FOLDS TO GO 31%). The end-plate overlap in fix 1 is real (10 words; OCR undercounts it, I counted from the frames). |
| Overlay right edge < x 900 | PASS | Every OCR token past x 900 is footage or noise (9:41 status bar, watermark, wide merged noise boxes); I viewed 14.0, 50.0, 52.5 and 57.5 s: overlay text right edges about 750 to 850. |
| Sync moves | PASS | AND SAMSUNG appears at 32.1-32.3 s vs whisper "And" 32.08-32.16 (on the new timeline = old ~29.95). ISN'T DONE appears at 32.70 s vs "isn't" 32.56-32.60 (+0.1 s, old ~30.50). Both inside 0.3 s. Whole-file whisper: 0.08 s p95 per QA; my spot checks agree. |
| CNET inset gone | PASS | No CNET inset on the procedural shot at 23.6-26.4 s or anywhere else; only the small CNET watermark inside CNET footage. |
| Thumbnails own graphics | PASS | thumb-A is a 61,227 bar graphic, thumb-B is a $1,999 plate; both 1080x1920, no CNET/Apple/Samsung pixels. |
| Third-party footage 24.65 s | PASS (advisory) | shots.json: CNET 17.07 s (cnet_d1_10000 4.95, cnet_day1_end 3.40 and 2.45, cnet_d1_20000 2.66, cnet_d1_30000 3.62), Apple intro video 3.80 s, Samsung ad 3.77 s (2.07 + 1.70). Total 24.64 s, all transformed with zooms, overlays and captions, no clip over 5 s. Plus three blurred, dimmed Apple/web screenshots (specs_view 4.3 s, word_p 3.7 s, dd_p 2.2 s) with a spotlight line. Advisory only: Content ID risk is medium for CNET and Samsung; description credits all three. |
| $1,999 punch-in vs "nineteen ninety nine dollars" | PASS | Overlay frame-exact: appears 7.05-7.10 s, held to 8.75 s (330 px punch-in). Speech energy: "nineteen" onset about 6.86 s, price phrase runs to about 7.9 s. The overlay is on screen for all but the first 0.2 s and stays up about 0.8 s after the phrase, inside the 0.3 s rule for the lead. Whisper still hears "$19 .99" (VO wording accepted by you; the overlay lands). |
| 'won't say' VO + 'Apple lists no fold rating' on screen | PASS | Hook shows APPLE LISTS then NO FOLD RATING; description and pinned say "lists no fold rating". |
| 'Drop a comment' end plate / description / pinned | PASS (after fix 1) | Plate DROP A COMMENT button from 58.37 s; description has "Drop a comment with your answer:" then DEBATE_Q last; pinned has "Drop a comment:" . |
| script.txt PUBLISH line 1 + WORDS | PASS | Line 1 PUBLISH Mon Oct 26 tonight, stale after Tue Oct 27 10:00 AM AZ; line 2 WORDS: 148 (wc agrees). |
| QA newer than master | PASS | QA-GATE.md 7:55 PM AZ vs video.mp4 7:53 PM AZ; this report is newer than both. |
| Publish before Tue Oct 27 10 AM AZ | PASS | PUBLISH tonight (post by 9:30 PM AZ). Stale lines ("as of Monday", "still alive", "returns Tuesday 1PM ET") expire Tue 10 AM AZ. |

## Notes for S&T
- Fix 1 is a one-line staging time; fix 2 is the music bed only. After the re-render run your checks again and tell me; my re-check takes about 5 minutes (frames 1745-1775 for fix 1, tail audio for fix 2).
- Still open and accepted by the user, not holds: VO "$19 .99" (overlay carries it), VO "won't say".
- Nothing posted or sent.
