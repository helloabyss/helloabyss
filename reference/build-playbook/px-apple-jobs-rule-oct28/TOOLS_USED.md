# TOOLS_USED: px-apple-jobs-rule-oct28
- Research/fact lock: WebSearch + WebFetch, saved to /workspace/research/breaking/apple-oct28/facts.md (event start/length block at the top). Bloomberg is paywalled, so its claims are relayed via MacRumors and The Mac Observer. Apple Newsroom does not list the event; start time confirmed via Greg Joswiak's X post and invite coverage.
- Receipts: headless browser screenshots of source pages (caps/), cropped to graphics/r_*.png.
- Footage: Jobs 2010 "Back to the Mac" clip (yt-dlp, real audio, 8.15 s excerpt), Pexels stock (4 clips, free licence). Reuse check: check_reuse.py PASS (9 clips, 0 reused). OCR gate: broll_ocr_check.py PASS (two false-positive frames moved by shifting the clip start).
- Voice: ElevenLabs eleven_v3, PX voice, 4 segments, 798 credits (paid before this decision; no extra generation). Pronunciation lexicon gate pronounce_check.py PASS before VO.
- Timing: faster-whisper small.en and medium.en for word times (local, 0 credits).
- Render: in-house Python PIL/numpy compositor to ffmpeg libx264 (render.py), mix.sh (ffmpeg sidechain-ducked music, PX paradocs SFX, loudnorm).
- Music: Kevin MacLeod "Exit the Premises" from the channel library.
- QA: qa_short.py, lineqa, debateq_check.py, thumb_size_check.py, freezedetect, ebur128.
- Skipped on purpose (paid or not needed): HeyGen 0, Higgsfield 0, Picsart 0, Canva 0, OpusClip 0, GenerateImage/GenerateVideo not used. No Zul in PX.
- X search/trend tool: not used in this build.
Total new credits this segment: 0. ElevenLabs total for the Short: 798 of 1,010.
