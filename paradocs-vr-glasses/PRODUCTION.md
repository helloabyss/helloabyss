# Production Record — PARADOCS10X "The Headset Disappears" (Meta VR Glasses)

- **Session:** https://app.heygen.com/video-agent/07bdf30108254e5292557bc560dc7dfc
- **Mode:** chat (session is alive and readable, unlike the 404s hit on Short 1)
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`
- **Orientation:** portrait 9:16
- **Credits at start:** 275 premium

## Source material — none from meta.com
Asked to reuse images and clips from meta.com/vr-glasses. Not used:
- `www.meta.com` is blocked by the egress proxy (curl 403, WebFetch EGRESS_BLOCKED).
- Flipping or remixing Meta's copyrighted ad material to get past Content ID was declined.
- It would also break the no-faces and no-logos rules in the style guide.
All imagery is generated as generic, unbadged hardware. If real footage is wanted, Meta's
newsroom press assets can be added in the edit under their terms, unaltered.

## Research constraints
roadtovr.com and engadget.com are also egress-blocked, so the facts come from search-result
summaries of several outlets that agree with each other (UploadVR, VR.org, Hardware
Busters, CNBC, Meta 10-Q). The FOV figure differs between sources (70°×66° vs 84°), so the
script says only "narrower than a Quest 3".

## Prompt guardrails
- Generic, unbadged glasses and headset — no Meta/Apple/Ray-Ban/Oakley likeness or logos.
- Puck-in-pocket shot cropped at the shoulder — no face.
- Bookend: same desk, same camera position — headset at the open, only glasses at the close.
- Captions explicitly required (Short 1 rendered with `caption.enabled: false`).

## Brief change
The user removed the "Educational only. Not financial advice." card because PARADOCS10X is a tech
channel. The change was sent into the session before the blueprint was approved.

## Status
Blueprint pending. Restate the grade, bookend, hero-shot and captions rules at approval.

## Verification checklist (a human has to watch it — CDN egress is blocked)
- [ ] **No** "Not financial advice" card (removed by user; tech channel)
- [ ] VO verbatim, ends "This is Paradocs 10X."
- [ ] Burned-in word-by-word captions present
- [ ] Imagery base layer on every scene — not flat white or abstract
- [ ] No faces, no real logos, no recognisable Meta/Apple product design
- [ ] Near-black / white / red only; imagery desaturated
- [ ] Footnotes on battery (Meta's figure) and Reality Labs (Q2 2026, 10-Q)
- [ ] Bookend: same desk at open and close
