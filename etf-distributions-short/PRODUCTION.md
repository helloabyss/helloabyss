# Production Record — ETF Distributions vs Total Return Short

## Session

### Live render (generate mode) — use this one
- **video_id:** `b7a129ec80da4064876a9ff0077e50d1`
- **Watch:** https://app.heygen.com/videos/b7a129ec80da4064876a9ff0077e50d1
- **session_id:** `eccac57ef7b541cca32e60cb967bfa97`
- **Mode:** `generate` (fallback — see below)
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`
- **Orientation:** portrait 9:16
- **Premium credits at session start:** 299 (reset 2026-10-06)

### Chat mode failed again — same defect as the PARADOCS10X build
Chat session `baed2cc7ccb547fab464368b4e195246` was accepted with `status: thinking` and a
null `video_id`, then **404'd on `get_video_agent_session`** on two consecutive polls and
produced nothing. This is the third occurrence of the failure recorded in
`paradocs-short-1/PRODUCTION.md`.

Diagnostics run before falling back, per `STYLE-GUIDE.md` §7:
- **Endpoint healthy** — the older PDT session `71d5eedc10cf48a49e21ba04c4e4a99c` returns
  full detail including its message history. So it is not the endpoint.
- **Credits fine** — 299 premium remaining.
- Same tool, same parameters, same account.

**Conclusion: chat mode is not a transient failure on this account — treat `generate` as the
default and chat as the thing to re-test, not the other way round.** Worth updating
`STYLE-GUIDE.md` §7 if it fails once more.

**Cost of the fallback:** no blueprint approval step, so the constraints could not be
restated at approval — which §7 identifies as what makes them survive generation. To
compensate, the six load-bearing constraints were moved to the TOP of the initial prompt as
a numbered block, including an explicit "burned-in captions must be enabled" (the exact
defect the PARADOCS10X render shipped with) and an explicit instruction not to trim the
counter-evidence beat for runtime.

## The brief
Built from the `STYLE-GUIDE.md` §6 template. Script sent VERBATIM (191 words, ~75s).
The agent is told explicitly that the longer runtime means MORE cuts, not slower ones —
the same note that kept the 1.2–1.8s rhythm intact on the PDT rebuild.

## Decisions worth keeping

### Logos — text name-tags, not real marks
The request asked for logo PNGs. `CLAUDE.md` and `STYLE-GUIDE.md` §4 both ban real corporate
logos and badges, so every brand reference is a plain heavy-condensed **text name-tag** on a
dark plate: `YIELDMAX — FUND DISCLOSURE`, `MSTY · DIST. 09/02/2026`, `FORM 19a-1`.
Beyond house style, this video criticises a named product — using the mark would change its
legal posture for no visual gain. If this is ever reversed, reverse it deliberately.

### The hero shot carries the argument
A sealed tank feeding a glass through a tube. The glass fills (looks like income); the tank
drains by the same volume. Return of capital in one frame, no narration needed. The glass
bookends the video — tight macro at the open, pulled wide at the close to reveal the rig.

### The counter-evidence beat is load-bearing
"A falling price isn't automatically a loss. When distributions outrun the decline, total
return is still positive." This is the mandatory honest-counter beat, and it is also what
stops the video being a hit piece — NAV erosion on its own genuinely does not prove a loss.
It gets its own re-lit repeat of the column-chart shot, with the bars overtopping the line.

## Fact-checking — read this before publishing

Full fact table in `SCRIPT.md`. Two things need your eyes:

1. **The MSTY 98.90% ROC figure (09/02/2026).** This is the video's strongest claim and it
   came from the issuer's own page — but `yieldmaxetfs.com` is **egress-blocked** here, so it
   was read from search-index snippets rather than the live page. Corroborated across two
   independent queries with consistent figures. **Open the MSTY product page and confirm the
   number and its date before upload.** If it has rolled to a newer distribution, swap the
   number in the VO — the argument holds for any ROC figure above ~80%, so it is a number
   change, not a rewrite.
2. **Nothing in the VO is an analyst estimate or a price target.** The one "estimate" is the
   issuer's own label on the ROC split, and the script says "disclosed as" to carry that.

Also blocked this session: `stockanalysis.com`, `sec.gov`, `financecharts.com`. Primary
documents could not be loaded directly; the YieldMax prospectus NAV-erosion risk language
(fact table item 7) was confirmed the same indirect way.

## NOT VERIFIED — needs your eyes
HeyGen CDN egress (`files2.heygen.ai`, `resource2.heygen.ai`) is blocked, so the MP4 cannot be
downloaded or watched from here. The render will be **complete, not verified**. Check on
first view:
1. **No human face anywhere** — the hard constraint for a faceless channel.
2. **Burned-in captions actually enabled.** The PARADOCS10X render shipped with
   `caption.enabled: false`. Verify this one has them, word-by-word, current word highlighted.
3. **Imagery-first** — every scene should have a photographic BASE plate. Watch for stretches
   that are type on a flat or white background; that was the v1 failure mode on the PDT short.
4. **Palette** — near-black, white, one red. No neon, no gradients.
5. **Compliance card** — "Educational only. Not financial advice." visible within 4s.
6. **"HYPOTHETICAL" label** on screen when the $1,000 first appears.
7. **No real logos** — YieldMax and MSTY should be plain text name-tags only.
8. **The counter beat survived** — the "erosion alone doesn't prove you lost money" section
   must be in the final cut. If the agent trimmed it for runtime, that is a re-run, not a
   nitpick: without it this is a hit piece.
9. **Cut rhythm** — no shot held past ~2s.
10. **The close** — "how much of your income was actually income", no subscribe animation.

Any of these missing → reply in the chat session; it can revise without a full rebuild.

## Constraints hit
- **HeyGen CDN egress blocked** — render complete, not verified (above).
- **`create_speech` needs separate `api` credits**, which the Creator plan lacks. No detached
  VO stem; narration is baked into the render.
- **Higgsfield: 0 credits.** No custom B-roll. If topped up, the shot worth buying is the
  tank-draining-into-glass hero — it is the whole thesis and the piece most likely to be
  approximated badly by a stock plate.
- **vidIQ: ~1 credit.** Thumbnail generation costs 22, scoring 5. Use the thumbnail HeyGen
  generates in this session instead (visible on the session page, not fetchable via API).
- **Research egress:** the fund and market-data domains were all blocked — see above.

## Adobe connector — asked about, not connected
"Adobe for creativity" exists in the connector registry (`22854937-9510-4b57-9230-62c820102d8f`,
~67 tools incl. `asset_get_brand`, `asset_get_brand_color_themes`, `animate_design`) but is
`not_installed`. It has to be authorized from claude.ai → Settings → Connectors, then enabled
for the chat; it cannot be connected from inside a session. Worth doing for one specific
reason: `STYLE-GUIDE.md` §7 notes HeyGen brand kits do not persist to the workspace, so the
palette is re-specified in prose in every brief. An Adobe brand record would be a durable home
for it. It would **not** unblock the HeyGen CDN or top up Higgsfield/vidIQ.

---

## RENDER COMPLETE — one confirmed defect, one workaround

- **Watch:** https://app.heygen.com/videos/b7a129ec80da4064876a9ff0077e50d1
- **video_id:** `b7a129ec80da4064876a9ff0077e50d1`
- **Duration:** 82.8s · 9:16 · 1080p · 25 scenes
- **HeyGen auto-title:** "The Power of No: Total Return vs. Yield" — **ignore it**, it is off-script
  in the way `STYLE-GUIDE.md` §7 documents. Upload under a title from `SCRIPT.md`.

### Verified from scene data (not from watching — CDN egress is blocked)
| Check | Result |
|---|---|
| VO script **verbatim** across all 25 scenes | **PASS** — every beat present, in order, unaltered |
| The counter-evidence beat survived into the cut | **PASS** — scenes 20–22 carry it in full |
| Series voice (`0db3abd8…`) on every scene | **PASS** |
| 9:16 portrait, 1080p | **PASS** |
| **Burned-in captions** | **FAIL — `caption.enabled: false`** |
| Imagery-first base layer | **UNKNOWN** — see below |
| Palette / grade / no-logos / compliance card | **UNKNOWN** — needs human eyes |

### The caption defect is now systematic, not bad luck
This is **2 for 2 on generate mode**. The instruction was hoisted to the top of the prompt as
constraint #5 in a numbered "hold these through generation" block, in capitals, and it was
still ignored. Conclusion: **generate mode does not honour a captions instruction from the
prompt.** Stop trying to fix it by rewording the brief.

**Workaround, same as PARADOCS10X — publish the captioned cut, not the base render:**
`captioned_video_url` → `caption_b7a129ec80da4064876a9ff0077e50d1.mp4`, linked from the video
page above. Check its caption styling against house style before publishing. An `.srt` is also
exposed (`subtitle_url`) if you would rather burn captions yourself in an editor with full
control over the word-by-word highlight.

### Two things to look at with your own eyes
1. **Scene pacing.** 25 scenes across 82.8s averages ~3.3s per scene, against a house rule of a
   cut or punch-in every 1.2–1.8s and nothing past 2s. A scene can legitimately contain several
   internal cuts, so this is not proof of a violation — but it is the first place to look. If
   scenes are holding static for 3s each, the piece will feel slow and needs a re-run with the
   cut rhythm restated even harder.
2. **The white-background question, unresolved again.** Every scene reports
   `background: {color: '#ffffff'}` with a single `motion_graphics` element. Read literally that
   is a white background, failing both the imagery-first rule and the near-black palette. But
   `get_video_scenes` does not describe `motion_graphics` elements beyond an id and a type, so a
   full-frame photographic plate would be invisible to this API and the white would never be
   seen. **Identical ambiguity to the PARADOCS10X render — still cannot be resolved without
   watching it.** If the video reads white and flat, the imagery instruction did not land and
   it needs a re-run.
