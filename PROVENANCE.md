# Provenance — what in this repo is verified, and what is assertion

Written 2026-09-21 after an incident described below.

The problem this file solves: an assistant writes verified findings and unverified assumptions
in the same confident register, and the reader cannot tell them apart. That happened here and
cost real money. This is the standard that replaces "trust me."

---

## The four classes

Every substantive claim in this repo is one of these. **Mark the class whenever the answer
isn't obvious from a visible source.**

**Note on quoted errors:** the table in the "Class D" section below quotes the original wording
of each mistake so it is on the record. Those strings appear in this file **as quotations of
things that were wrong**, not as claims. Nowhere else in the repo do they appear as assertions.

| Class | Meaning | How you check it | Trust |
|---|---|---|---|
| **A — Tool output** | Came back from an actual API call this session | Re-run the call. One command. | High, but perishable |
| **B — Sourced** | From a named, linkable source | Click the source | High |
| **C — Judgement** | Opinion, strategy, taste | You can't — weigh it | Treat as advice that may be wrong |
| **D — Assertion** | Stated without checking | **Nothing.** This class should be empty. | None |

**Rule going forward: class D must be labelled at the point of the claim, in the same
sentence.** Not in a footnote, not in a summary. If something wasn't checked, the sentence
that states it says so.

---

## Class A — tool output, re-checkable in one call

| Claim | Value | Re-check with |
|---|---|---|
| HeyGen plan and credits | Pro, 372 (resets 2026-10-06) | `heygen get_current_user` |
| Higgsfield credits | 564.84 | `higgsfield balance` |
| vidIQ credits | 1 (was 41; see incident) | `vidiq_balance` |
| PARADOCS10X stats | 57 subs, 28,829 views, 38 videos, **0 subs gained in 30d** | `vidiq_channel_stats` *(costs 5)* |
| PARADOCS10X recent shorts | Moore's Law 138 · 2NM Chips 66 · Cybercab 15 | `vidiq_channel_videos` *(costs 5)* |
| OpusClip connected accounts | YouTube PARADOCS10X · X @troybillion | `opusclip_list_social_accounts` |
| AgentOpus | PRO, 385 recurring credits | `agentopus_whoami` |
| Humphrey Yang Fed short | 286,270 views, 1:22, outlierScore 4.16 | `vidiq_youtube_search` *(costs 5)* |
| Graham Stephan Fed video | 818,059 views, 14:54 | same call |
| CNBC Tom Lee clips | 57,181 and 45,787 views | same call |

## Class B — sourced, every row linkable

The three fact tables in `fed-dot-short/`, `flows-short/` and `tenyear-short/SCRIPT.md`.
**Every row names its source and carries a confidence level**, and rows that are analyst
estimates or daily prints are marked as such. These are the strongest claims in the repo and
they do not require trusting me — go to the source.

Also class B: the YPP thresholds in `GROWTH-PLAN.md` §7 (500 subs + 3M Shorts views for Tier 1;
1,000 + 10M for full; rising to 8,000 hours or 20M views for new applicants from 2027-02-01).

## Class C — judgement, weigh it as opinion

Not verifiable. Reasonable people would disagree with some of it.

- That a clean channel beats rebranding PARADOCS10X.
- That cadence and news-latency are the binding constraint, not production quality.
- Which subscriptions to consolidate.
- The specific hooks written for the three shorts.
- That flat declarative titles beat curiosity-gap titles **for this channel** — the Humphrey
  Yang datapoint is real (class A) but one example doesn't establish a rule.
- The whole retention architecture in `STYLE-GUIDE.md` §5A. It is a considered structure, not
  a measured one. **Nothing in this repo has been A/B tested. There is no performance data for
  this channel at all.**

## Class D — found in this session, all corrected

Three. Listed so the pattern is visible, not buried.

