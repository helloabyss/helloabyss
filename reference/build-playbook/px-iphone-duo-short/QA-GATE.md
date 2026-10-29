# QA-GATE v3: PX iPhone Duo Short (Mon Oct 26, 2026, ~8:12 PM AZ). Supersedes v2 (kept in v2/). EIC HOLD on v2 = 2 free fixes; both done, no credits.
Final: video.mp4 (1080x1920, 30 fps, 60.000 s, 1800 frames, h264/aac), share-720p.mp4. Nothing posted. ElevenLabs credits unchanged at 946 of 1,010; no HeyGen, no Higgsfield. VO untouched (vo_v2.wav).

## v3 gates (the 2 EIC fixes + re-run technical gates)
| # | Gate | Result | Evidence |
|---|------|--------|----------|
| F1 | End plate: no frame shows more than 8 words; "WILL THE DUO" + "BEAT" gone at 58.35 | PASS | render3.py: lines 0-1 skipped for t >= 58.35 (hard cut, was a 0.4 s fade-flag that never drew faded). Frame-exact, frames 1740-1775 (qa/plate_v3/, qa/plate_ocr_v3.log, qa/plate_v3_sheet_a.png): frame 1750 (58.333 s) = WILL THE DUO / BEAT / SAMSUNG'S / 200,000 / FOLDS? (7 words, no button); frame 1751 (58.367 s) = SAMSUNG'S 200,000 FOLDS? + DROP A COMMENT = 6 words, no WILL/DUO/BEAT. OCR max over frames 1751-1775: 7 tokens at conf>=40 (frame 1754, noise tokens, true count 6), 5 at conf>=60 (frame 1771). Over 1740-1750 max is 8 (conf>=40 and conf>=60), at or under the limit. Viewed frames 1750, 1751, 1755, 1760, 1766, 1772. |
| F2 | Music bed runs to 60.0 s with fade-out; both streams 60.000 s | PASS | Root cause: sidechaincompress truncated the music bed at 58.857 s (silencedetect on v2 mix: silence_start 58.857, 1.154 s of digital zero). v3: bed built separately (music looped, -16 dB, ducked by the VO, 63 s in so nothing is truncated, trimmed to 60.0), then afade 0.8 s (st 59.2 d 0.8) ending at 60.0, then mixed with VO + SFX (mix_v3.py). 50 ms RMS: -29.5 dBFS at 58.94-59.20 (no step at 58.87), -31 at 59.41, -36 at 59.58, -47.6 at 59.88, -60.8 at 59.97. silencedetect n=-70 dB d=0.05: 0 events. |
| T1 | ffprobe | PASS | qa/ffprobe_v3.log: video 60.000000 s, 1800 frames counted, 30 fps, 1080x1920; audio 60.000000 s (2814 AAC packets); container 60.000000 s |
| T2 | Loudness / true peak | PASS | qa/ebur128_v3.log: integrated -13.8 LUFS, true peak -1.4 dBFS (<= -1 dBTP), LRA 2.8 LU. loudnorm measured I -17.13, TP -0.84 before the limiters |
| T3 | freezedetect n=-60dB d=4 | PASS | qa/freezedetect_v3.log: 0 freeze events |
| T4 | DEBATEQ | PASS | qa/debateq_v3.log: 7-word Q; pinned and description last line OK; end-plate OCR finds 100% of Q words |
| T5 | Rest of video unchanged | PASS | framemd5 vs v2: frames 0-1710 bit-identical; 89 frames differ (1711-1799, the end plate, incl. x264 re-encode after the change). shots.json identical to v2. Thumbs, paste-in.md, script.txt unchanged. VO unchanged so whisper sync from v2 (137/139 words matched, p95 0.08 s, VO ends 56.86 s) carries over, but I did not re-run whisper on v3. |

Note: decoding the AAC file with a decoder that reports priming reads 60.0107 s of samples; the stream and container durations are 60.000000 s, same as v2 and as the EIC measured.

