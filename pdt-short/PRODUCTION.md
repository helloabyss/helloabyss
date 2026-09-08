# Production Record

## Active HeyGen render
- **Session:** https://app.heygen.com/video-agent/fa5ccb1b99894aaebce888736e4f1df5
- **Mode:** chat (revisable — send follow-up notes in the session)
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639` (9:16, print/editorial typography)
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`

### Superseded (stopped while still `pending`, before render — no stale output)
- `c47710a235614401b1899b0977cee955` (chat) / video `e3fd8adcea554ae0be5e2c0c08f5c7bb`
- `003f5f6ca58340eaa75e7b47e70f3d97` (generate) / video `b75f28ecaecc4057b57767df077267a1`

Both carried the earlier CTA ("Follow for what your broker won't email you") and were
stopped when the close was rewritten.

## Notes / constraints hit
- **Higgsfield: 0 credits** (starter plan). No custom B-roll generated. If topped up, the
  shots worth buying are the seatbelt-shatter and the margin-meter fill — HeyGen stock
  won't have close equivalents.
- **HeyGen standalone TTS (`create_speech`) is unavailable** on this plan: it bills to
  separate `api` credits, not the 501 premium credits. Narration is produced inside the
  video-agent pipeline rather than as a separate .wav stem. A detached VO stem for
  editing in CapCut/Premiere would require API credits.
- Premium credits at session start: 501 (reset 2026-10-06).
