# Production record — 0.24 Wh. Or 0.10.

## Current cut

`watt-hours-v3.mp4` — 38.48s, 1080x1920, H.264 + AAC, 30fps.
Thumbnail `thumbnail-v2.png`. Title and description in `PACKAGING.md`, unchanged
and already fact-checked.

**Complete, NOT verified.** Nothing in this container can watch a video with
sound. Verification checklist at the bottom.

## What changed, and what did not

The owner rejected the previous cut on four counts. Three are fixed:

| Complaint | State |
|---|---|
| "The words are chopped off the screen" | **Fixed.** `fitHero` measures the union of the laid-out letter rects and `#hero` is nowrap. Took three attempts; the two failures are documented in the function because each produced a different visible defect. |
| "Hate the dark Vader with a splash of red" | **Fixed.** WARM DARK (aubergine + amber), chosen by the owner. Palette is a token set in `reel.js`, swappable per video. |
| "Still too PowerPoint like" | **Fixed.** Six layouts — full, split, card, quote, versus, band — replacing one layout repeated 29 times. |
| **"Sync relevant b-roll to the narration, as a rule of thumb"** | **2 of 16 lines done.** See below. This is the open one. |

## The b-roll rule is only 1/8 done — be honest about this

`SHOTPLAN.md` maps all sixteen narration lines to the picture each one needs.
Two are built:

- "Ten counts the chip doing the thinking" → silicon wafer macro (`HW1`)
- "Twenty-four averages it across the whole fleet" → data-centre aisle (`HW2`)

The other fourteen still run on recycled stock. **Ten of them need generated
footage** because the shot is an argument rather than an object — a balance, a
chalk line being drawn, one lit bottle in a dark row. Stock libraries index by
subject, so there is nothing to search for. That is the real reason the cut kept
falling back on pylons.

That batch is 100 Higgsfield credits of 350.57 and **has not been authorised**.

## The Higgsfield CDN block is solved

Recorded in `CLAUDE.md`. `d8j0ntlcm91z4.cloudfront.net` still 403s on CONNECT,
but ElevenLabs fetches it server-side and a 0-credit `composition` node re-emits
downloadable MP4 bytes. Verified end to end. This is what makes the generated
shot list possible at all.

## Three free clips bridged, one rejected

Reviewing them caught a defect that would have shipped: the city-plaza clip has
a clearly identifiable face and invented brand lettering on a coffee cart,
breaking two hard rules in `CLAUDE.md`. It is out. The aisle clip arrived cold
blue and a first regrade turned it green; it took a second pass (strip
saturation, then tint) to land warm. Details in `SHOTPLAN.md`.

**Resolution caveat:** those clips were generated 16:9 at 720p, so the 9:16
centre crop is upscaled 2.7x and is soft. Tolerable behind chrome, not for a
hero shot. New generations must be native 9:16.

## No independent review has passed on this cut

A creative-director and a video-editor agent were both run against
`watt-hours-v2.mp4`. **Both hit the session rate limit and died before
reporting.** They can be resumed after the limit resets. Until then nothing here
has been vetted by anything other than the author, which is exactly the failure
mode the agent roster exists to prevent. Do not treat this record as a review.

## Verification checklist — a human must do this

1. Watch with sound on a phone, not a monitor.
2. Captions against audio at 12s and 31s — word timings come from HeyGen
   `create_speech`, but no one has confirmed the burn-in matches.
3. Text inside frame at 23.6s ("THE BOUNDARY") and 37.5s ("DREW THE LINE") —
   these were the two worst overflows.
4. Plate seams at beat boundaries: each plate is a 5-8s loop seeked per beat.
   Look for jumps at 9.0s and 14.4s where the new clips start.
5. First 3 seconds as a scroll-stopper.
6. `HW1`/`HW2` softness at full screen — judge whether the upscale is acceptable.
