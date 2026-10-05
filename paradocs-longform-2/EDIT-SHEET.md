# CapCut Edit Sheet — Apple event pieces

For assembling the long-form and both shorts **in CapCut on your machine**, using your own
event clips over a HeyGen-rendered base.

**Why this file exists:** CapCut has no MCP connector — it cannot be connected to this session
(checked against the registry, 2026-09-09). Your clips also cannot be sent to me: Google
Drive's download tool returns base64 into context, which is unusable for video, and HeyGen's
upload needs an S3 PUT the proxy blocks. So the split is: **I write the edit, you execute it.**

---

## THE WORKFLOW

```
1. HeyGen renders the piece        → house-style imagery + VO baked in
2. Download the render + the SRT   → subtitle_url gives you exact VO timings
3. Open both in CapCut             → render on V1, SRT as your timing guide
4. Drop your event clips on V2     → at the beats marked below
5. Export
```

**Step 2 is the important one.** HeyGen returns a `subtitle_url` (an .srt) alongside every
render. Import it into CapCut and you get the narration timed to the frame — that's how you
land a clip exactly on the word it illustrates, instead of eyeballing it.

⚠️ **There is no separate VO stem.** `create_speech` needs `api` credits the Creator plan
lacks, so narration is baked into the render. That means: **clips go over the top, video only.**
Mute your clip audio or duck it hard under the VO. You cannot re-time the narration in CapCut.

⚠️ **Get the URLs fresh.** HeyGen's `video_url` and `subtitle_url` are signed and expire in a
few days. They're reissued every time `get_video` / `list_videos` is called — ask me and I'll
pull you current ones.

---

## USING EVENT FOOTAGE WITHOUT BREAKING THE CHANNEL

I flagged this before and you're proceeding, which is your call. So here's how to do it well
rather than whether to do it:

- **Short and purposeful.** 1.5–3 seconds per cut, as evidence for a specific claim. Footage
  as the video's backbone is what breaks the identity; footage as a cited exhibit doesn't.
- **Crop tight where you can.** A close shot of a spec slide or a device carries the
  information without the stage, the logo wall, or a presenter's face.
- **Attribute on screen.** A small persistent tag — `Source: Apple, 9 Sept 2026` — while any
  clip is up. It does the honest-citation job *and* satisfies the house rule against
  unattributed corporate marks.
- **Grade them to match.** Your clips will arrive bright and saturated; the channel is
  near-black and desaturated. Drop saturation hard and crush the blacks or the cuts will
  visibly not belong.
- **Never over the compliance card** (first 4 seconds) and never over the sign-off.

---

## LONG-FORM — where footage helps, and where it hurts

Most of this video is a history and economics argument. Event footage only belongs in the
present-tense beats; cutting it into the 1965 or fab sections would actively damage them.

| Beat | Script moment | Clip? | What it needs to show |
|---|---|---|---|
| 1 | Cold open, new CEO on stage | ✅ **Yes** | Wide of the stage/venue. 2s. Sets the "today" anchor before the historical turn |
| 2–13 | The whole Moore's Law + fab + wafer argument | ❌ **No** | Keep house imagery. Footage here would wreck the through-line |
| **14** | **"what was actually shown today"** | ✅ **Strongest use** | The product reveal and any spec slide. **This is the beat the footage is for** — 3–4 short cuts |
| 15 | The price, in context | ✅ **Yes** | The pricing slide, if there is one. Freeze on the number and let the graphic build over it |
| 16 | The wafer caveat | ❌ No | House diagram only — this beat is about *not* trusting a number |
| 17–18 | Who else is in the queue | ❌ No | Data-centre / fab imagery |
| 19 | "premiumisation wearing physics as a costume" | ✅ **Optional, ironic** | The most polished, luxurious product beauty-shot you have. Used *against* the marketing |
| 20 | Split launch cycle | ⚠️ Only if stated | A slide showing the spring timing, if one exists |
| 21–27 | Skeptics → signals → close | ❌ **No** | House imagery. The close must be the channel's voice, not Apple's |

**Rule of thumb:** footage belongs where the script says *"today"* or *"what was shown."*
Everywhere else, the argument is yours and the visuals should be too.

---

## SHORT 3 — "The $30,000 Wafer"

| Beat | Clip? | Notes |
|---|---|---|
| 0:00–0:08 hook | ❌ No | Opens on "$30,000" in type. Don't dilute it |
| 0:08–0:32 the wafer case | ❌ No | Wafer + price bars. Pure house imagery |
| 0:32–0:44 honest counter | ❌ No | Cost-stack diagram |
| 0:44–0:52 close | ⚠️ Optional | One 1.5s product cut *only if* it earns the "you paid for it" line |

**Verdict: this short is stronger with no footage at all.** Its whole point is that the
interesting number wasn't on stage.

## SHORT 4 — "Moore's Law Was Never About Speed"

**No clips. Any.** This short has no Apple reference in the visuals by design — that's what
makes it evergreen and re-postable long after the news cycle. Adding event footage would date
it and cost you the reuse.

---

## IF YOU'D RATHER NOT HAND-EDIT

**Descript** has an MCP connector in the registry (`import_media`, `prompt_project_agent`) —
not currently installed, but you could connect it at claude.ai and then I *could* drive an
import-and-edit from here. It's the only editor connector that exists. Worth it only if you
expect to do this repeatedly; for one video, CapCut by hand is faster.

---

## CHECKLIST BEFORE EXPORT

- [ ] "Educational only. Not financial advice." visible in the first 4 seconds, unobstructed
- [ ] Captions present — HeyGen has returned `caption.enabled: false` on all four renders so
      far, so use the `captioned_video_url` cut as your V1, not the bare one
- [ ] Every event clip: muted or ducked, graded down, attributed on screen
- [ ] No clip longer than ~3s
- [ ] Long-form exported 16:9, shorts 9:16
- [ ] Sign-off intact and clean — no like/subscribe overlay (that's `longform-1` defect 5)
