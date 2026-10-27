# FACTS.md — PARADOCS10X short, research pass
**Researched 2026-10-27.** Channel: **PARADOCS10X** (AI/tech, faceless, no host, no Zul).
**Compliance:** names Microsoft and Sony but quotes **no ticker, no valuation, no share price,
and implies no buy/sell/hold** → per `CLAUDE.md`, **no financial disclaimer**. Carries an
**on-frame sourcing strip** instead: `Secondary reporting · company statements · sources in description`.

> **No primary source was reachable.** Verified again this session against the standing repo
> constraint: `WebFetch`/`curl` cannot resolve primary hosts, so Xbox Wire, the TrendForce
> reports, the Deloitte report, the Circana data and the court docket were **all** read only
> through secondary coverage. **Nothing below is graded CONFIRMED and nothing can be.**
> No figure here may be set on screen as a verbatim quotation (`engine/qc.py` blocks it).

---

## 1. The topic, in one sentence

On **1 August 2026 Microsoft raised Xbox console prices worldwide for the third time since
May 2025 — the Series S 512GB from $399.99 to $499.99 — and named memory and storage costs as
the reason, saying those costs are already up "more than 2.5x" and will roughly double again
by autumn 2027**: the AI data-centre memory crunch has arrived on a consumer price tag, and
the $100 on the sticker is the smaller half of the story.

**Why it fits the proven shape:** a named thing (Xbox Series S), one hard number ($399.99 →
$499.99), and a cost that number hides (the component under it is up 2.5x and the company says
it is not finished — plus US Xbox unit sales down 33%).

**Nothing on the already-covered list is touched.** No Gemini watt-hours, no Agents' Last Exam,
no $30,000 wafer, no Moore's Law, no Roadster, no Cybercab, no Apple 2nm.

---

## 2. Three candidate titles (named thing + hard number + hidden cost)

1. **`Xbox Series S: $399 to $499, Because AI Bought the RAM`** (53 chars) — *recommended.*
   Named thing, one price delta, and the hidden cause in four words. Silent-frame-safe:
   `$399 → $499` is a picture.
2. **`Xbox Hits $799. Memory Is Up 2.5x and Doubling Again`** (51 chars) — leads on the component
   multiple rather than the sticker. Stronger number, weaker named-thing recognition, and the
   2.5x is Microsoft's own figure, which must be said in the sentence carrying it.
3. **`Xbox: +$100 on the Shelf, −33% in Sales, One Cause`** (50 chars) — the consequence version.
   Hardest hook, but −33% is Circana YTD-through-August and must be dated on frame; it is also
   the most confounded number in the set (see §4.5).

**Recommended first frame (silent, number inside 2s):** two stacked plain-text panels —
`XBOX SERIES S  $399.99` in white above `AUG 1, 2026  $499.99` with `$499.99` in red.
No logos (plain text name-tag only, `STYLE-GUIDE.md` §4).

---

## 3. Fact table

Grades: **HIGH** = several genuinely independent outlets agree · **MEDIUM** = one credible
source or one source replicated · **DISPUTED** = sources conflict · **UNUSABLE** = not established.
**CONFIRMED is unavailable in this environment.**

