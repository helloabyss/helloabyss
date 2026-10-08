# Assignment board

Standing queue for the six agents in `.claude/agents/`. They are committed to git, so they
persist across sessions and load automatically — nothing needs re-creating.

Assign by name: `Agent(subagent_type: "<name>", prompt: "…")`, or say **"run <task id>"**.

**Status key:** `READY` assignable now · `BLOCKED` waiting on something named · `NEEDS-YOU` a
decision or credential only Sheldon can supply.

---

## Open queue

| ID | Agent | Task | Status |
|---|---|---|---|
| **T1** | `packager` | **Review fed-dot-short + flows-short packaging.** Never agent-reviewed — titles, descriptions and tags in both are unverified work by the assistant. The one packaging section that *was* reviewed (tenyear) turned out to carry a false claim in its title. | **READY** |
| **T2** | `fact-checker` | **Pre-publish re-verify of daily prints**, morning of upload. tenyear rows 7/8/9 (mortgage index, Brent, WTI) moved materially within one week and are flagged in-file. fed row 8's Dow close should be reconfirmed as final/unrevised. | BLOCKED — run on render day, not before |
| **T3** | `retention-editor` | **Render-time verification.** Confirm the hook survived generation, the compliance strip rendered as an edge strip not a card, and fed's filled-socket shot is *held* through the closing line. | BLOCKED — needs a render to exist |
| **T4** | `scout` | **Weekly sweep** — 5 ranked angles for next cycle. | **READY** — unblocked 2026-10-05: vidIQ measured at **121 credits**, ~24 calls at the pessimistic 5/call |
| **T5** | `art-director` | **Generate hero reference plates.** Fed pin-grid socket carries both hook and bookend payoff; flows two-pan composition is the hardest physics to read in one frame. | **BLOCKED** — not a decision any more. Higgsfield measured at **0.35 credits** on 2026-10-05, not 564.84. Needs a top-up before it can run at all |
| **T6** | — | **Render the three shorts.** Chat mode, restate grade/bookend/hero at blueprint approval per `STYLE-GUIDE.md` §7. | **BLOCKED until 2026-10-06 12:57 UTC** — HeyGen measured at **0** premium credits on 2026-10-05, not 372. Then ~1 credit each |
| **T8** | — | **Decide the ONE NUMBER series question** in `SERIES-ONE-NUMBER.md` §6: does the stickman format run as the weekly cadence engine, or stay a parked option? It is a visual-identity call, and on a 6-sub channel running two looks splits the signal. | **NEEDS-YOU** |
| **T7** | — | **Connect `@meticulousmoney` to OpusClip.** OAuth in its UI; mints its own `post_account_id`. Until then uploads are manual. The X account (@troybillion) is channel-agnostic and usable today. | **NEEDS-YOU** |

---

## Standing rules for any assignment

- **Adversarial briefs only.** Tell the agent the existing work is unverified and who produced
  it. The passes that found real defects were the ones told not to trust the file.
- **Never say "confirm X is fixed."** Say "verify X." Four findings in `PROVENANCE.md` exist
  because a check asked whether work had happened rather than whether it was correct.
- **A verification record must quote the text it verified** (finding #12), so it visibly goes
  stale when that text changes.
- **A correction is not done when the primary document is fixed** (finding #14) — it has to
  reach every document that acts on it, and the checklist is read last.
- **Never introduce a number into a prompt that isn't in the spec** (finding #11). Invented
  tolerances propagate silently because agents obey prompts.
- **vidIQ: assume 5 credits per call.** Weekly budget scout 3 · retention-editor 1 · packager 1.
  Never `vidiq_outliers`.
- **No generation spend without Sheldon's yes in the same turn.**

## Decay watch

`fed-dot-short` is pegged to the 2026-09-16 FOMC. Its hook is not date-stamped (the "this week"
phrasing was removed), so it degrades in relevance rather than becoming false. `flows-short` is
a fixed historical print and `tenyear-short` is largely evergreen — both keep indefinitely,
subject to T2.
