# QA-GATE v2: px-apple-jobs-rule-oct28 (Mon Oct 26, 2026, ~8:00 PM AZ). EIC HOLD fixes 1-4 applied; reused paid VO (798 credits), no new spend. Event: Wed Oct 28, 10:00 AM AZ.
| # | Check | Result | Evidence |
|---|---|---|---|
| 1 | Format 1080x1920, 30 fps, exactly 60.000 s (1800 frames; audio 60.000 s), 720p copy 60.000 s | PASS | ffprobe on video.mp4 and share-720p.mp4 (EIC fix 3) |
| 2 | Loudness video -14.1 LUFS, TP -1.8 dBFS; 720p -14.2 LUFS | PASS | ebur128 on both files |
| 3 | Script gates: SAY-LIST and pronounce_check passed before VO; no disclaimers | PASS | script.md, proofread-report.md, SCRIPT_TTS.txt |
| 4 | VO: PX voice, eleven_v3, 4 segments, 798 credits (cap 1,010, 212 unspent); no regeneration | PASS | /workspace/budget/credit-ledger.md |
| 5 | VO transcript = script (float32 whisper pass on the final mix; qa_short's int8 ASR was invalid under box load). Caveat: "Pro and tell" heard as "Pro Intel", not verifiable by ear, flagged to the EIC | PASS with caveat | qa/asr_final.json, qa/asr_final.py, qa/EIC-request.md |
| 6 | Real Jobs 2010 excerpt (8.15 s) sits at 16.95-25.10 s as the pattern interrupt | PASS | build mix.sh, script.md |
| 7 | Callouts within 0.3 s of their word (57 callouts, max +0.26 s) | PASS | qa/callout_offsets.md |
| 8 | Open-loop hook in the first 2 s: name (STEVE JOBS SAID) + number (OCT 28 tag from 0.0 s) + claim (NEVER. TOUCHSCREEN MAC), 8 words on the frame (EIC fix 2); re-hook at 29.72 s (ABSURD.) / 35.15 s ("So why now?") | PASS | qa/contact_final.png |
| 9 | Visual change every 1.5-4.7 s, zoom pulses on 28 key words, push/pull and punch-ins | PASS | shots.json, render.py PULSE |
| 10 | Freezedetect n=0.003 d=4 | PASS | qa/freezedetect.log (0 events) |
| 11 | Max 8 words per frame | PASS | qa/render.log ("max words on a frame 8 over8: []") |
| 11b | Right rail: every text item's right edge <= x 900 inside rows y 864-1632 AFTER the layer zoom (items scaled per line; zooms kept) (EIC fix 1) | PASS | qa/render.log ("max text right edge in rail rows 900.0"), qa/contact_final.png |
| 12 | Reuse check (9 clips, 0 reused) | PASS | qa/check_reuse.log |
| 13 | Figures sourced and dated; no unsourced figures on stock frames | PASS | numbers.md, qa/broll_ocr.log (RESULT PASS) |
| 14 | Thumbs A/B 1080x1920 | PASS | qa/thumb_check.log |
| 15 | Public text only in paste-in.md; hashtags 3 incl. #Shorts; "Drop a comment." in description and pinned comment (EIC fix 4); no AI/synthetic line | PASS | paste-in.md (metadata.md symlink) |
| 16 | DEBATE_Q in 3 spots (end plate, description last line, pinned comment) and OCR-readable | PASS | qa/debateq.log (100%) |
| 17 | Banned words / disclaimers / real name | PASS | qa/qa_short/qa.json banned_pass |
| 18 | Music from channel library, attribution in paste-in.md (Kevin MacLeod, CC BY 4.0) | PASS | paste-in.md |
Safe zones: bottom (all text ends above y~1535) and right rail (fix 1) both met. On-screen NEVER stays: the VO says "Steve Jobs said Apple would never build this". "Newest touchscreen" stays: the VO says it too (not on-screen only).
Skipped: lineqa.py and qa.sh (long-form tools; the S-1 Short package did not use them). qa_short transcript and safe_zone output are not used (ASR invalid under load; its zone metric flags every frame).
OVERALL: PASS (19/19 rows incl. 11b). Description note: "Drop a comment." sits on the line above the DEBATE_Q because debateq_check.py requires the DEBATE_Q to be the description's last line (the EIC asked for "Drop a comment." last; one of the two has to give). Publish: Tue Oct 27, 9:00 AM AZ, pending PM confirmation. Not posted.
