# TOOLS_USED: paradocs-watt-hours

| Stage | Tool | Credits | Note |
|---|---|---|---|
| Narration + word timings | HeyGen `create_speech`, Alex Wright | pre-existing | Word-level timestamps are the spine: every beat cut lands within 0.253s of a word onset (QA-GATE V3) |
| B-roll, generated | Higgsfield `kling3_0`, 9:16, 5s | **40** | 4 shots at 10 each: balance scale, cooling fans, counter wheel, chalk line |
| B-roll, already paid | Higgsfield back catalogue | 0 | 3 bridged; 2 used, 1 rejected for showing an identifiable face and brand lettering |
| CDN bridge | ElevenLabs `creative_attach_reference_file` + `composition` | **0** | Higgsfield's CDN 403s on CONNECT here; confirmed 0 with `estimate_only` before running |
| B-roll, stock | Adobe Stock video | 5 licences | Shots where real hands and real crowds matter; generation gets those wrong |
| Grade | `engine/getwarm.sh` (ffmpeg) | 0 | Lifted and warmed, not crushed |
| Render | `engine/reel.js` (Playwright + ffmpeg) | 0 | 4 workers, 15.1 fps, 1m37s |
| Room tone | `engine/bed.sh` (ffmpeg) | 0 | Dead air 6.26s to 1.71s |
| QC | `engine/qc.py` | 0 | 22 gates, emits QA-GATE.md |
| Review | creative-director agent | 0 | Found 9 blocking defects; see REVIEW.md |

**Deliberately not used:** HeyGen video 0, Canva 0, Picsart 0, OpusClip 0,
vidIQ 0, HyperFrames 0 (installed, not used on this cut — rebuilding in a new
framework mid-fix would have mixed two changes).

**Total new credits this build: 40 Higgsfield.** Balance 350.57 before.
