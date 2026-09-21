# Agent Registry — The Meticulous Investor

Six agents, defined in `.claude/agents/`, each owning one stage of the weekly cycle. They are
deliberately narrow: a narrow agent can't drift into the next one's job, which is what keeps a
six-stage chain from collapsing into six copies of the same generalist.

Invoke by name: `Agent(subagent_type: "scout", prompt: "…")`, or say **"run the weekly cycle"**
and the whole chain runs in order.

---

## The chain

```
scout ─→ fact-checker ─→ scriptwriter ─→ retention-editor ─→ art-director ─→ [HeyGen] ─→ packager ─→ [OpusClip]
 find       verify           write          HOOK / VETO          design         render       title        schedule
                                                  │
                                              FAIL ─┘ back to scriptwriter
```

Two gates can stop a video. **`fact-checker`** kills a piece with no honest counter-argument —
that makes it a promo, not an explainer. **`retention-editor`** vetoes any script that fails
the five-second test. Neither is advisory.

---

## The table

| # | Agent | Owns | Takes in | Hands off | Authority |
|---|---|---|---|---|---|
| 1 | **`scout`** | Finding the week's stories | Nothing — sweeps news + demand data | 5 ranked angles, each with decay estimate and a comparable video's real numbers | Recommends only |
| 2 | **`fact-checker`** | Truth | A chosen angle | The `SCRIPT.md` fact table, per-claim confidence | **Can kill a video** — no honest counter-argument means it's a promo |
| 3 | **`scriptwriter`** | The words | The verified fact table | Verbatim VO, 150–175 words | May not use a number that isn't in the table |
| 4 | **`retention-editor`** | **The first 5 seconds + retention** | The draft VO | PASS/FAIL, rewritten hook, timestamped retention map, brief amendments | **VETO** — a FAIL does not proceed |
| 5 | **`art-director`** | How it looks | The approved VO | Beat-by-beat shot list + the HeyGen brief | Can request a Higgsfield spend; can't make it |
| 6 | **`packager`** | How it's found | The finished render | Titles, description, tags, thumbnail direction | Can't spend a vidIQ generation credit unsolicited |

---

## What each one is actually for

### 1. `scout` — finds the stories
Sweeps 4–6 web searches across rates, bonds, commodities, a single name, a regulatory change
and a flows datapoint; then checks real YouTube demand per candidate. Returns the
**differentiated beat**, not the headline everyone ran, plus the counter-evidence that exists —
if it can't name one, it says so, because that candidate is probably a promo.

**Knows:** `vidiq_outliers` is broken (ignores its query argument). Uses `channel_search` and
`youtube_search` instead.

### 2. `fact-checker` — the reason this channel can publish finance content
Every number gets a live search; nothing from memory. Marks analyst figures as **estimates**
and forbids them rendering as prices or targets. Scopes every dataset on screen ("BofA client
flows, not market-wide"). Flags daily prints for re-check on render day. Requires two sources
for anything load-bearing.

**Standing authority:** if a thesis has no credible counter-argument, it reports the piece as a
promo and it doesn't run.

### 3. `scriptwriter` — the words, and only from the table
Hook → define → case → **counter-evidence** → actionable close. Writes numbers as *spoken*
("three and three quarters to four percent", "E T Fs") because the VO is generated verbatim and
a numeral gets mispronounced.

**Hard limit:** cannot search the web. Wants a fact that isn't in the table → stops and says so.

### 4. `retention-editor` — owns the first five seconds
The one you asked for. Every other agent optimises for being *right*; this one optimises for
being *watched*. Runs the five-second test — **could the first sentence be the title?** — maps
the script onto the timed retention spine, hunts the killers (throat-clearing, recap, slow build
to a number that could have opened), and checks the compliance line renders as a bottom-edge
strip rather than a full-frame card that eats the hook.

**Veto.** And a limit that matters: it may reorder and rewrite freely but **may not introduce a
fact outside the verified table**. Otherwise "make it interesting" becomes licence to drift.

Run it again on the finished brief — a hook that survives the script can still be destroyed by a
generator that opens on a title card.

### 5. `art-director` — imagery-first, never typography on textures
Builds `Beat | BASE | MID | TOP`. Every beat gets a concrete photographable shot, not "financial
imagery". Picks one hero shot, bookends the video on it changed, and puts the failure animation
on the negative beat only.

### 6. `packager` — titles that match what actually wins
Flat declarative news titles — the model is Humphrey Yang's 82-second Fed short at 286k views.
No clickbait, no question marks. Validates against live outliers before finalising.

**Knows:** vidIQ's thumbnail scorer penalises low saturation, which conflicts with this
channel's palette. **Does not chase the score.**

---

## Standing rules, enforced in every definition

| Rule | Why |
|---|---|
| **Every vidIQ call costs 5 credits** except `vidiq_balance` | Corrected 2026-09-21 — research is NOT free, and believing it was cost 40 of 41 credits in one session |
| Weekly vidIQ budget: **scout 3 · retention-editor 1 · packager 1** | 150/month renewable ≈ 7 calls/week across the whole chain |
| Never call `vidiq_outliers` | Ignores its query argument — 5 credits for unrelated results |
| No generation credit without your yes **in that turn** | thumbnail 22, score 5 |
| Check balances at session start | `CLAUDE.md` has been stale before and cost the channel usable tools |
| Never script from memory | Every figure gets a live search |
| Analyst numbers are estimates, never prices | Regulatory exposure on content people act on |
| Never chase the thumbnail score | The palette is the identity; already a decided trade |
| A human watches every render | CDN egress is blocked — **no agent has ever seen a render** |

---

## Running them

```
Agent(subagent_type="scout",            prompt="Weekly sweep. Return 5 ranked angles.")
Agent(subagent_type="fact-checker",     prompt="Verify all claims for <angle>. Write the table into <dir>/SCRIPT.md.")
Agent(subagent_type="scriptwriter",     prompt="Write the VO for <dir> from its fact table.")
Agent(subagent_type="retention-editor", prompt="Review <dir>. Five-second test and retention map.")
Agent(subagent_type="art-director",     prompt="Shot list + HeyGen brief for <dir>.")
Agent(subagent_type="packager",         prompt="Titles, description, tags for <dir>.")
```

Day-by-day cadence: `WEEKLY-RUNBOOK.md`. Channel strategy: `GROWTH-PLAN.md`.
Editorial standard: `STYLE-GUIDE.md` — §5A governs the hook and outranks everything except the
factual standard and the faceless rule.
