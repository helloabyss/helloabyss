# FACTS — "82% / 25%" (PARADOCS10X short 5)

Researched 2026-10-25. **No claim here is graded CONFIRMED and none can be.**

## Why nothing is CONFIRMED

Every primary source for this topic is unreachable from this environment. `WebFetch`
returned `getaddrinfo ENOTFOUND` — DNS-level block, not the 403-on-CONNECT the repo had
previously recorded — for all of:

- `arxiv.org` (the paper, arXiv:2606.05405)
- `metr.org`
- `agents-last-exam.org`
- `dailycal.org`

Only server-side web search works. So every figure below is **corroborated secondary
reporting**, graded by how many *independent* outlets agree and how credible they are.
Where outlets conflict, the conflict is recorded rather than resolved in our favour.

## Graded claims

| # | Claim | Grade | Basis |
|---|---|---|---|
| 1 | Agents' Last Exam (ALE) is a UC Berkeley RDI + Snorkel AI benchmark | **High** | Berkeley RDI blog, Snorkel leaderboard, Klu, VentureBeat coverage — all agree |
| 2 | Built from **1,490 task instances** across **960 real workflows**, **55 subfields**, **13 industry clusters**, mapped to O*NET/SOC 2018 | **High** | Snorkel + Klu + paper summaries agree on all five numbers |
| 3 | Tasks sourced from **300+** working professionals' own completed work | **Medium-high** | Body/leaderboard say 300+; the abstract reportedly says **250+**. VO says "three hundred" — matches the more widely quoted figure, but see note |
| 4 | Graded **deterministically against the expert's own deliverable** | **High** | Multiple independent summaries; this is the benchmark's distinguishing design claim |
| 5 | Best configuration scores **82.0% on Terminal-Bench** but **25.2% on ALE-CLI** | **Medium-high** | Berkeley RDI's own framing, repeated by learnagentic. Philipp Schmid cites **23%** for the same comparison — see failed checks |
| 6 | On the hardest "Last Exam" tier, top configurations score **0.0%** | **Medium-high** | Tier breakdown (Codex/GPT-5.5: 38.1 near-term / 22.7 full-spectrum / **0.0** last-exam / 24.0 overall; Claude Code/Fable 5: 34.3 / 20.9 / **0.0** / 22.0) reported consistently across two independent write-ups |
| 7 | Cross-configuration **average** on the hardest tier is **2.6%** | **Medium** | Widely repeated. Does **not** contradict #6 — 2.6% is the mean across mainstream configs, 0.0% is the leaders. Conflating the two is the trap |
| 8 | ~**three quarters** of failures are missing domain knowledge / wrong approach, not broken tool execution | **Medium** | Single analysis (learnagentic) reading the paper. Load-bearing for the short's payoff — flagged |
| 9 | Scores rising: **24.0%** (June launch) → **38.2%** (Claude Opus 5.5, Snorkel board) → **59.3%** (GPT-6 Astra, BenchLM, 17 Oct 2026) | **Medium** | Three different boards with different scoring methods. Directionally solid, not like-for-like |

## Did NOT survive re-checking

- **"AI agents pass just 2.6% of real-world tasks."** This was the first search's headline and
  it is wrong as stated. 2.6% is the hardest tier only, and it is a cross-configuration
  average. The overall figure is ~24%. Scripting the first result would have published a
  10x error. **The short says "on the hardest tier" explicitly for this reason.**
- **"Frontier agents pass less than 1% of real professional work"** (co-r-e.com headline) —
  same error, worse. Rejected.
- **82% → 25% exact spread.** Berkeley RDI and learnagentic say 25.2%; Philipp Schmid says
  23%. VO rounds to "twenty-five," which is the better-sourced of the two. Not a safe
  decimal to put on screen.
- **Gemini 4 Argon at 39.5%** (llmlearner leaderboard) — that page is partly vendor
  self-report. Dropped entirely; no vendor ranking appears in this short.
- **Any claim about which lab is "winning."** Sources conflict on ordering and the boards
  use different scoring. The short names **no model and no vendor** — deliberately.

## Note on #3

"Three hundred working professionals" is spoken. If the abstract's 250+ is the true figure,
the claim is overstated by 20%. Both numbers appear in the same sources describing different
parts of the paper. Lower-risk alternative if a correction is ever needed: "hundreds of
working professionals."