## Open WARNs carried over from v2 (unchanged)
- Whisper hears "$19 .99" in the price line; the overlay lands (EIC accepted).
- VO "won't say" kept; screen and copy say "lists no fold rating" (EIC accepted).
- End plate is staged (replace mode) to hold the 8-word limit.
- Pauses at 3.0 and 16.0 s not widened.
- Third-party footage 24.65 s against a target of about 20 (advisory; CNET 17.07, Apple 3.80, Samsung 3.78).
- Footage text (status bars, Samsung ad) can add OCR tokens past x 900.
- Staleness: "still alive" and "returns Tuesday 1PM ET" go stale after Tue Oct 27 10:00 AM AZ. Post tonight (PM target 9:30 PM AZ).

---------------- v2 gate (kept for reference; the v2 numbers below are superseded where v3 differs) ----------------
# QA-GATE v2: PX iPhone Duo Short (Mon Oct 26, 2026, ~8:00 PM AZ). Replaces the v1 gate, which the EIC overruled with HOLD.
Final: video.mp4 (60.000 s, 1800 frames, 1080x1920, 30 fps, h264/aac), share-720p.mp4 (720x1280, 60.000 s). v1 kept in v1/. Nothing posted. No ElevenLabs credits spent (946 of 1,010; the VO WAV was only reworked locally: atempo 0.94, widened pauses, price slice stretched).
EIC fixes are by gate number of qa/EIC-signoff.md. Status is stated plainly; WARNs are real.

