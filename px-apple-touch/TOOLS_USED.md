# TOOLS_USED: px-apple-touch

| Stage | Tool | Credits | Note |
|---|---|---|---|
| Connectivity check | curl | 0 | Direct fetch re-verified dead today: apple.com, federalreserve.gov, arxiv.org, en.wikipedia.org all HTTP 000 |
| Fact lock | WebSearch x2 | 0 | The first pass returned $2,899 from a single outlet. The second corroborated it across three more. That re-check is why the figure is usable |
| Narration + word timings | HeyGen `create_speech`, Alex Wright | 1 generation | 31.37s. Pre-narration gate first: zero digits in the TTS input, no banned phrasing, no quotation marks |
| CDN bridge | ElevenLabs `creative_attach_reference_file` | 0 | |
| Loudness + room tone | `engine/bed.sh` | 0 | |
| Plates | reused from `paradocs-watt-hours` | **0** | No new generation |
| Render + gate | `engine/build.sh` | 0 | 941 frames |
| Thumbnail | `engine/layouts.py` + Playwright | 0 | |

**Deliberately not used:** Higgsfield 0, Adobe Stock 0, Canva 0, vidIQ 0, OpusClip 0.

**Total new credits: 1 HeyGen speech generation.**
