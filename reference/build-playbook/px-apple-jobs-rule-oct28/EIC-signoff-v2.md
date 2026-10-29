# EIC SIGN-OFF v2: px-apple-jobs-rule-oct28 (PX Apple preview Short)
Date: Mon Oct 26, 2026, ~7:40 PM AZ. Master: video.mp4 (7:18 PM AZ). QA-GATE.md v2 (7:20 PM AZ) is newer than the master: PASS.
Scope: changed parts only, checked against qa/EIC-signoff.md fixes 1 to 4, plus regression spot-checks. Working files: /workspace/eic/apple_v2/.

# VERDICT: PASS
Posts Tue Oct 27, 9 AM AZ (before the Wed Oct 28 10 AM AZ event). Not posted by me. No new spend.

## Fix list result
1. RIGHT RAIL: PASS. Measured myself on 240 frames (every 0.25 s) and on all 1,800 frames at 30 fps, text pixels only, rail rows y 864 to 1632: every overlay text element ends at x <= 886 (worst 886 at 53.0 s; typical 880 to 884). The old offenders (NEVER, DOES., OLED, REJECTED, FLIPS, WHY NOW?, CUSTOMERS EXPECT TOUCH, TOUCH = OPTIONAL, SIGNIFICANTLY HIGHER, RIGHT?, MISTAKE?) all clear. GENIUS spans wide but sits at about y 620 (above the rail rows). The only things wider than x 900 in the rail rows are source screenshots and the Jobs clip frame (X post card, Bloomberg and MacRumors article cards, Cook article, Jobs clip) and thin orange bars, not text overlays; they were not flagged in v1 either. OCR hits above 900 were these panels or noise.
2. HOOK NUMBER: PASS. OCT 28 is on screen at frame 0 (t=0.00) and stays through the hook. Whole frame at 0.0 s: OCT 28 (2) + STEVE JOBS SAID (3) + ????? (1) + TOUCHSCREEN MAC (2) = 8. After NEVER lands (1.4 s): 8. Name + number + claim in the first 2 s.
3. LENGTH: PASS. video.mp4 and share-720p.mp4: video 1800 frames, 60.000000 s; audio 60.000000 s (container). Audio decays naturally to zero by 59.21 s (last sample about 1e-4, no click), then 0.8 s of digital silence to the end; no cut or pop. Last frames are still moving (no freeze).
4. CTA: PASS. paste-in.md: "Drop a comment." is the second-to-last description line, then the DEBATE_Q last (accepted by you). Pinned comment ends "...Apple may prove him wrong. Drop a comment." Spoken "Tell me below." stays.

## Other gates
- PUBLISH: script.md line 1 = Tue Oct 27, 2026 9:00 AM AZ. package.md and build-state match. No stale 6 AM left. PASS.
- Whole-frame words <= 8: PASS. My frame sheets (all 240 frames) show max 8 (hook); typical 2 to 6; render.log "max 8, over8 none" agrees. Captions <= 3 words.
- Zooms: PASS. Pushes and pulls on every shot (render.py zs table unchanged), 28 pulse times unchanged. Text outside the rail rows still punches (WEDNESDAY, measured 1,012 px wide shrinking to 920 px across the shot with a pulse jump). ADVISORY: words inside the rail rows are now width-capped, so their punch-in is mostly flat (DOES. measured about 651 to 661 px wide, no visible punch). That is the cap trade-off I allowed in fix 1 ("shift or cap"); background zoom and the other words still move. Not a hold. If you want the punch back on those words, a later pass could zoom the background only and keep a +/-4% text pulse.
- Visual change every 3 to 5 s: PASS (changes every 1.5 to 4.7 s; no freeze; freezedetect log empty).
- Pattern interrupts / re-hooks: unchanged (Jobs audio 16.95 s, ABSURD. 29.72 s, "So why now?" 35.15 s).
- Sync: PASS. faster-whisper small.en float32 on the final audio vs on-screen: NEVER voice 1.38 s, on screen by 1.5 s (appears between 1.25 and 1.5); DOES. voice 4.16 s, on screen at 4.25 s; OLED voice 13.24 s, on screen 13.25 s; GENIUS voice 56.34 s, on screen 56.25 s; MISTAKE? voice 57.34 s, on screen 57.25 s. All within 0.3 s. Pro and tell heard as "pro and tell" at 6.72 to 7.20 s (small.en).
- Loudness: video -14.1 LUFS; 720p -14.2 LUFS. PASS. True-peak as reported -1.8 dBTP (unchanged audio). Transcript 137 words heard = unchanged VO.
- Text vs VO, facts, title, hashtags (3), no disclaimer (PX), event length never stated, no robot hands: unchanged from v1 PASS.
- QA report newer than master: PASS (7:20 PM vs 7:18 PM).
- QA-GATE.md header says "7:20 PM AZ" but the file was written at 7:20 PM AZ. Cosmetic; fix the label if you touch the file again.

## Advisories (user decisions, not holds)
A. NEVER: Jobs said touch "doesn't work", not "never" (VO line 1 + slam). Re-voice about 14 credits needs user OK and PM spend OK.
B. "Apple's newest touchscreen, the iPhone Duo": arguable (iPad mini announced Oct 26). Left as is.
C. Rail-row text punch-ins flattened (see zoom note).

## Hard stop
Must go live before Wed Oct 28, 10 AM AZ, or the Wed/"reportedly does" lines go stale. Check Gurman/Bloomberg and the event page once more right before posting.