| # | Gate | Result | Evidence |
|---|------|--------|----------|
| 1 | script.txt PUBLISH line 1 + WORDS | PASS | script.txt lines 1-2 (PUBLISH ... stale after Tue Oct 27 10:00 AM AZ; WORDS: 148) |
| 2 | Video and audio exactly 60.000 s | PASS | qa/ffprobe_v2.log: video 60.000000 s / 1800 frames; audio 60.000000 s; container 60.000000 |
| 3 | ~150 VO words | PASS | 148 (unchanged) |
| 4 | Dead tail | PASS (WARN: partial) | VO at 0.94x; last spoken word ends 56.86 s by whisper (qa/sync_v2.txt), silence from ~57.1 s (inside the EIC's 56-57 s target). Own bar "61,227 / 200,000 = 31%" 53.1-57.0 with punch-ins at 54.0 and 55.5; 3 s end plate 57-60. WARN: only the 8.0 and 38.6 pauses (plus ~0.25 s before the price) were widened; the 3.0 and 16.0 pauses were NOT, because the full set pushes VO end past 57 s. The bar shot is sparse in its lower half. |
| 5 | Hook tag | PASS | "iPHONE DUO · $1,999" 0-2.0 s (qa/v2final_sheet.png) |
| 6 | Pattern interrupt 20-30 s | PASS | cards/prog shots (own graphics) |
| 7 | Zooms | PASS | punches at 54.0, 55.5; end-plate pull-out 1.12 to 1.0 |
| 8 | Captions <=3 words, splits | PASS | "A DAY"/"DAY AND NIGHT", "NO FOLD RATING", "ITS NEW AD", "WORLD'S LIGHTEST FOLD" quote card, "TUESDAY 1PM ET". "AND SAMSUNG" / "ISN'T DONE" anchored to the VO words (whisper: and 32.08, Samsung 32.26, isn't 32.56 on the new timeline = old 29.95/30.50 stretched). |
| 9 | Whole-frame OCR <= 8 words | PASS with explanation | qa/ocr_v2_frames.log (tesseract --psm 11, OMP_THREAD_LIMIT=1, 4 fps, 240 frames): max 8 words per frame at conf >= 60. At conf >= 40 low-confidence noise from footage raises some frames to 20 (texture noise; the EIC's OCR count may differ). Web captures are now blurred and dimmed to 0.30 with one 3-5 word spotlight line, and pass. Staged captions (replace mode) were needed on the hook, weight chart and end plate to stay at 8. |
| 10 | Safe zones | PASS (WARN: footage text) | Overlay captions centered at x 460 and max width 790 (x 65-855 plus stroke); top text edge <= 900; chart labels above y 1500; CNET inset dropped. OCR still sees text beyond x 900 only inside footage (CNET watermark/robot noise, Apple intro "9:41/8:30AM" status bar, 0.1-0.5 s each); not our overlays. |
| 11 | Disclaimer | PASS | unchanged |
| 12 | Drop a comment | PASS with deviation | Plate shows DROP A COMMENT (staged, replaces the first two Q lines at 58.35 s) ; description has "Drop a comment with your answer:" then DEBATE_Q as the LAST line; pinned comment opens with the DEBATE_Q (debateq_check requires that) then "Drop a comment: CNET's counter read 61,227 ...". Deviation from the EIC text: the description's last line is exactly the DEBATE_Q (as asked in the fix) instead of "Drop a comment: will the Duo ..."; the end plate's last 1.7 s shows only the second half of the question plus DROP A COMMENT because 7 Q words + 3 would break the 8-word OCR gate. qa/debateq_v2.log: DEBATEQ PASS (100%). The plate (57-60 s) is music only (the VO ends at ~56.9 s). |
| 13 | Hashtags | PASS | 3 |
| 14 | No generated faces/hands | PASS | real footage + procedural only |
| 15 | Sync within 0.3 s | PASS (WARN: price) | qa/sync_v2.txt: 137/139 words matched, mean -0.03 s, p95 0.08 s. Outliers: "$19" -0.25 s (whisper numeral timing; the energy onset of "nineteen" is ~6.9 s and the overlay lands ~6.97-7.07 s) and "At" +0.48 s (whisper quirk). |
| 16 | Audio | PASS | qa/ebur128_v2.log: -13.8 LUFS integrated, true peak -1.5 dBFS (2-pass loudnorm) |

Other checks
- $19.99 risk: WARN, not fixed. Whisper float32 STILL reads "$19 .99" (qa/asr_v2_final.txt) although the slice is stretched ~1.08x with +0.12 s of room; the on-screen "$1,999" punch-in (330 px, held to 8.75 s) carries the number. The VO cannot be re-taken (credits).
- "Apple lists no fold rating": ON-SCREEN only (hook). The VO still says "won't say" (cannot re-take); description and pinned comment say "lists no fold rating".
- freezedetect (-60 dB, d=4): 0 events (qa/freezedetect_v2.log).
- check_reuse: PASS, 12 real clips, 0 reused, 0 over-used (qa/check_reuse_v2.log; the last CNET shot now uses cnet_d1_30000.mp4 so cnet_day1_end is used twice).
- Figures: thumb_size_check PASS (SIZE, DARK, SOFT, STRAY; 31% added to numbers.md). Frame-OCR figure check (qa/figcheck_v2.log) lists 25 digit tokens not in numbers.md: split pieces of "200,000" and "20,000", OCR noise on "201g/254g", and the transient count-up values of the Samsung card (e.g. 105,898 at 25.5 s). The standard broll_ocr_check was not rerun because the v2 shots are re-cropped with no per-shot source offsets.
- pronounce_check PASS (qa/pronounce_v2.log); banned-term scan of paste-in.md and script.txt: clean.
- Third-party video seconds: CNET 17.07 s, Apple intro video 3.80 s, Samsung ad 3.78 s (<5 s), total 24.65 s. EIC target was about 20 s. The hook CNET 0-4.95 s was NOT cut to 3.5 s; the CNET 46-57 hold is replaced by 3.6 s of CNET plus our bar; the Apple 38.5-40.5 intro is replaced by the weight chart; Samsung 31.4-34.8 is an own text card plus a 1.7 s ad cut. Thumbs A and B are 100% own graphics (no CNET/Apple/Samsung pixels).
- Staleness: "still alive", "as of Monday", "stream returns Tuesday 1PM ET" are true only if posted tonight; after Tue Oct 27 10:00 AM AZ the end plate/pinned comment need a recut.

Overall: items 1-3, 5-8, 11, 13-14, 16 PASS; items 4, 9, 10, 12, 15 PASS with the stated WARNs; $19.99 and the VO wording are open WARNs. EIC re-check requested (about 20 minutes).
