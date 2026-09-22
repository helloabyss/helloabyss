# Research — Frontier AI lane, week ending 2026-09-22

**Lane:** Frontier AI models and tools people can actually use.
**Verification method:** primary sources fetched and read in full via the Higgsfield sandbox
(this container blocks news domains). Secondary sources used only where no primary exists.

---

## ✅ FACT 1 — Grok 4.7 · VERIFIED VERBATIM AT PRIMARY SOURCE

Source: **https://x.ai/news/grok-4-7** — fetched, HTTP 200, dated **Sep 21, 2026**.
Note the company is branded **SpaceXAI** on its own page ("SpaceXAI's most powerful model").

Quoted verbatim from the post:

| Claim | Source wording | Status |
|---|---|---|
| Release date | "Sep 21, 2026" | ✅ |
| Larger base | "Grok 4.7 uses a new, larger base model compared to Grok 4.6" | ✅ |
| Longer RL run | "trained with a longer reinforcement learning run on a harder mix of tasks, weighted toward problems that take many hours to complete" | ✅ |
| Self-check | "better at verifying its own work and managing longer context" | ✅ |
| Availability | "available today in Cursor and Grok Build… also available through the Grok API, third-party coding harnesses, and model routers and cloud platforms" | ✅ |
| Price | "priced starting at $2 per million input tokens and $6 per million output tokens" | ✅ |
| Same price as 4.6 | "Served at the same price and speed as Grok 4.6" — table shows $2/$6 for both | ✅ |
| CursorBench 4.0 | 46.3% vs 40.4% | ✅ |
| EEBench | 64.0% vs 53.0% | ✅ |

### ⚠️ CORRECTION 1 — the benchmark comparison is NOT like-for-like
The table's own column headers read **"Grok 4.7 xHigh"** vs **"Grok 4.6 High"**. Those are
different reasoning-effort settings. Presenting 46.3 vs 40.4 as a clean generational gain,
with no qualifier, overstates what xAI published.

**Every on-screen benchmark graphic must read `Grok 4.7 xHigh vs Grok 4.6 High — company-reported`.**
This is the single most important fix in this package.

### ⚠️ CORRECTION 2 — "at the frontier" is a price-performance claim, not "best"
From the same table, **Fable 5.1 Max beats Grok 4.7** on three of the rows shown:

| Benchmark | Grok 4.7 xHigh | Fable 5.1 Max |
|---|---:|---:|
| CursorBench 4.0 | 46.3% | **51.8%** |
| Terminal-Bench 4.0 | 38.0% | **57.9%** |
| AA Briefcase v1.1 | 1,657 | **1,678** |

xAI's own wording is "at the frontier **in price-performance**" — true at $2/$6 against
Fable 5.1 Max's $10/$50. The video must not imply Grok 4.7 is the top-scoring model. Grok 4.7
does lead EEBench (64.0%) and DeepSWE carries an asterisk in the source (71.0%*).

---

## ✅ FACT 2 — Step 5 Preview · VERIFIED, ONE CLAIM DISPUTED

Announced **2026-09-20**, API live same day.

| Claim | Status |
|---|---|
| 600B total / ~27B active sparse MoE | ✅ multi-source |
| 1M-token context | ✅ |
| API available now | ✅ |
| Open weights **2026-10-15** | ✅ |
| Artificial Analysis Intelligence Index **44** | ✅ |
| **Native text / image / VIDEO input** | ⚠️ **DISPUTED — see below** |

### ⚠️ CORRECTION 3 — drop "video" from the Step 5 line
Sources split. `datastudios.org`: "native **text and image** input." `cellcog.ai`: "text,
image **and video** input." No primary StepFun doc was reachable to settle it.

House rule is *unsourced means cut*. **Say "text and image."** One word, and it removes the
only claim in the package that a commenter could disprove.

### Facts the brief missed, worth adding
- **Pricing: $1 per M input / $2.70 per M output, with a 95% cache discount.** This is the
  strongest number in the story — Step 5 is *cheaper than Grok 4.7* at a comparable index score.
- Same effort-setting asymmetry as Grok: StepFun's own footnotes pit **Step 5 High** against
  rivals. The pattern is the honest through-line for this episode.

---

## ✅ FACT 3 — Digit 5 · VERIFIED, BUT OFF-LANE

Unveiled **2026-09-15**.

| Claim | Status |
|---|---|
| First "cooperatively safe" humanoid at scale | ✅ |
| Repeated 50 lb / 22.7 kg payload | ✅ |
| 90-min runtime, 9-min charge, 10:1 ratio | ✅ (vs 2:1 on Digit 4) |
| **7.2 ft reach** | ✅ "Up to 7.2 feet, compared with 5.5 feet for the previous version" |
| Early access H1 2027 | ✅ |
| "General availability by end of 2027" | ⚠️ sources say "wider availability later that year" — soften |

**Also verified, and stronger than anything in the brief:** >**$300M** in multi-year Digit 5
orders as of May 2026 (conditions attached); 5 ft 11 in tall, 284 lb; swappable ISO-flange
grippers; EU/UK availability planned 2027 — first time outside North America.

### ⚠️ CORRECTION 4 — Digit 5 does not fit the stated lane
The lane is "tools people can **actually use**." Digit 5 is early-access **H1 2027** — nobody
can use it today, and the brief's own SKIP list says unreleased robots must be labelled.

Two honest options: cut it, or run it explicitly as a **"NOT YET — 2027"** segment. The
package below takes the second and labels it on screen.