| # | Figure | Value | Sources (independent unless noted) | Grade | Conflict / note |
|---|---|---|---|---|---|
| F1 | Xbox Series S 512GB, US | **$399.99 → $499.99**, effective **1 Aug 2026** | [PureXbox price breakdown](https://www.purexbox.com/news/2026/08/heres-a-breakdown-of-the-new-prices-for-xbox-series-xs-consoles-as-of-august-2026) · [Digital Citizen](https://www.digitalcitizen.life/microsoft-raises-xbox-console-prices-by-up-to-150-and-ends-2tb-models/) · [TechRepublic](https://www.techrepublic.com/article/news-xbox-console-price-increase/) · [TechSpot](https://www.techspot.com/news/112906-third-xbox-price-hike-15-months-raises-all.html) | **HIGH** | [Thurrott](https://www.thurrott.com/games/337919/microsoft-announces-up-to-150-price-increases-for-xbox-consoles-starting-on-august-1) listed $449 pre-launch. Treated as stale/erroneous — four later sources agree on $499.99 |
| F2 | Xbox Series X 1TB **with disc**, US | **$649.99 → $799.99** | [PureXbox](https://www.purexbox.com/news/2026/08/heres-a-breakdown-of-the-new-prices-for-xbox-series-xs-consoles-as-of-august-2026) · [TheNextWeb](https://thenextweb.com/news/microsoft-xbox-price-increase-third-time-memory-shortage-800) · [Digital Citizen](https://www.digitalcitizen.life/xbox-series-x-and-series-s-prices-will-rise-sharply-on-august-1/) | **HIGH** | An early summary showed "$749 vs $799" as a conflict. **Resolved, not a conflict:** $749.99 is the all-digital model, $799.99 the disc model |
| F3 | Xbox Series X 1TB **all-digital**, US | **$599.99 → $749.99** | [PureXbox](https://www.purexbox.com/news/2026/08/heres-a-breakdown-of-the-new-prices-for-xbox-series-xs-consoles-as-of-august-2026) · [Digital Citizen](https://www.digitalcitizen.life/xbox-series-x-and-series-s-prices-will-rise-sharply-on-august-1/) | MEDIUM-HIGH | Two sources, same price table lineage |
| F4 | Xbox Series S 1TB, US | **$449.99 → $599.99** | [PureXbox](https://www.purexbox.com/news/2026/08/heres-a-breakdown-of-the-new-prices-for-xbox-series-xs-consoles-as-of-august-2026) · [TechSpot](https://www.techspot.com/news/112906-third-xbox-price-hike-15-months-raises-all.html) | MEDIUM-HIGH | |
| F5 | Size of the rise | **+$100 on 512GB models, +$150 on 1TB models** | [Barchart](https://www.barchart.com/story/news/8569/microsoft-raises-xbox-console-prices-worldwide-as-memory-and-storage-chip-costs-surge) · [Digital Citizen](https://www.digitalcitizen.life/microsoft-raises-xbox-console-prices-by-up-to-150-and-ends-2tb-models/) · [Computing](https://www.computing.co.uk/news/2026/microsoft-raises-xbox-console-prices) | **HIGH** | Cleanest single on-screen number after F1 |
| F6 | **Microsoft's stated reason** | Xbox Wire: storage and memory prices have risen **"more than 2.5x"** and **"could double again by fall 2027"** | [TechRepublic](https://www.techrepublic.com/article/news-xbox-console-price-increase/) · [Barchart](https://www.barchart.com/story/news/8569/microsoft-raises-xbox-console-prices-worldwide-as-memory-and-storage-chip-costs-surge) · [Computing](https://www.computing.co.uk/news/2026/microsoft-raises-xbox-console-prices) · [ARY News](https://arynews.tv/microsoft-just-drove-up-xbox-prices-as-ai-creates-a-memory-crunch) | **HIGH that Microsoft said it** · the number itself is **company-supplied and unaudited** | **Baseline date disputed.** One outlet says "since 2024"; the others give no baseline. On frame it must read **"Microsoft says"**, in the sentence, not the description. Must NOT be set as a quotation (qc.py) — paraphrase |
| F7 | Consoles sold below cost | Microsoft states consoles are typically sold **below manufacturing cost**, making component inflation hard to absorb | [TechRepublic](https://www.techrepublic.com/article/news-xbox-console-price-increase/) · [Computing](https://www.computing.co.uk/news/2026/microsoft-raises-xbox-console-prices) | **HIGH that Microsoft said it** | Company claim, not an audited margin |
| F8 | 2TB Series X | **Discontinued / sunset** alongside the rise | [Digital Citizen](https://www.digitalcitizen.life/microsoft-raises-xbox-console-prices-by-up-to-150-and-ends-2tb-models/) · [TechSpot](https://www.techspot.com/news/112906-third-xbox-price-hike-15-months-raises-all.html) | MEDIUM-HIGH | |
| F9 | Hike count | **Third** Xbox price increase, first since **May 2025** | [TechSpot](https://www.techspot.com/news/112906-third-xbox-price-hike-15-months-raises-all.html) · [TheNextWeb](https://thenextweb.com/news/microsoft-xbox-price-increase-third-time-memory-shortage-800) · [Hitmarker](https://hitmarker.net/news/microsoft-has-announced-a-third-price-increase-for-xbox-series-x-s-consoles-effective-august-1-1745609) | **HIGH on "third"** · **DISPUTED on the window** | TechSpot says **15 months**, TheNextWeb says **13 months**. **Say "third increase since May 2025"** and print no month count |
| F10 | Prior hikes | **May 2025** (first, widely tied to tariffs); **3 Oct 2025**, US-only, **+$20–$70** | [Thurrott](https://www.thurrott.com/games/337919/microsoft-announces-up-to-150-price-increases-for-xbox-consoles-starting-on-august-1) · [Android Authority](https://androidauthority.com/microsoft-xbox-price-increase-in-august-3681588/) | MEDIUM | **Second date disputed:** Android Authority says October 2025, [Gigazine](https://gigazine.net/gsc_news/en/20260626-xbox-console-prices-update/) says September 2025. Avoid the second date entirely |
| F11 | Aug 2026 scope | **Worldwide**, unlike the US-only October 2025 change | [Digital Citizen](https://www.digitalcitizen.life/xbox-series-x-and-series-s-prices-will-rise-sharply-on-august-1/) · [Barchart](https://www.barchart.com/story/news/8569/microsoft-raises-xbox-console-prices-worldwide-as-memory-and-storage-chip-costs-surge) | MEDIUM-HIGH | UK disc Series X reported **£500 → £670** ([Easterneye](https://www.easterneye.biz/xbox-prices-rise-uk-microsoft-chip-costs/)) — single-source, use only if a UK cut is wanted |
| F12 | **Sony PS5**, US | **$549.99 → $649.99**, effective **2 April 2026**; Digital $599.99, Pro $899.99, Portal $249.99 | [AOL/Reuters-style wire](https://www.aol.com/finance/sony-hikes-prices-ps5-ps5-060300791.html) · [Bloomberg headline](https://www.bloomberg.com/news/articles/2026-03-27/sony-raises-playstation-5-pricing-by-as-much-as-150) · [Checkpoint Gaming](https://checkpointgaming.net/news/2026/03/sony-announces-substantial-price-increases-for-ps5-ps5-pro-and-playstation-portal/) | **HIGH** on the base console; MEDIUM on Pro/Portal | |
| F13 | **Sony's stated reason** | **"Continued pressures in the global economic landscape."** Sony did **not** name memory | [Bloomberg](https://www.bloomberg.com/news/articles/2026-03-27/sony-raises-playstation-5-pricing-by-as-much-as-150) · [AOL](https://www.aol.com/finance/sony-hikes-prices-ps5-ps5-060300791.html) · [NBC Palm Springs](https://www.nbcpalmsprings.com/2026/03/27/sony-raising-ps5-price-to-650-starting-next-week) | **HIGH** | **This is the counterweight, see §4.1.** Memory attribution for Sony is analyst inference only |
| F14 | US hardware sales (Circana) | YTD through **Aug 2026**: Xbox units **−33%** (all-time low), PlayStation **−25%** (lowest since 2013) | [TweakTown](https://www.tweaktown.com/news/114010/xbox-us-sales-hit-an-all-time-low-while-playstation-suffers-its-worst-year-since-2013-as-console-prices-reach-record-highs/index.html) · [VGC](https://www.videogameschronicle.com/news/us-console-hardware-market-at-its-most-precarious-position-since-the-80s-says-circana/) · [Gaming.net](https://www.gaming.net/circana-xbox-us-unit-sales-at-all-time-low-playstation-lowest-since-2013/) | **MEDIUM** | Three outlets, **one origin**: Circana's Mat Piscatella, 9 Oct 2026. That is replication, not independence. Date must be on frame |
| F15 | US average price paid | Xbox **$529** (+26% YoY), PlayStation **$597** (+20% YoY), both US records | [TweakTown](https://www.tweaktown.com/news/114010/xbox-us-sales-hit-an-all-time-low-while-playstation-suffers-its-worst-year-since-2013-as-console-prices-reach-record-highs/index.html) · [TechEnclave](https://techenclave.com/news/items/us-xbox-and-playstation-sales-fall-average-prices-reach-records) | MEDIUM | **Average price *paid*, not list price.** Same single Circana origin |
| F16 | DRAM contract prices, Q1 2026 | Conventional DRAM **+90–95% QoQ**, revised up from an earlier 55–60% forecast | [Guru3D](https://www.guru3d.com/story/another-major-dram-and-nand-price-surge-in-q1-2026-predicted/) · [TweakTown](https://tweaktown.com/news/109996/analysts-say-pc-dram-pricing-for-q1-2026-will-hit-record-highs-doubling-the-previous-estimate/index.html) · [HWCooling](https://www.hwcooling.net/en/memory-prices-to-double-in-q1-2026-compared-to-year-end/) | MEDIUM-HIGH | All trace to **TrendForce forecasts**, which were revised upward more than once. Forecast, not settled contract data |
| F17 | DRAM contract prices, Q4 2026 | **+~20% QoQ** (reported 20 Oct 2026) vs **+10–15% QoQ conventional** (TrendForce, 30 Sep 2026) | [StockHub](https://www.stockhub.kr/en/news/news_b7244c205001) · [TrendForce bulletin listing](https://trendforce.com/research/download/RP260923EN) · [TechNews TW](https://technews.tw/?p=1622115) | **DISPUTED** | Probably a **scope** difference (conventional DRAM vs total DRAM incl. HBM), not a revision — but that is an inference and the scopes could not be checked against the source report. **Do not put a Q4 number on screen** |
| F18 | Mechanism — HBM crowd-out | HBM consumes roughly **3x the wafer supply per bit** of DDR5; HBM is ~**20% of DRAM wafer capacity now, ~30% expected in 2027** | [Newsquawk, Samsung exec](https://www.newsquawk.com/headlines/samsung-electronics-005930-ks-executive-expects-hbm-to-comprise-approximately-30-of-dram-chipmakers-total-wafer-capacity-in-2027-vs-around-20-currently) · [Damnang substack](https://damnang2.substack.com/p/will-the-memory-stock-rally-keep) · [Utmel](https://www.utmel.com/blog/categories/memory%20chip/2026-dram-and-the-3-to-1-hbm-rule-market-supply-analysis-and-b2b-procurement-guide) | **MEDIUM** | Estimates spread 3x–4x. [Xenospectrum](https://xenospectrum.com/en/micron-hbm-ddr-silicon-gap/) argues the ratio **cannot be translated into retail pricing** and that blaming HBM alone overstates it. Second and third sources are trade-blog/substack — weak. Usable as **"roughly three times"**, never as a precise figure |
| F19 | Duration | Deloitte (report dated **2 Aug 2026**, read only via coverage): new supply from current capex **not arriving until 2029–2030**; big-three combined capex **+~340% 2024→2027** | [GamesBeat](https://gamesbeat.com/ramageddon-why-the-memory-chip-crisis-is-worse-than-expected-lasting-to-2029-or-2030-deloitte/) · [Borncity (DE)](https://borncity.com/news/ki-speicherkrise-deloitte-warnt-vor-teuerung-bis-2030/) · [TechRadar](https://techradar.com/computing/memory/samsungs-latest-report-suggests-the-ram-crisis-is-only-just-getting-started-could-we-be-looking-at-a-new-normal) | MEDIUM | Secondary only; outlets restate Deloitte's price figures inconsistently |
| F20 | **Antitrust allegation** | Proposed US class action **filed 25 Jun 2026, N.D. Cal.**, Sherman Act §1, vs Samsung / SK Hynix / Micron — alleges coordinated production cuts and capacity shift to HBM | [Digital Citizen](https://www.digitalcitizen.life/samsung-sk-hynix-and-micron-face-us-lawsuit-over-soaring-dram-prices/) · [Notebookcheck](https://www.notebookcheck.net/Samsung-Micron-SK-Hynix-sued-over-DRAM-price-fixing-triggering-a-RAMpocalypse-as-memory-prices-soar.1333523.0.html) · [ProPakistani](https://propakistani.pk/2026/07/01/samsung-and-sk-hynix-sued-for-alleged-ram-price-fixing/) | **MEDIUM** on the filing · the claims are **untested allegations** | **See §4.4.** No company response or ruling found. Case no. 3:26-cv-06345 is single-source (TrendForce citing Wccftech) — **do not print the case number** |
| F21 | Knock-on, PCs and phones | IDC: PC prices **+4–8% globally in 2026**, with some vendors quoting large clients up to **+20%**; Counterpoint: smartphone ASP **+~7%** | [Boston Globe](https://www.bostonglobe.com/2026/01/09/business/pc-computer-phones-prices-ai/) · [Axios](https://www.axios.com/2025/12/16/phone-pc-xbox-prices-ai-ram-shortage) · [TechSpot](https://www.techspot.com/news/110679-memory-shortages-raise-pc-smartphone-prices-8-2026.html) | MEDIUM | **Dated Dec 2025 / Jan 2026 forecasts.** Nine to ten months stale. Use only as context, never as a current figure |

---

## 4. Counter-evidence — what weakens the thesis

The thesis is "AI data-centre memory demand is why your console costs more." Five things cut against it.

**4.1 Sony never said it.** Sony's March 2026 increase — the larger of the two in dollar terms —
was justified only as *"continued pressures in the global economic landscape."* Memory is the
press's and analysts' explanation for Sony, **not Sony's own** (F13, HIGH). Only Microsoft
named the component. Any line implying "both console makers blamed AI memory" is false.

**4.2 The 2.5x is the price-raiser's own number.** Microsoft supplied the multiple that
justifies Microsoft's price rise. No outlet checked it, no audited baseline exists, and the
sources don't even agree on what date it is measured from (F6). The attribution has to sit in
the sentence — *"Microsoft says"* — the way the Google watt-hours short handled it.

**4.3 Tariffs are a live confound.** The **first** Xbox increase (May 2025) and Sony's August
2025 +$50 were both tied to tariffs, not memory (F10, F13 note). So the cumulative
$399.99 → $499.99 journey on the Series S is **not** all an AI memory story; only the Aug 2026
leg is attributed to memory by the company. The video must be about the **third hike**, not the
whole run, or it overstates.

**4.4 There is a live allegation that the shortage is not purely demand.** A June 2026 proposed
class action alleges the three DRAM makers **coordinated** production cuts and the shift to HBM
(F20). If that were true, the cause is collusion, not AI appetite. It is an **untested
allegation** with no company response or ruling found, so it cannot be asserted — but it is the
honest reason not to narrate the AI explanation as settled.

**4.5 The −33% is the most confounded number in the set.** Xbox US unit sales were already in
structural decline before any of these hikes, and Microsoft has been publishing its games on
rival platforms, which is an independent reason to buy fewer Xboxes. **No source found in this
session separates the price effect from the strategy effect.** That attribution is mine, not
reported, and the short must not imply the price rise caused the 33%.

**4.6 One counterweight that failed to appear, recorded as such.** I went looking for the
standard cyclical rebuttal — "memory always crashes, new fabs will fix it in a year" — and
**could not substantiate it for 2027**. TrendForce, Samsung, Micron (via coverage) and Deloitte
all point the other way: tight into 2027–2028, meaningful new supply 2029–2030 (F19). The only
oversupply warning found applies to **NAND**, or to DRAM only once fabs ramp 2–3 years out
(Morningstar via [Webull](https://www.webull.com/news/15350144979772416)). So the "it's just the
cycle" rebuttal is **not available on the evidence**, and the short should not manufacture one.

---

## 5. Not usable — found, but not establishable

| Claim | Why it is out |
|---|---|
| **"Wholesale memory prices are up 700%"** | Appears twice from **different origins** — a Windows Central insider report, and as an **allegation** in the class action ("~700% over four years"). It conflicts head-on with Microsoft's "more than 2.5x" (150%), almost certainly a different scope and baseline. **This is exactly the 10x-wrong trap the repo logged on 2026-10-25. Banned from the frame and from narration.** |
| **"Microsoft loses ~$150 per Xbox sold"** / "~$50 after the hike" | Single origin: Jez Corden / Windows Central, attributed to anonymous sources, recycled by aggregators. No Microsoft statement, no filing breakdown. Tempting and unusable. Also names a real person, which pulls in `DISCLAIMER.md` lines for no benefit. |
| **"Xbox failed to lock in fixed-price memory supply"** | Same single insider origin. Unverifiable. |
| **Any Q3 or Q4 2026 DRAM percentage** | Forecasts disagree violently: TrendForce 13–18% for Q3 vs an analyst's 40–50%; Q4 at 10–15% vs ~20% with unclear scope (F17). No number here is safe on screen. |
| **Current US retail price as of 27 Oct 2026** | The 1 Aug 2026 list prices are well sourced, but **no source confirms what the consoles actually sell for today**, and no source was found confirming the increase took effect as announced. On frame the figures must be labelled **"announced 1 Aug 2026"**, not "today's price." |
| **A fourth Xbox increase** | Searched for; **none found**. That is "I found none," not "none exists." Do not say it. |
| **Exact Xbox Wire wording** | Primary page unreachable. **No sentence may be set as a quotation** (`engine/qc.py` blocks sourced quotations). Paraphrase everything. |
| **"Third increase in 13/15 months"** | Sources conflict (F9). Use "third since May 2025." |
| **UK £500 → £670** | Single source. Only if a UK-specific cut is wanted, and then labelled single-source. |
| **Case number 3:26-cv-06345 / "17 plaintiffs"** | Single-source via an aggregator citing another aggregator. Docket unreachable. |
| **PC +4–8% / phone ASP +7%** | Real forecasts, but from Dec 2025 / Jan 2026. Too stale to state in the present tense. |

---

## 6. Re-check of claims the repo already carries

Nothing in this repo has covered console pricing or the memory market, so there was no inherited
figure to re-verify here. For the record of the standing instruction: the already-covered list
(Gemini 0.24/0.10 Wh, Agents' Last Exam 82%/25%, the $30,000 wafer, Moore's Law, Tesla Roadster,
Cybercab, Apple 2nm) was checked against `reference/VIDEO-IDEAS.md` and this topic overlaps none
of them. `VIDEO-IDEAS.md` P1 (Gemini watt-hours) and P2 (Waymo) remain the other open PARADOCS10X
candidates and are untouched by this pass.

---

## 7. Decay

**Holds for roughly two to three months, with one dated element.**

- The **1 Aug 2026 price change already happened** and cannot rot (F1–F5, F9).
- **Microsoft's "doubles again by fall 2027" is a company forecast** and could be superseded;
  it is labelled as a company statement, so even if it proves wrong the video stays true.
- **Decays fastest:** the Circana YTD-through-August figures (F14, F15) — a fresh Circana read
  lands roughly monthly, so the date must be printed on frame.
- **Kills it:** a fourth Xbox increase, or a Microsoft walk-back. **Re-search both on build day.**
- **Deliberately excluded:** every market price, every ticker, every DRAM percentage. Consistent
  with the standing rule that price-led topics cannot be re-verified from this environment.
