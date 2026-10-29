# build-state: PX iPhone Duo Short (Mon Oct 26, 2026, resumed 6:38 PM AZ)
- [x] facts.md verified (/workspace/research/breaking/iphone-duo/facts.md); "26 vs 50+" claim dropped, Apple's "more than 50 are or will soon be" wording not used
- [x] script + lexicon/SAY-LIST gate PASS
- [x] VO: ONE take, DONE, never regenerate. Credits 67 (lextest) + 879 (VO) = 946 of 1,010 cap; 64 left. Ledger: /workspace/budget/credit-ledger.md
- [x] footage plan (14 real clips, 19 shots), check_reuse PASS
- [x] render FINAL v3 (safe-zone layout BOTY=1430; HUD pill removed, single-word source labels, S7 duplicate callout removed so every frame <= 8 overlay words), mix (Ether Vox, -16 dB), loudnorm, 720p: final/finish.done 18:48 AZ
- [x] video.mp4 / share-720p.mp4 copied here 18:50 AZ; 1080x1920 30fps 59.97 s, -14.0 LUFS, TP -1.5 dBTP, freezedetect d=4 = 0
- [x] thumbs A/B, paste-in.md (+ metadata.md symlink), numbers.md, package.md
- [x] QA logs in qa/ ; QA-GATE.md
- Work dir: /workspace/shorts/build_iphone_duo/ (render.py, finish.sh, final/)
- Status: PASS (QA-GATE.md). Nothing posted or sent.
- ASR note: qa_short_local.py's best-of-N whisper chunking hallucinated on the music bed in 3 runs (qa/qa_short_local.run*.json, kept for the record). The plain whole-file faster-whisper pass (tx.py, small.en) on the final video is the evidence used: qa/asr_final.txt (149 of 164 normalised words, all differences are number-format or "its/it's"; only the near-silent tail loops with p=0).
- Deliberate hold: 53.1-60 s is music-only with silent closing text (retention risk, disclosed).
- VO NOT regenerated. 946 / 1,010 credits. Higgsfield 0, HeyGen 0.

## v2 (EIC HOLD fixes) - Mon Oct 26, 2026, ~8:00 PM AZ
- [x] Applied qa/EIC-signoff.md: VO reworked locally (atempo 0.94, widened pauses 8.0/38.6, price slice stretched; NO ElevenLabs credits; VO ends 56.9 s), render2.py + tmap.py + build_vo.py + sfx2.py + finish_v2.sh (copies in qa/), 60.000 s / 1800 frames, -13.8 LUFS / -1.5 dBTP
- [x] thumbs A/B rebuilt from own graphics (thumbs2.py), numbers.md +31%, script.txt PUBLISH/WORDS, paste-in.md Drop a comment + "lists no fold rating"
- [x] gates: QA-GATE.md v2 (honest WARNs). v1 files in v1/ (video, share, thumbs, shots, QA-GATE).
- Work dir: /workspace/shorts/build_iphone_duo/ (render2.py, thumbs2.py, finish_v2.sh, final/video_v2.mp4)
- Status: v2 ready for EIC re-check. Nothing posted or sent. Credits 946 / 1,010, Higgsfield 0, HeyGen 0.

## v3 (Mon Oct 26, 2026, ~8:12 PM AZ), EIC HOLD on v2, 2 free fixes
- [x] v2 deliverables backed up in v2/ (video, share, thumbs, shots, QA-GATE.md, build-state.md, paste-in.md)
- [x] Fix 1: render3.py (frame_debate: lines 0-1 skipped for t >= 58.35). Plate frame-exact OCR/visual: max 6 true words from 58.367.
- [x] Fix 2: music bed rebuilt (final/bed_v3.wav, built outside mix.py because sidechaincompress truncated at 58.857 s), 0.8 s fade ending 60.0, mix_v3.py, finish_v3.sh. True peak -1.4 dBFS, -13.8 LUFS, both streams 60.000 s.
- [x] QA-GATE.md v3 (qa/ffprobe_v3.log, ebur128_v3.log, freezedetect_v3.log, debateq_v3.log, plate_ocr_v3.log)
- Work dir: /workspace/shorts/build_iphone_duo/ (render3.py, mix_v3.py, finish_v3.sh, final/video_v3.mp4)
- Status: v3 ready for EIC re-check (frames 1745-1775 and the audio tail). Nothing posted or sent. Credits 946 / 1,010, Higgsfield 0, HeyGen 0.
