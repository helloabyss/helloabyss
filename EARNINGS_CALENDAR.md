# EARNINGS CALENDAR — rolling

Upcoming reports worth covering on **This Week in the Market**. Updated every `/twim` run
(Phase 9.1): drop what reported, add newly confirmed dates 4–6 weeks out.

**Last updated: 2026-09-20.**

---

## Confidence legend

| Mark | Meaning |
|---|---|
| ✅ **Confirmed** | Date announced by the company (IR release or 8-K). Traceable to a primary document. |
| 🟡 **Reported** | Carried by calendar aggregators or press, **not yet verified against company IR**. Usable for planning; verify before it appears in a script. |
| ⬜ **Estimated** | Projected from the company's historical reporting pattern. Planning only. **Never stated on screen as a date.** |

> `COMPLIANCE.md §6` applies to this file. Only a ✅ date may be spoken as fact in an
> episode. A 🟡 or ⬜ date is framed as "expected to report" or left out.

## ⚠️ The weekday trap — check every date

**Recycled prior-year calendars are the main failure mode here.** While seeding this file on
2026-09-20, a widely-syndicated "Q3 bank earnings preview" gave Bank of America and Goldman
Sachs as **17 October** and Morgan Stanley as **18 October**. In 2026 those are a **Saturday
and a Sunday** — the article was 2025 content recycled. The dates are wrong.

**Every date added to this file gets its weekday checked** (`date -d YYYY-MM-DD +%A`).
A bank or mega cap reporting on a weekend is a stale source, not a scoop.

---

## Priority window — next 4 weeks

Q3 2026 reporting season opens mid-October, led by the banks.

| Date | Weekday | Company | Ticker | Quarter | Confidence | Why it matters |
|---|---|---|---|---|---|---|
| 2026-10-13 | Tue | JPMorgan Chase | JPM | Q3 2026 | ✅ **Confirmed** | Opens the season. Results ~7:00am ET, call 8:30am ET. Credit quality and NII guide set the tone for the whole financials complex. |
| 2026-10-14 → 10-16 | Wed–Fri | Bank of America · Goldman Sachs · Morgan Stanley · Citi · Wells Fargo | BAC GS MS C WFC | Q3 2026 | ⬜ **Estimated** | Big-bank cluster follows JPM within the same week. **Dates unverified — the widely-cited 17/18 Oct figures are stale 2025 content (see above). Confirm against each bank's IR before scripting.** |
| 2026-10-20 → 10-30 | — | Mega-cap tech: Microsoft · Alphabet · Meta · Apple · Amazon | MSFT GOOGL META AAPL AMZN | FY/CY Q3 | ⬜ **Estimated** | Late-October cluster is the single biggest index-weight week of the quarter. Apple last reported FY Q3 on 2026-07-30; Microsoft FY Q4 on 2026-07-29 — both on their usual late-month cadence. **Confirm each against IR.** |

## Following weeks

| Date | Weekday | Company | Ticker | Quarter | Confidence | Why it matters |
|---|---|---|---|---|---|---|
| 2026-11-25 | Wed | NVIDIA | NVDA | Q3 FY2027 | 🟡 **Reported** | After close. The highest-surprise single report in the market and the clearest read on AI capex. Also the cleanest **China** read-through in the format — data-center revenue and export-licence commentary. **Verify against NVIDIA IR.** |

## Standing watch-list — recurring, date TBC

Add with real dates as they are announced.

| Company | Ticker | Why it earns a beat |
|---|---|---|
| Taiwan Semiconductor | TSM | Monthly revenue + quarterly call: the upstream read on the entire US semi complex |
| ASML | ASML | Litho orders lead the fab cycle; export-control exposure |
| Micron | MU | Memory pricing cycle, off-calendar quarter |
| Broadcom | AVGO | Custom AI silicon; off-calendar quarter |
| Walmart · Costco · Target | WMT COST TGT | The US consumer read, and the clearest tariff/import-cost transmission |
| Caterpillar · Deere | CAT DE | China demand and global industrial capex |
| Freeport-McMoRan | FCX | Copper — the cleanest China-demand transmission to a US ticker |
| Tesla | TSLA | China demand and production; already a channel subject (see `ARCHIVE.md`) |
| FedEx · UPS | FDX UPS | Freight volumes as a real-time macro read |

## Recently reported — context only

Useful for "versus last quarter" framing. Not upcoming.

| Date | Company | Quarter | Note |
|---|---|---|---|
| 2026-07-29 | Microsoft | FY2026 Q4 | Reported after close |
| 2026-07-30 | Apple | FY2026 Q3 | $109.4B revenue, $29.8B profit (press reports — verify against the 8-K before use) |

---

## Update procedure (Phase 9.1)

1. Remove anything that reported; move it to **Recently reported** if it is useful context.
2. Add newly **confirmed** dates 4–6 weeks out, promoting ⬜/🟡 → ✅ as IR confirms.
3. **Check the weekday of every date added or promoted.**
4. Keep the "Why it matters" column written as an **equity-transmission** sentence
   (`STYLE.md §1`) — if a report cannot be tied to a ticker/sector/index and a mechanism, it
   does not belong on this list.
5. Update the **Last updated** date at the top.
