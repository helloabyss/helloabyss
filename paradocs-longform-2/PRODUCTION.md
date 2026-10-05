# Production Record — PARADOCS10X Long-Form 2

- **Status: ❌ RENDER FAILED** — see "Attempt 1 failed" below. Not shipped.
- **Attempted:** 2026-09-09, ~11:32 PT
- **video_id:** `1422e737e3804d26b100e754b1bbb46e` (failed)
- **Session:** https://app.heygen.com/video-agent/d6dd2619f6634d64be96d1ec37d443df
- **Mode:** `generate` — chat mode 404s account-wide (see `CLAUDE.md`)
- **Orientation:** **landscape 16:9**
- **Style:** Economist — `e7f9a12679ec426099db7646b70a4639`
- **Voice:** Alex Wright – Informative — `0db3abd83c74452fb2460b0dd113daad`
- **Script as sent:** `VO-FINAL.txt` (1,348 words) · **Full brief:** `render-prompt.txt` (9,996 chars)

## Why it waited, and what released it
Rendering was held through two explicit requests because beats 14/15/20 depended on
announcements that had not been made. Searches at 11:10 PT still returned only pre-event
previews hedged with "reportedly" and "expected to" — the LOW-confidence leaks the fact table
forbids. At **11:27 PT** post-event reporting landed with corroborated prices from MacRumors and
TheApplePost, and the slots were filled from that, not from the leak.

**Shipped on HeyGen, not Higgsfield.** Higgsfield has **0 credits** (plan `starter`), re-checked
this session; it cannot render anything. HeyGen had 129 premium credits.

## The 10,000-character prompt cap — a real constraint for long-form
`create_video_agent` accepts a prompt of **1–10,000 characters**. A verbatim 1,850-word script
is ~10,500 characters *before* any brief, so the planned length was impossible in one call.

**Resolution: trim the script to 1,348 words (~8.1 min) and keep it verbatim.** The rejected
alternative was sending a shorter prompt and letting the agent expand it — unacceptable here,
because anything it invented would be unverified claims in a finance video.

**Record this in `LONGFORM-GUIDE.md`:** the practical ceiling for a single-call verbatim
long-form is **~1,350–1,400 words, about 8 minutes**. `paradocs-longform-1` reached 11 minutes,
so a longer piece is possible — but not through one `create_video_agent` prompt.

## VERIFICATION CHECKLIST — human eyes required
**Complete, not verified** — HeyGen CDN egress is blocked here.

| # | Check | Why |
|---|---|---|
| 1 | **Burned-in captions** | Disabled on all 5 previous renders. If `caption.enabled: false`, publish the `captioned_video_url` cut |
| 2 | **"Educational only. Not financial advice." in first 4s** | Non-negotiable; this names a listed company on the day of its product launch. `longform-1` appears to lack it |
| 3 | **Wafer-price footnote on screen** | The spoken caveat is confirmed in the script; the on-screen one can't be verified from the API |
| 4 | **NO Apple or TSMC logo; no device resembling a real iPhone** | Highest drift risk in this brief — the script names both companies repeatedly |
| 5 | **No faces** — no Moore portrait, no executives, no audience | A keynote-topic brief invites all three |
| 6 | **Imagery-first**, not type on flat colour | The `longform-1` failure mode |
| 7 | **Numbers count up** — $30,000, $1,199, +$100 | `longform-1` visualised none |
| 8 | **VO verbatim** vs `VO-FINAL.txt` | Check via `get_video_scenes` |
| 9 | **Bookend** — same stage shot at open and close | |
| 10 | Runtime ~8 min, 16:9 | |

## Defects from long-form 1 deliberately fixed
| `longform-1` defect | Status here |
|---|---|
| 1. Repeated the unsourced 1894 manure claim | ✅ N/A — different subject, and every claim carries a confidence level |
| 2. No compliance card | ⚠️ Requested in the brief — **verify by eye** |
| 3. Captions disabled | ⚠️ Requested explicitly on its own line — **verify** |
| 4. No MID/TOP layers, no numbers visualised | ⚠️ Brief demands every number count up — **verify** |
| 5. Like/subscribe follow-bait CTA | ✅ **Fixed** — closes on the three actions and "Watch the cost. Not the phone." No appeal |

## Thumbnails
Two 1280×720 variants ready — see `THUMBNAILS.md`. Variant **A** recommended.

## Constraints hit
- HeyGen chat mode 404 account-wide → generate mode, no blueprint approval
- **`create_video_agent` 10k-char prompt cap** → script trimmed to ~8 min
- HeyGen CDN egress blocked → complete, not verified
- Higgsfield 0 credits → could not be used to ship
- vidIQ 1 credit → no thumbnail generation (built locally instead) and no title/thumbnail scoring

---

## ❌ ATTEMPT 1 FAILED — 2026-09-09

`get_video` returned `status: "failed"` with **`failure_code: null` and
`failure_message: null`**. HeyGen supplied no diagnostic of any kind. `get_video_agent_session`
still 404s account-wide, so the session carries no detail either.

### Credit cost of the failure
| Moment | Premium credits |
|---|---|
| Before the two shorts | 129 |
| After 2 successful shorts + 1 failed long-form | **54** |

**75 credits consumed; the long-form produced nothing.** Exact attribution is impossible —
the two dead chat-mode sessions may also have drawn down — but the failed long-form plainly
accounted for a large share. **A blind retry risks ~45 more of the remaining 54.** Credits do
not reset until **2026-10-06**.

### What the evidence points at
| Render | Words | Runtime | Orientation | Result |
|---|---|---|---|---|
| Short 4 | 148 | 55.8s | portrait | ✅ completed |
| Short 3 | 152 | 55.8s | portrait | ✅ completed |
| **Long-form 2** | **1,348** | **~8 min** | **landscape** | ❌ **failed** |

Both short generate-mode renders succeeded minutes earlier with the same style, voice, account
and mode. The long-form differed in exactly two ways: **a ~9× longer script** and **landscape
orientation**. Script length is the more likely cause — ~20 scenes is a far larger generation
job — but orientation is not ruled out, and with a null error message this is **inference, not
diagnosis**.

`paradocs-longform-1` (11 min) proves long landscape renders can exist on this account, but its
session was never recorded, so **there is no evidence it was made through
`create_video_agent`** — it may have been built in the HeyGen app. That precedent should not be
treated as proof the API path supports this length.

### Do not retry blind
At ~45 credits per attempt against a balance of 54, one failed retry leaves the channel unable
to render anything until October. The options, cheapest first:

1. **Split into two ~4-minute parts**, render separately, join in CapCut. Halves the per-call
   risk and fits the prompt cap comfortably. Two publishable halves even if one fails.
2. **Cut to ~5 minutes (~830 words).** Smaller job, materially better odds, still a real
   long-form. Costs the "what it means for you" and second-order beats.
3. **Retry identical once.** Only sensible if the failure was transient — unknowable here.
   Highest risk.
4. **Build it in the HeyGen app** from `VO-FINAL.txt`, bypassing the API entirely. Zero API
   risk; needs a human at the keyboard.

The script, fact table and thumbnails are all finished and unaffected — this is purely a
rendering problem.