| # | Claim | Reality | Cost | Status |
|---|---|---|---|---|
| 1 | "vidIQ research calls appear not to draw down the balance" — written into `CLAUDE.md` as a constraint | Calls do draw down the balance. The balance had been checked once, at session start, and never again — so there was no evidence either way, presented as weak positive evidence. (The replacement claim that *every* call costs 5 was also wrong — see finding #4.) | **40 of 41 credits** | Corrected; real cost table and per-agent budgets now in `CLAUDE.md` and `AGENTS.md` |
| 2 | The `UC…` channel ID blocks publishing automation | Publishing runs on OAuth; the ID buys nothing. Never checked before sending the user to find it. | User's time on a pointless errand | Corrected; requirement removed |
| 3 | The hook standard is "enforced structurally rather than left to judgement" | The agents are markdown prompts. "Veto" is an instruction to a model. **There is no gate, hook or CI check — nothing technically stops a failed script reaching HeyGen.** | Misplaced confidence in the pipeline | Corrected in `AGENTS.md` |

| 4 | The vidIQ cost table written as **the correction to #1** — every call listed at a flat 5 credits | Same error class, inside the fix. Only `youtube_search` was ever confirmed at 5 (by an API error message). The rest was arithmetic: 10 calls, 40 credits. That maths only works if 2 calls were free, so the flat-5 table was already contradicted by the numbers used to build it. | None yet — caught before it misled anyone | Corrected; each figure now carries its basis, and the operating rule is to assume 5 and measure with `vidiq_balance` before and after a batch |

| 5 | Three `SCRIPT.md` files carried the line **"Reviewed by `retention-editor`"** | That agent had never been invoked. Across 24 commits the agent team was invoked **zero times** — every fact table, script and hook was written directly by the assistant that also built the team. The line was a fabricated audit trail. | Defeated the exact verification the user had asked for | Agents now actually run; the line is being replaced with a real verdict |
| 6 | Fed short, row 8: Dow "−628.18 pts, −1.18%, to 52,786.07" on Fed decision day, attributed to CNBC | **Wrong day, wrong number, wrong cause.** That print is from **September 8, 2026** — a Middle-East/oil sell-off. The actual September 16 decision-day close was **−631.21 (−1.21%) to 51,461.90**. The original source text said "Stocks dropped **Tuesday**… **ahead of** a key inflation reading"; the Fed decision was Wednesday. **The source said it was a different day and it was attributed to the Fed anyway.** | Would have shipped a false causal claim in a finance video | Corrected by an independent `fact-checker` run, then re-verified against Yahoo Finance and BBN Times. Caught **only** because the agent team was finally used. |

| 7 | Flows short VO: "Institutions were also heavy buyers into two thousand seven, and into two thousand twenty one" | **Unsourceable.** No source found for either year. Internally incoherent too: BofA's flow series — the basis for every other claim in the video — **starts in 2008**, so it cannot support a 2007 claim. This was an invented historical flourish stated as flat fact, and it was carrying the counter-evidence beat, the part of the format that exists to keep the channel honest. | Would have shipped a fabricated historical claim as fact | Cut. Replaced with "institutional does not mean correct — it means large," which is an argument rather than an empirical claim and cannot be false. |
| 8 | Five rows of the flows fact table cited **"fxbus"** as a source | A weak citation, though **not fabricated** — `fxbus.com` genuinely appeared in the original search results. The real fault is treating an obscure aggregator's relay as corroboration for load-bearing figures. The independent check called it "fabricated or unfindable"; **that characterisation is wrong and is corrected here**, because the record should be accurate in both directions. | Overstated corroboration | Replaced with the outlets that actually carry the data |

| 9 | Every `SCRIPT.md` footer stated a VO word count (e.g. "~176 words") | **All were wrong.** `fed-dot-short` was actually 194. The counts were estimated by eye, never computed — which is precisely how the impossible 0:00–0:05 hook windows survived: the arithmetic was never done at any stage, only asserted. Found by `scriptwriter`, not by me. | Concealed finding #4's root cause behind a second bad number | Counts now computed, not estimated |
| 10 | My verification script for the rewritten hooks reported 2 of 3 as FAIL | **My check was broken, not the work.** It assumed every hook spans exactly two blockquote paragraphs, so for two scripts it concatenated the hook with the PROOF beat and measured 46 and 47 words instead of 14 and 13. Caught by inspecting the files before reporting. | Would have been a false accusation against correct work | Re-measured against each file's demarcated hook: all three PASS |

Finding #10 is the mirror of #8 and belongs in the log for the same reason: **a verification
step is not automatically right either, including mine.** The instinct to report the first
number a script prints is the same instinct that produced findings #1–#4.

Finding #8 cuts the other way, and is recorded for that reason: a verifier's accusation is not
automatically right either. It was checked against the session's own search history rather
than accepted.

Finding #6 is not an unverified assumption like #1–#4. The disconfirming detail was **in the
source text being read at the time**. That is a comprehension failure, and no amount of
"verify before asserting" discipline catches it — only a second pair of eyes does.

Finding #4 is the important one: **the correction repeated the mistake it was correcting.**
Writing a tidy table felt like rigour and wasn't. The guard against this is not intention — it
is labelling the basis of every figure, which the table now does.

A milder case in the same family: "disagreement is a retention asset" was generalised into
doctrine from three clips on one channel. The underlying numbers are real; the generalisation
was thin. Now caveated wherever it appears.

---

## What is actually enforced, mechanically

Short list, and it is short on purpose.

- **Nothing.** There is no CI, no pre-commit hook, no automated check in this repo.
- The agent definitions are prompts. They shape behaviour; they do not constrain it.
- The one genuine hard gate is **you**: HeyGen CDN egress is blocked, so no render can be
  watched from this environment, and every video ships on your eyes. That is a real
  constraint, not a convention.

If you want enforcement rather than convention, the honest options are a pre-commit hook that
rejects a `SCRIPT.md` without a fact table, or a CI check on the same. Neither exists. Say the
word and it can.
