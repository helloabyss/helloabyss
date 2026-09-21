# Provenance — what in this repo is verified, and what is assertion

Written 2026-09-21 after an incident described below.

The problem this file solves: an assistant writes verified findings and unverified assumptions
in the same confident register, and the reader cannot tell them apart. That happened here and
cost real money. This is the standard that replaces "trust me."

---

## The four classes

Every substantive claim in this repo is one of these. **Mark the class whenever the answer
isn't obvious from a visible source.**

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
| 1 | "vidIQ research calls appear not to draw down the balance" — written into `CLAUDE.md` as a constraint | Every call costs 5 credits. The balance had been checked once, at session start, and never again — so there was no evidence either way, presented as weak positive evidence. | **40 of 41 credits** | Corrected; real cost table and per-agent budgets now in `CLAUDE.md` and `AGENTS.md` |
| 2 | The `UC…` channel ID blocks publishing automation | Publishing runs on OAuth; the ID buys nothing. Never checked before sending the user to find it. | User's time on a pointless errand | Corrected; requirement removed |
| 3 | The hook standard is "enforced structurally rather than left to judgement" | The agents are markdown prompts. "Veto" is an instruction to a model. **There is no gate, hook or CI check — nothing technically stops a failed script reaching HeyGen.** | Misplaced confidence in the pipeline | Corrected in `AGENTS.md` |

| 4 | The vidIQ cost table written as **the correction to #1** — every call listed at a flat 5 credits | Same error class, inside the fix. Only `youtube_search` was ever confirmed at 5 (by an API error message). The rest was arithmetic: 10 calls, 40 credits. That maths only works if 2 calls were free, so the flat-5 table was already contradicted by the numbers used to build it. | None yet — caught before it misled anyone | Corrected; each figure now carries its basis, and the operating rule is to assume 5 and measure with `vidiq_balance` before and after a batch |

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
